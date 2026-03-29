# 🎤 SmartLift Voice - AI-Powered Voice Controlled Elevator

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Raspberry%20Pi-red.svg)]()

> An intelligent elevator control system that responds to voice commands, designed for accessibility and hands-free operation.

---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Demo](#demo)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [How to Use](#how-to-use)
- [Voice Commands](#voice-commands)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Course Integration](#course-integration)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contact](#contact)

---

## 🎯 About the Project

**SmartLift Voice** is an AI-powered elevator control system that allows users to operate elevators using voice commands. It is specifically designed to help:

| User Group | Challenge Solved |
|------------|------------------|
| 👴 **Elderly with Arthritis** | Cannot press small buttons due to pain |
| 🦯 **Visually Impaired** | Cannot see which button is which |
| ♿ **Wheelchair Users** | Cannot reach higher buttons |
| 👶 **Parents with Infants** | Hands are full, cannot reach buttons |
| 🦠 **Everyone during COVID-19** | Fear of touching contaminated surfaces |
| 🩹 **Temporary Injuries** | Arm injuries make button pressing difficult |

### How It Works

```
User Speaks → Speech Recognition → AI Agent Processes → Voice Feedback → Button Pressed
     ↓              ↓                    ↓                    ↓              ↓
 "Floor 5"    Text: "floor 5"     Extract floor number    "Going to      Relay 
                                  Check permissions       floor 5"       activates
```

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🎤 **Voice Control** | Natural language voice commands | ✅ Working |
| 🔊 **Voice Feedback** | Text-to-speech confirmation | ✅ Working |
| 🌐 **Web Dashboard** | Real-time elevator monitoring | ✅ Working |
| 🔒 **Access Control** | Restricted floor authentication | ✅ Working |
| 🚨 **Emergency Mode** | Instant emergency response | ✅ Working |
| 📊 **Command History** | Logs all commands for analytics | ✅ Working |
| 💻 **Simulation Mode** | Run without hardware (Windows/Mac) | ✅ Working |
| 🥧 **Raspberry Pi Support** | Deploy on actual hardware | ✅ Ready |

---



## 🛠️ Hardware Requirements

### For Development (Simulation Mode - No Hardware Needed)
| Component | Specification |
|-----------|---------------|
| Computer | Windows 10/11, Linux, or macOS |
| Microphone | USB or built-in |
| Speaker | Any audio output |
| RAM | 4GB minimum |
| Storage | 500MB free space |

### For Production (Raspberry Pi - Optional)
| Component | Estimated Cost (₹) |
|-----------|-------------------|
| Raspberry Pi 4/Zero 2W | ₹3,000 - ₹5,000 |
| USB Microphone | ₹500 |
| USB Speaker | ₹500 |
| 8-Channel Relay Module | ₹600 |
| Connecting Wires | ₹100 |
| Power Supply | ₹300 |
| **Total** | **₹5,000 - ₹7,000** |

---

## 💻 Software Requirements

| Software | Version | Purpose | Installation Command |
|----------|---------|---------|---------------------|
| Python | 3.8 - 3.10 | Programming language | [python.org](https://python.org) |
| Flask | 2.0+ | Web dashboard | `pip install flask` |
| SpeechRecognition | 3.8+ | Voice input | `pip install speechrecognition` |
| pyttsx3 | 2.90+ | Text-to-speech | `pip install pyttsx3` |
| NumPy | 1.19+ | Numerical operations | `pip install numpy` |
| scikit-learn | 0.24+ | Machine learning | `pip install scikit-learn` |
| PyAudio | 0.2.11+ | Microphone capture | `pip install pyaudio` |

---

## 📦 Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/anshikasingh2008/smartlift-voice.git
cd smartlift-voice
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# First, install numpy (pre-compiled to avoid compilation issues)
pip install numpy --only-binary :all: --no-cache-dir

# Install remaining packages
pip install flask speechrecognition pyttsx3 scikit-learn joblib

# For PyAudio (microphone support)
pip install pipwin
pipwin install pyaudio
```

### Step 4: Verify Installation

```bash
python -c "import numpy, sklearn, flask, speech_recognition, pyttsx3; print('✅ All packages installed successfully!')"
```

**Expected output:**
```
✅ All packages installed successfully!
```

---

## 🚀 Running the Project

### Quick Start

```bash
python run.py
```

### Command Line Options

| Command | Description |
|---------|-------------|
| `python run.py` | Full system (voice + web) |
| `python run.py --web-only` | Web dashboard only |
| `python run.py --voice-only` | Voice control only |
| `python run.py --test` | Run tests only |
| `python run.py --port 8080` | Run on custom port |

### Expected Output

```
⚠️ RPi.GPIO not available - Running in SIMULATION mode
🚀 SmartLift Agent initialized
   Mode: SIMULATION
   Total Floors: 10

======================================================================
🎤 SmartLift Voice - Listening Mode
======================================================================
Commands: 'Floor 5', 'Open door', 'Emergency', 'Where am I?'
Press Ctrl+C to stop
======================================================================

🌐 Starting web server at http://0.0.0.0:5000
   Dashboard: http://localhost:5000/

🔊 SmartLift: SmartLift Voice activated. Please say your floor.
🎤 Listening...
```

### Open Web Dashboard

Once running, open your browser and go to:
```
http://localhost:5000
```

---

## 🎤 How to Use

### Voice Commands

| Command Type | Examples | Response |
|--------------|----------|----------|
| **Floor Request** | "Floor 5", "Take me to third floor", "Ground floor" | "Going to floor 5" |
| **Door Control** | "Open door", "Close door" | "Opening doors" |
| **Emergency** | "Emergency", "Help", "Stuck" | "Emergency mode activated" |
| **Information** | "Where am I?", "What floor?" | "You are on floor X" |
| **Cancel** | "Cancel", "Stop", "Nevermind" | "Request cancelled" |

### Web Dashboard Usage

1. Open `http://localhost:5000`
2. View current elevator status
3. Type commands in text box or click microphone icon
4. Click quick action buttons for common commands
5. View command history in logs section

### Sample Session

```
User: "Floor 5"
SmartLift: "Going to floor 5"
[System presses floor 5 button]

User: "Open door"
SmartLift: "Opening doors"

User: "Where am I?"
SmartLift: "You are on floor 5"

User: "Cancel"
SmartLift: "Request cancelled"
```

---

## 📁 Project Structure

```
smartlift-voice/
│
├── smartlift/                         # Main package directory
│   ├── __init__.py                    # Package initializer
│   ├── agent.py                       # Main SmartLiftAgent class (PEAS framework)
│   ├── helpers.py                     # Utility functions (extract floor, logging)
│   ├── knowledge_base.py              # Floor mappings, access rules, commands
│   ├── ml_models.py                   # ML classifiers (Naive Bayes)
│   ├── web_interface.py               # Flask web server
│   │
│   └── templates/                     # HTML templates
│       └── dashboard.html             # Web dashboard interface
│
├── venv/                              # Virtual environment (auto-created)
├── run.py                             # Main entry point
├── requirements.txt                   # Package dependencies
├── lift_logs.json                     # Command history (auto-created)
└── README.md                          # Project documentation (this file)
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `agent.py` | Main intelligent agent with perceive-think-act loop |
| `helpers.py` | Text extraction, command classification, logging |
| `knowledge_base.py` | Floor name mappings, access control rules |
| `ml_models.py` | Machine learning for command classification |
| `web_interface.py` | Flask routes and API endpoints |
| `dashboard.html` | Web UI for monitoring and control |
| `run.py` | Entry point with command line arguments |

---

## 🐛 Troubleshooting

### Issue 1: ModuleNotFoundError: No module named 'RPi'

**Error:**
```
ModuleNotFoundError: No module named 'RPi'
```

**Solution:** This is normal on Windows. The system automatically runs in simulation mode. The code includes a conditional import that handles this:

```python
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for Windows
    class MockGPIO:
        # ... mock methods
    GPIO = MockGPIO()
```

### Issue 2: NumPy installation fails with GCC error

**Error:**
```
ERROR: NumPy requires GCC >= 8.4
```

**Solution:** Install pre-compiled wheel:
```bash
pip install numpy --only-binary :all: --no-cache-dir
```

### Issue 3: PyAudio installation fails

**Error:**
```
error: command 'gcc' failed
```

**Solution:** Use pipwin:
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue 4: Microphone not working

**Solution:**

**Windows:**
1. Go to Settings → Privacy → Microphone
2. Turn on "Allow apps to access your microphone"
3. Restart VS Code/Terminal

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue 5: Port 5000 already in use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution:** Use a different port:
```bash
python run.py --port 5001
```

### Issue 6: Speech recognition not accurate

**Solutions:**
- Speak clearly and slowly
- Reduce background noise
- Use a better quality microphone
- Adjust ambient noise in code:
```python
recognizer.adjust_for_ambient_noise(source, duration=1)
```

### Issue 7: Virtual environment not activating

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

---

## 📚 Course Integration (CSA2001)

This project was developed for **CSA2001 - Fundamentals in AI and ML** at VIT.

| Course Outcome | How Implemented |
|----------------|-----------------|
| **CO1** - Explain capabilities, strengths and limitations of AI/ML techniques | PEAS framework analysis, agent architecture documentation |
| **CO2** - Explain AI and ML algorithms and applications | Search strategies (A* for emergency), rule-based systems |
| **CO3** - Describe learning models and algorithms | Bayesian confidence scoring, ML classification |
| **CO4** - Analyze and design problems using AI techniques | Complete system architecture, knowledge base design |
| **CO5** - Apply AI/ML algorithms to solve real-world problems | Working elevator control system with voice interface |
| **CO6** - Understand Prolog Programming | Prolog-style rule-based reasoning in knowledge_base.py |

### Topics Covered

| Topic | Implementation |
|-------|----------------|
| Intelligent Agents | SmartLiftAgent class with PEAS framework |
| Search Strategies | A* for emergency response planning |
| Knowledge Representation | Floor mappings, rule-based system |
| Propositional & Predicate Logic | IF-THEN rules for command processing |
| Probability Theory | Bayesian confidence scoring |
| Machine Learning | Naive Bayes command classification |
| NLP Applications | Speech recognition, intent classification |
| Reinforcement Learning | Feedback-based learning (planned) |

---

## 🔮 Future Enhancements

| Enhancement | Description | Priority |
|-------------|-------------|----------|
| **Multi-language Support** | Add Hindi, Tamil, Telugu | High |
| **Voice Authentication** | Secure restricted floors | High |
| **User Profiles** | Personalized floor preferences | Medium |
| **Usage Analytics** | Track peak usage times | Medium |
| **Facial Recognition** | Automatic user identification | Low |
| **Mobile App** | Remote elevator calling | Low |
| **IoT Integration** | Smart building integration | Low |
| **Emergency Detection** | Detect medical emergencies via voice | Medium |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 [anshikasingh2008]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

## 👥 Contact

**Project Developer:** Anshika Singh
**Course:** CSA2001 - Fundamentals in AI and ML
**Institution:** Vellore Institute of Technology (VIT)
**GitHub:** [https://github.com/anshikasingh2008/smartlift-voice](https://github.com/anshikasingh2008/smartlift-voice)
**Email:** your.email@example.com

---

## 🙏 Acknowledgments

- **Google Speech API** - For voice recognition capabilities
- **Flask** - Lightweight web framework
- **scikit-learn** - Machine learning algorithms
- **Open Source Community** - For amazing libraries and tools

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

## 📊 Project Status

| Aspect | Status |
|--------|--------|
| Development | ✅ Complete |
| Testing | ✅ Passed |
| Documentation | ✅ Complete |
| Deployment | ✅ Ready |

---

## 🚀 Quick Start (Copy-Paste for New Users)

```bash
# Clone the repository
git clone https://github.com/anshikasingh2008/smartlift-voice.git
cd smartlift-voice

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install numpy --only-binary :all: --no-cache-dir
pip install -r requirements.txt

# Run the application
python run.py

# Open browser to http://localhost:5000
```

---

## 📸 Screenshots

*(Add your actual screenshots here)*

### Project Structure in VS Code
![Project Structure](screenshots/project_structure.png)

### Web Dashboard
![Dashboard](screenshots/dashboard.png)

### Voice Command Processing
![Voice Command](screenshots/voice_command.png)

### Command History
![Command History](screenshots/logs.png)

### Installation Success
![Installation](screenshots/installation.png)

### System Running
![System Running](screenshots/system_running.png)

---

## 🎯 Final Notes

SmartLift Voice demonstrates how Artificial Intelligence and Machine Learning can solve real-world accessibility problems. The system is:

- ✅ **Inclusive** - Works for all users regardless of physical ability
- ✅ **Practical** - Can be deployed in existing buildings
- ✅ **Cost-effective** - Uses affordable hardware
- ✅ **Educational** - Implements core AI/ML concepts
- ✅ **Extensible** - Easy to add new features

---

**Made with ❤️ for CSA2001 - Fundamentals in AI and Machine Learning**

**Vellore Institute of Technology (VIT)**

---

*"Technology is best when it brings people together and removes barriers."*
```
