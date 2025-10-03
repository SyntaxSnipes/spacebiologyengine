import "./globals.css";
import type { ReactNode } from "react";


export const metadata = {
  title: "Space Biology Engine",
  description: "NASA Space Apps – Space Biology Engine",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900">
        <main className="">{children}</main>
      </body>
    </html>
  );
}
