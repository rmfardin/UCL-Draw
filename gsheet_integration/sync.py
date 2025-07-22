# gsheet_integration/sheets_sync.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def sync_matrix_to_sheet(
    matrix_df,
    spreadsheet_id: str,
    sheet_name: str = "UCL Matrix"
):
    """
    Sync a Pandas adjacency matrix to a Google Sheet.

    Args:
        matrix_df (pd.DataFrame): 36×36 DataFrame of 0/1 values.
        spreadsheet_id (str): the ID from your Sheet's URL.
        sheet_name (str): the name of the tab to write to.
    """
    # 1. Authenticate with service account credentials
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "gsheet/credentials.json", scope
    )
    client = gspread.authorize(creds)

    # 2. Open the spreadsheet by ID
    #    (URL looks like https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit)
    spreadsheet = client.open_by_key(spreadsheet_id)

    # 3. Select or create the worksheet/tab
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # If it does not exist, add a new one of the right size
        rows = matrix_df.shape[0] + 1
        cols = matrix_df.shape[1] + 1
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=str(rows),
            cols=str(cols)
        )

    # 4. Prepare the values to write: header + each row
    header = [""] + matrix_df.columns.tolist()
    values = [header]
    for idx, row in matrix_df.iterrows():
        # each row: team name, then its row of 0/1 values
        values.append([idx] + row.tolist())

    # 5. Clear existing contents and write new values in one batch
    worksheet.clear()
    worksheet.update("A1", values)
