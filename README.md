🛡️ Phishing Website Detector

A Machine Learning-powered web app to detect phishing URLs

This project is built as part of a Cybersecurity project. It uses Python, Flask, HTML, CSS, JavaScript, and a Machine Learning model to predict whether a given URL is phishing or legitimate.

✅ Features

Web-based Interface – Simple, clean UI for quick detection.

ML Model – Trained using scikit-learn with lexical URL-based features.

Real-time Detection – Enter any URL and get an instant phishing probability score.

Explainability – Feature breakdown for each prediction.

Responsive Design – Works on desktop and mobile.

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Flask (Python)

Machine Learning: scikit-learn (RandomForest Classifier)

Data: URLs with labels (phishing / legitimate)

🔍 How It Works

Feature Extraction – Extracts key features from the input URL:

Length of URL, domain, path

Number of special characters (@, -, ?, %, =)

Presence of IP address in the domain

Suspicious TLDs (.xyz, .zip)

URL entropy

Query parameter count

And more...

Model Prediction – The trained ML model predicts:

0 → Legitimate

1 → Phishing

Result Display – Shows:

Verdict Badge: Likely Safe / Likely Phishing

Risk Score (Probability %)

Feature Breakdown

📂 Project Structure
phish-detector/
│
├── app/                     # Web application
│   ├── app.py               # Flask app (UI + API)
│   ├── feature_extractor.py # Feature extraction logic
│   ├── templates/
│   │   └── index.html       # Frontend HTML
│   ├── static/
│   │   ├── style.css        # Styling
│   │   └── script.js        # Frontend JS
│   ├── model.pkl            # Trained ML model (generated after training)
│   └── requirements.txt     # Python dependencies
│
├── training/                # Model training scripts
│   ├── train.py             # Train model using dataset
│   └── feature_extractor.py # Same feature logic for consistency
│
└── README.md                # Project documentation

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/phishing-website-detector.git
cd phishing-website-detector/app

2️⃣ Create Virtual Environment & Install Dependencies
python -m venv .venv
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt

🧠 Train the Model (Optional but Recommended)

Prepare a CSV file with two columns:

url,label
http://example.com,0
http://phishing-site.com,1


Run the training script:

cd ../training
python train.py --data data.csv --out ../app/model.pkl


This will:
✔ Train a RandomForest Classifier
✔ Save the model as model.pkl for the web app

▶️ Run the Web App
cd ../app
python app.py


Now open http://127.0.0.1:5000
 in your browser.

📊 Model Details

Algorithm: RandomForest Classifier

Features: URL length, special chars, digits, entropy, suspicious TLDs, IP presence, etc.

Dataset: Public phishing URL datasets (PhishTank, OpenPhish, UCI) + legit URLs.

🛡️ Security Note

This app does not fetch external websites (avoids SSRF & malicious code execution).
Detection is based on URL structure only, making it safe for demo use.

✅ Future Improvements

✔ Add WHOIS & SSL certificate features
✔ Integrate FastAPI + React for modern stack
✔ Deploy on Docker / AWS / Heroku
✔ Use deep learning for advanced detection

📜 License

This project is licensed under the MIT License – feel free to use and modify.
