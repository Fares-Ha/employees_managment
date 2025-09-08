# HR Dashboard

A modern, cross-platform employee management desktop application built with PyQt6 and SQLite.

## Features
- Modern dashboard UI (inspired by ProtonVPN, Telegram Desktop, Slack)
- Sidebar navigation: Dashboard, Employees, Analytics, Settings
- Employee CRUD (with images for Emirates ID & Passport)
- Search, filter, and sortable employee table
- Analytics with charts and KPIs
- Theme switch (light/dark), customizable logo
- User preferences saved (JSON or DB)
- Responsive, animated, and production-ready

## Project Structure
```
hr-dashboard/
    src/
        core/           # Database, theme, settings, migrations
        services/       # Business logic (CRUD, analytics, etc.)
        ui/             # UI components (pages, dialogs, sidebar, navbar)
        widgets/        # Custom widgets (charts, tables, etc.)
        assets/         # Images, icons, themes
        main.py         # App entry point
    requirements.txt
    README.md
```

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python src/main.py
   ```
3. Build executable (Windows):
   ```
   pyinstaller --onefile --windowed src/main.py
   ```

## License
MIT
