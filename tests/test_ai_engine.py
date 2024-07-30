# Test AI Engine

import unittest
import asyncio
import sys
import os

# Add the harness-ai-integration directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_engine.ai_engine import AIEngine
from unittest.mock import patch, MagicMock

class TestAIEngine(unittest.TestCase):
    @patch('gptscript.gptscript.GPTScript.evaluate')
    def test_process_request(self, mock_evaluate):
        ai_engine = AIEngine()
        mock_run = MagicMock()
        mock_run.text.return_value = 'Mocked response'
        mock_evaluate.return_value = mock_run

        request = 'List all pipelines'
        response = ai_engine.process_request(request)

        self.assertEqual(response, 'Mocked response')
        mock_evaluate.assert_called_once()

    @patch('gptscript.gptscript.GPTScript.list_tools')
    def test_list_tools(self, mock_list_tools):
        ai_engine = AIEngine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mock_list_tools.return_value = loop.create_future()
        mock_list_tools.return_value.set_result(['tool1', 'tool2'])

        tools_future = ai_engine.list_tools()
        tools = loop.run_until_complete(tools_future)

        self.assertEqual(tools.result(), ['tool1', 'tool2'])
        mock_list_tools.assert_called_once()

    @patch('gptscript.gptscript.GPTScript.list_models')
    def test_list_models(self, mock_list_models):
        ai_engine = AIEngine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mock_list_models.return_value = loop.create_future()
        mock_list_models.return_value.set_result(['model1', 'model2'])

        models_future = ai_engine.list_models()
        models = loop.run_until_complete(models_future)

        self.assertEqual(models.result(), ['model1', 'model2'])
        mock_list_models.assert_called_once()

    @patch('gptscript.gptscript.GPTScript.parse_tool')
    def test_parse_tool(self, mock_parse_tool):
        ai_engine = AIEngine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mock_parse_tool.return_value = loop.create_future()
        mock_parse_tool.return_value.set_result(['parsed_tool'])

        tool_content = 'Instructions: Say hello!'
        tools_future = ai_engine.parse_tool(tool_content)
        tools = loop.run_until_complete(tools_future)

        self.assertEqual(tools.result(), ['parsed_tool'])
        mock_parse_tool.assert_called_once_with(tool_content)

    @patch('gptscript.gptscript.GPTScript.fmt')
    def test_format_tool(self, mock_fmt):
        ai_engine = AIEngine()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mock_fmt.return_value = loop.create_future()
        mock_fmt.return_value.set_result('Formatted tool')

        tool = MagicMock()
        formatted_tool_future = ai_engine.format_tool(tool)
        formatted_tool = loop.run_until_complete(formatted_tool_future)

        self.assertEqual(formatted_tool.result(), 'Formatted tool')
        mock_fmt.assert_called_once_with(tool)

    @patch('gptscript.gptscript.GPTScript.evaluate')
    def test_evaluate_tool(self, mock_evaluate):
        ai_engine = AIEngine()
        mock_run = MagicMock()
        mock_run.text.return_value = 'Evaluation response'
        mock_evaluate.return_value = mock_run

        tool = MagicMock()
        response = ai_engine.evaluate_tool(tool)

        self.assertEqual(response, 'Evaluation response')
        mock_evaluate.assert_called_once_with(tool)

if __name__ == '__main__':
    unittest.main()
