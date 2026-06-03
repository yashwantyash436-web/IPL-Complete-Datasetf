# =========================================
# IPL Analytics Streamlit Dashboard
# app.py
# =========================================

# Import Libraries
import os
import zipfile
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------------
# Streamlit Page Config
# -----------------------------------------

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------------------
# Title
# -----------------------------------------

st.title("PragyanAI - IPL Analytics Dashboard")

st.markdown("Interactive Cricket Data Analytics using Python, NumPy, Pandas and Streamlit")

# -----------------------------------------
# Create folders
# -----------------------------------------

os.makedirs("../data", exist_ok=True)

# -----------------------------------------
# Extract ZIP File
# -----------------------------------------

zip_path = "archive.zip"

extract_path = "data"

# Extract ZIP only if CSV files do not exist
matches_file = os.path.join(extract_path, "matches.csv")
deliveries_file = os.path.join(extract_path, "deliveries.csv")

if not os.path.exists(matches_file):

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    st.success("ZIP File Extracted Successfully")

# -----------------------------------------
# Load Dataset
# -----------------------------------------

matches = pd.read_csv(matches_file)
deliveries = pd.read_csv(deliveries_file)

# -----------------------------------------
# Sidebar
# -----------------------------------------

st.sidebar.title("Filters")

teams = sorted(matches['team1'].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)

# -----------------------------------------
# Main Metrics
# -----------------------------------------

total_matches = matches.shape[0]

total_teams = len(teams)

top_team = matches['winner'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", total_matches)

col2.metric("Total Teams", total_teams)

col3.metric("Most Successful Team", top_team)

# -----------------------------------------
# Team Matches
# -----------------------------------------

st.header(f" {selected_team} Match Analysis")

team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

st.dataframe(team_matches.head(10))

# -----------------------------------------
# Team Wins
# -----------------------------------------

team_wins = matches['winner'].value_counts()

st.header(" Team Wins Analysis")

fig1 = px.bar(
    x=team_wins.index,
    y=team_wins.values,
    labels={'x': 'Team', 'y': 'Wins'},
    title="IPL Team Wins"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------
# Toss Decision Analysis
# -----------------------------------------

toss_decision = matches['toss_decision'].value_counts()

st.header("Toss Decision Analysis")

fig2 = px.pie(
    values=toss_decision.values,
    names=toss_decision.index,
    title="Toss Decisions"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------
# Top Batsmen
# -----------------------------------------

top_batsmen = deliveries.groupby(
    'batter'
)['batsman_runs'].sum().sort_values(
    ascending=False
).head(10)

st.header("Top Run Scorers")

fig3 = px.bar(
    x=top_batsmen.index,
    y=top_batsmen.values,
    labels={'x': 'Player', 'y': 'Runs'},
    title="Top 10 Batsmen"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------
# Strike Rate Analysis
# -----------------------------------------

runs = deliveries.groupby(
    'batter'
)['batsman_runs'].sum()

balls = deliveries.groupby(
    'batter'
)['ball'].count()

strike_rate = ((runs / balls) * 100)

strike_rate = strike_rate.sort_values(
    ascending=False
).head(10)

st.header("⚡ Top Strike Rate Players")

fig4 = px.bar(
    x=strike_rate.index,
    y=strike_rate.values,
    labels={'x': 'Player', 'y': 'Strike Rate'},
    title="Top Strike Rate Players"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------
# Wicket Analysis
# -----------------------------------------

wickets = deliveries[
    deliveries['is_wicket'] == 1
]

top_bowlers = wickets['bowler'].value_counts().head(10)

st.header("Top Bowlers")

fig5 = px.bar(
    x=top_bowlers.index,
    y=top_bowlers.values,
    labels={'x': 'Bowler', 'y': 'Wickets'},
    title="Top Wicket Takers"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------
# Venue Analysis
# -----------------------------------------

venues = matches['venue'].value_counts().head(10)

st.header("Top IPL Venues")

fig6 = px.bar(
    x=venues.index,
    y=venues.values,
    labels={'x': 'Venue', 'y': 'Matches'},
    title="Top IPL Venues"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------
# Season Analysis
# -----------------------------------------

season_matches = matches['season'].value_counts().sort_index()

st.header("Season Wise Matches")

fig7 = px.line(
    x=season_matches.index,
    y=season_matches.values,
    labels={'x': 'Season', 'y': 'Matches'},
    title="Matches Per Season"
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------------------
# NumPy Statistics
# -----------------------------------------

match_scores = deliveries.groupby(
    'match_id'
)['total_runs'].sum()

scores_array = np.array(match_scores)

st.header("NumPy Statistics")

avg_score = np.mean(scores_array)

max_score = np.max(scores_array)

min_score = np.min(scores_array)

std_score = np.std(scores_array)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Score", round(avg_score, 2))

c2.metric("Maximum Score", max_score)

c3.metric("Minimum Score", min_score)

c4.metric("Std Deviation", round(std_score, 2))

# -----------------------------------------
# Score Distribution
# -----------------------------------------

st.header("Match Score Distribution")

fig8 = px.histogram(
    x=scores_array,
    nbins=20,
    title="Distribution of Match Scores"
)

st.plotly_chart(fig8, use_container_width=True)

# -----------------------------------------
# Raw Dataset
# -----------------------------------------

st.header("Raw Dataset")

if st.checkbox("Show Matches Dataset"):
    st.dataframe(matches)

if st.checkbox("Show Deliveries Dataset"):
    st.dataframe(deliveries)

# -----------------------------------------
# Footer
# -----------------------------------------

st.markdown("---")

st.markdown("### IPL Analytics Dashboard using Streamlit")

st.markdown("Built with Python, NumPy, Pandas, Plotly and Streamlit")
