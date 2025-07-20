import pandas as pd

# Manually transcribed from the image provided
teams_data = [
    # Pot 1
    ("Real Madrid", "Spain", 1),
    ("Manchester City", "England", 1),
    ("Bayern Munich", "Germany", 1),
    ("Liverpool", "England", 1),
    ("PSG", "France", 1),
    ("Inter", "Italy", 1),
    ("Chelsea", "England", 1),
    ("Dortmund", "Germany", 1),
    ("Barcelona", "Spain", 1),
    
    # Pot 2
    ("Arsenal", "England", 2),
    ("Leverkusen", "Germany", 2),
    ("Atlético Madrid", "Spain", 2),
    ("Benfica", "Portugal", 2),
    ("Atalanta", "Italy", 2),
    ("Villarreal", "Spain", 2),
    ("Juventus", "Italy", 2),
    ("Eintracht", "Germany", 2),
    ("Club Brugge", "Belgium", 2),

    # Pot 3
    ("Tottenham", "England", 3),
    ("PSV", "Netherlands", 3),
    ("Ajax", "Netherlands", 3),
    ("Napoli", "Italy", 3),
    ("Sporting CP", "Portugal", 3),
    ("Olympiacos", "Greece", 3),
    ("Slavia Praha", "Czech Republic", 3),
    ("Bodø/Glimt", "Norway", 3),
    ("Marseille", "France", 3),

    # Pot 4
    ("FC Copenhagen", "Denmark", 4),
    ("Crvena Zvezda", "Serbia", 4),
    ("AS Monaco", "France", 4),
    ("Ferencváros", "Hungary", 4),
    ("Galatasaray", "Turkey", 4),
    ("Celtic", "Scotland", 4),
    ("Union SG", "Belgium", 4),
    ("Athletic Club", "Spain", 4),
    ("Newcastle", "England", 4)
]

# Create DataFrame
teams_df = pd.DataFrame(teams_data, columns=["Team", "Country", "Pot"])

# Save to CSV
csv_path = "data/teams.csv"
teams_df.to_csv(csv_path, index=False)

csv_path
