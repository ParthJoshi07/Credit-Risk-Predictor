function Hero() {
  return (
    <section className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <h1 className="text-5xl font-bold text-slate-900">
        CreditRisk AI
      </h1>

      <p className="mt-6 max-w-2xl text-lg text-slate-600">
        AI-powered credit risk assessment using Machine Learning and FastAPI.
        Predict loan default probability instantly.
      </p>

      <button className="mt-10 rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700">
        Start Assessment
      </button>
    </section>
  );
}

export default Hero;