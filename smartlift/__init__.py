# smartlift/__init__.py
"""
SmartLift Voice - AI-Powered Voice Controlled Elevator System
=============================================================

An intelligent elevator control system that uses voice commands,
machine learning, and web technologies to provide hands-free,
accessible elevator operation.

Course: CSA2001 - Fundamentals in AI and ML
Author: [ANSHIKA SINGH]
Version: 1.0.0
"""

# Version information
__version__ = "1.0.0"
__author__ = "ANSHIKA SINGH"
__email__ = "anshika.25bai10498@vitbbhopal.ac.in"
__license__ = "MIT"
__description__ = "AI-Powered Voice Controlled Elevator for Accessibility"

# Import main classes for easy access
from smartlift.agent import SmartLiftAgent
from smartlift.lift_utils import (
    extract_floor_number,
    validate_floor,
    is_emergency,
    is_door_command,
    is_cancel_command,
    is_info_command,
    log_event,
    format_response,
    sanitize_input,
    get_recent_logs,
    calculate_confidence
)
from smartlift.knowledge_base import AgriculturalKnowledgeBase
from smartlift.ml_models import VoiceCommandClassifier, CommandConfidenceScorer

# Package metadata
__all__ = [
    # Main classes
    "SmartLiftAgent",
    "AgriculturalKnowledgeBase",
    "VoiceCommandClassifier",
    "CommandConfidenceScorer",
    
    # Helper functions
    "extract_floor_number",
    "validate_floor",
    "is_emergency",
    "is_door_command",
    "is_cancel_command",
    "is_info_command",
    "log_event",
    "format_response",
    "sanitize_input",
    "get_recent_logs",
    "calculate_confidence",
    
    # Package info
    "__version__",
    "__author__",
    "__description__"
]

# Module initialization
def initialize():
    """
    Initialize the SmartLift Voice package.
    Checks system requirements and prints welcome message.
    """
    print("=" * 60)
    print("🔊 SmartLift Voice v{}".format(__version__))
    print("=" * 60)
    print("🎯 AI-Powered Voice Controlled Elevator System")
    print("📚 Course: CSA2001 - Fundamentals in AI and ML")
    print("=" * 60)
    print()
    
    # Check for required packages
    check_requirements()
    
    print("✅ SmartLift Voice ready!")
    print()
    print("💡 Quick Commands:")
    print("   - Voice: 'Floor 5', 'Open door', 'Emergency'")
    print("   - Web Dashboard: http://localhost:5000")
    print("   - Type 'exit' to quit")
    print()
    print("=" * 60)


def check_requirements():
    """
    Check if all required packages are installed.
    """
    required_packages = {
        "flask": "Web interface",
        "speech_recognition": "Voice input",
        "pyttsx3": "Text-to-speech",
        "numpy": "Numerical operations",
        "sklearn": "Machine Learning",
        "joblib": "Model persistence"
    }
    
    missing = []
    for package, purpose in required_packages.items():
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(f"   - {package}: {purpose}")
    
    if missing:
        print("⚠️ Missing optional packages:")
        for m in missing:
            print(m)
        print()
        print("Install with: pip install flask speechrecognition pyttsx3 numpy scikit-learn joblib")
        print()


# Run initialization when module is imported
initialize()

# Import main agent for quick start
def main():
    """
    Quick start function to run SmartLift Voice.
    Usage: python -m smartlift
    """
    from smartlift.agent import SmartLiftAgent
    from smartlift.web_interface import start_web_server
    
    # Create agent
    agent = SmartLiftAgent()
    
    # Start web server
    start_web_server(agent)
    
    # Run voice agent
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye from SmartLift Voice!")


# If run directly
if __name__ == "__main__":
    main()