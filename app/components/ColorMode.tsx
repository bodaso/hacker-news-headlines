"use client";

import { useEffect } from "react";
import { HiOutlineSun } from "react-icons/hi2";

export const ColorMode = () => {
  const handleClick = (e: any) => {
    e.preventDefault();

    if (document.documentElement.classList.contains("dark")) {
      document.documentElement.classList.remove("dark");
      localStorage.theme = "light";
    } else {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
    }
  };

  return (
    <button onClick={handleClick}>
      <HiOutlineSun size={24} />
    </button>
  );
};
