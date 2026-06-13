import "./globals.css";

export const metadata = {
  title: "VANI — AI Voice Assistant for Nepal",
  description: "Multilingual AI-powered virtual assistant for transparent governance and smart tourism in Nepal. Supporting Nepali and English.",
  keywords: "VANI, Nepal, AI, Voice Assistant, Governance, Tourism, Nepali, NLP",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>{children}</body>
    </html>
  );
}
