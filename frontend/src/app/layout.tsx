import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Multilingual Chatbot",
  description: "Chat in any language",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
