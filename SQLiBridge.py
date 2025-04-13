#!/usr/bin/env python3

import argparse
import os
import json
import sys
from openai import OpenAI
from config import DEFAULT_CONFIG

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate SQL injection proxy PHP scripts using LLM")
    parser.add_argument("--model", help="Specify which LLM model to use", default=DEFAULT_CONFIG["model"])
    parser.add_argument("--output", "-o", help="Output PHP file name", default="generated_proxy.php")
    parser.add_argument("--submit-url", "-s", help="URL for submitting parameters", required=True)
    parser.add_argument("--result-url", "-r", help="URL for viewing results", required=True)
    parser.add_argument("--session-cookie", "-c", help="Session cookie value", required=True)
    parser.add_argument("--param-name", "-p", help="Name of the injection parameter", default="id")
    parser.add_argument("--method", "-m", help="HTTP method for parameter submission (GET or POST)", choices=["GET", "POST"], default="POST")
    parser.add_argument("--custom-prompt", help="Custom prompt template file", default=None)
    
    return parser.parse_args()

def create_prompt(submit_url, result_url, cookie, param_name, method):
    # Create a prompt that avoids specific technical terms
    prompt = f"""
    Write a PHP script that:
    
    1. Accepts an 's' parameter via GET request (this is the SQL injection payload)
    2. Uses cURL to send this payload to a target web application
    3. The script should:
       - First URL encode the received 's' parameter
       - Submit it as '{param_name}=$encoded_payload&Submit=Submit' via {method} to {submit_url}
       - Then fetch the results page with a GET request from {result_url}
       - Return the results to the client
    
    Configuration details:
    - Submit URL: {submit_url}
    - Result URL: {result_url}  
    - Cookie: {cookie}
    - Target parameter name: {param_name} (the parameter that will receive the encoded injection payload)
    - HTTP method for submission: {method}
    
    Important implementation notes:
    - The script should receive SQL injection content through GET parameter 's'
    - The script should encode this content and send it to the target application as '{param_name}'
    - Use the same cURL session for both requests to maintain session state
    - Handle URL encoding properly and include error handling
    - Add proper comments explaining the proxy functionality
    """
    return prompt.strip()

def generate_proxy_script(args, config):
    # Set up OpenAI API with new client approach
    client = OpenAI(
        api_key=config["openai_key"],
        base_url=config["api_base"]
    )
    
    # Load custom prompt if provided, otherwise create default
    if args.custom_prompt and os.path.exists(args.custom_prompt):
        with open(args.custom_prompt, 'r') as f:
            prompt = f.read()
    else:
        prompt = create_prompt(args.submit_url, args.result_url, args.session_cookie, args.param_name, args.method)
    
    try:
        # Make API call to generate the proxy script using the new client approach
        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates PHP code for web utilities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        generated_code = response.choices[0].message.content
        
        # Extract PHP code from the response if it's wrapped in markdown code blocks
        if "```php" in generated_code and "```" in generated_code:
            start_index = generated_code.find("```php") + 6
            end_index = generated_code.rfind("```")
            generated_code = generated_code[start_index:end_index].strip()
        elif "```" in generated_code:
            start_index = generated_code.find("```") + 3
            end_index = generated_code.rfind("```")
            generated_code = generated_code[start_index:end_index].strip()
        
        # Ensure it starts with <?php if not already
        if not generated_code.startswith("<?php"):
            generated_code = "<?php\n" + generated_code
        
        return generated_code
    
    except Exception as e:
        print(f"Error generating proxy script: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    args = parse_arguments()
    
    # Load config
    config = DEFAULT_CONFIG
    
    # Generate the proxy script
    proxy_script = generate_proxy_script(args, config)
    
    # Write to output file
    with open(args.output, 'w') as f:
        f.write(proxy_script)
    
    print(f"Proxy script generated successfully: {args.output}")

if __name__ == "__main__":
    main() 