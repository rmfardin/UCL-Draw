import pandas as pd

# Manually transcribed from the image provided
teams_data = [
    # Pot 1
    ("Paris Saint-Germain", "France", 1),
    ("Real Madrid", "Spain", 1),
    ("Manchester City", "England", 1),
    ("Bayern München", "Germany", 1),
    ("Liverpool", "England", 1),
    ("Internazionale", "Italy", 1),
    ("Chelsea", "England", 1),
    ("Borussia Dortmund", "Germany", 1),
    ("FC Barcelona", "Spain", 1),

    # Pot 2
    ("Arsenal", "England", 2),
    ("Bayer Leverkusen", "Germany", 2),
    ("Atlético Madrid", "Spain", 2),
    ("Benfica", "Portugal", 2),
    ("Atalanta", "Italy", 2),
    ("Villarreal", "Spain", 2),
    ("Juventus", "Italy", 2),
    ("Eintracht Frankfurt", "Germany", 2),
    ("Club Brugge", "Belgium", 2),

    # Pot 3
    ("Tottenham Hotspur", "England", 3),
    ("PSV Eindhoven", "Netherlands", 3),
    ("Ajax", "Netherlands", 3),
    ("Napoli", "Italy", 3),
    ("Sporting CP Lisbon", "Portugal", 3),
    ("Olympiakos Piraeus", "Greece", 3),
    ("Slavia Praha", "Czech Republic", 3),
    ("Bodø/Glimt", "Norway", 3),
    ("Olympique Marseille", "France", 3),

    # Pot 4
    ("FC København", "Denmark", 4),
    ("Red Star Belgrade", "Serbia", 4),
    ("AS Monaco", "France", 4),
    ("Ferencváros", "Hungary", 4),
    ("Galatasaray", "Turkey", 4),
    ("Celtic", "Scotland", 4),
    ("Union Saint-Gilloise", "Belgium", 4),
    ("Athletic Bilbao", "Spain", 4),
    ("Newcastle United", "England", 4)
]

# Create DataFrame
teams_df = pd.DataFrame(teams_data, columns=["Team", "Country", "Pot"])

# Save to CSV
csv_path = "data/teams.csv"
teams_df.to_csv(csv_path, index=False)

csv_path
