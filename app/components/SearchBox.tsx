"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
// import debounce from "debounce";

const SearchBoxElement = () => {
  const [search, setSearch] = useState("");
  const searchParams = useSearchParams();

  useEffect(() => {
    const qParam = searchParams.get("q"); // first load, look for any query strings
    if (qParam && qParam.length > 0) {
      setSearch(qParam);
    }
  }, []);

  useEffect(() => {
    if (search === "") {
      document.querySelectorAll(".postItem.hidden").forEach((el) => {
        el.classList.remove("hidden");
      });
      window.history.replaceState({}, "", "/");
    }

    if (search && search.length > 0) {
      // replace url query string with new search value
      const params = new URLSearchParams(searchParams.toString());
      params.set("q", search);
      window.history.pushState(null, "", `?${params.toString()}`);

      document.querySelectorAll(".postItem").forEach((el) => {
        const textContent = el.textContent;
        if (textContent && textContent.toLowerCase().includes(search.toLowerCase())) {
          el.classList.remove("hidden");
        } else {
          el.classList.add("hidden");
        }
      });
    }
  }, [search]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  return (
    <div className="mt-8 mb-3">
      <form className="group relative">
        <input
          id="searchBox"
          className="w-42 focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none leading-4 text-slate-900 placeholder-slate-400 rounded-sm py-1 pl-3 ring-1 ring-slate-200 shadow-sm"
          type="text"
          aria-label="Search keyword"
          placeholder="Search keyword..."
          value={search}
          onInput={handleChange}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
            }
          }}
          onSubmit={(e) => {
            e.preventDefault();
          }}
        />
      </form>
    </div>
  );
};

export const SearchBox = () => {
  return (
    <Suspense>
      <SearchBoxElement />
    </Suspense>
  );
};
