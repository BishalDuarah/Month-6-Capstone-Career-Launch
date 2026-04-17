import { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    area: "",
    bedrooms: "",
    location: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/predict", form);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("API error");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>🏠 Real Estate Price Predictor</h1>

      <form onSubmit={handleSubmit}>
        <input name="area" placeholder="Area" onChange={handleChange} />
        <br /><br />
        <input name="bedrooms" placeholder="Bedrooms" onChange={handleChange} />
        <br /><br />
        <input name="location" placeholder="Location" onChange={handleChange} />
        <br /><br />

        <button type="submit">Predict</button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Predicted Price:</h2>
          <p>₹ {result.predicted_price}</p>
        </div>
      )}
    </div>
  );
}

export default App;