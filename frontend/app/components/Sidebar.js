"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", icon: "📊", label: "Dashboard" },
  { href: "/sales", icon: "💰", label: "Sales" },
  { href: "/inventory", icon: "📦", label: "Inventory" },
  { href: "/customers", icon: "👥", label: "Customers" },
  { href: "/invoices", icon: "🧾", label: "Invoices" },
  { href: "/voice-assistant", icon: "🎙️", label: "Voice Assistant" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <Link href="/" className="sidebar-logo">
        <div className="sidebar-logo-icon">V</div>
        <span className="sidebar-logo-text">VANI</span>
      </Link>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`sidebar-link ${pathname === item.href ? "active" : ""}`}
          >
            <span className="sidebar-link-icon">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
      <div style={{ padding: "16px 8px", borderTop: "1px solid var(--border-color)", marginTop: "auto" }}>
        <div style={{ fontSize: "11px", color: "var(--text-muted)", textAlign: "center" }}>
          🇳🇵 Built for Transparent Nepal
        </div>
      </div>
    </aside>
  );
}
