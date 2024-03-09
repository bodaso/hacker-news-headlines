import { Analytics } from "@vercel/analytics/react";

import { Header } from "@/app/components/Header";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <meta charSet="UTF-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />

        <title>Hacker News Headlines | hnhd.io</title>
        <meta name="description" content="The complete history of #1 posts on hacker news" />

        <link rel="icon" type="image/png" href="./coffee.png" />
        <link rel="apple-touch-icon" href="./coffee.png" />

        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://www.hnhd.io/" />
        <meta property="og:title" content="Hacker News Headlines | hnhd.io" />
        <meta property="og:image" content="https://www.hnhd.io/coffee.png" />
        <meta property="og:description" content="The complete history of #1 posts on hacker news" />

        <meta name="twitter:card" content="summary" />
        <meta name="twitter:url" content="https://www.hnhd.io/" />
        <meta name="twitter:title" content="Hacker News Headlines | hnhd.io" />
        <meta name="twitter:description" content="The complete history of #1 posts on hacker news" />
        <meta name="twitter:image" content="https://www.hnhd.io/coffee.png" />

        {/* On page load or when changing themes, best to add inline in `head` to avoid FOUC */}
        {/* <script
          dangerouslySetInnerHTML={{
            __html: `
          document.documentElement.classList.add("dark");
          if ( localStorage.theme === "light" || (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: light)").matches)) {
            document.documentElement.classList.remove("dark");
          }
        `,
          }}
        ></script> */}
      </head>

      <body className="max-w-screen-md mx-auto mb-28 p-2 bg-slate-50 dark:bg-[#09090b] dark:text-white">
        <Header />
        {children}
        <Analytics />
      </body>
    </html>
  );
}
