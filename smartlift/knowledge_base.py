# smartlift/knowledge_base.py
"""
Knowledge Base for SmartLift Voice
==================================
Expert system containing:
- Floor mappings and rules
- Command patterns and synonyms
- Access control rules
- Emergency protocols
- Building-specific knowledge
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, time

# For type hints
from typing import Dict, List, Optional, Any, Tuple


class AgriculturalKnowledgeBase:
    """
    Knowledge Base for SmartLift Voice System.
    
    Contains all the rules, mappings, and domain knowledge needed
    for intelligent elevator operation.
    
    This is like a Prolog-style knowledge base but in Python.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the knowledge base.
        
        Args:
            config_file: Optional JSON config file path
        """
        # Floor name mappings (spoken words to floor numbers)
        self.floor_name_mapping = {
            # Floor 1 aliases
            "ground": 1,
            "lobby": 1,
            "main": 1,
            "first": 1,
            "1st": 1,
            "floor one": 1,
            "one": 1,
            
            # Floor 2 aliases
            "second": 2,
            "2nd": 2,
            "floor two": 2,
            "two": 2,
            
            # Floor 3 aliases
            "third": 3,
            "3rd": 3,
            "floor three": 3,
            "three": 3,
            
            # Floor 4 aliases
            "fourth": 4,
            "4th": 4,
            "floor four": 4,
            "four": 4,
            
            # Floor 5 aliases
            "fifth": 5,
            "5th": 5,
            "floor five": 5,
            "five": 5,
            
            # Floor 6 aliases
            "sixth": 6,
            "6th": 6,
            "floor six": 6,
            "six": 6,
            
            # Floor 7 aliases
            "seventh": 7,
            "7th": 7,
            "floor seven": 7,
            "seven": 7,
            
            # Floor 8 aliases
            "eighth": 8,
            "8th": 8,
            "floor eight": 8,
            "eight": 8,
            
            # Floor 9 aliases
            "ninth": 9,
            "9th": 9,
            "floor nine": 9,
            "nine": 9,
            
            # Floor 10 aliases
            "tenth": 10,
            "10th": 10,
            "floor ten": 10,
            "ten": 10,
            "top": 10,
            "penthouse": 10
        }
        
        # Reverse mapping: floor number to display names
        self.floor_display_names = {
            1: ["Ground Floor", "Lobby", "Main Floor"],
            2: ["Second Floor", "Floor 2"],
            3: ["Third Floor", "Floor 3"],
            4: ["Fourth Floor", "Floor 4"],
            5: ["Fifth Floor", "Floor 5"],
            6: ["Sixth Floor", "Floor 6"],
            7: ["Seventh Floor", "Floor 7"],
            8: ["Eighth Floor", "Floor 8"],
            9: ["Ninth Floor", "Floor 9"],
            10: ["Top Floor", "Penthouse", "Floor 10"]
        }
        
        # Emergency protocols
        self.emergency_protocols = {
            "fire": {
                "priority": 1,
                "action": "move_to_ground",
                "message": "Fire emergency detected. Moving to ground floor.",
                "notification": "🚨 FIRE ALERT: Evacuate immediately"
            },
            "medical": {
                "priority": 2,
                "action": "fastest_to_ground",
                "message": "Medical emergency. Fastest route to ground floor.",
                "notification": "🚑 Medical emergency in progress"
            },
            "stuck": {
                "priority": 1,
                "action": "emergency_stop",
                "message": "Elevator stuck. Emergency services alerted.",
                "notification": "⚠️ Elevator malfunction - Maintenance dispatched"
            },
            "power_outage": {
                "priority": 1,
                "action": "emergency_lighting",
                "message": "Power outage detected. Emergency lighting activated.",
                "notification": "💡 Backup power engaged"
            },
            "general": {
                "priority": 3,
                "action": "alert_security",
                "message": "Emergency mode activated. Security notified.",
                "notification": "🚨 Emergency mode active"
            }
        }
        
        # Access control rules (restricted floors)
        self.access_rules = {
            "restricted_floors": [8, 9, 10],  # Floors requiring authorization
            "admin_floors": [8, 9],            # Admin only floors
            "vip_floors": [10],                 # VIP/Penthouse floors
            "time_restricted": {
                8: {"start": 9, "end": 17},     # Floor 8 accessible only 9 AM - 5 PM
                9: {"start": 9, "end": 17}
            }
        }
        
        # Command patterns (for rule-based classification)
        self.command_patterns = {
            "floor_request": [
                r"(?:go|take|move|bring).*?(?:to)?.*?(\d+)(?:st|nd|rd|th)?\s*(?:floor)?",
                r"(\d+)(?:st|nd|rd|th)?\s*(?:floor)",
                r"(?:to\s+)?(?:floor\s+)?(\d+)",
                r"(ground|lobby|main|top|penthouse)"
            ],
            "door_control": [
                r"(?:open|close|shut)\s*(?:the)?\s*(?:door|doors)",
                r"(?:keep|hold)\s*(?:door|doors)\s*(?:open)?"
            ],
            "emergency": [
                r"emergency",
                r"help",
                r"stuck",
                r"fire",
                r"medical",
                r"911"
            ],
            "information": [
                r"where\s*(?:am|are)",
                r"what\s*floor",
                r"current\s*floor",
                r"status"
            ],
            "cancel": [
                r"cancel",
                r"stop",
                r"nevermind",
                r"forget"
            ]
        }
        
        # Building-specific knowledge
        self.building_info = {
            "name": "SmartLift Tower",
            "total_floors": 10,
            "basement_floors": 0,
            "has_parking": True,
            "has_restaurant": True,
            "has_gym": True,
            "floor_services": {
                1: ["Lobby", "Security", "Mail Room", "Cafe"],
                2: ["Offices", "Conference Rooms"],
                3: ["Offices", "Meeting Rooms"],
                4: ["Offices", "Break Room"],
                5: ["Offices", "Library"],
                6: ["IT Department", "Server Room"],
                7: ["HR Department", "Training Room"],
                8: ["Executive Offices"],
                9: ["Board Room", "Executive Lounge"],
                10: ["Penthouse", "Rooftop Garden", "Restaurant"]
            }
        }
        
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
    
    # ============================================================
    # FLOOR MAPPING FUNCTIONS
    # ============================================================
    
    def get_floor_from_text(self, text: str) -> Optional[int]:
        """
        Get floor number from spoken text.
        
        Args:
            text (str): Spoken or typed command
            
        Returns:
            int: Floor number or None if not found
            
        Examples:
            >>> kb = AgriculturalKnowledgeBase()
            >>> kb.get_floor_from_text("take me to floor 5")
            5
            >>> kb.get_floor_from_text("ground floor")
            1
        """
        if not text:
            return None
        
        text_lower = text.lower().strip()
        
        # Direct mapping lookup
        for word, floor in self.floor_name_mapping.items():
            if word in text_lower:
                return floor
        
        # Try to extract number
        import re
        numbers = re.findall(r'\d+', text_lower)
        if numbers:
            floor = int(numbers[0])
            if 1 <= floor <= self.building_info["total_floors"]:
                return floor
        
        return None
    
    def get_floor_display_name(self, floor: int) -> str:
        """
        Get display name for a floor number.
        
        Args:
            floor (int): Floor number
            
        Returns:
            str: Display name
            
        Examples:
            >>> kb.get_floor_display_name(1)
            "Ground Floor"
            >>> kb.get_floor_display_name(10)
            "Top Floor"
        """
        if floor in self.floor_display_names:
            return self.floor_display_names[floor][0]
        return f"Floor {floor}"
    
    def get_floor_services(self, floor: int) -> List[str]:
        """
        Get services available on a specific floor.
        
        Args:
            floor (int): Floor number
            
        Returns:
            list: Services available on that floor
        """
        return self.building_info["floor_services"].get(floor, [])
    
    # ============================================================
    # ACCESS CONTROL FUNCTIONS
    # ============================================================
    
    def check_access(self, floor: int, user_role: str = "guest", current_time: Optional[datetime] = None) -> Tuple[bool, str]:
        """
        Check if user has access to a specific floor.
        
        Args:
            floor (int): Floor number
            user_role (str): User role (guest, resident, admin, vip)
            current_time (datetime): Current time for time restrictions
            
        Returns:
            tuple: (access_granted, reason)
            
        Examples:
            >>> kb.check_access(5, "guest")
            (True, "Access granted")
            >>> kb.check_access(8, "guest")
            (False, "Floor 8 is restricted")
        """
        # Allow all floors by default
        if floor not in self.access_rules["restricted_floors"]:
            return True, "Access granted"
        
        # Check time restrictions
        if current_time is None:
            current_time = datetime.now()
        
        time_restrictions = self.access_rules.get("time_restricted", {})
        if floor in time_restrictions:
            rules = time_restrictions[floor]
            current_hour = current_time.hour
            if current_hour < rules["start"] or current_hour > rules["end"]:
                return False, f"Floor {floor} is only accessible between {rules['start']}:00 and {rules['end']}:00"
        
        # Check role-based access
        if floor in self.access_rules["admin_floors"]:
            if user_role not in ["admin", "vip"]:
                return False, f"Floor {floor} requires admin access"
        
        if floor in self.access_rules["vip_floors"]:
            if user_role != "vip":
                return False, f"Floor {floor} is VIP only"
        
        return True, "Access granted"
    
    def authenticate(self, floor: int, pin: str) -> bool:
        """
        Authenticate user for restricted floor access.
        
        Args:
            floor (int): Floor number
            pin (str): PIN code
            
        Returns:
            bool: True if authenticated
            
        Note:
            In production, this should use secure authentication.
        """
        # This is a simple demo implementation
        # In real system, use proper authentication
        valid_pins = {
            8: ["1234", "admin8"],
            9: ["5678", "admin9"],
            10: ["9999", "vip10"]
        }
        
        if floor in valid_pins:
            return pin in valid_pins[floor]
        
        return False
    
    # ============================================================
    # EMERGENCY PROTOCOLS
    # ============================================================
    
    def get_emergency_protocol(self, emergency_type: str = "general") -> Dict[str, Any]:
        """
        Get emergency protocol for a specific emergency type.
        
        Args:
            emergency_type (str): Type of emergency
            
        Returns:
            dict: Emergency protocol
        """
        if emergency_type in self.emergency_protocols:
            return self.emergency_protocols[emergency_type]
        return self.emergency_protocols["general"]
    
    def get_all_emergency_types(self) -> List[str]:
        """
        Get all available emergency types.
        
        Returns:
            list: Emergency type names
        """
        return list(self.emergency_protocols.keys())
    
    # ============================================================
    # COMMAND PATTERN MATCHING
    # ============================================================
    
    def match_command_pattern(self, text: str, command_type: str) -> bool:
        """
        Check if text matches a command pattern.
        
        Args:
            text (str): User input
            command_type (str): Type of command to match
            
        Returns:
            bool: True if pattern matches
        """
        if command_type not in self.command_patterns:
            return False
        
        import re
        text_lower = text.lower()
        
        for pattern in self.command_patterns[command_type]:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def classify_command(self, text: str) -> Dict[str, Any]:
        """
        Classify command using pattern matching.
        
        Args:
            text (str): User input
            
        Returns:
            dict: Classification result
        """
        result = {
            "type": "unknown",
            "confidence": 0.0,
            "floor": None
        }
        
        # Check each command type
        if self.match_command_pattern(text, "emergency"):
            result["type"] = "emergency"
            result["confidence"] = 0.95
            return result
        
        if self.match_command_pattern(text, "cancel"):
            result["type"] = "cancel"
            result["confidence"] = 0.90
            return result
        
        if self.match_command_pattern(text, "door_control"):
            if "open" in text.lower():
                result["type"] = "door_open"
            else:
                result["type"] = "door_close"
            result["confidence"] = 0.90
            return result
        
        if self.match_command_pattern(text, "information"):
            result["type"] = "info"
            result["confidence"] = 0.85
            return result
        
        # Check for floor request
        floor = self.get_floor_from_text(text)
        if floor:
            result["type"] = "floor_request"
            result["floor"] = floor
            result["confidence"] = 0.95
            return result
        
        return result
    
    # ============================================================
    # RULE-BASED REASONING (Prolog-style)
    # ============================================================
    
    def forward_chaining(self, facts: List[str]) -> List[str]:
        """
        Simple forward chaining inference engine.
        
        Args:
            facts (list): Initial facts
            
        Returns:
            list: Inferred facts
        """
        # Rules in format: (conditions, conclusion)
        rules = [
            (["emergency_activated"], "alert_security"),
            (["alert_security", "fire"], "evacuate_building"),
            (["power_outage"], "activate_backup"),
            (["door_open", "timeout"], "close_door"),
        ]
        
        inferred = []
        facts_set = set(facts)
        
        for conditions, conclusion in rules:
            if all(cond in facts_set for cond in conditions):
                inferred.append(conclusion)
        
        return inferred
    
    # ============================================================
    # CONFIGURATION MANAGEMENT
    # ============================================================
    
    def load_config(self, config_file: str) -> bool:
        """
        Load configuration from JSON file.
        
        Args:
            config_file (str): Path to JSON config file
            
        Returns:
            bool: True if successful
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Update floor mappings
            if "floor_name_mapping" in config:
                self.floor_name_mapping.update(config["floor_name_mapping"])
            
            # Update access rules
            if "access_rules" in config:
                self.access_rules.update(config["access_rules"])
            
            # Update building info
            if "building_info" in config:
                self.building_info.update(config["building_info"])
            
            print(f"✅ Config loaded from {config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return False
    
    def save_config(self, config_file: str) -> bool:
        """
        Save current configuration to JSON file.
        
        Args:
            config_file (str): Path to save config
            
        Returns:
            bool: True if successful
        """
        config = {
            "floor_name_mapping": self.floor_name_mapping,
            "floor_display_names": self.floor_display_names,
            "access_rules": self.access_rules,
            "building_info": self.building_info,
            "emergency_protocols": self.emergency_protocols
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Config saved to {config_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    def get_all_floors(self) -> List[int]:
        """
        Get list of all floors in the building.
        
        Returns:
            list: Floor numbers
        """
        return list(range(1, self.building_info["total_floors"] + 1))
    
    def get_restricted_floors(self) -> List[int]:
        """
        Get list of restricted floors.
        
        Returns:
            list: Restricted floor numbers
        """
        return self.access_rules["restricted_floors"]
    
    def get_floor_aliases(self, floor: int) -> List[str]:
        """
        Get all aliases for a specific floor.
        
        Args:
            floor (int): Floor number
            
        Returns:
            list: Aliases for that floor
        """
        aliases = []
        for word, num in self.floor_name_mapping.items():
            if num == floor:
                aliases.append(word)
        return aliases
    
    def print_knowledge_summary(self) -> None:
        """
        Print summary of knowledge base contents.
        """
        print("\n" + "=" * 60)
        print("📚 KNOWLEDGE BASE SUMMARY")
        print("=" * 60)
        
        print(f"\n🏢 Building: {self.building_info['name']}")
        print(f"📊 Total Floors: {self.building_info['total_floors']}")
        
        print(f"\n🗣️ Floor Mappings: {len(self.floor_name_mapping)} aliases")
        print(f"   Example: 'ground' → Floor 1")
        
        print(f"\n🔒 Restricted Floors: {self.get_restricted_floors()}")
        
        print(f"\n🚨 Emergency Protocols: {len(self.emergency_protocols)}")
        for protocol in self.emergency_protocols.keys():
            print(f"   - {protocol}")
        
        print(f"\n📝 Command Patterns: {len(self.command_patterns)}")
        for pattern_type in self.command_patterns.keys():
            print(f"   - {pattern_type}")
        
        print("\n" + "=" * 60)


# ============================================================
# TEST FUNCTIONS
# ============================================================

def test_knowledge_base():
    """
    Test the knowledge base functionality.
    """
    print("\n" + "=" * 60)
    print("🧪 TESTING KNOWLEDGE BASE")
    print("=" * 60)
    
    kb = AgriculturalKnowledgeBase()
    
    # Test floor mapping
    print("\n📌 Testing Floor Mapping:")
    test_phrases = [
        ("ground floor", 1),
        ("take me to floor 5", 5),
        ("go to lobby", 1),
        ("top floor", 10),
        ("penthouse", 10),
        ("second floor", 2),
        ("just 7", 7),
    ]
    
    for phrase, expected in test_phrases:
        result = kb.get_floor_from_text(phrase)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{phrase}' → {result} (expected: {expected})")
    
    # Test floor display names
    print("\n📌 Testing Floor Display Names:")
    for floor in [1, 5, 10]:
        name = kb.get_floor_display_name(floor)
        print(f"   Floor {floor}: {name}")
    
    # Test access control
    print("\n📌 Testing Access Control:")
    test_access = [
        (5, "guest", True),
        (8, "guest", False),
        (8, "admin", True),
        (10, "vip", True),
    ]
    
    for floor, role, expected in test_access:
        granted, reason = kb.check_access(floor, role)
        status = "✅" if granted == expected else "❌"
        print(f"   {status} Floor {floor}, Role {role}: {granted} - {reason}")
    
    # Test command classification
    print("\n📌 Testing Command Classification:")
    test_commands = [
        ("emergency help", "emergency"),
        ("cancel that", "cancel"),
        ("open the door", "door_open"),
        ("close door", "door_close"),
        ("where am I", "info"),
        ("floor 5", "floor_request"),
    ]
    
    for text, expected_type in test_commands:
        result = kb.classify_command(text)
        status = "✅" if result["type"] == expected_type else "❌"
        print(f"   {status} '{text}' → {result['type']} (expected: {expected_type})")
    
    # Test emergency protocols
    print("\n📌 Testing Emergency Protocols:")
    for emergency_type in ["fire", "medical", "general"]:
        protocol = kb.get_emergency_protocol(emergency_type)
        print(f"   {emergency_type}: {protocol['message']}")
    
    # Print summary
    kb.print_knowledge_summary()
    
    print("\n" + "=" * 60)
    print("✅ Knowledge base tests completed!")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Run tests
    test_knowledge_base()
    
    print("\n💡 Knowledge Base is ready!")
    print("   Import using: from smartlift.knowledge_base import AgriculturalKnowledgeBase")
    print("   Then create: kb = AgriculturalKnowledgeBase()")