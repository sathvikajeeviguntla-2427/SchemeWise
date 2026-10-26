from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

training_data = [
    ("What schemes are available for farmers?", "farmer_schemes"),
    ("Tell me about PM Kisan", "farmer_schemes"),
    ("Government benefits for agriculture", "farmer_schemes"),
    ("How can farmers get financial support?", "farmer_schemes"),

    ("Tell me about health insurance", "health_schemes"),
    ("What is Ayushman Bharat?", "health_schemes"),
    ("Help with hospital expenses", "health_schemes"),
    ("Government medical coverage schemes", "health_schemes"),

    ("What documents are required?", "documents"),
    ("Which certificates should I submit?", "documents"),
    ("Do I need an income certificate?", "documents"),

    ("How do I apply for a scheme?", "application_process"),
    ("Where can I submit my application?", "application_process"),
    ("How can I register for government benefits?", "application_process"),

    ("Hello", "greeting"),
    ("Hi, can you help me?", "greeting"),
    ("Good morning", "greeting"),

    ("Thank you for your help", "thanks"),
    ("Thanks a lot", "thanks"),

    ("Tell me about PM Mudra Yojana", "scheme_information"),
    ("What benefits does PM Ujjwala provide?", "scheme_information"),
    ("Explain the government housing scheme", "scheme_information"),
]

questions = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(questions, labels)

joblib.dump(model, "chatbot_model.pkl")

print("Chatbot model trained and saved successfully.")