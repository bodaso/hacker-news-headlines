import posts from "@/data/best.json";

export type PostItemProps = {
  post: {
    id: string;
    title: string;
    link: string;
    scores: string;
    user: string;
    date: string; // "2006-10-09 18:21:51.000000"
  };
};

export function cleanPostData(post: PostItemProps["post"]) {
  const thisYear = new Date().getFullYear();
  const dbDate = post.date.split(" ")[0].split("-");
  const year = dbDate[0];

  if (year === thisYear.toString()) {
    dbDate.shift(); // remove year if it's current year
  } else {
    dbDate[0] = dbDate[0].slice(2); // change "2023" to "23"
  }

  const date = dbDate.reverse().join("/");
  return { ...post, date };
}

export const PostItem = ({ post }: PostItemProps) => {
  return (
    <tr className="postItem odd:bg-slate-50 even:bg-slate-100 dark:odd:bg-[#09090b] dark:even:bg-[#27272a] dark:text-[#a1a1aa]">
      <td className="p-1 sm:p-2 text-right whitespace-nowrap">{post.scores}</td>

      <td className="p-1 sm:p-2 text-left text-gray-700 dark:text-[#fafafa]">
        <a href={post.link} target="_blank" rel="nofollow" className="hover:underline decoration-1">
          {post.title}
        </a>
      </td>

      <td className="p-1 sm:p-2 whitespace-nowrap text-right">
        <a
          className="hover:underline decoration-1"
          href={`https://news.ycombinator.com/item?id=${post.id}`}
          target="_blank"
        >
          {post.date}
        </a>
      </td>
    </tr>
  );
};

export const PostList = () => {
  return (
    <table className="text-sm md:text-base text-gray-400 w-full table-fixed">
      <thead>
        <tr className="leading-6">
          <th className="w-10 sm:w-12 opacity-50 whitespace-nowrap p-2 border-b dark:border-slate-600 text-right">
            ☕
          </th>
          <th className="p-2 border-b dark:border-slate-600 text-center">Title</th>
          <th className="w-16 sm:w-20 p-2 pr-4 opacity-50 whitespace-nowrap border-b dark:border-slate-600 text-right">
            💬
          </th>
        </tr>
      </thead>

      <tbody id="postList" className="">
        {posts.map((post) => {
          return <PostItem key={post.id} post={cleanPostData(post)} />;
        })}
      </tbody>
    </table>
  );
};
