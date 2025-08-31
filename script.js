
async function predict(url) {
  const res = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });
  return res.json();
}

function fmtProb(p) {
  return (p*100).toFixed(1) + "%";
}

function featureCard(k, v) {
  return `<div class="feature">
    <h4>${k}</h4>
    <div class="value">${typeof v === "number" ? v.toFixed ? v.toFixed(4) : v : v}</div>
  </div>`;
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("urlInput");
  const btn = document.getElementById("checkBtn");
  const result = document.getElementById("result");
  const features = document.getElementById("features");

  async function handle() {
    const url = input.value.trim();
    if (!url) return;
    result.classList.remove("hidden");
    result.innerHTML = "Checking…";
    features.classList.add("hidden");
    features.innerHTML = "";
    try {
      const data = await predict(url);
      const prob = data.phishing_probability;
      const isPhish = prob >= 0.5;
      result.innerHTML = `
        <span class="badge ${isPhish ? "phish":"safe"}">${isPhish ? "Likely Phishing" : "Likely Safe"}</span>
        <strong>Risk:</strong> ${fmtProb(prob)}
        <div class="muted small">This is a machine-learning estimate based on URL features; always verify manually.</div>
      `;
      const entries = Object.entries(data.features);
      features.innerHTML = entries.map(([k,v]) => featureCard(k, v)).join("");
      features.classList.remove("hidden");
    } catch (e) {
      result.innerHTML = "Something went wrong. Is the server running?";
    }
  }

  btn.addEventListener("click", handle);
  input.addEventListener("keydown", gaw => {
    if (gaw.key === "Enter") handle();
  });
});
