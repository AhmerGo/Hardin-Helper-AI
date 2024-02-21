import React from "react";

function Navbar() {
  return (
    <nav className="navbar bg-purple p-4 shadow-md">
      <div className="container mx-auto flex justify-center">
        <a
          href="/"
          className="font-semibold text-white hover:text-[#FFC72C] mx-4 lg:mx-10 transition duration-300 transform hover:-translate-y-1"
        >
          Home
        </a>
        <a
          href="/about"
          className="font-semibold text-white hover:text-yellow-500 mx-4 lg:mx-10 transition duration-300 transform hover:-translate-y-1"
        >
          About
        </a>
        {/* Add other navigation links as needed */}
      </div>
    </nav>
  );
}

export default Navbar;
