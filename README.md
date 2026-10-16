# Phishing Email Detection Model

A beginner-friendly, **command-line Python project** that uses Scikit-learn to classify email text as **Phishing** or **Safe**. It is not a website.

## Features
- Creates a labeled sample dataset of phishing and legitimate emails
- Extracts TF-IDF word features plus URL and suspicious-language indicators
- Trains a Logistic Regression classifier
- Prints accuracy, ROC-AUC, classification report, and confusion matrix
- Saves `outputs/confusion_matrix.png` and `outputs/results.txt`
- Lets you paste an email to test a prediction

## Requirements
- Python 3.10 or newer recommended
- Internet is needed only to install Python packages the first time

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `Phishing_Email_Detection_Model` folder.
3. Click the folder address bar in File Explorer, type `cmd`, and press Enter.
4. Install dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

5. Generate the sample dataset:

   ```bash
   py generate_dataset.py
   ```

6. Run the detector:

   ```bash
   py phishing_detector.py
   ```

7. Paste an email subject/body into the terminal. Press Enter on a blank line to finish input and view the prediction.

If `py` does not work, try replacing `py` with `python`.

## Files
- `generate_dataset.py` — creates the example dataset
- `emails_dataset.csv` — labeled sample emails
- `phishing_detector.py` — trains, evaluates, and predicts
- `requirements.txt` — required Python libraries
- `outputs/` — results are created here after running the program

## Important limitation
The included data is synthetic and designed for learning. A good test score on this dataset does **not** mean the detector is reliable against real-world phishing. Never use its prediction as the only security check.

## Submission checklist
- [ ] Run the program successfully
- [ ] Keep `outputs/results.txt` and `outputs/confusion_matrix.png` after running
- [ ] Take screenshots of the terminal output and confusion matrix
- [ ] Submit this ZIP plus any report or screenshots specifically required by your training portal
