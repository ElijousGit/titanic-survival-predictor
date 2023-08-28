import streamlit as st
import pandas as pd
from model import * 
import streamlit as st
import pandas as pd
import pickle

sex = age = pClass = parch = sibsp = fare = embarked = None

st.title("Who :blue[could] survive :orange[the Titanic?]")
st.divider()
st.header("Create a character and see their chances of :red[survival]")

st.divider()
Isex = st.selectbox("What is their sex?", ("male", "female"))
sex = Isex

st.divider()
Iage = st.slider("What is their age?", 0, 80, 30)
age = Iage

st.divider()
IPclass = st.selectbox("What is their passenger class? (1st being highest socio-economic status, and 3rd being the lowest)", 
                         ("1st class", "2nd class", "3rd class"))
match IPclass:
    case "1st class":
        pClass = 1
    case "2nd class":
        pClass = 2
    case "3rd class":
        pClass = 3
    case other:
        pClass = None

st.divider()
Isibsp = st.number_input("How many sibling and spouses are with them?", 0, 8, 0, 1)
sibsp = Isibsp

st.divider()
Iparch = st.number_input("How many parents and children are with them?", 0, 6, 0, 1)
parch = Iparch

st.divider()
Ifare = st.slider("How much are they spending on their trip? (What's their fare/budget)?", 0.0, 100.0, 512.3, 1.0)
fare = Ifare

st.divider()
Iembarked = st.selectbox("Where did they embark from?", ("Southampton", "Cherbourg", "Queenstown"))

match Iembarked:
    case "Southampton":
        embarked = 'S'
    case "Cherbourg":
        embarked = 'C'
    case "Queenstown":
        embarked = 'Q'

st.divider()

MSex = 'No sex detected'
if Iage < 18:
    if Isex == 'male':
        MSex = 'boy'
    else: 
        MSex = 'girl'
elif Isex == 'male':
    MSex = 'man'
else: MSex = 'woman'

st.header("So, your character is a " + str(Iage) + ' year old ' + MSex + '.')


data = [[pClass, sex, age, sibsp, parch, fare, embarked]]
characterDf = pd.DataFrame(data, columns=['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked'])
st.write(characterDf)


input = clean(characterDf, False)
input = label_encode(input)
model = pickle.load(open('model.sav', 'rb'))
survival = model.predict(input)
survivalChance = round((((model.predict_proba(input))[0])[1]) * 100, 2)

color = 'green'

if survivalChance < 85:
    color = 'blue'
if survivalChance < 70:
    color = 'violet'
if survivalChance < 60:
    color = 'orange'
if survivalChance < 50:
    color = 'red'

resultMes = 'Your character would have a :' + color + '[' + str(survivalChance) + '%] chance of survival on the titanic'
st.title(resultMes)
