import { SearchBox } from "@/app/components/SearchBox";
import { PostList } from "@/app/components/PostList";
import { BackToTop } from "./components/BackToTop";

export default function Page() {
  return (
    <>
      <SearchBox />
      <PostList />
      <BackToTop />
    </>
  );
}
