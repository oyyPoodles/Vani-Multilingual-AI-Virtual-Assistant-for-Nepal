"use client";
import Sidebar from "./components/Sidebar";

export default function DashboardPage() {
  const stats = [
    { label: "Total Sales", value: "NPR 2.4M", change: "+12.5%", positive: true },
    { label: "Active Customers", value: "8,432", change: "+340", positive: true },
    { label: "Pending Invoices", value: "127", change: "-15", positive: true },
    { label: "Employees", value: "500", change: "98% attendance", positive: true },
  ];

  const recentSales = [
    { id: "S-10042", customer: "Ram Sharma", amount: "NPR 15,400", date: "2026-06-13", product: "Laptop" },
    { id: "S-10041", customer: "Sita Adhikari", amount: "NPR 3,200", date: "2026-06-13", product: "Stationery" },
    { id: "S-10040", customer: "Hari Gurung", amount: "NPR 8,750", date: "2026-06-12", product: "Electronics" },
    { id: "S-10039", customer: "Gita Thapa", amount: "NPR 22,000", date: "2026-06-12", product: "Hardware" },
    { id: "S-10038", customer: "Krishna Basnet", amount: "NPR 5,600", date: "2026-06-12", product: "Grocery" },
  ];

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Welcome to VANI — your AI business assistant for Nepal</p>
        </header>
        <div className="page-body">
          <div className="stat-grid">
            {stats.map((s, i) => (
              <div className="stat-card" key={i}>
                <div className="stat-label">{s.label}</div>
                <div className="stat-value">{s.value}</div>
                <div className={`stat-change ${s.positive ? "positive" : "negative"}`}>
                  {s.change}
                </div>
              </div>
            ))}
          </div>

          <div className="card" style={{ marginBottom: 24 }}>
            <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16, color: "var(--text-primary)" }}>
              Recent Sales
            </h2>
            <div className="table-container" style={{ border: "none" }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Sale ID</th>
                    <th>Customer</th>
                    <th>Product</th>
                    <th>Amount</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentSales.map((sale) => (
                    <tr key={sale.id}>
                      <td style={{ color: "var(--accent-indigo)", fontWeight: 600 }}>{sale.id}</td>
                      <td>{sale.customer}</td>
                      <td>{sale.product}</td>
                      <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{sale.amount}</td>
                      <td>{sale.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
            <div className="card">
              <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>🎙️ Quick Voice Command</h3>
              <p style={{ color: "var(--text-secondary)", fontSize: 14, lineHeight: 1.6 }}>
                Try: &ldquo;आजको बिक्री कति भयो?&rdquo; or &ldquo;Show today&apos;s sales&rdquo;
              </p>
              <a href="/voice-assistant" className="btn btn-primary" style={{ marginTop: 16, display: "inline-block", textDecoration: "none" }}>
                Open Voice Assistant
              </a>
            </div>
            <div className="card">
              <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>📊 System Status</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 8, fontSize: 14, color: "var(--text-secondary)" }}>
                <div>✅ Backend API — Online</div>
                <div>✅ Database — Connected</div>
                <div>✅ Vector Store — Ready</div>
                <div>✅ ASR Engine — Loaded</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
