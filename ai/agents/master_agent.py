"""
VANI — Master Agent
Routes intents to specialized sub-agents and aggregates responses.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MasterAgent:
    """
    Central orchestrator that routes user intents to specialized agents.

    Architecture:
        Master Agent
        ├── Sales Agent       — sales queries and revenue
        ├── Invoice Agent     — invoice creation and status
        ├── Inventory Agent   — stock queries and updates
        ├── CRM Agent         — customer lookup and management
        ├── HR Agent          — employee and attendance queries
        └── Analytics Agent   — reports and business intelligence
    """

    def __init__(self, db_connection=None):
        self.db = db_connection
        self.agents = {}
        self._register_agents()

    def _register_agents(self):
        """Register all sub-agents."""
        from .sales_agent import SalesAgent
        from .invoice_agent import InvoiceAgent
        from .inventory_agent import InventoryAgent
        from .crm_agent import CRMAgent
        from .hr_agent import HRAgent
        from .analytics_agent import AnalyticsAgent

        self.agents = {
            "sales_query": SalesAgent(self.db),
            "invoice_creation": InvoiceAgent(self.db),
            "inventory_query": InventoryAgent(self.db),
            "customer_lookup": CRMAgent(self.db),
            "employee_query": HRAgent(self.db),
            "attendance_query": HRAgent(self.db),
            "report_generation": AnalyticsAgent(self.db),
        }
        logger.info(f"Registered {len(self.agents)} sub-agents")

    def route(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        """
        Route intent to the appropriate agent.

        Args:
            intent: Classified intent string
            entities: Extracted entities dict
            context: Conversation context

        Returns:
            Response dict with keys: text, data, agent, success
        """
        agent = self.agents.get(intent)

        if agent is None:
            if intent == "general_conversation":
                return self._handle_general(entities, context)
            elif intent == "reminder":
                return self._handle_reminder(entities, context)
            else:
                return {
                    "text": "I'm not sure how to help with that. Could you rephrase?",
                    "data": None,
                    "agent": "master",
                    "success": False
                }

        try:
            result = agent.handle(intent, entities, context)
            result["agent"] = agent.__class__.__name__
            result["success"] = True
            logger.info(f"Routed '{intent}' to {result['agent']}")
            return result
        except Exception as e:
            logger.error(f"Agent error for '{intent}': {e}")
            return {
                "text": f"Sorry, I encountered an error processing your request.",
                "data": None,
                "agent": "master",
                "success": False,
                "error": str(e)
            }

    def _handle_general(self, entities: Dict, context: Dict = None) -> Dict:
        return {
            "text": "Namaste! I'm VANI, your AI assistant for Nepal. I can help with sales, inventory, invoices, customer info, employees, and reports. How can I assist you?",
            "data": None, "agent": "master", "success": True
        }

    def _handle_reminder(self, entities: Dict, context: Dict = None) -> Dict:
        return {
            "text": "Reminder noted. I'll remind you when it's time.",
            "data": {"reminder": entities},
            "agent": "master", "success": True
        }
