"""VANI — HR Agent: Handles employee and attendance queries."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class HRAgent:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def handle(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        if intent == "attendance_query":
            return self._get_attendance(entities)
        return self._get_employee_info(entities)

    def _get_attendance(self, entities: Dict) -> Dict:
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FILTER (WHERE attendance = TRUE), "
                    "COUNT(*) FILTER (WHERE attendance = FALSE), COUNT(*) FROM employees"
                )
                present, absent, total = cursor.fetchone()
                return {
                    "text": f"Attendance: {present}/{total} present, {absent} absent.",
                    "data": {"present": present, "absent": absent, "total": total}
                }
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "Attendance: 420/500 present, 80 absent.", "data": {"mock": True}}

    def _get_employee_info(self, entities: Dict) -> Dict:
        name = entities.get("customers", [None])[0] if entities.get("customers") else None
        if name and self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    "SELECT name, department, position, salary FROM employees WHERE name ILIKE %s LIMIT 5",
                    (f"%{name}%",)
                )
                rows = cursor.fetchall()
                if rows:
                    emp = [{"name": r[0], "dept": r[1], "position": r[2], "salary": float(r[3])} for r in rows]
                    e = emp[0]
                    return {"text": f"{e['name']} — {e['position']}, {e['dept']} (NPR {e['salary']:,.0f}/mo)",
                            "data": {"employees": emp}}
                return {"text": f"No employee found matching '{name}'.", "data": None}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}

        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT COUNT(*), AVG(salary) FROM employees")
                count, avg_sal = cursor.fetchone()
                return {"text": f"Total employees: {count}. Average salary: NPR {avg_sal:,.0f}.",
                        "data": {"count": count, "avg_salary": float(avg_sal)}}
            except Exception as e:
                return {"text": f"Error: {e}", "data": None}
        return {"text": "500 employees. Average salary: NPR 25,000.", "data": {"mock": True}}
