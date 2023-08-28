# titanic-survival-predictor
A locally hosted streamlit website that has the user create a character with specific attributes and measures their chances of survival onboard the titanic.

If you're wondering how to run the local streamlit website, just go to ui.py and run that file.

This program uses a gradient boosted classifer from sklearn. The training & testing dataset for the model is from kaggle's [titanic project]([url](https://www.kaggle.com/competitions/titanic/data?select=train.csv)https://www.kaggle.com/competitions/titanic/data?select=train.csv) (Specifically the train.csv)

As of now, the gradient boosted classifier has about an 83% accuracy on validation; hopefully it can rise a bit more in future commits.
