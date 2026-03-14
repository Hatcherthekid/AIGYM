"""
指令路由器
解析用户输入的命令，分发到不同处理器
"""

from typing import Dict, Optional, Callable
import re
from dataclasses import dataclass


@dataclass
class CommandResult:
    """指令解析结果"""
    command: str          # /记录 /llm /今天练什么
    args: list           # 位置参数
    kwargs: dict         # 命名参数
    raw_text: str        # 原始文本
    is_command: bool     # 是否是指令格式


class CommandRouter:
    """指令路由器"""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
    
    def register(self, command: str, handler: Callable):
        """注册指令处理器"""
        self.handlers[command] = handler
    
    def parse(self, text: str) -> CommandResult:
        """
        解析指令
        
        支持格式：
        - /记录 卧推 60kg 10次 4组
        - /记录 动作=卧推 重量=60kg 次数=10 组数=4
        - /llm 今天练胸做了卧推和飞鸟
        """
        text = text.strip()
        
        # 判断是否以 / 开头
        if not text.startswith('/'):
            return CommandResult(
                command="",
                args=[],
                kwargs={},
                raw_text=text,
                is_command=False
            )
        
        # 分割命令和参数
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args_text = parts[1] if len(parts) > 1 else ""
        
        # 解析参数
        args, kwargs = self._parse_args(args_text)
        
        return CommandResult(
            command=command,
            args=args,
            kwargs=kwargs,
            raw_text=text,
            is_command=True
        )
    
    def _parse_args(self, text: str) -> tuple:
        """
        解析参数
        
        支持：
        - 位置参数: 卧推 60kg 10次
        - 键值对: 动作=卧推 重量=60kg
        """
        if not text:
            return [], {}
        
        args = []
        kwargs = {}
        
        # 先尝试匹配键值对
        kv_pattern = r'(\w+)[=:：]\s*([^\s]+)'
        kv_matches = re.findall(kv_pattern, text)
        
        if kv_matches:
            # 键值对模式
            for key, value in kv_matches:
                kwargs[key] = value
            # 剩余部分作为位置参数
            remaining = re.sub(kv_pattern, '', text).strip()
            if remaining:
                args = remaining.split()
        else:
            # 纯位置参数模式
            args = text.split()
        
        return args, kwargs
    
    async def handle(self, text: str, user_id: str = None) -> dict:
        """
        处理指令
        
        Returns:
            {
                "success": bool,
                "type": "command" | "natural",
                "command": str,
                "result": dict,
                "message": str
            }
        """
        parsed = self.parse(text)
        
        if not parsed.is_command:
            # 非指令，按自然语言处理
            return {
                "success": True,
                "type": "natural",
                "command": "",
                "result": None,
                "message": "非指令格式，建议用 /记录 或 /llm"
            }
        
        handler = self.handlers.get(parsed.command)
        if not handler:
            available = ", ".join(self.handlers.keys())
            return {
                "success": False,
                "type": "command",
                "command": parsed.command,
                "result": None,
                "message": f"未知指令: {parsed.command}\n可用指令: {available}"
            }
        
        # 调用处理器
        result = await handler(parsed, user_id)
        return {
            "success": True,
            "type": "command",
            "command": parsed.command,
            "result": result,
            "message": result.get("message", "处理完成")
        }


# ============ 指令处理器 ============

async def handle_record(cmd: CommandResult, user_id: str) -> dict:
    """
    /记录 指令处理器
    
    格式: /记录 动作 重量 次数 组数
    示例: /记录 卧推 60kg 10次 4组
    """
    args = cmd.args
    
    # 参数校验
    if len(args) < 3:
        return {
            "success": False,
            "message": "格式错误。正确格式:\n/记录 动作 重量 次数 [组数]\n例: /记录 卧推 60kg 10次 4组"
        }
    
    # 解析参数
    exercise = args[0]
    
    # 提取数字（支持 60kg, 60公斤, 60 等格式）
    weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|公斤)?', args[1])
    reps_match = re.search(r'(\d+)\s*(?:次|个)?', args[2])
    sets_match = re.search(r'(\d+)\s*(?:组|set)?', args[3]) if len(args) > 3 else None
    
    if not weight_match or not reps_match:
        return {
            "success": False,
            "message": "无法解析重量或次数。请使用格式: 60kg 10次"
        }
    
    weight = float(weight_match.group(1))
    reps = int(reps_match.group(1))
    sets = int(sets_match.group(1)) if sets_match else 1
    
    # 计算容量
    total_volume = weight * reps * sets
    
    # TODO: 写入飞书表格
    return {
        "success": True,
        "data": {
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets,
            "total_volume": total_volume
        },
        "message": f"✅ 已记录: {exercise} {weight}kg × {reps}次 × {sets}组 = {total_volume}kg"
    }


async def handle_llm(cmd: CommandResult, user_id: str) -> dict:
    """
    /llm 指令处理器
    调用 LLM 解析复杂输入
    """
    natural_text = " ".join(cmd.args)
    
    # TODO: 调用 LLM API 解析
    # result = await llm_parser.parse(natural_text)
    
    return {
        "success": True,
        "data": {
            "raw_text": natural_text,
            "parsed_by": "llm"
        },
        "message": f"🤖 LLM 解析中: {natural_text[:50]}..."
    }


async def handle_today(cmd: CommandResult, user_id: str) -> dict:
    """
    /今天练什么 指令处理器
    """
    # TODO: 查询最近训练记录，AI生成建议
    
    body_part = cmd.args[0] if cmd.args else None
    
    return {
        "success": True,
        "data": {
            "suggested_body_part": body_part or "根据历史自动推断",
            "exercises": []
        },
        "message": "🎯 正在生成今日训练计划..."
    }


async def handle_view(cmd: CommandResult, user_id: str) -> dict:
    """
    /查看 指令处理器
    查询飞书表格记录
    """
    return {
        "success": True,
        "data": {
            "query": cmd.args
        },
        "message": "📊 正在查询训练记录..."
    }


async def handle_help(cmd: CommandResult, user_id: str) -> dict:
    """
    /帮助 指令处理器
    """
    help_text = """
🎯 健身助手指令列表

📌 快速记录（推荐）
/记录 动作 重量 次数 [组数]
例: /记录 卧推 60kg 10次 4组
例: /记录 深蹲 100公斤 5次 5组

🤖 智能记录（复杂描述）
/llm 自然语言描述
例: /llm 今天练胸，先用60kg卧推热身，然后上重量到80kg做正式组

📋 查看记录
/查看 [日期/动作]
例: /查看 昨天
例: /查看 卧推

🎯 训练建议
/今天练什么 [部位]
例: /今天练什么
例: /今天练什么 背

❓ 帮助
/帮助 - 显示本帮助信息

💡 提示
- 重量支持: 60kg, 60公斤, 60
- 次数支持: 10次, 10个, 10
- 组数支持: 4组, 4set, 4
    """
    return {
        "success": True,
        "data": {},
        "message": help_text
    }


# 创建路由器实例
def create_router() -> CommandRouter:
    """创建并配置指令路由器"""
    router = CommandRouter()
    
    router.register("/记录", handle_record)
    router.register("/record", handle_record)  # 英文别名
    router.register("/llm", handle_llm)
    router.register("/今天练什么", handle_today)
    router.register("/today", handle_today)  # 英文别名
    router.register("/查看", handle_view)
    router.register("/view", handle_view)  # 英文别名
    router.register("/帮助", handle_help)
    router.register("/help", handle_help)  # 英文别名
    
    return router
