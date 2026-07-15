import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
# Sample Dataset
data = {
'stress':[2,8,5,9,1,7,3,10,6,4],
'anxiety':[1,9,4,8,2,7,3,10,5,4],
'depression':[1,7,3,9,1,6,2,10,5,4],
'sleep':[8,4,6,3,9,5,7,2,6,7],
'academic_pressure':[2,9,5,10,1,7,3,10,6,4],
'risk':[
'Low',
'High',
'Moderate',
'High',
'Low',
'High',
'Low',
'High',
'Moderate',
'Moderate'
]
}
df = pd.DataFrame(data)
X = df.drop('risk',axis=1)
y = df['risk']
X_train,X_test,y_train,y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42
)
model = RandomForestClassifier(
n_estimators=100,
random_state=42
)
model.fit(X_train,y_train)
pred = model.predict(X_test)
print(
"Accuracy:",
accuracy_score(y_test,pred)
)
joblib.dump(
model,
'models/risk_model.pkl'
)
print("Risk Model Saved Successfully")