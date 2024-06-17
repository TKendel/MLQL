import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics



df = pd.read_csv('test_out.csv')

df = df.drop(columns=['sitting', 'timestamp'])
df = df.dropna()

X = df.drop('label', axis = 1)
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify = y)

clf = DecisionTreeClassifier()

clf = clf.fit(X_train,  y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))