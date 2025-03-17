"""
Direct configuration script for OpenAI API settings.
This file provides hardcoded configuration to use if .env loading fails.
"""
import os
import openai
import logging

def setup_openai_config():
    """Apply hardcoded OpenAI API settings"""
    logger = logging.getLogger(__name__)
    logger.info("Applying hardcoded OpenAI configuration")
    
    # Apply configuration directly to openai module
    openai.api_type = "azure"
    openai.api_base = "https://it-risk-advisory.cognitiveservices.azure.com"
    openai.api_version = "2024-08-01-preview"
    openai.api_key = "6sYzk9nd49SnrWNfxdMsUqeLUnnhfwTOHCnAYVTllARQ1JQxywz0JQQJ99BAACYeBjFXJ3w3AAAAACOGc2jb"
    
    # Set environment variables as well
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_BASE"] = "https://it-risk-advisory.cognitiveservices.azure.com"
    os.environ["OPENAI_API_VERSION"] = "2024-08-01-preview"
    os.environ["OPENAI_API_KEY"] = "6sYzk9nd49SnrWNfxdMsUqeLUnnhfwTOHCnAYVTllARQ1JQxywz0JQQJ99BAACYeBjFXJ3w3AAAAACOGc2jb"
    os.environ["AZURE_DEPLOYMENT_NAME"] = "gpt-4o-it-risk"
    
    # Log settings
    logger.info(f"API type: {openai.api_type}")
    logger.info(f"API base: {openai.api_base}")
    logger.info(f"API version: {openai.api_version}")
    logger.info(f"API key (first 5 chars): {openai.api_key[:5] if openai.api_key else 'None'}")
    logger.info(f"Deployment name: {os.environ.get('AZURE_DEPLOYMENT_NAME')}")
    
    return True 