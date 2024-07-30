import sys
import os
import asyncio
import logging
import yaml
from gptscript.gptscript import GPTScript
from gptscript.tool import ToolDef
from gptscript.opts import GlobalOptions, Options
from gptscript.install import install, gptscript_binary_name, python_bin_dir
import subprocess
import json
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class AIEngine:
    def __init__(self, api_key=None, base_url=None, default_model=None, env=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or "https://api.openai.com/v1"
        self.default_model = default_model
        self.env = env or os.environ
        self.gpt_script = None  # Initialize the attribute
        self.chat_states = {}  # Store chat states for multiple users
        logger.info("Starting AIEngine initialization...")
        logger.info(f"API Key: {self.api_key}")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Default Model: {self.default_model}")
        logger.info(f"Environment: {self.env}")
        try:
            bin_name = str(python_bin_dir / gptscript_binary_name)
            logger.info(f"GPTScript binary path: {bin_name}")
            if not os.path.exists(bin_name):
                logger.error(f"GPTScript binary not found at: {bin_name}")
            else:
                logger.info(f"GPTScript binary found at: {bin_name}")
            # Check if the binary runs correctly
            result = subprocess.run([bin_name, '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                logger.error(f"Failed to run GPTScript binary: {result.stderr}")
            else:
                logger.info(f"GPTScript version: {result.stdout.strip()}")
            self.gpt_script = GPTScript(GlobalOptions(apiKey=self.api_key, baseURL=self.base_url, defaultModel=self.default_model,
env=self.env))
            logger.info("GPTScript initialized successfully with global tools.")
        except Exception as e:
            logger.error(f"Failed to initialize GPTScript: {e}")

    def __del__(self):
        if self.gpt_script:
            self.gpt_script.close()
    
    # had some trouble with this
    async def process_request(self, user_id, request):
        """Process a request using the GPTScript tool."""
        if not self.gpt_script:
            logger.error("GPTScript is not initialized.")
            return {"response": "GPTScript is not initialized."}
        try:
            tool_def = ToolDef(                                                                                                         
                tools=[],                                                                        
                instructions=f"{request}"                                                              
            )
            dir = os.getcwd() + "/agent.gpt"
            logger.info(dir)
            run = self.gpt_script.run(dir,
                    Options(disableCache=True),
                    )                
            # run = self.gpt_script.evaluate(tool_def)                                                                                    
            response = await run.text()                                                                                                 
            print("Raw Response:", response)                                                
            return {"results": response}   
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {"response": f"run encountered an error: {e}"}

    async def demonstrate_tooldefs(self, request):
        """Demonstrate the creation and evaluation of ToolDef instances."""
        if not self.gpt_script:
            logger.error("GPTScript is not initialized.")
            return {"response": "GPTScript is not initialized."}
        try:
            tool_def = ToolDef(
                tools=[],
                jsonResponse=True,
                cache=False,
                instructions="""
                Create three short graphic artist descriptions and their muses.
                These should be descriptive and explain their point of view.
                Also come up with a made-up name, they each should be from different
                backgrounds and approach art differently.
                The JSON response format should be:
                {
                    artists: [{
                        name: "name",
                        description: "description"
                    }]
                }
                """
            )
            run = self.gpt_script.evaluate(tool_def)
            response = await run.text()
            return {"response": json.loads(response)}
        except Exception as e:
            logger.error(f"Error demonstrating tool definitions: {e}")
            return {"response": f"run encountered an error: {e}"}
