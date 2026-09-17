function Navbar() {
  return (
    <nav className="w-full border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

        <h1 className="text-2xl font-bold text-blue-600">
          CreditRisk AI
        </h1>

        <div className="flex gap-8 text-slate-700 font-medium">
          <a href="#" className="hover:text-blue-600 transition">
            Home
          </a>

          <a href="#" className="hover:text-blue-600 transition">
            About
          </a>

          <a href="#" className="hover:text-blue-600 transition">
            Contact
          </a>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;