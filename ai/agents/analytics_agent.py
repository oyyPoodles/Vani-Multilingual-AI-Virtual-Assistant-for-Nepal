"""VANI — Analytics Agent: Handles reports and business intelligence."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AnalyticsAgent:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        dates = entities.get("dates", [])
        period = dates[0]["value"] if dates else "this_month"

        report_type = self._detect_report_type(entities)

        if report_type == "sales":
            return self._sales_report(period)
        elif report_type == "inventory":
            return self._inventory_report()
        elif report_type == "employee":
            return self._employee_report()
        return self._general_report(period)

    def _detect_report_type(self, entities: Dict) -> str:
        text = str(entities).lower()
        if any(w in text for w in ["sales", "revenue", "बिक्री"]):
            return "sales"
        elif any(w in text for w in ["inventory", "stock", "स्टक"]):
            return "inventory"
        elif any(w in text for w in ["employee", "staff", "कर्मचारी"]):
            return "employee"
        return "general"

    def _sales_report(self, period: str) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT date, COUNT(*), SUM(amount) FROM sales "
                    "WHERE date >= date_trunc(%s, CURRENT_DATE) "
                    "GROUP BY date ORDER BY date DESC LIMIT 30",
                    (period.replace("this_", ""),)
                )
                rows = cursor.fetchall()
                data = [{"date": str(r[0]), "transactions": r[1], "revenue": float(r[2])} for r in rows]
                total = sum(d["revenue"] for d in data)
                return {
                    "text": f"Sales Report ({period}): NPR {total:,.2f} across {len(data)} days.",
                    "data": {"report": data, "total": total, "period": period}
                }
            except Exception as e:
                return {"text": f"Error generating report: {e}", "data": None}
        return {"text": f"Sales Report ({period}): NPR 2,450,000 total revenue.", "data": {"mock": True}}

    def _inventory_report(self) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT category, COUNT(*), SUM(stock), "
                    "COUNT(*) FILTER (WHERE stock = 0), "
                    "COUNT(*) FILTER (WHERE stock < 10) "
                    "FROM products GROUP BY category"
                )
                rows = cursor.fetchall()
                data = [{"category": r[0], "products": r[1], "stock": r[2],
                         "out_of_stock": r[3], "low_stock": r[4]} for r in rows]
                return {"text": "Inventory report generated.", "data": {"categories": data}}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "Inventory Report: 5000 products, 120 out of stock.", "data": {"mock": True}}

    def _employee_report(self) -> Dict:
        return {"text": "Employee report: 500 staff across 8 departments.", "data": {"mock": True}}

    def _general_report(self, period: str) -> Dict:
        return {
            "text": f"Business report ({period}): Specify type — sales, inventory, or employee.",
            "data": {"period": period}
        }
