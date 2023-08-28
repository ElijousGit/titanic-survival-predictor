import numpy as np
import pandas as pd
import pickle

from sklearn import preprocessing
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier

def label_encode(data):
    label_encoder = LabelEncoder()

    for col in data.columns:
    # Check if the column contains categorical data
        if data[col].dtype == 'object':
        # Use LabelEncoder to encode the categorical values
            data[col] = label_encoder.fit_transform(data[col])
    return data

def normalize_data(data):
    scalar = preprocessing.StandardScaler().fit(data)
    scaled_data = scalar.transform(data)
    return scaled_data

def clean(data, dropColumns):
    if dropColumns:
        data = data.drop(columns=['Name', 'PassengerId', 'Cabin', 'Ticket'], axis=1)

    cols = []
    datatypes = data.dtypes
    for col in data.columns:
        if (datatypes[col] != 'object'):
            cols.append(col)
    
    for col in cols:
        data[col].fillna(data[col].median(), inplace=True)
    data.Embarked.fillna("U", inplace=True)
    return data

main_df = pd.read_csv('./data/train.csv')
main_df = clean(main_df, True)
main_df = label_encode(main_df)


X = main_df.drop("Survived", axis=1)
y = main_df["Survived"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1234)

clf = GradientBoostingClassifier(max_features='sqrt', 
                                 subsample=0.8, 
                                 min_samples_split=500, 
                                 min_samples_leaf=50, 
                                 max_leaf_nodes=8, 
                                 n_estimators=1000, 
                                 learning_rate=0.1,
                                 max_depth=None, 
                                 random_state=1234,
                                 loss='log_loss',
                                 )

clf.fit(X_train, y_train)


filename = 'model.sav'
pickle.dump(clf, open(filename, 'wb'))

Y_pred = clf.predict(X_val)
Y_prob = clf.predict_proba(X_val)
print(Y_prob)

# Test accuracy by comparing the answers vs the prediction
accuracy = accuracy_score(y_val, Y_pred)

# Final testing data to submit
final_df = pd.read_csv('./data/test.csv')
final_df = clean(final_df, True)
final_df = label_encode(final_df)

X = []
for col in main_df.columns:
    if col != "Survived":
        X.append(col)

Final_X_test = final_df[X]

Final_pred = clf.predict(Final_X_test)

final_df['Survived'] = Final_pred
