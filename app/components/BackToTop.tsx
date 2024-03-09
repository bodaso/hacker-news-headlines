"use client";

export const BackToTop = () => {
  return (
    <div className="back-to-top mt-8 text-center text-gray-500">
      <button
        onClick={(e) => {
          e.preventDefault();
          window.scrollTo(0, 0);
        }}
      >
        Back to top
      </button>
    </div>
  );
};
