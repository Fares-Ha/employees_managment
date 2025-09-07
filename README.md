# HR Management Dashboard

This is a modern, cross-platform desktop application for managing HR data, built with Python and PyQt6.

## Features

*   **Employee Management**: Add, edit, and delete employee records.
*   **Search & Filtering**: Powerful search and filtering capabilities for the employee list.
*   **Dashboard**: A high-level overview of key HR metrics with charts and KPIs.
*   **Analytics**: Detailed analytics page with charts for deeper insights.
*   **Customization**: Change the application theme (light/dark) and logo from the settings page.
*   **Modern UI**: A clean, modern user interface with smooth animations.

## Setup & Running

### 1. Install Dependencies

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

To run the application from source, execute the `main.py` file:

```bash
python hr-dashboard/src/main.py
```

## Building an Executable

You can build a standalone executable using [PyInstaller](https://pyinstaller.org/).

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the Executable

Run the following command from the root of the project:

```bash
pyinstaller --name "HRDashboard" --windowed --onefile hr-dashboard/src/main.py
```

**Note:**
*   `--name`: Sets the name of the executable.
*   `--windowed`: Prevents a console window from appearing when the application is run.
*   `--onefile`: Packages everything into a single executable file.
*   You can add an `--icon` argument to provide a custom icon for your application.

The executable will be created in the `dist` directory.