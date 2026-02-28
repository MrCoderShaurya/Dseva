# DesparateSeva - Attendance Management System

Mobile-friendly attendance management system for tracking devotee attendance across multiple teams and sessions.

## Features
- Mobile-optimized UI with card-based layout
- Real-time Google Sheets integration
- Support for multiple teams (Yudhishthira, Bhima, Arjuna, Nakula)
- Track attendance across 3 sessions (SA, SB, MA)
- Search and filter devotees
- Batch save functionality

## Deployment Instructions

### Prerequisites
- Python 3.8+
- Google Sheets API credentials (cred.json)

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your `cred.json` file (Google Service Account credentials)

3. Run the app:
   ```bash
   python app.py
   ```

### Deploy to Render
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Add environment variable: Upload `cred.json` content
5. Deploy!

### Deploy to Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add credentials: `heroku config:set GOOGLE_CREDENTIALS="$(cat cred.json)"`
5. Deploy: `git push heroku main`

### Deploy to Railway
1. Push code to GitHub
2. Create new project on Railway
3. Connect repository
4. Add `cred.json` as a file in the dashboard
5. Deploy automatically

## File Structure
```
DesparateSeva/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Mobile-optimized UI
├── cred.json           # Google API credentials (not in git)
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
└── .gitignore         # Git ignore rules
```

## Important Notes
- Keep `cred.json` secure and never commit it to version control
- Update the `sheet_id` in app.py with your Google Sheet ID
- The app is configured for production deployment (debug=False)
