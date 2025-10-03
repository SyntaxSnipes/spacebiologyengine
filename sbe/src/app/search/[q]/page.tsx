// sbe/src/app/search/[q]/page.tsx
import { headers } from "next/headers";

export const runtime = "nodejs"; // safe for localhost + env

type SearchItem = {
  id: string;
  name: string;
  type: "experiment" | "dataset" | "assay" | string;
};

function getBaseUrl() {
  const h = headers();
  // Vercel/Proxy friendly
  const host = h.get("x-forwarded-host") ?? h.get("host");
  const proto = h.get("x-forwarded-proto") ?? "http";
  return `${proto}://${host}`;
}

export default async function SearchResults({
  params,
}: { params: { q: string } }) {
  const q = decodeURIComponent(params.q);
  const base = getBaseUrl();

  const res = await fetch(`${base}/api/search?q=${encodeURIComponent(q)}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    return (
      <div className="p-6 text-red-400">
        Search failed ({res.status}). Make sure the mock route exists at
        <code className="ml-1">src/app/api/search/route.ts</code> and that the dev server was restarted.
      </div>
    );
  }

  const data: { results: SearchItem[] } = await res.json();

  return (
    <div className="p-6 text-[#FFFEFE]">
      <h1 className="mb-4 text-xl">
        Results for <span className="opacity-90">“{q}”</span>
      </h1>
      <ul className="space-y-2">
        {data.results?.length ? (
          data.results.map((item) => (
            <li key={item.id} className="opacity-90">
              {item.name} <span className="text-xs opacity-60">({item.type})</span>
            </li>
          ))
        ) : (
          <li className="opacity-60">No results</li>
        )}
      </ul>
    </div>
  );
}
