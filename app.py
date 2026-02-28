from flask import Flask, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("cred.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1Gj9a6yZb3zGnwfLcqkW7MEDNihLSu0QoYqubCUe68yo"
spreadsheet = client.open_by_key(sheet_id)

# Hardcoded member list
ALL_MEMBERS = [
    {'team': 'Yudhishthira', 'index': 0, 'name': 'HG Ārādhan Pr'},
    {'team': 'Yudhishthira', 'index': 1, 'name': 'Tanmay Pr'},
    {'team': 'Yudhishthira', 'index': 2, 'name': 'Rohit Pr'},
    {'team': 'Yudhishthira', 'index': 3, 'name': 'Amol Pr'},
    {'team': 'Yudhishthira', 'index': 4, 'name': 'Anish Pr'},
    {'team': 'Bhima', 'index': 0, 'name': 'Abhishek Pr'},
    {'team': 'Bhima', 'index': 1, 'name': 'Hemant Pr'},
    {'team': 'Bhima', 'index': 2, 'name': 'Āditya M. Pr'},
    {'team': 'Bhima', 'index': 3, 'name': 'Shantanu Pr'},
    {'team': 'Bhima', 'index': 4, 'name': 'Vedānt S. Pr'},
    {'team': 'Arjuna', 'index': 0, 'name': 'Chaitanya Pr'},
    {'team': 'Arjuna', 'index': 1, 'name': 'Achintya Pr'},
    {'team': 'Arjuna', 'index': 2, 'name': 'Adithya S. Pr'},
    {'team': 'Arjuna', 'index': 3, 'name': 'Shaurya Pr'},
    {'team': 'Arjuna', 'index': 4, 'name': 'Asmit Pr'},
    {'team': 'Arjuna', 'index': 5, 'name': 'Pranav I. Pr'},
    {'team': 'Arjuna', 'index': 6, 'name': 'Manan Pr'},
    {'team': 'Arjuna', 'index': 7, 'name': 'Mahesh Pr'},
    {'team': 'Arjuna', 'index': 8, 'name': 'Sanket Pr'},
    {'team': 'Arjuna', 'index': 9, 'name': 'Pranav B. Pr'},
    {'team': 'Arjuna', 'index': 10, 'name': 'Rushikesh Pr'},
    {'team': 'Arjuna', 'index': 11, 'name': 'Sumit Pr'},
    {'team': 'Nakula', 'index': 0, 'name': 'Shriram Pr'},
    {'team': 'Nakula', 'index': 1, 'name': 'Rishit pr'},
    {'team': 'Nakula', 'index': 2, 'name': 'Vedant M. Pr'},
    {'team': 'Nakula', 'index': 3, 'name': 'Anurag pr'},
    {'team': 'Nakula', 'index': 4, 'name': 'Prithviraj Pr'},
    {'team': 'Nakula', 'index': 5, 'name': 'Shaunak pr'},
    {'team': 'Nakula', 'index': 6, 'name': 'Atul Pr'},
    {'team': 'Nakula', 'index': 7, 'name': 'Atharva pr'},
    {'team': 'Nakula', 'index': 8, 'name': 'Vipul pr'}
]

TEAMS = {
    'Yudhishthira': {'count': 5, 'name_row': 6, 'data_start_row': 8, 'start_col': 5},
    'Bhima': {'count': 5, 'name_row': 6, 'data_start_row': 8, 'start_col': 5},
    'Arjuna': {'count': 12, 'name_row': 6, 'data_start_row': 8, 'start_col': 5},
    'Nakula': {'count': 9, 'name_row': 5, 'data_start_row': 7, 'start_col': 5}
}

# Assuming 6 columns per person. 'location' at index 0 (not used in UI)
# and then the fields from the UI.
COL_MAP = {'level': 1, 'pa': 2, 'extra': 3, 'dk': 4, 'comment': 5}

@app.route('/')
def index():
    return render_template('index.html', teams=TEAMS)

@app.route('/get_all_members')
def get_all_members():
    return jsonify(ALL_MEMBERS)

@app.route('/get_attendance_data')
def get_attendance_data():
    team = request.args.get('team')
    day = int(request.args.get('day'))
    
    worksheet = spreadsheet.worksheet(team)
    team_info = TEAMS[team]
    data_start_row = team_info['data_start_row']
    start_col = team_info['start_col']
    num_members = team_info['count']
    
    start_row = data_start_row + (day - 1) * 3
    end_row = start_row + 2
    
    end_col = start_col + num_members * 6 - 1
    
    range_to_get = f'{gspread.utils.rowcol_to_a1(start_row, start_col)}:{gspread.utils.rowcol_to_a1(end_row, end_col)}'
    
    try:
        data = worksheet.get(range_to_get, value_render_option='UNFORMATTED_VALUE')
    except gspread.exceptions.APIError as e:
        # This can happen if the range is invalid, e.g., for a day that doesn't exist in the sheet
        return jsonify({'error': f'Could not retrieve data from sheet: {e}'}), 500

    attendance_data = {}
    sessions = ['sa', 'sb', 'ma']
    
    for row_idx, session in enumerate(sessions):
        if row_idx < len(data):
            row_data = data[row_idx]
            for member_idx in range(num_members):
                person_key = f"{team}_{member_idx}"
                if person_key not in attendance_data:
                    attendance_data[person_key] = {}

                start_offset = member_idx * 6
                
                for field, col_idx in COL_MAP.items():
                    data_col_idx = start_offset + col_idx
                    if data_col_idx < len(row_data):
                        value = row_data[data_col_idx]
                        if field == 'dk':
                            value = bool(value)
                        attendance_data[person_key][f"{session}_{field}"] = value

    return jsonify(attendance_data)


@app.route('/update_attendance', methods=['POST'])
def update_attendance():
    data = request.json
    team = data['team']
    day = data['day']
    updates = data['updates']
    
    worksheet = spreadsheet.worksheet(team)
    
    team_info = TEAMS[team]
    data_start_row = team_info['data_start_row']
    start_col = team_info['start_col']
    
    session_map = {'sa': 0, 'sb': 1, 'ma': 2}
    
    cells_to_update = []
    for update in updates:
        person_idx = update['person_idx']
        field_full = update['field']
        value = update['value']
        
        parts = field_full.split('_')
        session = parts[0]
        field = parts[1]
        
        if field in COL_MAP and session in session_map:
            row_offset = (day - 1) * 3 + session_map[session]
            row = data_start_row + row_offset
            
            # 6 columns per person
            col_offset = start_col + person_idx * 6
            col = col_offset + COL_MAP[field]
            
            if field == 'dk':
                value = 'TRUE' if value else 'FALSE'
            
            cells_to_update.append({'range': f'{gspread.utils.rowcol_to_a1(row, col)}', 'values': [[value]]})
    
    if cells_to_update:
        worksheet.batch_update(cells_to_update)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
