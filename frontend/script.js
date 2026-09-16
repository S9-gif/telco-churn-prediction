//HTML de verdiğimiz key değerleri burdan kendisine topluyor bir nevi insert ediyor.
const form = document.getElementById("churn-form");
const submitBtn = document.getElementById("submit-btn");
const resultPanel = document.getElementById("result-panel");
const errorPanel = document.getElementById("error-panel");
const resultBadge = document.getElementById("result-badge");
const probBarFill = document.getElementById("prob-bar-fill");
const probLabel = document.getElementById("prob-label");
const errorMessage = document.getElementById("error-message");

//int olan değişkenleri js e tanımlıyoruz.Veri okuma sırasında default stringi engellemek için.
const numberFields = new Set(["tenure", "MonthlyCharges", "TotalCharges"]);


//CustomerData schemam ile uyumlu olacak JSON 'u belirliyoruz.
function buildPayload(formData) {
  const payload = {};

  for (const [key, value] of formData.entries()) {
    if (numberFields.has(key)) {
      payload[key] = Number(value);
    } else {
      payload[key] = value;
    }
  }

  payload.SeniorCitizen = document.getElementById("SeniorCitizen").checked ? 1 : 0;

  return payload;
}

//Burda da çıktı için JSON tanımlıyoruz.
function showResult(data) {
  errorPanel.hidden = true;

  const isChurn = String(data.Churn) === "1" || String(data.Churn).toLowerCase() === "yes";
  const probabilityPct = Math.round(data.PredictionRate * 100);

  resultBadge.textContent = isChurn ? "At risk of churn" : "Likely to stay";
  resultBadge.className = "result-badge " + (isChurn ? "churn" : "no-churn");

  probBarFill.style.width = probabilityPct + "%";
  probLabel.textContent = `Churn probability: ${probabilityPct}%`;

  resultPanel.hidden = false;
}

function showError(message) {
  resultPanel.hidden = true;
  errorMessage.textContent = message;
  errorPanel.hidden = false;
}

form.addEventListener("submit", async (event) => {
  //Alttaki satırla HTML'İn her istekte sayfayı yenilemesini engelleyip API a istek atmasını sağlıyoruz.
  event.preventDefault();

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting...";

  try {
    const formData = new FormData(form);
    const payload = buildPayload(formData);

    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Request failed (${response.status}): ${body}`);
    }

    const data = await response.json();
    showResult(data);
  } catch (err) {
    showError(err.message || "Unexpected error occurred.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict churn risk";
  }
});
