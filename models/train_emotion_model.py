import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
# Sample Dataset
data = {
"text":[
"I am very happy today",
"I feel sad and lonely",
"I am stressed because of exams",
"I feel anxious",
"I am excited",
"I feel depressed",
"I am angry",
"I am relaxed",
"I feel nervous",
"I am cheerful"
],
"emotion":[
"Happy",
"Sad",
"Stress",
"Anxiety",
"Happy",
"Depression",
"Angry",
"Relaxed",
"Anxiety",
"Happy"
]
}
df = pd.DataFrame(data)
X = df['text']
y = df['emotion']
# Vectorization
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
# Split
X_train,X_test,y_train,y_test = train_test_split(
X_vec,
y,
test_size=0.2,
random_state=42
)
# Model
model = MultinomialNB()
model.fit(X_train,y_train)
# Accuracy
pred = model.predict(X_test)
print(
"Accuracy :",
accuracy_score(y_test,pred)
)
# Save model
joblib.dump(
model,
'models/emotion_model.pkl'
)
joblib.dump(
vectorizer,
'models/vectorizer.pkl'
)
print("Model Saved Successfully")