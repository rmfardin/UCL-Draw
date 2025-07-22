import os
import sys
import pandas as pd

# Add project root to sys.path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.simulator import run_full_draw, build_draw_matrix
from gsheet_integration.sync import sync_matrix_to_sheet

def main():
    # Run the full draw simulation
    matchups = run_full_draw(
        teams_csv_path='data/teams.csv',
        max_retries=10
    )

    # Build the 36x36 adjacency matrix
    matrix_df = build_draw_matrix(matchups)

    # Save locally as CSV
    matrix_df.to_csv('draw_matrix.csv', index=True)
    print("Draw complete. Saved matrix to 'draw_matrix.csv'.")

    # Sync the matrix to Google Sheets
    SPREADSHEET_ID = "your_google_sheet_id_here"
    SHEET_NAME = "DrawMatrix"
    sync_matrix_to_sheet(matrix_df, SPREADSHEET_ID, SHEET_NAME)
    print("Matrix synced to Google Sheets successfully.")

if __name__ == '__main__':
    main()
