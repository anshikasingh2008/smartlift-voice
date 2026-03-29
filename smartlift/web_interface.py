# smartlift/web_interface.py

from flask import Flask, render_template, jsonify, request
import json
import threading
import os

# Create Flask app
app = Flask(__name__)

# Global variables
lift = None
monitor = None


class LiftMonitor:
    """
    Web interface for monitoring lift status
    """
    
    def __init__(self, lift_agent):
        self.lift = lift_agent
        self.logs = []
        
    def get_status(self):
        """
        Get current lift status
        """
        # Safely get attributes with defaults
        current_floor = getattr(self.lift, 'current_floor', 1)
        is_moving = getattr(self.lift, 'is_moving', False)
        doors_open = getattr(self.lift, 'doors_open', False)
        destination_floors = getattr(self.lift, 'destination_floors', [])
        peas = getattr(self.lift, 'peas', {"performance": {}})
        
        return {
            "current_floor": current_floor,
            "is_moving": is_moving,
            "doors_open": doors_open,
            "pending_requests": list(destination_floors),
            "performance": peas.get("performance", {})
        }
    
    def get_logs(self, limit=50):
        """
        Get recent logs
        """
        log_file = "lift_logs.json"
        logs = []
        
        try:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                logs.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            return logs[-limit:] if logs else []
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []
    
    def add_log(self, log_entry):
        """
        Add a log entry
        """
        try:
            with open("lift_logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error writing log: {e}")


@app.route('/')
def index():
    """Main dashboard"""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"<h1>Error loading dashboard</h1><p>{e}</p><p>Make sure templates/dashboard.html exists</p>"


@app.route('/api/status')
def api_status():
    """API endpoint for lift status"""
    if monitor:
        status = monitor.get_status()
        return jsonify(status)
    return jsonify({"error": "Monitor not initialized"})


@app.route('/api/logs')
def api_logs():
    """API endpoint for logs"""
    if monitor:
        logs = monitor.get_logs()
        return jsonify(logs)
    return jsonify({"error": "Monitor not initialized"})


@app.route('/api/command', methods=['POST'])
def api_command():
    """Send voice command via web"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        command_text = data.get('command')
        if not command_text:
            return jsonify({"error": "No command provided"}), 400
        
        if not lift:
            return jsonify({"error": "Lift agent not initialized"}), 500
        
        # Process command
        command = lift.process_command(command_text)
        response = lift.act(command)
        
        # Log the command
        if monitor:
            monitor.add_log({
                "type": "web_command",
                "command": command_text,
                "response": response
            })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "lift_initialized": lift is not None,
        "monitor_initialized": monitor is not None
    })


def start_web_server(lift_agent, host='0.0.0.0', port=5000, debug=False):
    """
    Start the web server in a separate thread
    
    Args:
        lift_agent: SmartLiftAgent instance
        host: Host to bind to (default: 0.0.0.0 for all interfaces)
        port: Port to listen on (default: 5000)
        debug: Enable debug mode (default: False)
    """
    global lift, monitor
    
    lift = lift_agent
    monitor = LiftMonitor(lift_agent)
    
    print(f"🌐 Starting web server at http://{host}:{port}")
    print(f"   Dashboard: http://{host}:{port}/")
    print(f"   API Status: http://{host}:{port}/api/status")
    print(f"   API Health: http://{host}:{port}/api/health")
    
    # Run in separate thread
    def run_server():
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    return server_thread


if __name__ == "__main__":
    # For testing without the lift agent
    print("⚠️ Running web server in standalone test mode")
    print("   (No lift agent connected)")
    
    # Create a mock lift agent for testing
    class MockLiftAgent:
        def __init__(self):
            self.current_floor = 3
            self.is_moving = False
            self.doors_open = True
            self.destination_floors = [5, 7]
            self.peas = {"performance": {"accuracy": 0.95}}
        
        def process_command(self, text):
            return {"type": "test", "original": text}
        
        def act(self, command):
            return {"status": "success", "message": f"Processed: {command.get('original')}"}
    
    mock_lift = MockLiftAgent()
    start_web_server(mock_lift, debug=True)
    
    print("\n✅ Web server running. Press Ctrl+C to stop.")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down web server...")