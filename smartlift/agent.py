# smartlift/agent.py

import speech_recognition as sr
import pyttsx3
import json
import re
import time
from collections import deque

# ============================================================
# CONDITIONAL IMPORT FOR RPi.GPIO (Fixes Windows Error)
# ============================================================

RPI_AVAILABLE = False

try:
    import RPi.GPIO as GPIO  # type: ignore
    RPI_AVAILABLE = True
    print("✅ Raspberry Pi GPIO available - Hardware mode enabled")
except (ImportError, ModuleNotFoundError, RuntimeError):
    # Mock GPIO class for Windows development
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        IN = "IN"
        HIGH = 1
        LOW = 0
        
        def setmode(self, mode):
            print(f"[SIMULATION] GPIO setmode({mode})")
        
        def setup(self, pin, mode):
            print(f"[SIMULATION] GPIO setup(pin={pin}, mode={mode})")
        
        def output(self, pin, value):
            print(f"[SIMULATION] GPIO output(pin={pin}, value={value})")
        
        def cleanup(self):
            print("[SIMULATION] GPIO cleanup")
    
    GPIO = MockGPIO()
    print("⚠️ RPi.GPIO not available - Running in SIMULATION mode")


class SmartLiftAgent:
    """
    Intelligent agent that controls elevator via voice commands.
    Implements goal-based agent architecture with PEAS framework.
    """
    
    def __init__(self):
        # PEAS Framework Implementation
        self.peas = {
            "performance": {
                "accuracy": 0,
                "response_time": 0,
                "user_satisfaction": 0,
                "error_rate": 0
            },
            "environment": {
                "type": "elevator_car",
                "observable": "fully",
                "deterministic": True,
                "episodic": True,
                "dynamic": False,
                "discrete": True
            },
            "actuators": [
                "floor_button_relay",
                "door_control_relay", 
                "voice_speaker",
                "emergency_alert"
            ],
            "sensors": [
                "microphone",
                "floor_position_sensor",
                "door_status_sensor"
            ]
        }
        
        # Agent state
        self.current_floor = 1
        self.destination_floors = deque()
        self.is_moving = False
        self.doors_open = False
        self.simulation_mode = not RPI_AVAILABLE
        
        # Floor configuration
        self.total_floors = 10
        self.floor_names = {
            1: ["ground", "lobby", "main", "first"],
            2: ["second", "floor two", "2nd"],
            3: ["third", "floor three", "3rd"],
            4: ["fourth", "floor four", "4th"],
            5: ["fifth", "floor five", "5th"],
            6: ["sixth", "floor six", "6th"],
            7: ["seventh", "floor seven", "7th"],
            8: ["eighth", "floor eight", "8th"],
            9: ["ninth", "floor nine", "9th"],
            10: ["tenth", "top", "10th"]
        }
        
        # Create reverse mapping for quick lookup
        self.text_to_floor = {}
        for floor, names in self.floor_names.items():
            for name in names:
                self.text_to_floor[name] = floor
        
        # Special commands
        self.special_commands = {
            "emergency": {
                "keywords": ["emergency", "help", "stuck", "fire", "medical"],
                "action": self.emergency_response
            },
            "door": {
                "open": ["open door", "keep open", "door open"],
                "close": ["close door", "shut door", "door close"]
            },
            "cancel": {
                "keywords": ["cancel", "stop", "wait", "nevermind"],
                "action": self.cancel_request
            },
            "info": {
                "keywords": ["where am i", "current floor", "what floor"],
                "action": self.announce_floor
            }
        }
        
        # Relay pins configuration
        self.relay_pins = {
            1: 17, 2: 18, 3: 27, 4: 22, 5: 23,
            6: 24, 7: 25, 8: 5, 9: 6, 10: 13
        }
        
        # Initialize hardware (if available)
        self.setup_hardware()
        
        # Initialize voice
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('rate', 150)
        self.speaker.setProperty('volume', 0.9)
        
        # Knowledge base
        self.access_rules = self.load_access_rules()
        
        # Performance tracking
        self.command_history = []
        
        print(f"🚀 SmartLift Agent initialized")
        print(f"   Mode: {'SIMULATION' if self.simulation_mode else 'HARDWARE'}")
        print(f"   Total Floors: {self.total_floors}")
        print("=" * 50)
        
    def setup_hardware(self):
        """Setup GPIO pins for relay control"""
        if self.simulation_mode:
            print("⚠️ Hardware disabled - Running in simulation mode")
            return
        
        try:
            GPIO.setmode(GPIO.BCM)
            for pin in self.relay_pins.values():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            print("✅ GPIO pins configured")
        except Exception as e:
            print(f"⚠️ GPIO setup failed: {e}")
            print("   Switching to simulation mode")
            self.simulation_mode = True
        
    def press_floor_button(self, floor):
        """
        Actuator: Presses the physical floor button
        """
        if self.simulation_mode:
            print(f"[SIMULATION] Pressing floor {floor} button")
            time.sleep(0.2)
            print(f"[SIMULATION] Floor {floor} button released")
            return True
        
        if floor not in self.relay_pins:
            return False
        
        try:
            pin = self.relay_pins[floor]
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(pin, GPIO.LOW)
            return True
        except Exception as e:
            print(f"Error pressing floor {floor}: {e}")
            return False
    
    def perceive(self, voice_input=None):
        """
        Sensor: Listen for voice commands
        Returns: Parsed command
        """
        if voice_input is None:
            try:
                with sr.Microphone() as source:
                    print("🎤 Listening...", end="\r")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language="en-IN")
                    print(f"📝 Heard: {text}                    ")
                    
            except sr.WaitTimeoutError:
                return {"type": "none", "message": "No command heard"}
            except sr.UnknownValueError:
                return {"type": "error", "message": "Could not understand"}
            except sr.RequestError:
                return {"type": "error", "message": "Speech recognition service error"}
            except Exception as e:
                return {"type": "error", "message": f"Error: {e}"}
        else:
            text = voice_input
        
        return self.process_command(text)
    
    def process_command(self, text):
        """
        Think: Process the voice command
        Returns: Structured command
        """
        text_lower = text.lower()
        
        # Check for emergency commands
        for cmd_name, cmd_info in self.special_commands.items():
            if cmd_name == "emergency":
                if any(kw in text_lower for kw in cmd_info["keywords"]):
                    return {
                        "type": "emergency",
                        "action": "emergency_response",
                        "original": text
                    }
            elif cmd_name == "door":
                if any(kw in text_lower for kw in cmd_info["open"]):
                    return {
                        "type": "door",
                        "action": "open",
                        "original": text
                    }
                elif any(kw in text_lower for kw in cmd_info["close"]):
                    return {
                        "type": "door",
                        "action": "close",
                        "original": text
                    }
            elif cmd_name == "cancel":
                if any(kw in text_lower for kw in cmd_info["keywords"]):
                    return {
                        "type": "cancel",
                        "action": "cancel_request",
                        "original": text
                    }
            elif cmd_name == "info":
                if any(kw in text_lower for kw in cmd_info["keywords"]):
                    return {
                        "type": "info",
                        "action": "announce_floor",
                        "original": text
                    }
        
        # Extract floor number
        floor = self.extract_floor(text_lower)
        
        if floor is not None:
            if self.check_access(floor):
                return {
                    "type": "floor_request",
                    "floor": floor,
                    "action": "go_to_floor",
                    "original": text
                }
            else:
                return {
                    "type": "access_denied",
                    "floor": floor,
                    "message": "Access denied for this floor",
                    "original": text
                }
        
        # Check for floor names
        for floor_num, names in self.floor_names.items():
            if any(name in text_lower for name in names):
                if self.check_access(floor_num):
                    return {
                        "type": "floor_request",
                        "floor": floor_num,
                        "action": "go_to_floor",
                        "original": text
                    }
        
        return {
            "type": "unknown",
            "message": "I didn't understand. Please say your floor number.",
            "original": text
        }
    
    def extract_floor(self, text):
        """
        Extract floor number using regex and text mapping
        """
        # First check text-to-floor mapping
        for spoken, floor in self.text_to_floor.items():
            if spoken in text:
                return floor
        
        # Then try regex patterns
        patterns = [
            r'(\d+)(?:st|nd|rd|th)?\s*(?:floor)?',
            r'floor\s*(\d+)',
            r'go to\s*(\d+)',
            r'take me to\s*(\d+)',
            r'(\d+)\s*(?:floor)?$',
            r'^(\d+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    floor = int(match.group(1))
                    if 1 <= floor <= self.total_floors:
                        return floor
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def check_access(self, floor):
        """
        Check if user has access to restricted floors
        """
        if floor not in self.access_rules.get("restricted_floors", []):
            return True
        return self.authenticate(floor)
    
    def authenticate(self, floor):
        """
        Simple voice authentication for restricted floors
        """
        self.speak(f"Floor {floor} is restricted. Please say your access code.")
        
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
                pin = self.recognizer.recognize_google(audio)
                
                if pin in self.access_rules.get("floor_pins", {}).get(floor, []):
                    self.speak("Access granted.")
                    return True
                else:
                    self.speak("Access denied. Invalid code.")
                    return False
        except:
            self.speak("I couldn't hear your code. Please try again.")
            return False
    
    def act(self, command):
        """
        Act: Execute the command
        """
        if command["type"] == "floor_request":
            floor = command["floor"]
            self.speak(f"Going to floor {floor}")
            success = self.press_floor_button(floor)
            
            if success:
                self.log_request(floor)
                return {
                    "status": "success",
                    "message": f"Floor {floor} selected",
                    "floor": floor
                }
            else:
                return {
                    "status": "error",
                    "message": f"Could not select floor {floor}"
                }
        
        elif command["type"] == "emergency":
            return self.emergency_response(command)
        
        elif command["type"] == "door" and command["action"] == "open":
            self.speak("Opening doors")
            return {"status": "success", "message": "Door open requested"}
        
        elif command["type"] == "door" and command["action"] == "close":
            self.speak("Closing doors")
            return {"status": "success", "message": "Door close requested"}
        
        elif command["type"] == "cancel":
            return self.cancel_request(command)
        
        elif command["type"] == "info":
            return self.announce_floor(command)
        
        else:
            self.speak("I didn't understand. Please try again.")
            return {"status": "error", "message": command.get("message", "Unknown command")}
    
    def speak(self, text):
        """
        Text-to-speech output
        """
        print(f"🔊 SmartLift: {text}")
        try:
            self.speaker.say(text)
            self.speaker.runAndWait()
        except Exception as e:
            print(f"⚠️ Text-to-speech error: {e}")
    
    def emergency_response(self, command):
        """
        Handle emergency situations
        """
        self.speak("Emergency mode activated. Stopping at next floor.")
        self.alert_security()
        
        return {
            "status": "emergency",
            "message": "Emergency mode activated",
            "action": "alerted_security"
        }
    
    def cancel_request(self, command):
        """
        Cancel current floor request
        """
        if self.destination_floors:
            cancelled = self.destination_floors.pop()
            self.speak(f"Cancelling floor {cancelled}")
        
        return {
            "status": "success",
            "message": "Request cancelled"
        }
    
    def announce_floor(self, command):
        """
        Announce current floor
        """
        self.speak(f"You are on floor {self.current_floor}")
        
        return {
            "status": "success",
            "message": f"Current floor: {self.current_floor}",
            "floor": self.current_floor
        }
    
    def alert_security(self):
        """
        Alert building security (simulated)
        """
        print("[ALERT] Security has been notified")
        # In production, this would send an actual alert
    
    def load_access_rules(self):
        """
        Load access control rules
        """
        return {
            "restricted_floors": [],  # Add restricted floors here
            "floor_pins": {},         # Floor PIN codes
            "time_restrictions": {}   # Time-based restrictions
        }
    
    def log_request(self, floor):
        """
        Log requests for analytics
        """
        import datetime
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": "floor_request",
            "floor": floor,
            "current_floor": self.current_floor
        }
        
        try:
            with open("lift_logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Warning: Could not write log: {e}")
    
    def update_metrics(self, result):
        """
        Update agent performance metrics
        """
        if result["status"] == "success":
            self.peas["performance"]["accuracy"] += 1
        else:
            self.peas["performance"]["error_rate"] += 1
        
        self.peas["performance"]["response_time"] = 0  # Reset for next
    
    def run(self):
        """
        Main agent loop
        """
        print("\n" + "=" * 60)
        print("🎤 SmartLift Voice - Listening Mode")
        print("=" * 60)
        print("Commands: 'Floor 5', 'Open door', 'Emergency', 'Where am I?'")
        print("Press Ctrl+C to stop")
        print("=" * 60 + "\n")
        
        self.speak("SmartLift Voice activated. Please say your floor.")
        
        while True:
            try:
                command = self.perceive()
                
                if command["type"] != "none" and command["type"] != "error":
                    result = self.act(command)
                    self.update_metrics(result)
                    self.command_history.append(result)
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Shutting down SmartLift Voice...")
                self.speak("Shutting down")
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                self.speak("System error. Please use buttons.")
                time.sleep(2)
    
    def cleanup(self):
        """
        Cleanup resources
        """
        if not self.simulation_mode and RPI_AVAILABLE:
            GPIO.cleanup()
        print("✅ Cleanup complete")


# Run the agent
if __name__ == "__main__":
    lift = SmartLiftAgent()
    try:
        lift.run()
    finally:
        lift.cleanup()