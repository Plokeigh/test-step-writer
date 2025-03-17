"""
Simple script to test OpenAI API connectivity.
Run this script to verify .env configuration is working properly.
"""
import os
import sys
import openai
from dotenv import load_dotenv
import logging
import traceback

# Try to import the direct configuration
try:
    from config_direct import setup_openai_config
    direct_config_available = True
except ImportError:
    direct_config_available = False

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openai_connection():
    """Test OpenAI API connectivity using settings from .env file"""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(script_dir, '.env')
    dotenv_new_path = os.path.join(script_dir, '.env.new')
    
    # Check if the alternate .env file exists
    if os.path.exists(dotenv_new_path) and not os.path.exists(dotenv_path):
        logger.info(f"Found .env.new but no .env. Renaming .env.new to .env")
        try:
            # If on Windows, first delete existing .env if it exists
            if os.path.exists(dotenv_path):
                os.remove(dotenv_path)
            os.rename(dotenv_new_path, dotenv_path)
        except Exception as e:
            logger.error(f"Error renaming .env.new to .env: {str(e)}")
    
    # Debug .env file contents
    try:
        if os.path.exists(dotenv_path):
            logger.info(f".env file exists at: {dotenv_path}")
            with open(dotenv_path, 'r') as file:
                contents = file.read()
                logger.info(f".env file contents (first 10 chars): {contents[:10]}...")
                logger.info(f".env file size: {len(contents)} bytes")
                logger.info(f".env file line count: {len(contents.splitlines())}")
                
                # Print each line for debugging
                logger.info("Contents of .env file:")
                for i, line in enumerate(contents.splitlines()):
                    logger.info(f"Line {i+1}: {line}")
        else:
            logger.error(f".env file not found at: {dotenv_path}")
            if direct_config_available:
                logger.info("Using direct configuration instead of .env file")
                setup_openai_config()
                return test_api_connection()
            return False
    except Exception as e:
        logger.error(f"Error reading .env file: {str(e)}")
        traceback.print_exc()
        
    # Load environment variables directly
    try:
        # Try loading with dotenv
        load_dotenv(dotenv_path=dotenv_path, override=True)
        
        # Directly read the file and set environment variables
        with open(dotenv_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    logger.info(f"Manually set env var: {key}={value[:5]}...")
    except Exception as e:
        logger.error(f"Error manually loading env vars: {str(e)}")
        traceback.print_exc()
    
    # Configure OpenAI
    openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
    
    # Log configuration
    logger.info(f"API type: {openai.api_type}")
    logger.info(f"API base: {openai.api_base}")
    logger.info(f"API version: {openai.api_version}")
    logger.info(f"API key (first 5 chars): {openai.api_key[:5] if openai.api_key else 'None'}")
    logger.info(f"Deployment name: {deployment_name}")
    
    # Verify directly from environment variables
    logger.info("Direct environment variable check:")
    logger.info(f"OPENAI_API_TYPE: {os.environ.get('OPENAI_API_TYPE', 'Not set')}")
    logger.info(f"OPENAI_API_BASE: {os.environ.get('OPENAI_API_BASE', 'Not set')}")
    logger.info(f"OPENAI_API_VERSION: {os.environ.get('OPENAI_API_VERSION', 'Not set')}")
    logger.info(f"OPENAI_API_KEY: {os.environ.get('OPENAI_API_KEY', 'Not set')[:5] if os.environ.get('OPENAI_API_KEY') else 'Not set'}")
    logger.info(f"AZURE_DEPLOYMENT_NAME: {os.environ.get('AZURE_DEPLOYMENT_NAME', 'Not set')}")
    
    # Verify required variables are set
    if not all([openai.api_type, openai.api_base, openai.api_version, openai.api_key, deployment_name]):
        missing = []
        if not openai.api_type: missing.append("OPENAI_API_TYPE")
        if not openai.api_base: missing.append("OPENAI_API_BASE") 
        if not openai.api_version: missing.append("OPENAI_API_VERSION")
        if not openai.api_key: missing.append("OPENAI_API_KEY")
        if not deployment_name: missing.append("AZURE_DEPLOYMENT_NAME")
        logger.error(f"The following required variables are missing: {', '.join(missing)}")
        
        # Try direct configuration as last resort
        if direct_config_available:
            logger.info("Trying direct configuration as last resort")
            setup_openai_config()
            return test_api_connection()
        
        return False
    
    return test_api_connection()

def test_api_connection():
    """Test the actual API connection using the current configuration"""
    deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o-it-risk")
    
    # Test API connection
    try:
        logger.info("Testing OpenAI API connection...")
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )
        logger.info(f"API response: {response.choices[0].message['content']}")
        logger.info("OpenAI API connection successful!")
        return True
    except Exception as e:
        logger.error(f"OpenAI API connection failed: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    if success:
        logger.info("✓ All checks passed!")
        sys.exit(0)
    else:
        logger.error("✗ OpenAI API test failed. Check configuration.")
        sys.exit(1) 