// import { ColorMode } from "./ColorMode";

export const Header = () => {
  return (
    <div className="relative isolate overflow-hidden pt-3">
      <div className="flex justify-center items-center">
        <a href="/">
          <strong className="font-semibold">Hacker News Headlines</strong>
          <svg viewBox="0 0 2 2" className="mx-2 inline h-0.5 w-0.5 fill-current" aria-hidden="true">
            <circle cx="1" cy="1" r="1" />
          </svg>
          <span className="tracking-wider">hnhd.io</span>
        </a>
      </div>

      <div className="flex justify-center items-center gap-x-3 mt-3">
        <a href="https://github.com/bodaso/hacker-news-headlines" target="_blank">
          <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/bodaso/hacker-news-headlines" />
        </a>
        {/* <ColorMode /> */}
      </div>
    </div>
  );
};
