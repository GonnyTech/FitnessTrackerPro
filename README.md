# FitnessTrackerPro

FitnessTrackerPro is a desktop application for Windows that allows you to track, analyze, and manage your workouts, including running, swimming, and cycling. It provides a modern, dark-themed user interface to view your progress, see detailed charts, and get personalized advice.

![App Screenshot](https://i.imgur.com/your-screenshot.png) <!-- Replace with a real screenshot URL -->

## Features

- **Multi-Sport Tracking**: Log workouts for running, swimming, and cycling.
- **Detailed Metrics**:
  - **Running**: Distance, Pace, Elevation Gain.
  - **Swimming**: Laps, Style, Average/Max Pace, Average/Max Stroke Rate.
  - **Cycling**: Distance, Average/Max Speed, Elevation Gain.
- **Workout History**: View, edit, or delete past workouts in a clean, organized table.
- **Data Visualization**: See detailed graphs comparing your performance over time.
- **Personalized Advice**: Get simple, actionable tips based on your performance.
- **Modern UI**: A sleek, dark-themed interface with intuitive controls.

---

## Installation (For Users)

To install FitnessTrackerPro on your computer, follow these simple steps:

1.  **Download the Release**:
    Go to the [Releases page](httpss://github.com/your-username/your-repo/releases) on GitHub and download the `release.zip` file from the latest version.

2.  **Extract the Files**:
    Unzip the downloaded `release.zip` file to a folder on your computer.

3.  **Run the Installer**:
    Inside the extracted folder, you will find an `install.bat` script. Double-click it to start the installation.

    > **Note**: Windows Defender or your antivirus might show a warning because the script is not signed. This is normal. Click "More info" and then "Run anyway" to proceed.

4.  **Done!**
    The installer will copy the application to `C:\Program Files\FitnessTrackerPro` and create a shortcut on your Desktop. You can now launch the app from your Desktop.

---

## For Developers

If you want to run the application from the source code or contribute to the project, follow these instructions.

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the app from the source code, execute:
```bash
python main.py
```

### Building the Executable

To build the executable and create the installation package, run the `build.bat` script:
```bash
build.bat
```
This will generate a `release` folder containing the `FitnessTrackerPro.exe` and the `install.bat` script.

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request. 