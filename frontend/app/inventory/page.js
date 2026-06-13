"use client";
import Sidebar from "../components/Sidebar";

export default function InventoryPage() {
  const products = [
    { id: 1, name: "CG Laptop (Premium)", stock: 42, price: "NPR 85,000", category: "Electronics" },
    { id: 2, name: "Goldstar Mobile Phone", stock: 128, price: "NPR 25,000", category: "Electronics" },
    { id: 3, name: "Rice (Basmati)", stock: 340, price: "NPR 180/kg", category: "Grocery" },
    { id: 4, name: "Notebook (Standard)", stock: 500, price: "NPR 120", category: "Stationery" },
    { id: 5, name: "Cement (50kg)", stock: 0, price: "NPR 950", category: "Hardware" },
    { id: 6, name: "Paracetamol", stock: 8, price: "NPR 25", category: "Pharmacy" },
    { id: 7, name: "T-Shirt", stock: 200, price: "NPR 800", category: "Clothing" },
    { id: 8, name: "Everest Drill Machine", stock: 15, price: "NPR 12,500", category: "Hardware" },
  ];

  const getStockBadge = (stock) => {
    if (stock === 0) return <span className="badge badge-overdue">Out of Stock</span>;
    if (stock < 10) return <span className="badge badge-pending">Low Stock</span>;
    return <span className="badge badge-paid">In Stock</span>;
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">📦 Inventory</h1>
          <p className="page-subtitle">Product stock management</p>
        </header>
        <div className="page-body">
          <div className="search-box">
            <span>🔍</span>
            <input type="text" placeholder="Search products..." id="inventory-search" />
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead><tr><th>ID</th><th>Product</th><th>Category</th><th>Price</th><th>Stock</th><th>Status</th></tr></thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id}>
                    <td style={{ color: "var(--accent-indigo)" }}>#{p.id}</td>
                    <td style={{ fontWeight: 600, color: "var(--text-primary)" }}>{p.name}</td>
                    <td>{p.category}</td>
                    <td>{p.price}</td>
                    <td>{p.stock}</td>
                    <td>{getStockBadge(p.stock)}</td>
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
