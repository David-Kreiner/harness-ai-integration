# Test AI Controller

import unittest
from ai_controller.ai_controller import AIController

class TestAIController(unittest.TestCase):
    def test_run(self):
        ai_controller = AIController()
        self.assertIsNotNone(ai_controller)

if __name__ == '__main__':
    unittest.main()