import csv
import random

random.seed(42)

PHISHING = [
    ("Urgent: Verify your account", "Dear customer, your account will be suspended today. Verify your password immediately at http://192.0.2.10/login"),
    ("You have won a prize", "Congratulations winner! Claim your cash reward now by clicking http://claim-prize.example.xyz"),
    ("Payment failed", "Your payment failed. Update your billing details immediately to avoid service interruption: http://secure-update.example.tk"),
    ("Mailbox storage full", "Your mailbox is full. Click here to keep receiving messages: http://mailbox-check.example.ml"),
    ("Security alert", "We detected unusual activity. Confirm your account and enter your login details now."),
    ("Final warning: account locked", "Act now! Your bank account is locked. Verify your identity at http://198.51.100.5/secure"),
    ("Refund waiting", "A refund is waiting for you. Submit your card information to receive the money today."),
    ("Password expires today", "Your password expires today. Click here immediately to prevent account closure."),
    ("Delivery issue", "Your package cannot be delivered. Pay a small fee using this link: http://delivery-fee.example.xyz"),
    ("Unusual sign-in", "We noticed a suspicious sign-in. If this was not you, confirm your password immediately."),
]
SAFE = [
    ("Meeting agenda for Monday", "Hello team, attached is the agenda for Monday's project meeting. Please review it before we meet."),
    ("Project update", "The project is on schedule. I have uploaded the revised notes to our shared folder."),
    ("Your appointment confirmation", "This is a reminder that your appointment is scheduled for Thursday at 10 AM."),
    ("Monthly newsletter", "Here is this month's newsletter with product updates, upcoming events, and helpful tips."),
    ("Lunch tomorrow", "Would you like to join us for lunch tomorrow? Let me know what time works for you."),
    ("Invoice for your records", "Please find the invoice attached for your recent purchase. Contact our support team if you have questions."),
    ("Class schedule update", "The lab session will begin at 2 PM in room 204. Please bring your notebook."),
    ("Thank you for your feedback", "Thank you for completing our survey. We appreciate your feedback and will review your suggestions."),
    ("Weekly status report", "I have completed the weekly status report and shared it with the project group."),
    ("Order confirmation", "Your order has been received. You can review the details in your account's order history."),
]

def main():
    rows = []
    for label, templates in [(1, PHISHING), (0, SAFE)]:
        for i in range(150):
            subject, body = random.choice(templates)
            # Small variations provide more examples while keeping the dataset reproducible.
            suffixes = [
                "", " Please review this message.", " Thank you.", " This message is for your attention.",
                " Contact support if you need help."
            ]
            rows.append({"subject": subject, "body": body + random.choice(suffixes), "label": label})
    random.shuffle(rows)
    with open("emails_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["subject", "body", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created emails_dataset.csv with {len(rows)} labeled examples.")

if __name__ == "__main__":
    main()
