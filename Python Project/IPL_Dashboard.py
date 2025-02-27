
import pandas as pd
from fontTools.afmLib import kernRE

# Load the datasets
matches_df = pd.read_csv("Matches.csv")
deliveries_df = pd.read_csv("Deliveries.csv")
#shape of dataset
print("shape of matches dataset: ",matches_df.shape)
print("shape of deliveries dataset: ",deliveries_df.shape)

# Display the first few rows
print(" Matches Dataset:")
print(matches_df.head())

print("\n Deliveries Dataset:")
print(deliveries_df.head())
#information for each dataset
print(matches_df.info())
print(deliveries_df.info())
# Check for missing values
print(" Missing Values in Matches Dataset:")
print(matches_df.isnull().sum())

print("\n Missing Values in Deliveries Dataset:")
print(deliveries_df.isnull().sum())
#dropping method column in matches dataset
matches_df.drop(columns='method',inplace=True)
print(matches_df.info())
# Drop columns in Deliveries dataset
#deliveries_df.drop(columns=['extras_type','player_dismissed','dismissal_kind','fielder'],inplace=True)
print(deliveries_df.info())
#dropping rows with missing values in matches dataset
matches_df.dropna(subset='city', inplace=True)
#  Fill missing values in Matches dataset (if any)
matches_df['player_of_match'].fillna("Unknown", inplace=True)
matches_df['winner'].fillna("No Result", inplace=True)
matches_df['result_margin'].fillna(0, inplace=True)
matches_df['target_runs'].fillna(0, inplace=True)
matches_df['target_overs'].fillna(0, inplace=True)

#print("\n Missing Values After Cleaning:")
print("Matches null values count:\n",matches_df.isnull().sum())
print("deliveries null values count:\n",deliveries_df.isnull().sum())

matches_df.to_csv("Matches_cleaned.csv",index=False)
print("File saved succesfully!")

deliveries_df.to_csv("Deliveries_cleaned.csv",index=False)
print("File saved successfully!")

import matplotlib.pyplot as plt

# Count the number of wins for each team
team_wins = matches_df['winner'].value_counts()

# Plot the bar chart
plt.figure(figsize=(12, 6))
team_wins.sort_values(ascending=True).plot(kind='barh', color='skyblue', edgecolor='black')

# Customize the plot
plt.xlabel('Number of Wins', fontsize=12)
plt.ylabel('Teams', fontsize=12)
plt.title('Most Successful IPL Teams Based on Wins', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# Count the occurrences of each toss decision
toss_decision_counts = matches_df['toss_decision'].value_counts()

# Plot the pie chart
plt.figure(figsize=(6, 6))
plt.pie(toss_decision_counts, labels=toss_decision_counts.index, autopct='%1.1f%%',
        colors=['#ff9999', '#66b3ff'], startangle=90, wedgeprops={'edgecolor': 'black'})

# Add title
plt.title('Toss Decision Trends in IPL', fontsize=14)

# Show the chart
plt.show()

# Identify home and away wins
matches_df['home_win'] = matches_df['winner'] == matches_df['team1']
matches_df['away_win'] = matches_df['winner'] == matches_df['team2']

# Count home and away wins per season
home_wins_per_season = matches_df.groupby('season')['home_win'].sum()
away_wins_per_season = matches_df.groupby('season')['away_win'].sum()

# Plot the line chart
plt.figure(figsize=(10, 5))
plt.plot(home_wins_per_season.index, home_wins_per_season, marker='o', linestyle='-', color='blue', label='Home Wins')
plt.plot(away_wins_per_season.index, away_wins_per_season, marker='o', linestyle='-', color='red', label='Away Wins')

# Customize the plot
plt.xlabel('Season', fontsize=12)
plt.ylabel('Number of Wins', fontsize=12)
plt.title('Home vs Away Performance in IPL', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# Show the chart
plt.show()

### **1. Top 10 Run-Scorers**
# Group by batsman and sum runs
top_run_scorers = deliveries_df.groupby('batter')['batsman_runs'].sum().nlargest(10)

# Plot horizontal bar chart for Top Run-Scorers
plt.figure(figsize=(10, 5))
top_run_scorers.sort_values().plot(kind='barh', color='orange', edgecolor='black')

# Customize the plot
plt.xlabel("Total Runs", fontsize=12)
plt.ylabel("Player", fontsize=12)
plt.title("Top 10 Run-Scorers in IPL", fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Show the chart
plt.show()

### **2. Highest Wicket-Takers**
# Filter out rows where a wicket was taken
wicket_data = deliveries_df[deliveries_df['is_wicket'] == 1]

# Group by bowler and count wickets
top_wicket_takers = wicket_data.groupby('bowler').size().nlargest(10)

# Plot horizontal bar chart for Highest Wicket-Takers
plt.figure(figsize=(10, 5))
top_wicket_takers.sort_values().plot(kind='barh', color='purple', edgecolor='black')

# Customize the plot
plt.xlabel("Total Wickets", fontsize=12)
plt.ylabel("Player", fontsize=12)
plt.title("Top 10 Wicket-Takers in IPL", fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Show the chart
plt.show()

###  **Most Player of the Match Awards**
# Count occurrences of each player winning the award
player_of_match_counts = matches_df['player_of_match'].value_counts().nlargest(10)

# Plot horizontal bar chart
plt.figure(figsize=(10, 5))
player_of_match_counts.sort_values().plot(kind='barh', color='gold', edgecolor='black')

# Customize the plot
plt.xlabel("Number of Awards", fontsize=12)
plt.ylabel("Player", fontsize=12)
plt.title("Top 10 Players with Most 'Player of the Match' Awards", fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Show the chart
plt.show()

### **Filter win margins based on type**
win_by_runs = matches_df[matches_df['result'] == 'runs']['result_margin']
win_by_wickets = matches_df[matches_df['result'] == 'wickets']['result_margin']

# Create the histogram
plt.figure(figsize=(10, 5))
plt.hist(win_by_runs, bins=15, alpha=0.7, color='red', label='Win by Runs', edgecolor='black')
plt.hist(win_by_wickets, bins=8, alpha=0.7, color='blue', label='Win by Wickets', edgecolor='black')

# Customize the plot
plt.xlabel("Win Margin", fontsize=12)
plt.ylabel("No. of Matches", fontsize=12)
plt.title("Distribution of Win Margins in IPL", fontsize=14)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Show the chart
plt.show()

###  **Count Super Over Matches**
super_over_counts = matches_df['super_over'].value_counts()

# Create a Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(super_over_counts, labels=['Normal Matches', 'Super Over Matches'], autopct='%1.1f%%',
        colors=['lightblue', 'red'], startangle=90, wedgeprops={'edgecolor': 'black'})

# Customize the plot
plt.title("Super Over Matches Count in IPL", fontsize=14)

# Show the chart
plt.show()

###  **Step 1: Merge Deliveries with Matches to Get Venue Info**
merged_df = deliveries_df.merge(matches_df[['id', 'venue']], left_on='match_id', right_on='id', how='left')

###  **Step 2: Calculate Total Runs Per Match for Each Venue**
venue_runs = merged_df.groupby('venue')['total_runs'].sum()  # Sum of runs at each venue
venue_matches = merged_df.groupby('venue')['match_id'].nunique()  # Number of matches at each venue
batting_friendly_stadiums = (venue_runs / venue_matches).sort_values(ascending=False)  # Avg runs per match

###  **Step 3: Create a Horizontal Bar Chart**
plt.figure(figsize=(10, 6))
batting_friendly_stadiums.head(10).plot(kind='barh', color='orange', edgecolor='black')

# Customize the plot
plt.xlabel("Average Runs Per Match", fontsize=12)
plt.ylabel("Venue (Stadium)", fontsize=12)
plt.title("Top Batting-Friendly Stadiums in IPL", fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis to show the highest first
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Show the chart
plt.show()


