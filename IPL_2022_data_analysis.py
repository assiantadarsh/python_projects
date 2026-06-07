# ============================================================
# IPL 2022 Ball-by-Ball Data Analysis Project
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#============================================================
# Download Dataset -> https://www.kaggle.com/datasets/vora1011/ipl-2022-match-dataset
#============================================================

# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("/content/IPL_Ball_by_Ball_2022.csv.zip")


# ============================================================
# 1. DATA UNDERSTANDING
# ============================================================

print("Rows and Columns:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

print("\nNumerical Summary:")
print(df.describe())


# ============================================================
# 2. DATA INSPECTION
# ============================================================

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Rows Before Cleaning:")
print(df.duplicated().sum())

print("\nObject Columns:")
print(df.select_dtypes(include='object').columns)

print("\nNumeric Columns:")
print(df.select_dtypes(include='number').columns)


# ============================================================
# 3. DATA CLEANING
# ============================================================

# Clean column names
df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
)

print("\nCleaned Column Names:")
print(df.columns)

# Remove extra spaces from text columns
text_columns = [
    'batter',
    'bowler',
    'non-striker',
    'battingteam',
    'extra_type',
    'player_out',
    'kind',
    'fielders_involved'
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Handle missing values with meaningful labels
df['extra_type'] = df['extra_type'].replace('nan', pd.NA).fillna('No Extra')
df['player_out'] = df['player_out'].replace('nan', pd.NA).fillna('No Wicket')
df['kind'] = df['kind'].replace('nan', pd.NA).fillna('No Dismissal')
df['fielders_involved'] = df['fielders_involved'].replace('nan', pd.NA).fillna('No Fielder')

# Remove duplicate rows
df = df.drop_duplicates()

print("\nDuplicate Rows After Cleaning:")
print(df.duplicated().sum())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Check and convert numeric columns
numeric_columns = [
    'id',
    'innings',
    'overs',
    'ballnumber',
    'batsman_run',
    'extras_run',
    'total_run',
    'non_boundary',
    'iswicketdelivery'
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nFinal Data Types:")
print(df.dtypes)


# ============================================================
# 4. DATA TRANSFORMATION
# ============================================================

# Wicket column
df['wicket'] = df['iswicketdelivery']

# Bowler wicket column
# Run out, retired hurt, and obstructing the field are usually not credited to bowler
non_bowler_wickets = ['run out', 'retired hurt', 'retired out', 'obstructing the field']

df['bowler_wicket'] = df.apply(
    lambda row: 1 if row['iswicketdelivery'] == 1 and row['kind'] not in non_bowler_wickets else 0,
    axis=1
)

# Over phase column
# IPL ball-by-ball datasets usually use overs from 0 to 19
def get_over_phase(over):
    if over <= 5:
        return 'Powerplay'
    elif over <= 14:
        return 'Middle Overs'
    else:
        return 'Death Overs'

df['over_phase'] = df['overs'].apply(get_over_phase)

# Boundary columns
df['is_four'] = df['batsman_run'].apply(lambda x: 1 if x == 4 else 0)
df['is_six'] = df['batsman_run'].apply(lambda x: 1 if x == 6 else 0)
df['is_boundary'] = df['batsman_run'].apply(lambda x: 1 if x in [4, 6] else 0)

# Dot ball column
df['is_dot_ball'] = df['total_run'].apply(lambda x: 1 if x == 0 else 0)

# Legal balls dataframe
# Wides are not counted as legal balls
legal_balls = df[df['extra_type'] != 'wides']

# Phase-wise dataframes
powerplay_data = df[df['over_phase'] == 'Powerplay']
middle_overs_data = df[df['over_phase'] == 'Middle Overs']
death_overs_data = df[df['over_phase'] == 'Death Overs']

# Each over total runs
df['each_over_total_run'] = df.groupby(['id', 'innings', 'overs'])['total_run'].transform('sum')

print("\nTransformed Data Preview:")
print(df[['battingteam', 'batter', 'bowler', 'overs', 'batsman_run',
          'total_run', 'wicket', 'bowler_wicket', 'over_phase',
          'is_four', 'is_six', 'is_boundary', 'is_dot_ball']].head())


# ============================================================
# 5. TEAM ANALYSIS
# ============================================================

# 1. Team-wise total runs
team_total_runs = df.groupby('battingteam')['total_run'].sum().sort_values(ascending=False)

print("\n1. Team-wise Total Runs:")
print(team_total_runs)

# 2. Team-wise balls faced
team_balls_faced = legal_balls.groupby('battingteam').size().sort_values(ascending=False)

print("\n2. Team-wise Balls Faced:")
print(team_balls_faced)

# 3. Team-wise fours
team_fours = df.groupby('battingteam')['is_four'].sum().sort_values(ascending=False)

print("\n3. Team-wise Fours:")
print(team_fours)

# 4. Team-wise sixes
team_sixes = df.groupby('battingteam')['is_six'].sum().sort_values(ascending=False)

print("\n4. Team-wise Sixes:")
print(team_sixes)

# 5. Team-wise boundaries
team_boundaries = df.groupby('battingteam')['is_boundary'].sum().sort_values(ascending=False)

print("\n5. Team-wise Boundaries:")
print(team_boundaries)

# 6. Team-wise wickets lost
team_wickets_lost = df.groupby('battingteam')['wicket'].sum().sort_values(ascending=False)

print("\n6. Team-wise Wickets Lost:")
print(team_wickets_lost)

# 7. Team-wise runs per ball
team_runs_per_ball = (team_total_runs / team_balls_faced).sort_values(ascending=False)

print("\n7. Team-wise Runs Per Ball:")
print(round(team_runs_per_ball, 2))

# 8. Team-wise powerplay runs
team_powerplay_runs = powerplay_data.groupby('battingteam')['total_run'].sum().sort_values(ascending=False)

print("\n8. Team-wise Powerplay Runs:")
print(team_powerplay_runs)

# 9. Team-wise middle overs runs
team_middle_runs = middle_overs_data.groupby('battingteam')['total_run'].sum().sort_values(ascending=False)

print("\n9. Team-wise Middle Overs Runs:")
print(team_middle_runs)

# 10. Team-wise death overs runs
team_death_runs = death_overs_data.groupby('battingteam')['total_run'].sum().sort_values(ascending=False)

print("\n10. Team-wise Death Overs Runs:")
print(team_death_runs)


# ============================================================
# 6. BATTING ANALYSIS
# ============================================================

# 1. Batter total runs
batter_runs = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)

print("\n1. Top 10 Run Scorers:")
print(batter_runs.head(10))

# 2. Batter balls faced
batter_balls = legal_balls.groupby('batter').size().sort_values(ascending=False)

print("\n2. Top 10 Batters by Balls Faced:")
print(batter_balls.head(10))

# 3. Batter fours
batter_fours = df.groupby('batter')['is_four'].sum().sort_values(ascending=False)

print("\n3. Top 10 Four Hitters:")
print(batter_fours.head(10))

# 4. Batter sixes
batter_sixes = df.groupby('batter')['is_six'].sum().sort_values(ascending=False)

print("\n4. Top 10 Six Hitters:")
print(batter_sixes.head(10))

# 5. Batter boundaries
batter_boundaries = df.groupby('batter')['is_boundary'].sum().sort_values(ascending=False)

print("\n5. Top 10 Boundary Hitters:")
print(batter_boundaries.head(10))

# 6. Batting stats table
batting_stats = pd.DataFrame({
    'runs': batter_runs,
    'balls': batter_balls,
    'fours': batter_fours,
    'sixes': batter_sixes,
    'boundaries': batter_boundaries
}).fillna(0)

batting_stats['strike_rate'] = (batting_stats['runs'] / batting_stats['balls']) * 100
batting_stats['runs_per_ball'] = batting_stats['runs'] / batting_stats['balls']
batting_stats['boundary_percentage'] = (batting_stats['boundaries'] / batting_stats['balls']) * 100

# Minimum 20 balls condition
batting_stats_20_balls = batting_stats[batting_stats['balls'] >= 20]

print("\n6. Top 10 Batters by Strike Rate:")
print(round(batting_stats_20_balls.sort_values(by='strike_rate', ascending=False).head(10), 2))

# 7. Powerplay runs by batter
batter_powerplay_runs = powerplay_data.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)

print("\n7. Top 10 Powerplay Run Scorers:")
print(batter_powerplay_runs.head(10))

# 8. Middle overs runs by batter
batter_middle_runs = middle_overs_data.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)

print("\n8. Top 10 Middle Overs Run Scorers:")
print(batter_middle_runs.head(10))

# 9. Death overs runs by batter
batter_death_runs = death_overs_data.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)

print("\n9. Top 10 Death Overs Run Scorers:")
print(batter_death_runs.head(10))

# 10. Dot balls faced by batter
batter_dot_balls = legal_balls.groupby('batter')['is_dot_ball'].sum().sort_values(ascending=False)

print("\n10. Top 10 Batters by Dot Balls Faced:")
print(batter_dot_balls.head(10))

# 11. Boundary percentage
print("\n11. Top 10 Batters by Boundary Percentage:")
print(round(batting_stats_20_balls.sort_values(by='boundary_percentage', ascending=False).head(10), 2))

# 12. Runs per ball
print("\n12. Top 10 Batters by Runs Per Ball:")
print(round(batting_stats_20_balls.sort_values(by='runs_per_ball', ascending=False).head(10), 2))


# ============================================================
# 7. BOWLING ANALYSIS
# ============================================================

# 1. Bowler runs conceded
bowler_runs = df.groupby('bowler')['total_run'].sum().sort_values(ascending=False)

print("\n1. Top 10 Bowlers Who Conceded Most Runs:")
print(bowler_runs.head(10))

# 2. Bowler legal balls
bowler_balls = legal_balls.groupby('bowler').size().sort_values(ascending=False)

print("\n2. Top 10 Bowlers by Legal Balls:")
print(bowler_balls.head(10))

# 3. Bowler wickets
bowler_wickets = df.groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False)

print("\n3. Top 10 Wicket Takers:")
print(bowler_wickets.head(10))

# 4. Bowler fours conceded
bowler_fours = df.groupby('bowler')['is_four'].sum().sort_values(ascending=False)

print("\n4. Top 10 Bowlers Who Conceded Most Fours:")
print(bowler_fours.head(10))

# 5. Bowler sixes conceded
bowler_sixes = df.groupby('bowler')['is_six'].sum().sort_values(ascending=False)

print("\n5. Top 10 Bowlers Who Conceded Most Sixes:")
print(bowler_sixes.head(10))

# 6. Bowler dot balls
bowler_dot_balls = legal_balls.groupby('bowler')['is_dot_ball'].sum().sort_values(ascending=False)

print("\n6. Top 10 Bowlers by Dot Balls:")
print(bowler_dot_balls.head(10))

# 7. Bowling stats table
bowling_stats = pd.DataFrame({
    'runs_conceded': bowler_runs,
    'balls_bowled': bowler_balls,
    'wickets': bowler_wickets,
    'dot_balls': bowler_dot_balls,
    'fours_conceded': bowler_fours,
    'sixes_conceded': bowler_sixes
}).fillna(0)

bowling_stats['overs_bowled'] = bowling_stats['balls_bowled'] / 6
bowling_stats['economy_rate'] = bowling_stats['runs_conceded'] / bowling_stats['overs_bowled']
bowling_stats['bowling_strike_rate'] = bowling_stats['balls_bowled'] / bowling_stats['wickets'].replace(0, pd.NA)
bowling_stats['bowling_average'] = bowling_stats['runs_conceded'] / bowling_stats['wickets'].replace(0, pd.NA)

# Minimum 60 balls condition
bowling_stats_60_balls = bowling_stats[bowling_stats['balls_bowled'] >= 60]

print("\n7. Top 10 Best Economy Bowlers:")
print(round(bowling_stats_60_balls.sort_values(by='economy_rate').head(10), 2))

print("\n8. Top 10 Best Bowling Strike Rate:")
print(round(bowling_stats[bowling_stats['wickets'] >= 3].sort_values(by='bowling_strike_rate').head(10), 2))

print("\n9. Top 10 Best Bowling Average:")
print(round(bowling_stats[bowling_stats['wickets'] >= 3].sort_values(by='bowling_average').head(10), 2))

# Phase-wise wickets by bowlers
bowler_powerplay_wickets = powerplay_data.groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False)
bowler_middle_wickets = middle_overs_data.groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False)
bowler_death_wickets = death_overs_data.groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False)

print("\n10. Top 10 Powerplay Wicket Takers:")
print(bowler_powerplay_wickets.head(10))

print("\n11. Top 10 Middle Overs Wicket Takers:")
print(bowler_middle_wickets.head(10))

print("\n12. Top 10 Death Overs Wicket Takers:")
print(bowler_death_wickets.head(10))


# ============================================================
# 8. OVER PHASE ANALYSIS
# ============================================================

phase_runs = df.groupby('over_phase')['total_run'].sum().sort_values(ascending=False)
phase_wickets = df.groupby('over_phase')['wicket'].sum().sort_values(ascending=False)
phase_fours = df.groupby('over_phase')['is_four'].sum().sort_values(ascending=False)
phase_sixes = df.groupby('over_phase')['is_six'].sum().sort_values(ascending=False)
phase_boundaries = df.groupby('over_phase')['is_boundary'].sum().sort_values(ascending=False)
phase_dot_balls = legal_balls.groupby('over_phase')['is_dot_ball'].sum().sort_values(ascending=False)
phase_balls = legal_balls.groupby('over_phase').size()

phase_runs_per_ball = (phase_runs / phase_balls).sort_values(ascending=False)

print("\n1. Runs by Over Phase:")
print(phase_runs)

print("\n2. Wickets by Over Phase:")
print(phase_wickets)

print("\n3. Fours by Over Phase:")
print(phase_fours)

print("\n4. Sixes by Over Phase:")
print(phase_sixes)

print("\n5. Boundaries by Over Phase:")
print(phase_boundaries)

print("\n6. Dot Balls by Over Phase:")
print(phase_dot_balls)

print("\n7. Runs Per Ball by Over Phase:")
print(round(phase_runs_per_ball, 2))

best_batting_phase = phase_runs_per_ball.idxmax()
best_bowling_phase = phase_wickets.idxmax()

print("\n8. Best Phase for Batters:")
print(best_batting_phase)

print("\n9. Best Phase for Bowlers:")
print(best_bowling_phase)


# ============================================================
# 9. DATA VISUALIZATION
# ============================================================

# 1. Top 10 Run Scorers
plt.figure(figsize=(12, 6))
batter_runs.head(10).plot(kind='bar')
plt.title("Top 10 Run Scorers")
plt.xlabel("Batter")
plt.ylabel("Runs")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 2. Top 10 Wicket Takers
plt.figure(figsize=(12, 6))
bowler_wickets.head(10).plot(kind='bar')
plt.title("Top 10 Wicket Takers")
plt.xlabel("Bowler")
plt.ylabel("Wickets")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 3. Top 10 Six Hitters
plt.figure(figsize=(12, 6))
batter_sixes.head(10).plot(kind='bar')
plt.title("Top 10 Six Hitters")
plt.xlabel("Batter")
plt.ylabel("Sixes")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 4. Top 10 Four Hitters
plt.figure(figsize=(12, 6))
batter_fours.head(10).plot(kind='bar')
plt.title("Top 10 Four Hitters")
plt.xlabel("Batter")
plt.ylabel("Fours")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 5. Team-wise Total Runs
plt.figure(figsize=(12, 6))
team_total_runs.plot(kind='bar')
plt.title("Team-wise Total Runs")
plt.xlabel("Team")
plt.ylabel("Total Runs")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 6. Team-wise Sixes
plt.figure(figsize=(12, 6))
team_sixes.plot(kind='bar')
plt.title("Team-wise Sixes")
plt.xlabel("Team")
plt.ylabel("Sixes")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 7. Team-wise Wickets Lost
plt.figure(figsize=(12, 6))
team_wickets_lost.plot(kind='bar')
plt.title("Team-wise Wickets Lost")
plt.xlabel("Team")
plt.ylabel("Wickets")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 8. Runs by Over Phase
plt.figure(figsize=(8, 5))
phase_runs.plot(kind='bar')
plt.title("Runs by Over Phase")
plt.xlabel("Over Phase")
plt.ylabel("Runs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 9. Wickets by Over Phase
plt.figure(figsize=(8, 5))
phase_wickets.plot(kind='bar')
plt.title("Wickets by Over Phase")
plt.xlabel("Over Phase")
plt.ylabel("Wickets")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 10. Boundaries by Over Phase
plt.figure(figsize=(8, 5))
phase_boundaries.plot(kind='bar')
plt.title("Boundaries by Over Phase")
plt.xlabel("Over Phase")
plt.ylabel("Boundaries")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 11. Runs vs Balls Faced
batter_scatter = pd.DataFrame({
    'runs': batting_stats['runs'],
    'balls': batting_stats['balls']
}).dropna()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=batter_scatter, x='balls', y='runs')
plt.title("Runs vs Balls Faced")
plt.xlabel("Balls Faced")
plt.ylabel("Runs")
plt.tight_layout()
plt.show()

# 12. Wickets vs Economy Rate
bowler_scatter = bowling_stats[['wickets', 'economy_rate']].dropna()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=bowler_scatter, x='wickets', y='economy_rate')
plt.title("Wickets vs Economy Rate")
plt.xlabel("Wickets")
plt.ylabel("Economy Rate")
plt.tight_layout()
plt.show()

# 13. Batter Runs Distribution
plt.figure(figsize=(10, 5))
plt.hist(batting_stats['runs'], bins=20)
plt.title("Batter Runs Distribution")
plt.xlabel("Runs")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 14. Bowler Economy Rate Distribution
plt.figure(figsize=(10, 5))
plt.hist(bowling_stats_60_balls['economy_rate'], bins=15)
plt.title("Bowler Economy Rate Distribution")
plt.xlabel("Economy Rate")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 15. Correlation Heatmap
corr_columns = [
    'batsman_run',
    'extras_run',
    'total_run',
    'wicket',
    'bowler_wicket',
    'is_four',
    'is_six',
    'is_boundary',
    'is_dot_ball'
]

corr_data = df[corr_columns].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr_data, annot=True, fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()


# ============================================================
# 10. FINAL INSIGHTS
# ============================================================

print("\nFinal Insights:")

print("1. Highest Run Scorer:",
      batter_runs.idxmax(), "-", batter_runs.max(), "runs")

print("2. Most Sixes Hit By:",
      batter_sixes.idxmax(), "-", batter_sixes.max(), "sixes")

print("3. Most Fours Hit By:",
      batter_fours.idxmax(), "-", batter_fours.max(), "fours")

print("4. Best Strike Rate Batter:",
      batting_stats_20_balls['strike_rate'].idxmax(), "-",
      round(batting_stats_20_balls['strike_rate'].max(), 2))

print("5. Best Powerplay Batter:",
      batter_powerplay_runs.idxmax(), "-", batter_powerplay_runs.max(), "runs")

print("6. Best Death Overs Batter:",
      batter_death_runs.idxmax(), "-", batter_death_runs.max(), "runs")

print("7. Highest Wicket Taker:",
      bowler_wickets.idxmax(), "-", bowler_wickets.max(), "wickets")

print("8. Best Economy Bowler:",
      bowling_stats_60_balls['economy_rate'].idxmin(), "-",
      round(bowling_stats_60_balls['economy_rate'].min(), 2))

print("9. Best Bowling Strike Rate:",
      bowling_stats[bowling_stats['wickets'] >= 3]['bowling_strike_rate'].idxmin(), "-",
      round(bowling_stats[bowling_stats['wickets'] >= 3]['bowling_strike_rate'].min(), 2))

print("10. Best Death Overs Bowler:",
      bowler_death_wickets.idxmax(), "-", bowler_death_wickets.max(), "wickets")

print("11. Highest Run Scoring Team:",
      team_total_runs.idxmax(), "-", team_total_runs.max(), "runs")

print("12. Team with Most Boundaries:",
      team_boundaries.idxmax(), "-", team_boundaries.max(), "boundaries")

print("13. Best Death Overs Team:",
      team_death_runs.idxmax(), "-", team_death_runs.max(), "runs")

print("14. Highest Scoring Phase:",
      phase_runs.idxmax(), "-", phase_runs.max(), "runs")

print("15. Phase with Most Wickets:",
      phase_wickets.idxmax(), "-", phase_wickets.max(), "wickets")

print("16. Best Phase for Batters:",
      best_batting_phase)

print("17. Best Phase for Bowlers:",
      best_bowling_phase)
