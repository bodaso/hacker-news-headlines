"use client";

import { useEffect, useState } from "react";
import { PostItemProps } from "../components/PostList";

/**
 * A fun page that shows a random post, more recent ones have a higher chance of being picked.
 */
export default function Page() {
  const [randomPost, setRandomPost] = useState<PostItemProps["post"]>();

  useEffect(() => {
    fetch("/api/random")
      .then((res) => res.json())
      .then((data) => {
        setRandomPost(data.post);
      });
  }, []);

  if (!randomPost) {
    return null;
  }

  return (
    <div className="w-full text-center mt-20 p-3">
      <div className="mb-3">
        <a className="text-xl hover:underline decoration-1" href={randomPost.link} target="_blank">
          {randomPost.title}
        </a>
        <p className="mt-1 text-sm">{randomPost.link}</p>
      </div>

      <div className="flex justify-center gap-x-10">
        <p>{randomPost.scores} points</p>
        <a
          className="hover:underline decoration-1"
          href={`https://news.ycombinator.com/item?id=${randomPost.id}`}
          target="_blank"
        >
          {randomPost.date.split(" ")[0].split("-").reverse().join("-")}
        </a>
      </div>
    </div>
  );
}
