# DesparateSeva - Attendance Management System

Mobile-friendly attendance management system for tracking devotee attendance across multiple teams and sessions.

## Features
- ⚡ Instant loading with optimized performance
- 📱 Mobile-responsive Excel-like interface
- 🔄 Real-time Google Sheets integration
- 👥 Support for 4 teams: Yudhishthira, Bhima, Arjuna, Nakula
- 📊 Track attendance across 3 sessions (SA, SB, MA)
- 💾 Fast batch save with parallel processing
- 📅 Auto-loads current date

## Quick Start

### Local Setup
```bash
pip install -r requirements.txt
python app.py
```

### Environment Variables
- `GOOGLE_CREDENTIALS`: JSON string of service account credentials
- `SHEET_ID`: Google Sheet ID (optional, defaults to hardcoded)
- `PORT`: Port number (optional, defaults to 5000)

## Deployment

### Render
1. Push to GitHub
2. Create Web Service on Render
3. Set environment variable: `GOOGLE_CREDENTIALS` = content of cred.json
4. Deploy

### Heroku
```bash
heroku create your-app-name
heroku config:set GOOGLE_CREDENTIALS="$(cat cred.json)"
git push heroku main
```

### Railway
1. Connect GitHub repo
2. Add `GOOGLE_CREDENTIALS` environment variable
3. Deploy

## File Structure
```
DesparateSeva/
├── app.py              # Flask application
├── templates/
│   └── index.html      # UI
├── requirements.txt    # Dependencies
├── Procfile           # Deployment config
├── runtime.txt        # Python version
└── .gitignore         # Git ignore
```

## Tech Stack
- Flask
- Google Sheets API (gspread)
- Parallel processing (ThreadPoolExecutor)
- Mobile-first responsive design
