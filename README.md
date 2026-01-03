# Space Defense Game with Hand Tracking 🚀

A Python-based arcade game controlled entirely by hand gestures using MediaPipe and OpenCV.

## ⚠️ Important: Python Version
**Required Python Version:** Python 3.10.x  
This project is optimized for **Python 3.10**. Newer versions (like 3.12 or 3.13) will cause errors with MediaPipe.

👉 **[Download Python 3.10.11 Here (Direct Installer)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)**

> **Installation Note:** When installing Python, make sure to check the box **"Add Python to PATH"** at the bottom of the installer window.

## 🎮 Controls
* **Move:** Point your **Index Finger** to move the spaceship.
* **Shoot:** **Pinch** (bring index finger and thumb together).
* **Restart:** Press **'r'**.
* **Quit:** Press **'q'**.

## 🚀 How to Run (Easy Way)
1. Clone or download this repository.
2. Double-click on **`start.bat`**.
   *(It will automatically set up the virtual environment, install dependencies, and launch the game.)*

## 🛠️ How to Run (Manual Way)
If you prefer running it manually via terminal:

1. Create a virtual environment (Python 3.10):
   ```bash
   python -m venv venv
2. Activate the environment:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the game:
   python spaceDefanse.py