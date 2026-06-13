"use client";
import Sidebar from "../components/Sidebar";

export default function SalesPage() {
  const salesData = [
    { date: "2026-06-13", transactions: 45, revenue: "NPR 125,400" },
    { date: "2026-06-12", transactions: 52, revenue: "NPR 143,200" },
    { date: "2026-06-11", transactions: 38, revenue: "NPR 98,750" },
    { date: "2026-06-10", transactions: 61, revenue: "NPR 167,000" },
    { date: "2026-06-09", transactions: 44, revenue: "NPR 112,600" },
    { date: "2026-06-08", transactions: 33, revenue: "NPR 87,300" },
    { date: "2026-06-07", transactions: 55, revenue: "NPR 155,800" },
  ];

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">💰 Sales</h1>
          <p className="page-subtitle">Daily and monthly sales analytics</p>
        </header>
        <div className="page-body">
          <div className="stat-grid">
            <div className="stat-card"><div className="stat-label">Today&apos;s Revenue</div><div className="stat-value">NPR 125K</div><div className="stat-change positive">+8.3% vs yesterday</div></div>
            <div className="stat-card"><div className="stat-label">Monthly Revenue</div><div className="stat-value">NPR 2.4M</div><div className="stat-change positive">+12.5% vs last month</div></div>
            <div className="stat-card"><div className="stat-label">Transactions Today</div><div className="stat-value">45</div><div className="stat-change positive">+5 vs avg</div></div>
            <div className="stat-card"><div className="stat-label">Top Product</div><div className="stat-value">Laptop</div><div className="stat-change positive">32 units sold</div></div>
          </div>
          <div className="card">
            <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Weekly Sales</h2>
            <div className="table-container" style={{ border: "none" }}>
              <table className="data-table">
                <thead><tr><th>Date</th><th>Transactions</th><th>Revenue</th></tr></thead>
                <tbody>
                  {salesData.map((d) => (
                    <tr key={d.date}>
                      <td>{d.date}</td>
                      <td>{d.transactions}</td>
                      <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{d.revenue}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
