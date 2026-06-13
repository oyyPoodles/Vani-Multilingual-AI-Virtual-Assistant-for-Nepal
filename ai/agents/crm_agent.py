"""VANI — CRM Agent: Handles customer lookup and management."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CRMAgent:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        customer = entities.get("customers", [None])[0] if entities.get("customers") else None
        if customer:
            return self._lookup_customer(customer)
        return self._get_customer_summary()

    def _lookup_customer(self, name: str) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT customer_id, name, phone, email, address, credit_balance "
                    "FROM customers WHERE name ILIKE %s LIMIT 5",
                    (f"%{name}%",)
                )
                rows = cursor.fetchall()
                if rows:
                    customers = [{"id": r[0], "name": r[1], "phone": r[2], "email": r[3],
                                  "address": r[4], "credit": float(r[5])} for r in rows]
                    c = customers[0]
                    text = (f"Customer: {c['name']}\nPhone: {c['phone']}\n"
                            f"Email: {c['email']}\nAddress: {c['address']}\n"
                            f"Credit Balance: NPR {c['credit']:,.2f}")
                    return {"text": text, "data": {"customers": customers}}
                return {"text": f"No customer found matching '{name}'.", "data": None}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": f"Customer '{name}': Phone: +977-9841234567, Credit: NPR 5,000", "data": {"mock": True}}

    def _get_customer_summary(self) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT COUNT(*), COALESCE(SUM(credit_balance),0) FROM customers")
                count, credit = cursor.fetchone()
                return {"text": f"Total customers: {count}. Total outstanding credit: NPR {credit:,.2f}.",
                        "data": {"count": count, "total_credit": float(credit)}}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "10,000 customers in database.", "data": {"mock": True}}
