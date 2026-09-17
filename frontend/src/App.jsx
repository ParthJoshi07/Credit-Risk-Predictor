import Navbar from "./components/layout/Navbar";
import Hero from "./components/layout/Hero";
import AssessmentForm from "./components/form/AssessmentForm";

function App() {
  return (
    <main className="min-h-screen bg-slate-100">
      <Navbar />
      <Hero />

      <div className="px-6 py-16">
        <AssessmentForm />
      </div>
    </main>
  );
}

export default App;