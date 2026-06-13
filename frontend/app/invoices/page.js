"use client";
import Sidebar from "../components/Sidebar";

export default function InvoicesPage() {
  const invoices = [
    { id: "INV-001", customer: "Ram Sharma", amount: "NPR 17,402", tax: "NPR 2,002", total: "NPR 19,404", status: "paid", date: "2026-06-13" },
    { id: "INV-002", customer: "Hari Gurung", amount: "NPR 45,000", tax: "NPR 5,850", total: "NPR 50,850", status: "pending", date: "2026-06-12" },
    { id: "INV-003", customer: "Gita Thapa", amount: "NPR 8,500", tax: "NPR 1,105", total: "NPR 9,605", status: "paid", date: "2026-06-11" },
    { id: "INV-004", customer: "Krishna Basnet", amount: "NPR 22,000", tax: "NPR 2,860", total: "NPR 24,860", status: "overdue", date: "2026-06-05" },
    { id: "INV-005", customer: "Laxmi Shrestha", amount: "NPR 12,300", tax: "NPR 1,599", total: "NPR 13,899", status: "pending", date: "2026-06-10" },
  ];

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">🧾 Invoices</h1>
          <p className="page-subtitle">Invoice management with 13% VAT</p>
        </header>
        <div className="page-body">
          <div className="stat-grid">
            <div className="stat-card"><div className="stat-label">Total Invoiced</div><div className="stat-value">NPR 1.2M</div></div>
            <div className="stat-card"><div className="stat-label">Paid</div><div className="stat-value">NPR 890K</div><div className="stat-change positive">74%</div></div>
            <div className="stat-card"><div className="stat-label">Pending</div><div className="stat-value">NPR 245K</div><div className="stat-change negative">12 invoices</div></div>
            <div className="stat-card"><div className="stat-label">Overdue</div><div className="stat-value">NPR 65K</div><div className="stat-change negative">3 invoices</div></div>
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead><tr><th>Invoice</th><th>Customer</th><th>Amount</th><th>Tax (13%)</th><th>Total</th><th>Status</th><th>Date</th></tr></thead>
              <tbody>
                {invoices.map((inv) => (
                  <tr key={inv.id}>
                    <td style={{ color: "var(--accent-indigo)", fontWeight: 600 }}>{inv.id}</td>
                    <td>{inv.customer}</td>
                    <td>{inv.amount}</td>
                    <td>{inv.tax}</td>
                    <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{inv.total}</td>
                    <td><span className={`badge badge-${inv.status}`}>{inv.status}</span></td>
                    <td>{inv.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
