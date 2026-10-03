# ============================================================
# IPL DATA ANALYSIS - COMPLETE BEGINNER PROJECT
# Dataset file expected: IPL_Cleaned_Final.csv
# ============================================================

# ---------------------------
# PART 1 - IMPORT LIBRARIES
# ---------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
sns.set_theme(style="whitegrid")

# ---------------------------
# PART 1 - DATA LOADING
# ---------------------------
df = pd.read_csv("IPL_Cleaned_Final.csv")

print("\nFIRST 5 ROWS")
print(df.head())

print("\nLAST 5 ROWS")
print(df.tail())

print("\nDATASET SHAPE (rows, columns)")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

numerical_columns = df.select_dtypes(include=np.number).columns.tolist()
categorical_columns = df.select_dtypes(exclude=np.number).columns.tolist()

print("\nNUMERICAL COLUMNS")
print(numerical_columns)

print("\nCATEGORICAL COLUMNS")
print(categorical_columns)

# ---------------------------
# PART 2 - EXPLORATION & CLEANING
# ---------------------------
print("\nDATA TYPES")
print(df.dtypes)

print("\nBASIC STATISTICS")
print(df.describe(include="all").T)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# Remove exact duplicate delivery records
df = df.drop_duplicates().copy()

print("\nUNIQUE TEAM1 VALUES")
print(sorted(df["Team1"].dropna().unique()))

print("\nUNIQUE TEAM2 VALUES")
print(sorted(df["Team2"].dropna().unique()))

print("\nUNIQUE TOSS DECISIONS")
print(df["Toss_Decision"].dropna().unique())

# Standardize text
text_columns = [
    "City","Venue","Team1","Team2","Toss_Winner","Toss_Decision","Winner",
    "Player_of_Match","Result","Batting_Team","Bowling_Team","Batsman","Bowler"
]
for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Example mapping for historical/inconsistent team names.
# Add more mappings here if your real dataset contains old franchise names.
team_name_mapping = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}
team_columns = ["Team1","Team2","Toss_Winner","Winner","Batting_Team","Bowling_Team"]
for col in team_columns:
    df[col] = df[col].replace(team_name_mapping)

# Missing-value handling
df["City"] = df["City"].fillna("Unknown")
df["Venue"] = df["Venue"].fillna("Unknown")
df["Player_of_Match"] = df["Player_of_Match"].fillna("Unknown")
df["Winner"] = df["Winner"].fillna("No Result")

numeric_fill_zero = [
    "Win_By_Runs","Win_By_Wickets","Runs_Scored","Extra_Runs",
    "Total_Runs","Wickets","Innings","Over","Ball"
]
for col in numeric_fill_zero:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Convert date
df["Match_Date"] = pd.to_datetime(df["Match_Date"], errors="coerce")

# Create useful derived columns
df["Toss_Match_Win"] = np.where(df["Toss_Winner"] == df["Winner"], "Yes", "No")
df["Boundary"] = np.where(df["Runs_Scored"].isin([4, 6]), "Yes", "No")

print("\nCLEANED DATASET INFO")
print(df.info())

print("\nMISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

# Save cleaned dataset again
df.to_csv("IPL_Cleaned_Final.csv", index=False)

# IMPORTANT:
# This CSV is delivery-level data, so match details repeat for every ball.
# Create one row per match before match-level analysis.
matches = df.drop_duplicates(subset="Match_ID").copy()

# ============================================================
# PART 3 - DATA ANALYSIS USING PANDAS & NUMPY
# ============================================================

# 18. Total number of matches
total_matches = matches["Match_ID"].nunique()
print("\n18. TOTAL MATCHES:", total_matches)

# 19. Matches played in each season
matches_by_season = matches.groupby("Season")["Match_ID"].nunique().sort_index()
print("\n19. MATCHES BY SEASON")
print(matches_by_season)

# 20. Matches won by each team
team_wins = matches["Winner"].value_counts()
team_wins = team_wins[team_wins.index != "No Result"]
print("\n20. TEAM WINS")
print(team_wins)

# 21. Team with highest wins
print("\n21. TEAM WITH HIGHEST WINS:", team_wins.idxmax(), "-", team_wins.max())

# 22. Team with lowest wins
print("\n22. TEAM WITH LOWEST WINS:", team_wins.idxmin(), "-", team_wins.min())

# 23. Most successful Player of the Match
pom_awards = matches["Player_of_Match"].value_counts()
print("\n23. MOST PLAYER OF MATCH AWARDS:", pom_awards.idxmax(), "-", pom_awards.max())

# 24. Most frequently used venue
venue_matches = matches["Venue"].value_counts()
print("\n24. MOST USED VENUE:", venue_matches.idxmax(), "-", venue_matches.max())

# 25. Toss decisions
toss_decisions = matches["Toss_Decision"].value_counts()
print("\n25. TOSS DECISIONS")
print(toss_decisions)

# 26. Percentage of matches won after winning toss
toss_win_percentage = (matches["Toss_Winner"].eq(matches["Winner"]).mean() * 100)
print("\n26. TOSS WIN -> MATCH WIN PERCENTAGE:", round(toss_win_percentage, 2), "%")

# 27. Highest winning margin by runs
max_runs_margin = matches["Win_By_Runs"].max()
print("\n27. HIGHEST WINNING MARGIN BY RUNS:", max_runs_margin)
print(matches.loc[matches["Win_By_Runs"].idxmax(),
                  ["Season","Team1","Team2","Winner","Win_By_Runs"]])

# 28. Highest winning margin by wickets
max_wickets_margin = matches["Win_By_Wickets"].max()
print("\n28. HIGHEST WINNING MARGIN BY WICKETS:", max_wickets_margin)
print(matches.loc[matches["Win_By_Wickets"].idxmax(),
                  ["Season","Team1","Team2","Winner","Win_By_Wickets"]])

# 29 & 31. Highest run scorer + top 10 batsmen
batsman_runs = df.groupby("Batsman")["Runs_Scored"].sum().sort_values(ascending=False)
print("\n29. HIGHEST RUN SCORER:", batsman_runs.idxmax(), "-", batsman_runs.max())
top10_batsmen = batsman_runs.head(10)
print("\n31. TOP 10 BATSMEN")
print(top10_batsmen)

# 30 & 32. Highest wicket taker + top 10 bowlers
# In this simplified dataset Wickets=1 means a wicket on that delivery.
bowler_wickets = df.groupby("Bowler")["Wickets"].sum().sort_values(ascending=False)
print("\n30. HIGHEST WICKET TAKER:", bowler_wickets.idxmax(), "-", bowler_wickets.max())
top10_bowlers = bowler_wickets.head(10)
print("\n32. TOP 10 BOWLERS")
print(top10_bowlers)

# 33. Season-wise total runs
season_runs = df.groupby("Season")["Total_Runs"].sum().sort_index()
print("\n33. SEASON-WISE TOTAL RUNS")
print(season_runs)

# 34. Season-wise total wickets
season_wickets = df.groupby("Season")["Wickets"].sum().sort_index()
print("\n34. SEASON-WISE TOTAL WICKETS")
print(season_wickets)

# 35. Average runs per match
match_runs = df.groupby("Match_ID")["Total_Runs"].sum()
average_runs_per_match = match_runs.mean()
print("\n35. AVERAGE RUNS PER MATCH:", round(average_runs_per_match, 2))

# 36. Team-wise average runs
team_match_runs = (
    df.groupby(["Match_ID","Batting_Team"])["Total_Runs"]
      .sum()
      .reset_index()
)
team_average_runs = (
    team_match_runs.groupby("Batting_Team")["Total_Runs"]
    .mean()
    .sort_values(ascending=False)
)
print("\n36. TEAM-WISE AVERAGE RUNS")
print(team_average_runs)

# 37. Season-wise team performance (wins)
season_team_performance = (
    matches.groupby(["Season","Winner"])["Match_ID"]
    .nunique()
    .reset_index(name="Wins")
)
season_team_performance = season_team_performance[
    season_team_performance["Winner"] != "No Result"
]
print("\n37. SEASON-WISE TEAM PERFORMANCE")
print(season_team_performance)

# 38. Most successful venue for each team
team_venue_wins = (
    matches[matches["Winner"] != "No Result"]
    .groupby(["Winner","Venue"])["Match_ID"]
    .nunique()
    .reset_index(name="Wins")
)
most_successful_venue = (
    team_venue_wins.sort_values(["Winner","Wins"], ascending=[True,False])
    .drop_duplicates("Winner")
)
print("\n38. MOST SUCCESSFUL VENUE FOR EACH TEAM")
print(most_successful_venue)

# 39. Toss outcome vs match result
toss_relationship = pd.crosstab(
    matches["Toss_Decision"],
    matches["Toss_Winner"].eq(matches["Winner"]),
    margins=True
)
print("\n39. TOSS OUTCOME VS MATCH RESULT")
print(toss_relationship)

# 40. Major trends
highest_run_season = season_runs.idxmax()
highest_wicket_season = season_wickets.idxmax()
most_wins_team = team_wins.idxmax()
print("\n40. MAJOR PERFORMANCE TRENDS")
print("Most successful team by wins:", most_wins_team)
print("Season with most runs:", highest_run_season)
print("Season with most wickets:", highest_wicket_season)
print("Most common toss decision:", toss_decisions.idxmax())
print("Toss winner also won match in", round(toss_win_percentage,2), "% of matches")

# ============================================================
# PART 4 - PYTHON VISUALIZATIONS
# ============================================================

# 1. Matches Played by Season
plt.figure(figsize=(10,5))
matches_by_season.plot(kind="bar")
plt.title("Matches Played by Season")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Matches Won by Team
plt.figure(figsize=(10,6))
team_wins.sort_values().plot(kind="barh")
plt.title("Matches Won by Team")
plt.xlabel("Wins")
plt.ylabel("Team")
plt.tight_layout()
plt.show()

# 3. Top 10 Run Scorers
plt.figure(figsize=(10,6))
top10_batsmen.sort_values().plot(kind="barh")
plt.title("Top 10 Run Scorers")
plt.xlabel("Total Runs")
plt.ylabel("Batsman")
plt.tight_layout()
plt.show()

# 4. Top 10 Wicket Takers
plt.figure(figsize=(10,6))
top10_bowlers.sort_values().plot(kind="barh")
plt.title("Top 10 Wicket Takers")
plt.xlabel("Wickets")
plt.ylabel("Bowler")
plt.tight_layout()
plt.show()

# 5. Player of the Match Awards
plt.figure(figsize=(10,6))
pom_awards.head(10).sort_values().plot(kind="barh")
plt.title("Top Player of the Match Award Winners")
plt.xlabel("Awards")
plt.ylabel("Player")
plt.tight_layout()
plt.show()

# 6. Toss Decision Distribution
plt.figure(figsize=(6,6))
toss_decisions.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Toss Decision Distribution")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 7. Matches Won After Winning Toss
toss_match_result = matches["Toss_Winner"].eq(matches["Winner"]).map(
    {True:"Won Match", False:"Lost Match"}
).value_counts()
plt.figure(figsize=(7,5))
toss_match_result.plot(kind="bar")
plt.title("Match Result After Winning Toss")
plt.xlabel("Result")
plt.ylabel("Matches")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 8. Season-wise Total Runs
plt.figure(figsize=(10,5))
plt.plot(season_runs.index, season_runs.values, marker="o")
plt.title("Season-wise Total Runs")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 9. Season-wise Total Wickets
plt.figure(figsize=(10,5))
plt.plot(season_wickets.index, season_wickets.values, marker="o")
plt.title("Season-wise Total Wickets")
plt.xlabel("Season")
plt.ylabel("Total Wickets")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 10. Runs Distribution
plt.figure(figsize=(8,5))
plt.hist(match_runs, bins=15, edgecolor="black")
plt.title("Runs Distribution per Match")
plt.xlabel("Total Match Runs")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 11. Team Performance Comparison
team_summary = pd.DataFrame({
    "Wins": team_wins,
    "Average_Runs": team_average_runs
}).fillna(0)
team_summary["Win_Index"] = team_summary["Wins"] / team_summary["Wins"].max() * 100
team_summary["Run_Index"] = team_summary["Average_Runs"] / team_summary["Average_Runs"].max() * 100

team_summary[["Win_Index","Run_Index"]].plot(kind="bar", figsize=(12,6))
plt.title("Team Performance Comparison (Indexed)")
plt.xlabel("Team")
plt.ylabel("Index (Max = 100)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 12. Venue-wise Match Count
plt.figure(figsize=(10,6))
venue_matches.head(10).sort_values().plot(kind="barh")
plt.title("Top Venues by Match Count")
plt.xlabel("Matches")
plt.ylabel("Venue")
plt.tight_layout()
plt.show()

# 13. Runs vs Wickets Scatter Plot
match_wickets = df.groupby("Match_ID")["Wickets"].sum()
match_stats = pd.DataFrame({
    "Runs": match_runs,
    "Wickets": match_wickets
}).dropna()

plt.figure(figsize=(8,5))
plt.scatter(match_stats["Runs"], match_stats["Wickets"], alpha=0.7)
plt.title("Runs vs Wickets")
plt.xlabel("Total Match Runs")
plt.ylabel("Total Match Wickets")
plt.tight_layout()
plt.show()

# 14. Correlation Heatmap
numeric_for_corr = df[
    ["Runs_Scored","Extra_Runs","Total_Runs","Wickets","Over","Ball",
     "Win_By_Runs","Win_By_Wickets"]
]
plt.figure(figsize=(9,6))
sns.heatmap(numeric_for_corr.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# ============================================================
# BUSINESS INSIGHTS - AUTOMATIC OUTPUT
# ============================================================
print("\n================ BUSINESS INSIGHTS ================")
print("1. Team with highest wins:", team_wins.idxmax(), "-", team_wins.max())
print("2. Season with highest matches:", matches_by_season.idxmax(), "-", matches_by_season.max())
print("3. Most Player of Match awards:", pom_awards.idxmax(), "-", pom_awards.max())
print("4. Highest run scorer:", batsman_runs.idxmax(), "-", batsman_runs.max())
print("5. Highest wicket taker:", bowler_wickets.idxmax(), "-", bowler_wickets.max())
print("6. Venue with highest matches:", venue_matches.idxmax(), "-", venue_matches.max())
print("7. Most common toss decision:", toss_decisions.idxmax())
print("8. Toss winner also won match:", round(toss_win_percentage,2), "%")
print("9. Season with highest runs:", season_runs.idxmax(), "-", season_runs.max())
print("10. Team with highest average runs:", team_average_runs.idxmax(),
      "-", round(team_average_runs.max(),2))

print("\nProject analysis completed successfully.")
