"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  return (
    <div className="min-h-screen grid grid-rows-[auto_1fr_auto] font-sans bg-[#202124] text-gray-900">
      <NavBar />
      <main className="flex flex-col items-center justify-center px-4">
        <SearchHero />
      </main>
      <Footer />
    </div>
  );
}

function NavBar() {
  return (
    <header className="sticky top-0 z-50 w-full border-[#444647] border-b bg-[#202124] backdrop-blur">
      <nav className="mx-auto flex h-14 w-full max-w-6xl items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Image src="/logos/TL.svg" alt="Logo" width={24} height={24} />
          <span className="text-sm font-semibold tracking-tight text-[#FFFEFE]">
            TL Space Biology Engine
          </span>
        </div>
      </nav>
    </header>
  );
}

function SearchHero() {
  const router = useRouter();
  const [results, setResults] = useState<unknown[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const query = formData.get("q")?.toString().trim();
    if (!query) return;
    router.push(`/search/${encodeURIComponent(query)}`);
  }

  return (
    <section className="flex w-full flex-col items-center justify-center py-16 bg-[#202124]">
      <div className="mb-8 flex flex-col items-center gap-3">
        <Image
          src="/logos/TLsearch.svg"
          alt="Space Bio Engine"
          width={72}
          height={72}
          className="opacity-90"
        />
        <h1 className="text-[3rem] font-semibold tracking-tight text-[#FFFEFE]">
          Space Biology Engine
        </h1>
      </div>

      {/* ✅ Enter will now submit this form */}
      <form onSubmit={handleSubmit} className="w-full flex justify-center">
        <div
          className="group flex w-[678px] max-w-full items-center gap-2 
                        rounded-full border bg-[#4d5156] px-4 py-3 shadow-sm transition"
        >
          <input
            autoFocus
            type="text"
            name="q"
            placeholder="Search experiments, datasets, assays…"
            className="mx-2 w-full bg-transparent text-[15px] outline-none 
                       text-[#FFFEFE] placeholder:text-gray-400"
            aria-label="Search"
          />
          <button
            type="submit"
            className="rounded-2xl bg-gray-300 px-4 py-2 text-sm transition hover:bg-gray-50"
          >
            Search
          </button>
        </div>
      </form>

      <p className="mt-4 text-xs text-gray-500">
        Tip: press <kbd className="rounded border bg-gray-50 px-1">Enter</kbd>{" "}
        to search
      </p>
    </section>
  );
}

function Footer() {
  return (
    <footer className="w-full border-t border-[#444647] bg-[#171616]">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-2 px-4 py-4 text-xs text-gray-500 sm:flex-row">
        <span>United Arab Emirates</span>
        <div className="flex items-center gap-4">
          <a
            className="hover:underline"
            href="https://www.spaceappschallenge.org/"
            target="_blank"
            rel="noreferrer"
          >
            NASA Space Apps
          </a>
          <span>•</span>
          <span>
            © {new Date().getFullYear()} TerraLumen Space Biology Engine
          </span>
        </div>
      </div>
    </footer>
  );
}
