"""
Reference commit/projection flow for a future backendized version.

This module documents the intended separation between:
- user-facing skills
- system-owned commit/projection steps

It is not wired into the current Feishu MVP runtime.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ProjectionResult:
    commit_status: str
    pending_sync_targets: List[str] = field(default_factory=list)


def commit_main_entities(entity_types: List[str]) -> Dict[str, List[str]]:
    """Reference step: commit main truth entities first."""
    return {"committed_entities": entity_types}


def run_projections(targets: List[str]) -> ProjectionResult:
    """Reference step: sync key projections after main commit.

    In the current skeleton this is intentionally a no-op reference.
    """
    return ProjectionResult(commit_status="committed", pending_sync_targets=[])


def mark_pending_sync_if_failed(targets: List[str]) -> ProjectionResult:
    """Reference step: represent projection failure explicitly."""
    return ProjectionResult(commit_status="pending_sync", pending_sync_targets=targets)
