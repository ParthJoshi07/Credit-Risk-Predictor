import { useState } from "react";
import axios from "axios";
import TextInput from "./TextInput";

function AssessmentForm() {
  const [formData, setFormData] = useState({
    age: "",
    credit_amount: "",
    duration: "",
    employment_since: "",
    existing_credits: "",
    housing: "own",
    income: "",
    purpose: "car",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async () => {
    console.log("Submit clicked");
    console.log("Sending data:", formData);

    try {
      setLoading(true);
      setResult(null);

      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        {
          age: Number(formData.age),
          credit_amount: Number(formData.credit_amount),
          duration: Number(formData.duration),
          employment_since: Number(formData.employment_since),
          existing_credits: Number(formData.existing_credits),
          housing: formData.housing,
          income: Number(formData.income),
          purpose: formData.purpose,
        }
      );

      console.log("Backend response:", response.data);
      setResult(response.data);

    } catch (error) {
      console.error("Prediction error:", error);

      if (error.response) {
        console.error("Backend error:", error.response.data);
        alert(
          error.response.data.detail || "Prediction failed."
        );
      } else {
        alert("Cannot connect to backend.");
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-2xl rounded-2xl bg-white p-8 shadow-xl">

      <h2 className="mb-8 text-3xl font-bold text-slate-900">
        Applicant Information
      </h2>

      <TextInput
        label="Loan Amount"
        name="credit_amount"
        type="number"
        placeholder="Enter loan amount"
        value={formData.credit_amount}
        onChange={handleChange}
      />

      <TextInput
        label="Annual Income"
        name="income"
        type="number"
        placeholder="Enter annual income"
        value={formData.income}
        onChange={handleChange}
      />

      <TextInput
        label="Age"
        name="age"
        type="number"
        placeholder="Enter age"
        value={formData.age}
        onChange={handleChange}
      />

      <TextInput
        label="Loan Duration (Months)"
        name="duration"
        type="number"
        placeholder="Enter duration"
        value={formData.duration}
        onChange={handleChange}
      />

      <TextInput
        label="Employment Since (Years)"
        name="employment_since"
        type="number"
        placeholder="Years employed"
        value={formData.employment_since}
        onChange={handleChange}
      />

      <TextInput
        label="Existing Credits"
        name="existing_credits"
        type="number"
        placeholder="Number of existing credits"
        value={formData.existing_credits}
        onChange={handleChange}
      />

      <div className="mb-5">
        <label className="mb-2 block text-sm font-semibold text-slate-700">
          Housing
        </label>

        <select
          name="housing"
          value={formData.housing}
          onChange={handleChange}
          className="w-full rounded-xl border border-slate-300 px-4 py-3"
        >
          <option value="own">Own</option>
          <option value="rent">Rent</option>
          <option value="free">Free</option>
        </select>
      </div>

      <div className="mb-6">
        <label className="mb-2 block text-sm font-semibold text-slate-700">
          Loan Purpose
        </label>

        <select
          name="purpose"
          value={formData.purpose}
          onChange={handleChange}
          className="w-full rounded-xl border border-slate-300 px-4 py-3"
        >
          <option value="car">Car</option>
          <option value="business">Business</option>
          <option value="education">Education</option>
          <option value="furniture">Furniture</option>
          <option value="radio_tv">Radio / TV</option>
          <option value="repairs">Repairs</option>
          <option value="domestic_appliances">
            Domestic Appliances
          </option>
          <option value="vacation">Vacation</option>
          <option value="retraining">Retraining</option>
          <option value="other">Other</option>
        </select>
      </div>

      <button
        type="button"
        onClick={handleSubmit}
        disabled={loading}
        className="w-full rounded-xl bg-blue-600 py-4 text-lg font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
      >
        {loading ? "Predicting..." : "Predict Credit Risk"}
      </button>

      {result && (
        <div className="mt-8 rounded-xl border border-green-300 bg-green-50 p-5">

          <h3 className="mb-3 text-xl font-bold text-green-700">
            Prediction Result
          </h3>

          <pre className="overflow-auto text-sm">
            {JSON.stringify(result, null, 2)}
          </pre>

        </div>
      )}

    </section>
  );
}

export default AssessmentForm;