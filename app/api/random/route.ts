import data from "@/data/best.json";

// tell route being rendered for each user at request time
export const dynamic = "force-dynamic";

function filterPosts(minYear: number, maxYear: number, posts: { year: number }[]) {
  return posts.filter(({ year }) => year >= minYear && year < maxYear);
}

export async function GET() {
  const randomNumber = Math.random();
  const thisYear = new Date().getFullYear();
  const yearDiff = thisYear - 2006;
  const quarterDiff = Math.ceil(yearDiff / 4);

  const posts = data.map((post) => ({
    ...post,
    year: new Date(post.date).getFullYear(),
  }));

  let post;
  let filtered = [];

  if (randomNumber < 0.4) {
    // 40% of chance
    filtered = filterPosts(thisYear - quarterDiff, thisYear + 1, posts);
  } else if (randomNumber < 0.7) {
    // 30% of chance
    filtered = filterPosts(thisYear - quarterDiff * 2, thisYear - quarterDiff, posts);
  } else if (randomNumber < 0.9) {
    // 20% of chance
    filtered = filterPosts(thisYear - quarterDiff * 3, thisYear - quarterDiff * 2, posts);
  } else {
    // 10% of chance
    filtered = filterPosts(2006, thisYear - quarterDiff * 3, posts);
  }

  if (filtered.length > 0) {
    post = filtered[Math.floor(Math.random() * filtered.length)];
  } else {
    // Handle the case where no posts are found in filtered
    post = posts[Math.floor(Math.random() * posts.length)];
  }

  return Response.json({ post });
}
