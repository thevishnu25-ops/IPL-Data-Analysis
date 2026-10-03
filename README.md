# IPL Data Analysis

## Project Title
IPL Performance Analytics

## Objective
The objective of this project is to analyze IPL match and player-related data and convert raw records into meaningful sports insights. The analysis focuses on team and player performance, match outcomes, batting, bowling, venues, toss decisions, and season-wise trends.

## Dataset
The project uses a cleaned delivery-level IPL dataset covering the 2015-2024 seasons. Match-level analysis is performed using one record per Match_ID, while delivery-level records are used for batting, bowling, runs, and wickets analysis.

Key dataset results:
- Total matches: 120
- Total runs: 52,857
- Total wickets: 1,386
- Average runs per match: 440.48

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Power BI Desktop
- Power Query
- DAX

## Analysis Performed
The project analyzes:
- Matches played by season
- Matches won by each team
- Highest and lowest team wins
- Player of the Match awards
- Venue-wise match counts
- Toss decisions and toss-to-match-win relationship
- Winning margins by runs and wickets
- Top run scorers and wicket takers
- Season-wise total runs and wickets
- Average runs per match
- Team-wise average runs
- Season-wise team performance
- Team performance by venue
- Runs vs wickets relationship
- Correlation between numerical variables

## Python Visualizations
The Python analysis includes 14 visualizations covering season trends, team wins, leading batsmen and bowlers, Player of the Match awards, toss decisions, toss results, run and wicket trends, run distribution, team comparison, venues, runs vs wickets, and a correlation heatmap.

## Power BI Dashboard
The Power BI dashboard provides an interactive one-page summary of the IPL dataset using KPI cards, team wins, matches by season, top run scorers, top wicket takers, season-wise runs, top venues, toss decisions, Player of the Match awards, and key insights.

## Key Insights
- Sunrisers Hyderabad recorded the highest number of wins with 17 victories.
- KL Rahul was the leading run scorer with 2,270 runs.
- Mohammed Shami was the leading wicket taker with 113 wickets.
- Rashid Khan recorded the most Player of the Match awards with 8.
- Fielding was selected in 77 of 120 matches (64.17%).
- Eden Gardens hosted the highest number of matches with 19.
- The 2023 season recorded the highest run total with 5,401 runs.
- Toss winners also won approximately 50.83% of matches, suggesting little advantage from winning the toss alone.
- Every season in the dataset contains 12 matches.
- Lucknow Super Giants recorded the highest team-wise average runs at approximately 223.96.

## Conclusion
This project demonstrates an end-to-end IPL data analysis workflow. The dataset was cleaned and standardized in Python, analyzed using Pandas and NumPy, visualized using Matplotlib and Seaborn, and presented through an interactive Power BI dashboard. The project highlights team and player performance, venue usage, toss behavior, season-wise trends, and relationships between major match variables.

## Submission Files
- `Dataset/IPL_Cleaned_Final.csv`
- `Python/IPL_Data_Analysis.py`
- `PowerBI/IPL_Analytics_Dashboard.pbix`
- `Report/IPL_Project_Report.pdf`
- `README.md`
