import sys
import os

# Add the harness-ai-integration directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_engine.ai_engine import AIEngine

class AIController:
    def __init__(self):
        self.ai_engine = AIEngine()

    def process_request(self, request):
        response = self.ai_engine.process_request(request)
        return response
