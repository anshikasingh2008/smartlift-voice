# smartlift/helpers.py
"""
Helper Functions for SmartLift Voice
====================================
Utility functions for:
- Text processing and command extraction
- Logging and file operations
- Validation and formatting
- System utilities
"""

import re
import json
import logging
import os
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# TEXT PROCESSING FUNCTIONS
# ============================================================

def extract_floor_number(text: str) -> Optional[int]:
    """
    Extract floor number from user input text.
    
    Args:
        text (str): User input text
        
    Returns:
        int: Floor number (1-10) or None if not found
        
    Examples:
        >>> extract_floor_number("take me to floor 5")
        5
        >>> extract_floor_number("ground floor")
        1
        >>> extract_floor_number("top floor")
        10
    """
    if not text:
        return None
    
    text_lower = text.lower().strip()
    
    # Pattern 1: Floor number with ordinal or explicit "floor"
    patterns = [
        r'(\d+)(?:st|nd|rd|th)?\s*(?:floor)?',  # "5th floor", "5"
        r'floor\s*(\d+)',                         # "floor 5"
        r'go to\s*(\d+)',                        # "go to 5"
        r'take me to\s*(\d+)',                   # "take me to 5"
        r'(\d+)\s*(?:floor)?$',                  # "5" at end
        r'^(\d+)$',                              # Just "5"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                floor = int(match.group(1))
                if 1 <= floor <= 10:
                    return floor
            except (ValueError, IndexError):
                continue
    
    # Pattern 2: Word-based floor names
    floor_words = {
        'ground': 1,
        'lobby': 1,
        'first': 1,
        'second': 2,
        'third': 3,
        'fourth': 4,
        'fifth': 5,
        'sixth': 6,
        'seventh': 7,
        'eighth': 8,
        'ninth': 9,
        'tenth': 10,
        'top': 10,
        'penthouse': 10
    }
    
    for word, floor in floor_words.items():
        if word in text_lower:
            return floor
    
    return None


def sanitize_input(text: str) -> str:
    """
    Clean and normalize user input text.
    
    Args:
        text (str): Raw user input
        
    Returns:
        str: Cleaned text
        
    Examples:
        >>> sanitize_input("  HELLO!  ")
        "hello"
        >>> sanitize_input("Take me to Floor 5!!!")
        "take me to floor 5"
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters (keep letters, numbers, spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text.strip()


def validate_floor(floor: int, total_floors: int = 10) -> bool:
    """
    Validate if floor number is within valid range.
    
    Args:
        floor (int): Floor number to validate
        total_floors (int): Maximum floor number
        
    Returns:
        bool: True if valid, False otherwise
    """
    if floor is None:
        return False
    return 1 <= floor <= total_floors


# ============================================================
# COMMAND CLASSIFICATION FUNCTIONS
# ============================================================

def is_emergency(text: str) -> bool:
    """
    Check if text contains emergency keywords.
    
    Args:
        text (str): User input text
        
    Returns:
        bool: True if emergency detected
        
    Examples:
        >>> is_emergency("HELP! I'm stuck!")
        True
        >>> is_emergency("floor 5")
        False
    """
    if not text:
        return False
    
    emergency_keywords = [
        'emergency', 'help', 'stuck', 'fire', 'medical',
        'accident', 'danger', 'save', 'urgent', '911',
        'trapped', 'assistance', 'problem', 'issue'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in emergency_keywords)


def is_door_command(text: str) -> Optional[str]:
    """
    Check if text is about door control.
    
    Args:
        text (str): User input text
        
    Returns:
        str: 'open', 'close', or None
        
    Examples:
        >>> is_door_command("open the door")
        'open'
        >>> is_door_command("close door please")
        'close'
        >>> is_door_command("floor 5")
        None
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    open_keywords = ['open', 'open door', 'open the door', 'keep open']
    close_keywords = ['close', 'shut', 'close door', 'shut door', 'close the door']
    
    if any(keyword in text_lower for keyword in open_keywords):
        return 'open'
    elif any(keyword in text_lower for keyword in close_keywords):
        return 'close'
    
    return None


def is_cancel_command(text: str) -> bool:
    """
    Check if text is a cancel/stop command.
    
    Args:
        text (str): User input text
        
    Returns:
        bool: True if cancel command
        
    Examples:
        >>> is_cancel_command("cancel that")
        True
        >>> is_cancel_command("nevermind")
        True
    """
    if not text:
        return False
    
    cancel_keywords = [
        'cancel', 'stop', 'nevermind', 'forget', 'ignore',
        'dont', 'don\'t', 'wait', 'hold', 'pause'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in cancel_keywords)


def is_info_command(text: str) -> bool:
    """
    Check if user is asking for information (current floor, status).
    
    Args:
        text (str): User input text
        
    Returns:
        bool: True if asking for info
        
    Examples:
        >>> is_info_command("where am I")
        True
        >>> is_info_command("what floor is this")
        True
    """
    if not text:
        return False
    
    info_keywords = [
        'where', 'what floor', 'current floor', 'which floor',
        'am i on', 'floor number', 'my floor', 'location'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in info_keywords)


def classify_command_type(text: str) -> Dict[str, Any]:
    """
    Classify the type of command from user input.
    
    Args:
        text (str): User input text
        
    Returns:
        dict: Classification result with type and details
        
    Examples:
        >>> classify_command_type("go to floor 5")
        {'type': 'floor_request', 'floor': 5, 'confidence': 0.95}
    """
    result = {
        'type': 'unknown',
        'original': text,
        'confidence': 0.0
    }
    
    if not text:
        return result
    
    sanitized = sanitize_input(text)
    
    # Check command types in priority order
    if is_emergency(sanitized):
        result['type'] = 'emergency'
        result['confidence'] = 0.98
        return result
    
    if is_cancel_command(sanitized):
        result['type'] = 'cancel'
        result['confidence'] = 0.95
        return result
    
    door_action = is_door_command(sanitized)
    if door_action:
        result['type'] = 'door'
        result['action'] = door_action
        result['confidence'] = 0.95
        return result
    
    if is_info_command(sanitized):
        result['type'] = 'info'
        result['confidence'] = 0.90
        return result
    
    floor = extract_floor_number(sanitized)
    if floor:
        result['type'] = 'floor_request'
        result['floor'] = floor
        result['confidence'] = 0.95
        return result
    
    return result


# ============================================================
# LOGGING FUNCTIONS
# ============================================================

def log_event(event_type: str, details: Dict[str, Any], log_file: str = "lift_logs.json") -> bool:
    """
    Log an event to the JSON log file.
    
    Args:
        event_type (str): Type of event (e.g., 'floor_request', 'emergency')
        details (dict): Event details
        log_file (str): Path to log file
        
    Returns:
        bool: True if successful, False otherwise
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        logger.info(f"Logged event: {event_type}")
        return True
    except Exception as e:
        logger.error(f"Failed to log event: {e}")
        return False


def get_recent_logs(log_file: str = "lift_logs.json", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get recent logs from the log file.
    
    Args:
        log_file (str): Path to log file
        limit (int): Maximum number of logs to return
        
    Returns:
        list: List of log entries
    """
    logs = []
    
    if not os.path.exists(log_file):
        return logs
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return logs[-limit:] if logs else []
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        return []


def clear_logs(log_file: str = "lift_logs.json") -> bool:
    """
    Clear all logs from the log file.
    
    Args:
        log_file (str): Path to log file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if os.path.exists(log_file):
            os.remove(log_file)
        logger.info("Logs cleared")
        return True
    except Exception as e:
        logger.error(f"Failed to clear logs: {e}")
        return False


# ============================================================
# FORMATTING FUNCTIONS
# ============================================================

def format_response(message: str, status: str = "success", data: Dict = None) -> Dict[str, Any]:
    """
    Format a standardized response dictionary.
    
    Args:
        message (str): Response message
        status (str): 'success' or 'error'
        data (dict): Additional data to include
        
    Returns:
        dict: Formatted response
        
    Examples:
        >>> format_response("Floor 5 selected")
        {'status': 'success', 'message': 'Floor 5 selected', 'timestamp': '...'}
    """
    response = {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if data:
        response["data"] = data
    
    return response


def calculate_confidence(match_count: int, total_possible: int) -> float:
    """
    Calculate confidence percentage based on matches.
    
    Args:
        match_count (int): Number of matches
        total_possible (int): Maximum possible matches
        
    Returns:
        float: Confidence score between 0 and 1
    """
    if total_possible <= 0:
        return 0.0
    return min(1.0, match_count / total_possible)


def get_floor_name(floor: int, floor_names: Dict[int, List[str]] = None) -> str:
    """
    Get friendly name for a floor number.
    
    Args:
        floor (int): Floor number
        floor_names (dict): Optional custom floor names mapping
        
    Returns:
        str: Floor name
        
    Examples:
        >>> get_floor_name(1)
        "Ground Floor"
        >>> get_floor_name(10)
        "Top Floor"
    """
    default_names = {
        1: "Ground Floor",
        2: "Second Floor",
        3: "Third Floor",
        4: "Fourth Floor",
        5: "Fifth Floor",
        6: "Sixth Floor",
        7: "Seventh Floor",
        8: "Eighth Floor",
        9: "Ninth Floor",
        10: "Top Floor"
    }
    
    names = floor_names or default_names
    
    if floor in names:
        if isinstance(names[floor], list):
            return names[floor][0]
        return names[floor]
    
    return f"Floor {floor}"


# ============================================================
# SYSTEM UTILITIES
# ============================================================

def check_system_requirements() -> Dict[str, bool]:
    """
    Check if all required packages are installed.
    
    Returns:
        dict: Package status dictionary
    """
    requirements = {
        "flask": False,
        "speech_recognition": False,
        "pyttsx3": False,
        "numpy": False,
        "sklearn": False,
        "joblib": False,
        "pyaudio": False
    }
    
    for package in requirements.keys():
        try:
            import_name = package.replace("-", "_")
            __import__(import_name)
            requirements[package] = True
        except ImportError:
            pass
    
    return requirements


def print_system_info() -> None:
    """
    Print system information for debugging.
    """
    print("\n" + "=" * 50)
    print("🔧 SYSTEM INFORMATION")
    print("=" * 50)
    
    # Python version
    import sys
    print(f"Python Version: {sys.version}")
    
    # Package status
    print("\n📦 Package Status:")
    packages = check_system_requirements()
    for package, installed in packages.items():
        status = "✅" if installed else "❌"
        print(f"   {status} {package}")
    
    # Current directory
    print(f"\n📁 Current Directory: {os.getcwd()}")
    
    # Log file status
    if os.path.exists("lift_logs.json"):
        size = os.path.getsize("lift_logs.json")
        print(f"📄 Log File: lift_logs.json ({size} bytes)")
    else:
        print(f"📄 Log File: Not created yet")
    
    print("=" * 50 + "\n")


# ============================================================
# SIMULATION FUNCTIONS (for testing without hardware)
# ============================================================

def simulate_button_press(floor: int, delay: float = 0.2) -> bool:
    """
    Simulate pressing a floor button (for testing without hardware).
    
    Args:
        floor (int): Floor number
        delay (float): Simulated press duration in seconds
        
    Returns:
        bool: Always True for simulation
    """
    import time
    print(f"[SIMULATION] 🔘 Pressing floor {floor} button")
    time.sleep(delay)
    print(f"[SIMULATION] ✅ Floor {floor} button released")
    return True


def simulate_door_open(delay: float = 1.0) -> bool:
    """
    Simulate opening doors (for testing without hardware).
    
    Args:
        delay (float): Simulated door open duration
        
    Returns:
        bool: Always True for simulation
    """
    import time
    print(f"[SIMULATION] 🚪 Opening doors...")
    time.sleep(delay)
    print(f"[SIMULATION] ✅ Doors open")
    return True


def simulate_door_close(delay: float = 1.0) -> bool:
    """
    Simulate closing doors (for testing without hardware).
    
    Args:
        delay (float): Simulated door close duration
        
    Returns:
        bool: Always True for simulation
    """
    import time
    print(f"[SIMULATION] 🚪 Closing doors...")
    time.sleep(delay)
    print(f"[SIMULATION] ✅ Doors closed")
    return True


# ============================================================
# TEST FUNCTIONS
# ============================================================

def test_helpers():
    """
    Run tests for all helper functions.
    """
    print("\n" + "=" * 60)
    print("🧪 TESTING HELPER FUNCTIONS")
    print("=" * 60)
    
    # Test extract_floor_number
    print("\n📌 Testing extract_floor_number():")
    test_cases = [
        ("floor 5", 5),
        ("take me to 3rd floor", 3),
        ("ground floor", 1),
        ("top floor", 10),
        ("lobby", 1),
        ("just 7", 7),
        ("hello", None),
    ]
    
    for text, expected in test_cases:
        result = extract_floor_number(text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{text}' → {result} (expected: {expected})")
    
    # Test command classification
    print("\n📌 Testing classify_command_type():")
    test_commands = [
        ("emergency help", "emergency"),
        ("cancel that", "cancel"),
        ("open door", "door"),
        ("close door", "door"),
        ("where am I", "info"),
        ("floor 5", "floor_request"),
        ("hello world", "unknown"),
    ]
    
    for text, expected_type in test_commands:
        result = classify_command_type(text)
        status = "✅" if result['type'] == expected_type else "❌"
        print(f"   {status} '{text}' → {result['type']} (expected: {expected_type})")
    
    # Test validate_floor
    print("\n📌 Testing validate_floor():")
    print(f"   ✅ validate_floor(5) → {validate_floor(5)}")
    print(f"   ✅ validate_floor(15) → {validate_floor(15)}")
    print(f"   ✅ validate_floor(0) → {validate_floor(0)}")
    
    # Test format_response
    print("\n📌 Testing format_response():")
    response = format_response("Test message")
    print(f"   ✅ Response: {response['status']} - {response['message']}")
    
    # Test calculate_confidence
    print("\n📌 Testing calculate_confidence():")
    print(f"   ✅ 3/4 matches → {calculate_confidence(3, 4):.2%}")
    print(f"   ✅ 5/5 matches → {calculate_confidence(5, 5):.2%}")
    
    print("\n" + "=" * 60)
    print("✅ All helper tests completed!")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_helpers()
    
    # Print system info
    print_system_info()
    
    print("\n💡 Helper functions are ready!")
    print("   Import using: from smartlift.helpers import *")