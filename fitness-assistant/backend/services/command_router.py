"""
指令路由器 v2

设计理念：
- /记录：结构化指令，规则解析，直接操作飞书表格
- /llm：自由模式，LLM 自主决策调用什么 agent/skill
- 其他指令：路由到特定 agent

Agents:
- trainer: 训练师（生成计划、分析记录）
- rehab: 康复师（伤病建议、动作替代）
- recorder: 记录员（写入飞书表格）
- querier: 查询员（读取飞书表格）
"""

from typing import Dict, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import re


class AgentType(Enum):
    """Agent 类型"""
    TRAINER = "trainer"      # 训练师：生成计划、分析趋势
    REHAB = "rehab"          # 康复师：伤病建议、动作替代
    RECORDER = "recorder"    # 记录员：写入飞书表格
    QUERIER = "querier"      # 查询员：读取飞书表格
    ROUTER = "router"        # 路由：LLM 自主决策


@dataclass
class CommandContext:
    """指令上下文"""
    user_id: str
    command: str
    raw_input: str          # 原始输入
    parsed_data: dict       # 解析后的数据
    history: List[dict]     # 对话历史
    feishu_token: dict      # 飞书 API token


@dataclass
class AgentResponse:
    """Agent 响应"""
    success: bool
    message: str
    data: Optional[dict]
    actions: List[dict]     # 需要执行的动作（如写入飞书）


class Agent:
    """Agent 基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, context: CommandContext) -> AgentResponse:
        raise NotImplementedError


class RecorderAgent(Agent):
    """
    记录员 Agent
    职责：将结构化数据写入飞书多维表格
    """
    def __init__(self):
        super().__init__(
            name="recorder",
            description="训练记录员，负责将训练数据写入飞书表格"
        )
    
    async def execute(self, context: CommandContext) -> AgentResponse:
        data = context.parsed_data
        
        # TODO: 调用飞书 API 写入表格
        # result = await feishu_api.append_record(data)
        
        return AgentResponse(
            success=True,
            message=f"✅ 已记录: {data.get('exercise')} {data.get('weight')}kg × {data.get('reps')}次 × {data.get('sets')}组",
            data=data,
            actions=[{"type": "feishu_write", "table": "training_logs", "data": data}]
        )


class LLMRouterAgent(Agent):
    """
    LLM 路由 Agent
    职责：理解用户意图，自主决策调用其他 agents
    
    输入示例：
    - "今天练胸，先用60kg卧推热身，然后正式组80kg做了8个"
    - [图片] 训记截图
    - "我肩膀有点疼，今天还能练推吗？"
    - "看看我最近卧推的趋势"
    
    LLM 决策：
    - 意图识别 → 调用 recorder/trainer/rehab/querier
    - 参数提取 → 传递给具体 agent
    - 或者直接回答（闲聊/建议）
    """
    def __init__(self):
        super().__init__(
            name="llm_router",
            description="智能路由，理解复杂输入并决策调用其他 agents"
        )
    
    async def execute(self, context: CommandContext) -> AgentResponse:
        """
        LLM 自主决策流程：
        
        1. 理解输入（可能是文字、图片、混合）
        2. 意图识别
        3. 决策：调用哪个 agent 或直接回答
        4. 执行
        """
        
        # TODO: 调用 LLM API 进行决策
        # llm_response = await llm_client.chat(
        #     system_prompt=ROUTER_PROMPT,
        #     user_input=context.raw_input,
        #     available_agents=[a.description for a in available_agents]
        # )
        
        # 模拟 LLM 决策
        text = context.raw_input.lower()
        
        if "肩" in text and ("疼" in text or "痛" in text):
            # 伤病相关 → 康复师
            return AgentResponse(
                success=True,
                message="🩺 检测到伤病描述，转接康复师...",
                data={"route_to": "rehab", "input": text},
                actions=[{"type": "delegate", "agent": "rehab", "context": context}]
            )
        
        elif any(kw in text for kw in ["kg", "次", "组", "卧推", "深蹲"]):
            # 训练记录 → 记录员
            return AgentResponse(
                success=True,
                message="📝 检测到训练记录，正在解析...",
                data={"route_to": "recorder", "input": text},
                actions=[{"type": "delegate", "agent": "recorder", "context": context}]
            )
        
        elif any(kw in text for kw in ["趋势", "查看", "历史"]):
            # 查询 → 查询员
            return AgentResponse(
                success=True,
                message="📊 正在查询训练记录...",
                data={"route_to": "querier", "input": text},
                actions=[{"type": "delegate", "agent": "querier", "context": context}]
            )
        
        else:
            # 默认 → 训练师给建议
            return AgentResponse(
                success=True,
                message="🤖 收到！正在分析并给出建议...",
                data={"route_to": "trainer", "input": text},
                actions=[{"type": "delegate", "agent": "trainer", "context": context}]
            )


class CommandRouter:
    """
    指令路由器
    
    简单指令 → 直接路由到对应 agent
    复杂指令 → 交给 LLMRouter 自主决策
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """注册默认 agents"""
        self.register_agent(RecorderAgent())
        self.register_agent(LLMRouterAgent())
        # TODO: 注册 trainer, rehab, querier
    
    def register_agent(self, agent: Agent):
        """注册 agent"""
        self.agents[agent.name] = agent
    
    def parse_command(self, text: str) -> tuple:
        """
        解析指令
        
        Returns: (command, args)
        """
        text = text.strip()
        
        if not text.startswith('/'):
            return (None, text)
        
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        return (command, args)
    
    async def route(self, text: str, user_id: str = None) -> AgentResponse:
        """
        路由指令
        
        策略：
        1. /记录 → 规则解析 → RecorderAgent
        2. /llm → LLMRouterAgent（自主决策）
        3. 其他特定指令 → 对应 agent
        4. 非指令 → 提示使用 /记录 或 /llm
        """
        command, args = self.parse_command(text)
        
        context = CommandContext(
            user_id=user_id or "anonymous",
            command=command or "",
            raw_input=text,
            parsed_data={},
            history=[],
            feishu_token={}
        )
        
        # 指令路由
        if command in ['/记录', '/record']:
            # 结构化记录，规则解析
            parsed = self._parse_record_args(args)
            if not parsed:
                return AgentResponse(
                    success=False,
                    message="格式错误。正确格式:\n/记录 动作 重量 次数 [组数]\n例: /记录 卧推 60kg 10次 4组",
                    data=None,
                    actions=[]
                )
            context.parsed_data = parsed
            return await self.agents['recorder'].execute(context)
        
        elif command in ['/llm', '/ai']:
            # 自由模式，LLM 自主决策
            context.raw_input = args
            return await self.agents['llm_router'].execute(context)
        
        elif command in ['/今天练什么', '/today']:
            # TODO: 调用 TrainerAgent
            return AgentResponse(
                success=True,
                message="🎯 正在生成今日训练计划...",
                data={},
                actions=[]
            )
        
        elif command in ['/查看', '/view']:
            # TODO: 调用 QuerierAgent
            return AgentResponse(
                success=True,
                message="📊 正在查询训练记录...",
                data={},
                actions=[]
            )
        
        elif command in ['/帮助', '/help']:
            return self._help_response()
        
        else:
            # 非指令或未知指令
            return AgentResponse(
                success=False,
                message="请输入指令:\n📌 /记录 动作 重量 次数 [组数] - 快速记录\n🤖 /llm 自然语言描述 - 智能记录\n/help - 查看全部指令",
                data=None,
                actions=[]
            )
    
    def _parse_record_args(self, args: str) -> Optional[dict]:
        """
        解析 /记录 参数
        格式: 动作 重量 次数 [组数]
        """
        if not args:
            return None
        
        parts = args.split()
        if len(parts) < 3:
            return None
        
        exercise = parts[0]
        
        # 提取重量
        weight_match = re.search(r'(\d+(?:\.\d+)?)', parts[1])
        if not weight_match:
            return None
        weight = float(weight_match.group(1))
        
        # 提取次数
        reps_match = re.search(r'(\d+)', parts[2])
        if not reps_match:
            return None
        reps = int(reps_match.group(1))
        
        # 提取组数（默认1组）
        sets = 1
        if len(parts) > 3:
            sets_match = re.search(r'(\d+)', parts[3])
            if sets_match:
                sets = int(sets_match.group(1))
        
        return {
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets,
            "total_volume": weight * reps * sets
        }
    
    def _help_response(self) -> AgentResponse:
        """帮助信息"""
        help_text = """
🎯 健身助手指令

📌 /记录 动作 重量 次数 [组数]
   快速标准记录，直接写入飞书表格
   例: /记录 卧推 60kg 10次 4组

🤖 /llm [自然语言描述]
   自由对话模式，AI 智能处理
   例: /llm 今天练胸，先用60kg热身然后80kg正式组
   例: /llm [图片] 识别这张训记截图
   例: /llm 我肩膀有点疼，今天还能练推吗？
   例: /llm 看看我最近卧推的趋势

🎯 /今天练什么 [部位?]
   AI 生成今日训练建议
   例: /今天练什么 背

📋 /查看 [日期/动作?]
   查询历史训练记录
   例: /查看 昨天
   例: /查看 卧推

❓ /帮助
   显示本帮助信息

💡 提示
- /记录 用于快速标准录入
- /llm 用于复杂场景（OCR识别、伤病咨询、趋势分析等）
        """
        return AgentResponse(
            success=True,
            message=help_text,
            data={},
            actions=[]
        )


# 全局路由器实例
_router = None

def get_router() -> CommandRouter:
    """获取路由器单例"""
    global _router
    if _router is None:
        _router = CommandRouter()
    return _router
