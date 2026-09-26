import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { Nav } from "./nav";

export const metadata: Metadata = {
  title: "AegisDeploy Console",
  description: "AI-powered SRE control plane — P2 scaffold",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="side">
            <div className="brand">
              Aegis<span>Deploy</span>
            </div>
            <p>SRE control plane · P2 scaffold</p>
            <Nav />
          </aside>
          <div className="main">{children}</div>
        </div>
      </body>
    </html>
  );
}
