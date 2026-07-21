"""Reusable, backend-neutral widgets for the JARVIS desktop interface."""

from gui.widgets.ai_core_widget import AICoreWidget
from gui.widgets.dashboard_panels import (
    ApplicationsPanel,
    CapabilitySummaryPanel,
    ConversationPanel,
    OfficeBrowserPanel,
    QuickActionsPanel,
    ReasoningPanel,
    SystemMetricsPanel,
    TaskPanel,
    TaskTimelinePanel,
    VoicePanel,
)
from gui.widgets.hud import DigitalClock, HudPanel, SubsystemStatusBar

__all__ = [
    "AICoreWidget",
    "ApplicationsPanel",
    "CapabilitySummaryPanel",
    "ConversationPanel",
    "DigitalClock",
    "HudPanel",
    "OfficeBrowserPanel",
    "QuickActionsPanel",
    "ReasoningPanel",
    "SubsystemStatusBar",
    "SystemMetricsPanel",
    "TaskPanel",
    "TaskTimelinePanel",
    "VoicePanel",
]
