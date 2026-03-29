# run.py - Main Entry Point for SmartLift Voice
"""
SmartLift Voice - AI-Powered Voice Controlled Elevator System
=============================================================
Main entry point for running the complete SmartLift Voice system.

Usage:
    python run.py          # Run with voice control and web dashboard
    python run.py --web-only   # Run only web dashboard (no voice)
    python run.py --voice-only # Run only voice control (no web)
    python run.py --test       # Run tests only
"""

import sys
import os
import time
import threading
import argparse
from datetime import datetime

# Add the current directory to path so we can import smartlift
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import SmartLift modules
from smartlift.agent import SmartLiftAgent
from smartlift.web_interface import start_web_server
from smartlift.lift_utils import print_system_info, log_event
from smartlift.knowledge_base import AgriculturalKnowledgeBase


# ============================================================
# CONFIGURATION
# ============================================================

# Web server configuration
WEB_HOST = "0.0.0.0"  # Listen on all network interfaces
WEB_PORT = 5000        # Port for web dashboard
WEB_DEBUG = False      # Set to True for development (auto-reload)

# Voice agent configuration
VOICE_ENABLED = True   # Enable voice recognition
VOICE_TIMEOUT = 5      # Seconds to wait for voice input
SIMULATE_HARDWARE = True  # Simulate button presses (no real hardware)


# ============================================================
# BANNER AND WELCOME MESSAGE
# ============================================================

def print_banner():
    """
    Print welcome banner for SmartLift Voice.
    """
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██╗             ║
    ║   ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██║             ║
    ║   ███████╗██╔████╔██║███████║██████╔╝   ██║   ██║             ║
    ║   ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║             ║
    ║   ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ██║             ║
    ║   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝             ║
    ║                                                               ║
    ║   ██╗     ██╗███████╗████████╗                               ║
    ║   ██║     ██║██╔════╝╚══██╔══╝                               ║
    ║   ██║     ██║█████╗     ██║                                  ║
    ║   ██║     ██║██╔══╝     ██║                                  ║
    ║   ███████╗██║██║        ██║                                  ║
    ║   ╚══════╝╚═╝╚═╝        ╚═╝                                  ║
    ║                                                               ║
    ║         AI-Powered Voice Controlled Elevator                  ║
    ║                   For Accessibility                           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
    print("\n" + "=" * 70)
    print("🔊 SmartLift Voice v1.0.0")
    print("=" * 70)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 Python Version: {sys.version.split()[0]}")
    print("=" * 70)
    print()


def print_instructions():
    """
    Print usage instructions.
    """
    print("\n" + "=" * 70)
    print("📖 INSTRUCTIONS")
    print("=" * 70)
    print()
    print("🎤 VOICE COMMANDS:")
    print("   • Floor numbers: 'Floor 5', 'Take me to 3rd floor', 'Ground floor'")
    print("   • Door control: 'Open door', 'Close door'")
    print("   • Emergency: 'Emergency', 'Help', 'Stuck'")
    print("   • Information: 'Where am I?', 'What floor?'")
    print("   • Cancel: 'Cancel', 'Stop', 'Nevermind'")
    print()
    print("🌐 WEB DASHBOARD:")
    print(f"   • Open browser to: http://localhost:{WEB_PORT}")
    print("   • Monitor elevator status in real-time")
    print("   • Send commands via web interface")
    print("   • View command history")
    print()
    print("⌨️ KEYBOARD CONTROLS:")
    print("   • Press Ctrl+C to stop the system")
    print("   • Type 'exit' in voice mode to quit")
    print()
    print("=" * 70)
    print()


# ============================================================
# TEST FUNCTIONS
# ============================================================

def run_tests():
    """
    Run all system tests.
    """
    print("\n" + "=" * 70)
    print("🧪 RUNNING SYSTEM TESTS")
    print("=" * 70)
    
    # Test 1: Import modules
    print("\n📦 Test 1: Importing Modules...")
    try:
        from smartlift import helpers
        print("   ✅ helpers module loaded")
        from smartlift import knowledge_base
        print("   ✅ knowledge_base module loaded")
        from smartlift import agent
        print("   ✅ agent module loaded")
        from smartlift import web_interface
        print("   ✅ web_interface module loaded")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 2: Knowledge Base
    print("\n📚 Test 2: Knowledge Base...")
    try:
        kb = AgriculturalKnowledgeBase()
        floor = kb.get_floor_from_text("floor 5")
        assert floor == 5, "Floor extraction failed"
        print(f"   ✅ Knowledge base working (floor 5 → {floor})")
    except Exception as e:
        print(f"   ❌ Knowledge base test failed: {e}")
    
    # Test 3: Helper Functions
    print("\n🛠️ Test 3: Helper Functions...")
    try:
        from smartlift.lift_utils import extract_floor_number, is_emergency
        floor = extract_floor_number("go to floor 7")
        assert floor == 7, "Helper floor extraction failed"
        emergency = is_emergency("emergency help")
        assert emergency is True, "Emergency detection failed"
        print(f"   ✅ Helper functions working")
    except Exception as e:
        print(f"   ❌ Helper test failed: {e}")
    
    # Test 4: System Requirements
    print("\n🔧 Test 4: System Requirements...")
    from smartlift.lift_utils import check_system_requirements
    reqs = check_system_requirements()
    for package, installed in reqs.items():
        status = "✅" if installed else "❌"
        print(f"   {status} {package}")
    
    # Test 5: Logging
    print("\n📝 Test 5: Logging System...")
    try:
        from smartlift.lift_utils import log_event, get_recent_logs
        log_event("test", {"message": "Test log entry"})
        logs = get_recent_logs(limit=1)
        print(f"   ✅ Logging working ({len(logs)} entries)")
    except Exception as e:
        print(f"   ❌ Logging test failed: {e}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)
    
    return True


# ============================================================
# MAIN RUN FUNCTION
# ============================================================

def run_full_system(voice_enabled=True, web_enabled=True):
    """
    Run the complete SmartLift Voice system.
    
    Args:
        voice_enabled (bool): Enable voice control
        web_enabled (bool): Enable web dashboard
    """
    print_banner()
    print_system_info()
    print_instructions()
    
    # Initialize the lift agent
    print("🔄 Initializing SmartLift Agent...")
    try:
        lift = SmartLiftAgent()
        print("✅ SmartLift Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\n⚠️ Make sure all dependencies are installed:")
        print("   pip install flask speechrecognition pyttsx3 numpy scikit-learn joblib")
        return
    
    # Start web server if enabled
    if web_enabled:
        print("\n🌐 Starting Web Dashboard...")
        try:
            start_web_server(lift, host=WEB_HOST, port=WEB_PORT)
            print(f"✅ Web dashboard running at http://localhost:{WEB_PORT}")
            print(f"   Access from other devices: http://<your-ip>:{WEB_PORT}")
        except Exception as e:
            print(f"⚠️ Failed to start web server: {e}")
            print("   Web dashboard disabled, voice control only")
    
    # Log system start
    log_event("system_start", {
        "voice_enabled": voice_enabled,
        "web_enabled": web_enabled,
        "timestamp": datetime.now().isoformat()
    })
    
    print("\n" + "=" * 70)
    print("🚀 SmartLift Voice is READY!")
    print("=" * 70)
    
    if voice_enabled:
        print("\n🎤 Speak into your microphone to control the elevator")
        print("   Try saying: 'Floor 5', 'Open door', or 'Emergency'")
    else:
        print("\n🎤 Voice control is disabled. Use web dashboard only.")
    
    print("\n💡 Press Ctrl+C to stop the system\n")
    
    # Run the voice agent
    if voice_enabled:
        try:
            lift.run()
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down SmartLift Voice...")
        except Exception as e:
            print(f"\n❌ Error in voice agent: {e}")
    else:
        # Voice disabled, keep running until Ctrl+C
        try:
            print("⏳ System running (voice disabled)...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down SmartLift Voice...")
    
    # Cleanup
    log_event("system_stop", {
        "uptime": "System stopped by user"
    })
    
    print("\n👋 Goodbye! Thank you for using SmartLift Voice.")


# ============================================================
# COMMAND LINE ARGUMENTS
# ============================================================

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="SmartLift Voice - AI-Powered Voice Controlled Elevator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run with voice and web
  python run.py --web-only         # Run only web dashboard
  python run.py --voice-only       # Run only voice control
  python run.py --test             # Run tests only
  python run.py --port 8080        # Run web server on port 8080
        """
    )
    
    parser.add_argument(
        '--web-only',
        action='store_true',
        help='Run only web dashboard (no voice control)'
    )
    
    parser.add_argument(
        '--voice-only',
        action='store_true',
        help='Run only voice control (no web dashboard)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run tests only'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port for web dashboard (default: 5000)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host for web dashboard (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--no-simulate',
        action='store_true',
        help='Use real hardware (requires Raspberry Pi)'
    )
    
    return parser.parse_args()


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    """
    Main entry point for SmartLift Voice.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Update global config
    global WEB_HOST, WEB_PORT, SIMULATE_HARDWARE
    WEB_HOST = args.host
    WEB_PORT = args.port
    
    if args.no_simulate:
        SIMULATE_HARDWARE = False
        from smartlift.agent import set_hardware_mode
        set_hardware_mode(real=True)
    
    # Run tests if requested
    if args.test:
        run_tests()
        return
    
    # Run based on mode
    if args.web_only:
        print("🌐 Starting SmartLift Voice in WEB-ONLY mode...")
        print("   Voice control disabled")
        run_full_system(voice_enabled=False, web_enabled=True)
    
    elif args.voice_only:
        print("🎤 Starting SmartLift Voice in VOICE-ONLY mode...")
        print("   Web dashboard disabled")
        run_full_system(voice_enabled=True, web_enabled=False)
    
    else:
        # Full mode (both voice and web)
        run_full_system(voice_enabled=True, web_enabled=True)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()