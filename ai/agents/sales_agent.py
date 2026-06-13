"""
VANI — Sales Agent
Handles sales queries, revenue analysis, and sales data retrieval.
"""

import logging
from typing import Dict, Any, Optional
from datetime import date, timedelta

logger = logging.getLogger(__name__)


class SalesAgent:
    """Handles all sales-related queries."""

    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        """Process sales query and return results."""
        date_filter = self._resolve_date(entities)
        product = entities.get("products", [None])[0] if entities.get("products") else None
        customer = entities.get("customers", [None])[0] if entities.get("customers") else None

        if self.db:
            return self._query_database(date_filter, product, customer)
        else:
            return self._mock_response(date_filter, product, customer)

    def _resolve_date(self, entities: Dict) -> str:
        """Resolve date entity to SQL date filter."""
        dates = entities.get("dates", [])
        if not dates:
            return "today"
        return dates[0].get("value", "today")

    def _query_database(self, date_filter: str, product: str = None, customer: str = None) -> Dict:
        """Query PostgreSQL for sales data."""
        # Build SQL based on filters
        where_clauses = []
        params = []

        if date_filter == "today":
            where_clauses.append("date = CURRENT_DATE")
        elif date_filter == "yesterday":
            where_clauses.append("date = CURRENT_DATE - INTERVAL '1 day'")
        elif date_filter == "this_week":
            where_clauses.append("date >= date_trunc('week', CURRENT_DATE)")
        elif date_filter == "this_month":
            where_clauses.append("date >= date_trunc('month', CURRENT_DATE)")

        where = " AND ".join(where_clauses) if where_clauses else "1=1"
        query = f"SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM sales WHERE {where}"

        try:
            cursor = self.db.cursor()
            cursor.execute(query, params)
            count, total = cursor.fetchone()
            return {
                "text": f"Total sales ({date_filter}): NPR {total:,.2f} across {count} transactions.",
                "data": {"count": count, "total": float(total), "period": date_filter}
            }
        except Exception as e:
            logger.error(f"Sales query failed: {e}")
            return {"text": "Unable to fetch sales data.", "data": None}

    def _mock_response(self, date_filter: str, product: str = None, customer: str = None) -> Dict:
        """Return mock response when DB is not connected."""
        import random
        total = random.randint(20000, 80000)
        count = random.randint(15, 50)
        return {
            "text": f"Total sales ({date_filter}): NPR {total:,} across {count} transactions.",
            "data": {"count": count, "total": total, "period": date_filter, "mock": True}
        }
