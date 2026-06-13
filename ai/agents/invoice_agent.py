"""VANI — Invoice Agent: Handles invoice creation, status, and management."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class InvoiceAgent:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        customer = entities.get("customers", [None])[0] if entities.get("customers") else None
        amounts = entities.get("amounts", [])
        amount = amounts[0]["value"] if amounts else None

        if "status" in str(entities) or "pending" in str(entities):
            return self._get_pending_invoices()
        elif customer and amount:
            return self._create_invoice(customer, amount)
        elif customer:
            return self._get_customer_invoices(customer)
        else:
            return self._get_invoice_summary()

    def _create_invoice(self, customer: str, amount: float) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                tax = round(amount * 0.13, 2)
                total = round(amount + tax, 2)
                cursor.execute(
                    "INSERT INTO invoices (customer_id, amount, tax_amount, total_amount) "
                    "VALUES ((SELECT customer_id FROM customers WHERE name ILIKE %s LIMIT 1), %s, %s, %s) RETURNING invoice_id",
                    (f"%{customer}%", amount, tax, total)
                )
                inv_id = cursor.fetchone()[0]
                self.db.commit()
                return {"text": f"Invoice #{inv_id} created for {customer}: NPR {total:,.2f} (incl. 13% VAT).",
                        "data": {"invoice_id": inv_id, "amount": amount, "tax": tax, "total": total}}
            except Exception as e:
                return {"text": f"Failed to create invoice: {e}", "data": None}
        return {"text": f"Invoice draft for {customer}: NPR {amount:,.2f} + 13% VAT.", "data": {"mock": True}}

    def _get_pending_invoices(self) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT COUNT(*), COALESCE(SUM(total_amount),0) FROM invoices WHERE status='pending'")
                count, total = cursor.fetchone()
                return {"text": f"{count} pending invoices totaling NPR {total:,.2f}.", "data": {"count": count, "total": float(total)}}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "12 pending invoices totaling NPR 345,000.", "data": {"mock": True}}

    def _get_customer_invoices(self, customer: str) -> Dict:
        return {"text": f"Retrieving invoices for {customer}...", "data": {"customer": customer}}

    def _get_invoice_summary(self) -> Dict:
        return {"text": "Invoice summary: Use 'create invoice for [customer] [amount]' to generate.", "data": None}
