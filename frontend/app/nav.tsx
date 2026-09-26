"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Command Center" },
  { href: "/services", label: "Services" },
  { href: "/incidents", label: "Incidents" },
  { href: "/deployments", label: "Deployments" },
];

export function Nav() {
  const path = usePathname();
  return (
    <nav className="nav">
      {LINKS.map((link) => (
        <Link key={link.href} href={link.href} className={path === link.href ? "active" : ""}>
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
