"""VANI — Inventory Agent: Handles stock queries and updates."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class InventoryAgent:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        product = entities.get("products", [None])[0] if entities.get("products") else None

        if product:
            return self._check_product_stock(product)
        return self._get_inventory_summary()

    def _check_product_stock(self, product: str) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT product_name, stock, price, category FROM products WHERE product_name ILIKE %s LIMIT 5",
                    (f"%{product}%",)
                )
                rows = cursor.fetchall()
                if rows:
                    items = [{"name": r[0], "stock": r[1], "price": float(r[2]), "category": r[3]} for r in rows]
                    text = "\n".join([f"- {i['name']}: {i['stock']} units @ NPR {i['price']:,.2f}" for i in items])
                    return {"text": f"Stock for '{product}':\n{text}", "data": {"items": items}}
                return {"text": f"No products found matching '{product}'.", "data": None}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}

        import random
        stock = random.randint(0, 200)
        return {"text": f"{product}: {stock} units in stock.", "data": {"product": product, "stock": stock, "mock": True}}

    def _get_inventory_summary(self) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT category, COUNT(*), SUM(stock) FROM products GROUP BY category")
                rows = cursor.fetchall()
                items = [{"category": r[0], "products": r[1], "total_stock": r[2]} for r in rows]
                text = "\n".join([f"- {i['category']}: {i['products']} products, {i['total_stock']} units" for i in items])
                return {"text": f"Inventory Summary:\n{text}", "data": {"categories": items}}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "Inventory: 5000 products across 6 categories.", "data": {"mock": True}}
