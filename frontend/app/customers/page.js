"use client";
import Sidebar from "../components/Sidebar";

export default function CustomersPage() {
  const customers = [
    { id: 1, name: "Ram Sharma", phone: "+977-9841234567", email: "ram@gmail.com", address: "Thamel-5, Kathmandu", credit: "NPR 5,200" },
    { id: 2, name: "Sita Adhikari", phone: "+977-9851234567", email: "sita@yahoo.com", address: "Kalimati-3, Kathmandu", credit: "NPR 0" },
    { id: 3, name: "Hari Gurung", phone: "+977-9861234567", email: "hari@outlook.com", address: "Lakeside-6, Pokhara", credit: "NPR 12,400" },
    { id: 4, name: "Gita Thapa", phone: "+977-9801234567", email: "gita@gmail.com", address: "Lagankhel-2, Lalitpur", credit: "NPR 800" },
    { id: 5, name: "Krishna Basnet", phone: "+977-9811234567", email: "krishna@mail.com", address: "Biratnagar-10", credit: "NPR 0" },
    { id: 6, name: "Laxmi Shrestha", phone: "+977-9741234567", email: "", address: "Bhaktapur-7", credit: "NPR 3,500" },
  ];

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">👥 Customers</h1>
          <p className="page-subtitle">Customer database and management</p>
        </header>
        <div className="page-body">
          <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
            <div className="search-box" style={{ flex: 1, marginBottom: 0 }}>
              <span>🔍</span>
              <input type="text" placeholder="Search customers by name, phone..." id="customer-search" />
            </div>
            <button className="btn btn-primary">+ Add Customer</button>
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Address</th><th>Credit Balance</th></tr></thead>
              <tbody>
                {customers.map((c) => (
                  <tr key={c.id}>
                    <td style={{ color: "var(--accent-indigo)" }}>#{c.id}</td>
                    <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{c.name}</td>
                    <td>{c.phone}</td>
                    <td>{c.email || "—"}</td>
                    <td>{c.address}</td>
                    <td style={{ fontWeight: 600, color: c.credit !== "NPR 0" ? "var(--accent-amber)" : "var(--accent-emerald)" }}>{c.credit}</td>
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
