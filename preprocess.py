import pandas as pd
import os

# Load and sort teams
df = pd.read_csv("data/teams.csv")
df_sorted = df.sort_values(by=["Pot", "Team"]).reset_index(drop=True)

# Country-to-code map for flags
country_to_code = {
    "France": "fr", "Spain": "es", "England": "gb-eng", "Germany": "de", "Italy": "it",
    "Portugal": "pt", "Netherlands": "nl", "Belgium": "be", "Austria": "at", "Scotland": "gb-sct",
    "Norway": "no", "Denmark": "dk", "Serbia": "rs", "Hungary": "hu", "Turkey": "tr",
    "Greece": "gr", "Croatia": "hr", "Switzerland": "ch", "Czech Republic": "cz", "Poland": "pl",
    "Russia": "ru", "Sweden": "se", "Finland": "fi", "Wales": "gb-wls", "Ireland": "ie"
}

# Generate in-cell IMAGE() formula for flags
def generate_image_formula(country):
    code = country_to_code.get(country, "un")
    return f'=IMAGE("https://flagcdn.com/48x36/{code}.png")'

df_sorted["Flag"] = df_sorted["Country"].apply(generate_image_formula)

# Setup matrix
num_teams = len(df_sorted)
matrix = [["" for _ in range(num_teams + 3)] for _ in range(num_teams + 3)]

# Header row
matrix[0][0] = "Pot"
matrix[0][1] = "Team"
matrix[0][2] = "Flag"

# Fill top header (teams across)
for i, row in enumerate(df_sorted.itertuples(), start=3):
    matrix[0][i] = f"Pot {row.Pot}"
    matrix[1][i] = row.Team
    matrix[2][i] = row.Flag

# Fill side header (teams down)
for i, row in enumerate(df_sorted.itertuples(), start=3):
    matrix[i][0] = f"Pot {row.Pot}"
    matrix[i][1] = row.Team
    matrix[i][2] = row.Flag

# Fill 1 for same-country matchups
for i, team_i in enumerate(df_sorted.itertuples()):
    for j, team_j in enumerate(df_sorted.itertuples()):
        if i != j and team_i.Country == team_j.Country:
            matrix[i + 3][j + 3] = "1"  # will apply red background in Google Sheets

# Create and save DataFrame
final_df = pd.DataFrame(matrix)
output_path = "teams_google_sheets_redfill.csv"
final_df.to_csv(output_path, index=False, header=False, quoting=3)  # quoting=3 disables quote wrapping

print(f"✅ Saved: {output_path}")
