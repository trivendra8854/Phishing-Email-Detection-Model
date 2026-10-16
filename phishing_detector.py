import os
import re
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, roc_auc_score
)

warnings.filterwarnings("ignore", category=UserWarning)

DATA_FILE = "emails_dataset.csv"
OUTPUT_DIR = "outputs"
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
IP_URL_RE = re.compile(r"https?://(?:\d{1,3}\.){3}\d{1,3}", re.IGNORECASE)
SUSPICIOUS_WORDS = [
    "urgent", "verify", "suspended", "password", "click here", "winner",
    "claim", "prize", "account locked", "act now", "login", "billing",
    "confirm", "immediately", "limited time", "bank", "payment"
]
SUSPICIOUS_TLDS = (".tk", ".ml", ".ga", ".cf", ".xyz", ".top", ".click")
SHORTENERS = ("bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd")

def extract_features(texts):
    """Create simple numeric features from email text and URLs."""
    rows = []
    for raw in texts:
        text = str(raw)
        lower = text.lower()
        urls = URL_RE.findall(text)
        rows.append([
            len(urls),
            int(bool(IP_URL_RE.search(text))),
            sum(1 for word in SUSPICIOUS_WORDS if word in lower),
            int(any(tld in lower for tld in SUSPICIOUS_TLDS)),
            int(any(short in lower for short in SHORTENERS)),
            text.count("!"),
            len(text),
            sum(1 for word in re.findall(r"\b[A-Z]{2,}\b", text)),
            int("$" in text or "₹" in text),
            int("dear customer" in lower or "dear user" in lower),
        ])
    return csr_matrix(np.asarray(rows, dtype=float))

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Dataset not found. Generating it now...")
        from generate_dataset import main as generate_dataset
        generate_dataset()
    data = pd.read_csv(DATA_FILE)
    required = {"subject", "body", "label"}
    if not required.issubset(data.columns):
        raise ValueError("Dataset must contain subject, body, and label columns.")
    data = data.dropna(subset=["subject", "body", "label"])
    data["text"] = data["subject"].astype(str) + " " + data["body"].astype(str)
    return data

def train_and_evaluate():
    data = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        data["text"], data["label"].astype(int), test_size=0.25,
        random_state=42, stratify=data["label"].astype(int)
    )
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, lowercase=True)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    X_train_all = hstack([X_train_tfidf, extract_features(X_train)]).tocsr()
    X_test_all = hstack([X_test_tfidf, extract_features(X_test)]).tocsr()

    model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
    model.fit(X_train_all, y_train)
    predictions = model.predict(X_test_all)
    probabilities = model.predict_proba(X_test_all)[:, 1]
    accuracy = accuracy_score(y_test, predictions)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cm = confusion_matrix(y_test, predictions, labels=[1, 0])
    disp = ConfusionMatrixDisplay(cm, display_labels=["Phishing", "Safe"])
    disp.plot(values_format="d")
    plt.title("Phishing Email Detection - Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"), dpi=150)
    plt.close()

    try:
        auc = roc_auc_score(y_test, probabilities)
    except ValueError:
        auc = float("nan")

    report = (
        "PHISHING EMAIL DETECTION MODEL\n"
        "================================\n"
        f"Dataset rows: {len(data)}\n"
        f"Test accuracy: {accuracy:.2%}\n"
        f"ROC-AUC: {auc:.3f}\n\n"
        "CLASSIFICATION REPORT\n"
        + classification_report(y_test, predictions, target_names=["Safe", "Phishing"])
        + "\nCONFUSION MATRIX (rows/columns: Phishing, Safe)\n"
        + str(cm) + "\n"
        + "\nNote: This is a learning demo trained on synthetic examples. "
          "Do not rely on it as the only protection against real phishing.\n"
    )
    print(report)
    with open(os.path.join(OUTPUT_DIR, "results.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    return vectorizer, model

def predict_email(vectorizer, model, email_text):
    tfidf = vectorizer.transform([email_text])
    combined = hstack([tfidf, extract_features([email_text])]).tocsr()
    pred = int(model.predict(combined)[0])
    probability = float(model.predict_proba(combined)[0][1])
    verdict = "PHISHING" if pred == 1 else "SAFE"
    print(f"\nPrediction: {verdict}")
    print(f"Estimated phishing probability: {probability:.1%}")
    print("Reminder: check the sender address and do not open suspicious links or attachments.")

def main():
    vectorizer, model = train_and_evaluate()
    print("\n--- Test an email ---")
    print("Paste an email subject/body below. Press Enter on an empty line to finish.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line and lines:
            break
        if not line and not lines:
            print("No email entered; showing a sample prediction.")
            lines = ["URGENT! Your account is suspended. Verify your password at http://192.0.2.10/login"]
            break
        lines.append(line)
    predict_email(vectorizer, model, " ".join(lines))

if __name__ == "__main__":
    main()
