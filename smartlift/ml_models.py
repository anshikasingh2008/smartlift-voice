# smartlift/ml_models.py

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import joblib
import os


class VoiceCommandClassifier:
    """
    ML model for classifying voice commands
    """
    
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.is_trained = False
        self.model_path = "models/command_classifier.joblib"
        
        # Training data: (text, label)
        self.training_data = [
            # Floor requests
            ("take me to floor five", "floor_request"),
            ("go to 3rd floor", "floor_request"),
            ("fifth floor please", "floor_request"),
            ("floor 7", "floor_request"),
            ("ground floor", "floor_request"),
            ("lobby", "floor_request"),
            ("second floor", "floor_request"),
            ("top floor", "floor_request"),
            ("go to floor 4", "floor_request"),
            ("I need floor 6", "floor_request"),
            
            # Door open commands
            ("open the door", "door_open"),
            ("open door", "door_open"),
            ("please open", "door_open"),
            ("open doors", "door_open"),
            ("keep door open", "door_open"),
            
            # Door close commands
            ("close door", "door_close"),
            ("shut the door", "door_close"),
            ("close doors", "door_close"),
            ("shut door", "door_close"),
            
            # Emergency commands
            ("emergency", "emergency"),
            ("help", "emergency"),
            ("I'm stuck", "emergency"),
            ("fire", "emergency"),
            ("medical emergency", "emergency"),
            
            # Cancel commands
            ("cancel", "cancel"),
            ("nevermind", "cancel"),
            ("stop", "cancel"),
            ("forget it", "cancel"),
            
            # Info commands
            ("where am I", "info"),
            ("what floor is this", "info"),
            ("current floor", "info"),
            ("which floor", "info"),
            ("tell me my floor", "info"),
        ]
    
    def train(self):
        """
        Train the classifier
        """
        print("Training ML classifier...")
        
        # Prepare data
        X_text = [item[0] for item in self.training_data]
        y_labels = [item[1] for item in self.training_data]
        
        # Vectorize text
        X = self.vectorizer.fit_transform(X_text)
        
        # Train classifier
        self.classifier.fit(X, y_labels)
        self.is_trained = True
        
        print(f"✅ ML classifier trained on {len(self.training_data)} examples")
        
        # Calculate accuracy
        X_test = self.vectorizer.transform(X_text)
        predictions = self.classifier.predict(X_test)
        accuracy = (predictions == y_labels).mean()
        print(f"   Training accuracy: {accuracy:.2%}")
        
        return accuracy
    
    def predict(self, text):
        """
        Predict command type
        """
        if not self.is_trained:
            self.train()
        
        # Vectorize input
        X = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.classifier.predict(X)[0]
        
        # Get confidence (probability)
        probabilities = self.classifier.predict_proba(X)[0]
        class_index = list(self.classifier.classes_).index(prediction)
        confidence = probabilities[class_index]
        
        return {
            "command_type": prediction,
            "confidence": confidence,
            "all_probabilities": dict(zip(self.classifier.classes_, probabilities))
        }
    
    def save_model(self, path=None):
        """
        Save trained model to file
        """
        if not self.is_trained:
            print("⚠️ Model not trained. Training first...")
            self.train()
        
        if path is None:
            path = self.model_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save model
        model_data = {
            "vectorizer": self.vectorizer,
            "classifier": self.classifier,
            "classes": self.classifier.classes_
        }
        
        joblib.dump(model_data, path)
        print(f"✅ Model saved to {path}")
    
    def load_model(self, path=None):
        """
        Load trained model from file
        """
        if path is None:
            path = self.model_path
        
        if not os.path.exists(path):
            print(f"⚠️ Model not found at {path}. Training new model...")
            self.train()
            return
        
        # Load model
        model_data = joblib.load(path)
        self.vectorizer = model_data["vectorizer"]
        self.classifier = model_data["classifier"]
        self.is_trained = True
        
        print(f"✅ Model loaded from {path}")
    
    def add_training_example(self, text, label):
        """
        Add new training example and retrain
        """
        self.training_data.append((text, label))
        print(f"📝 Added new example: '{text}' → {label}")
        self.train()  # Retrain with new data


class CommandConfidenceScorer:
    """
    Calculate confidence scores for commands using ML and heuristics
    """
    
    def __init__(self):
        self.classifier = VoiceCommandClassifier()
        
    def get_confidence(self, text, extracted_floor=None):
        """
        Calculate overall confidence for a command
        """
        # Get ML confidence
        ml_result = self.classifier.predict(text)
        ml_confidence = ml_result["confidence"]
        
        # Heuristic confidence based on command structure
        heuristic_score = self._heuristic_score(text, extracted_floor)
        
        # Combined confidence (weighted average)
        final_confidence = (ml_confidence * 0.7) + (heuristic_score * 0.3)
        
        return {
            "overall": final_confidence,
            "ml_confidence": ml_confidence,
            "heuristic_score": heuristic_score,
            "predicted_type": ml_result["command_type"]
        }
    
    def _heuristic_score(self, text, extracted_floor):
        """
        Calculate heuristic-based confidence
        """
        text_lower = text.lower()
        score = 0.5  # Base score
        
        # If floor number was successfully extracted
        if extracted_floor is not None:
            score += 0.3
        
        # Check for clear keywords
        if any(word in text_lower for word in ["floor", "take", "go"]):
            score += 0.1
        
        # Check length (very short commands are clearer)
        if len(text.split()) <= 5:
            score += 0.1
        
        return min(1.0, score)


# Test the ML models
if __name__ == "__main__":
    print("=" * 50)
    print("Testing ML Models for SmartLift Voice")
    print("=" * 50)
    
    # Test classifier
    classifier = VoiceCommandClassifier()
    classifier.train()
    
    # Test predictions
    test_commands = [
        "take me to floor 5",
        "open the door",
        "emergency help",
        "where am I",
        "cancel that",
        "I need to go to third floor",
        "close the door please"
    ]
    
    print("\n📊 Test Predictions:")
    print("-" * 50)
    
    for command in test_commands:
        result = classifier.predict(command)
        print(f"Command: '{command}'")
        print(f"  → Type: {result['command_type']}")
        print(f"  → Confidence: {result['confidence']:.2%}")
        print()
    
    # Test confidence scorer
    scorer = CommandConfidenceScorer()
    
    print("\n🎯 Confidence Scores:")
    print("-" * 50)
    
    confidence_test = [
        ("take me to floor 5", 5),
        ("open door", None),
        ("emergency", None),
        ("where am I", None),
        ("blah blah", None)
    ]
    
    for text, floor in confidence_test:
        result = scorer.get_confidence(text, floor)
        print(f"Command: '{text}'")
        print(f"  → Overall Confidence: {result['overall']:.2%}")
        print(f"  → ML Confidence: {result['ml_confidence']:.2%}")
        print()
    
    # Save model
    classifier.save_model()