import pandas as pd

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split




df = pd.read_csv('test_out.csv')

df = df.drop(columns=['sitting', 'timestamp'])
df = df.dropna()

dfTest = pd.read_csv('data/test/merged_out.csv')
dfTest = dfTest.drop(columns=['timestamp'])
XTest = dfTest.drop('label', axis = 1)
yTest = dfTest['label']

X = df.drop('label', axis = 1)
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify = y)

clf = DecisionTreeClassifier()

clf = clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(XTest)
print("Accuracy:",metrics.accuracy_score(yTest, y_pred))