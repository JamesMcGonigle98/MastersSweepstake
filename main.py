# %% --------------------------------------------------------------------------
# Imports 
# -----------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import requests
import json

from secret_key import secret_key


# %% --------------------------------------------------------------------------
# Access Data
# -----------------------------------------------------------------------------
url = "https://golf-leaderboard-data.p.rapidapi.com/leaderboard/651"

headers = {
	"X-RapidAPI-Key": f"{secret_key}",
	"X-RapidAPI-Host": "golf-leaderboard-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())

# %% --------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
leaderboard = response.json()

# %% --------------------------------------------------------------------------
# Players
# -----------------------------------------------------------------------------
player1 = [
    "James McG"
    ,"Jon Rahm"
    ,"Scottie Scheffler"
    ,"Sahith Theegala"
    ,"Shane Lowry"
]


player2 = [
    "Jack O'K"
    ,"Cameron Young"
    ,"Scottie Scheffler"
    ,"Brooks Koepka"
    ,"Shane Lowry"
]

player3 = [
    "Jack T"
    ,"Jon Rahm"
    ,"Scottie Scheffler"
    ,"Wyndham Clark"
    ,"Nicholas Dunlap"
]

player4 = [
    "Andy"
    ,"Si Woo Kim"
    ,"Xander Schauffele"
    ,"Viktor Hovland"
    ,"Jon Rahm"
]

player5 = [
    "Paul"
    ,"Adam Scott"
    ,"Scottie Scheffler"
    ,"Rory McIlroy"
    ,"Joaquín Niemann"
]

player6 = [
    "Katie"
    ,"Jordan Spieth"
    ,"Matt Fitzpatrick"
    ,"Tom Kim"
    ,"Brooks Koepka"
]

player7 = [
    "Louis"
    ,"Rory McIlroy"
    ,"Scottie Scheffler"
    ,"Corey Conners"
    ,"Joaquín Niemann"
]

player8 = [
    "Theresa"
    ,"Rory McIlroy"
    ,"Tommy Fleetwood"
    ,"Brooks Koepka"
    ,"Shane Lowry"
]

player9 = [
    "John"
    ,"Matt Fitzpatrick"
    ,"Tony Finau"
    ,"Cameron Young"
    ,"Joaquín Niemann"
]

player10 = [
    "Dave"
    ,"Matt Fitzpatrick"
    ,"Xander Schauffele"
    ,"Brooks Koepka"
    ,"Shane Lowry"
]

player11 = [
    "Vicky"
    ,"Rory McIlroy"
    ,"Justin Rose"
    ,"Justin Thomas"
    ,"Bryson DeChambeau"
]

player12 = [
    "Luke"
    ,"Jon Rahm"
    ,"Hideki Matsuyama"
    ,"Rory McIlroy"
    ,"Shane Lowry"
]


list_of_players = [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12]

# %% --------------------------------------------------------------------------
# Create players dataframe
# -----------------------------------------------------------------------------
df_players = pd.DataFrame(list_of_players, columns = ['Name', 'Golfer 1', 'Golfer 2','Golfer 3','Golfer 4'])

# %% --------------------------------------------------------------------------
# Live Leaderboard
# -----------------------------------------------------------------------------
position = []
first = []
last = []
score = []
full = []

for i in range(90):
    
    if i < len(leaderboard['results']['leaderboard']):

        position.append(leaderboard['results']['leaderboard'][i]['position'])
        first.append(leaderboard['results']['leaderboard'][i]['first_name'])
        last.append(leaderboard['results']['leaderboard'][i]['last_name'])
        score.append(leaderboard['results']['leaderboard'][i]['total_to_par'])

        full.append(leaderboard['results']['leaderboard'][i]['first_name'] + ' ' + leaderboard['results']['leaderboard'][i]['last_name'])

current_leaderboard = pd.DataFrame({
    'Position': position,
    'Full Name': full,
    'Score': score
})


# %% --------------------------------------------------------------------------
# Scores
# -----------------------------------------------------------------------------
scores = {}

for i in range(len(df_players)):

    name = df_players.iloc[i].loc['Name']
    golf1 = df_players.iloc[i].loc['Golfer 1']
    golf2 = df_players.iloc[i].loc['Golfer 2']
    golf3 = df_players.iloc[i].loc['Golfer 3']
    golf4 = df_players.iloc[i].loc['Golfer 4']

    player_score1 = current_leaderboard[(current_leaderboard['Full Name'] == golf1)]
    score1 = int(player_score1['Position'].iloc[0]) if not player_score1.empty else 80

    player_score2 = current_leaderboard[(current_leaderboard['Full Name'] == golf2)]
    score2 = int(player_score2['Position'].iloc[0]) if not player_score2.empty else 80

    player_score3 = current_leaderboard[(current_leaderboard['Full Name'] == golf3)]
    score3 = int(player_score3['Position'].iloc[0]) if not player_score3.empty else 80

    player_score4 = current_leaderboard[(current_leaderboard['Full Name'] == golf4)]
    score4 = int(player_score4['Position'].iloc[0]) if not player_score4.empty else 80

    total = score1 + score2 + score3 + score4

    scores[name] = [golf1, score1, golf2, score2, golf3, score3, golf4, score4, total]

scores = pd.DataFrame.from_dict(scores, orient='index')
scores.columns = ['Golfer 1', 'Place 1', 'Golfer 2', 'Place 2', 'Golfer 3','Place 3','Golfer 4','Place 4','Total']

# %% --------------------------------------------------------------------------
# Sort
# -----------------------------------------------------------------------------
score_sorted = scores.sort_values(by = 'Total', ascending=True)

# %% --------------------------------------------------------------------------
# Streamlit App
# -----------------------------------------------------------------------------
st.title("2024 Master's Prediction Table")

st.header("Current Prediction Standings")
st.table(score_sorted)

st.header('Player Picks')
st.table(df_players)

st.header("Live Master's Leaderboard")
st.table(current_leaderboard)
# %%
