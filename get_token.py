#!/usr/bin/env python
"""
QuickBooks Time OAuth Helper

This script helps you get an access token for the QuickBooks Time API.
It implements the OAuth 2.0 authorization code flow.

Usage:
1. Register an app at https://developer.intuit.com/
2. Set your client ID and secret below
3. Run this script
4. Follow the instructions to authorize your app
5. The script will display your access token
"""

import os
import sys
import webbrowser
import json
import base64
import requests
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Set your OAuth credentials here
CLIENT_ID = "ABa40QwqKXOuJtJ47KVQTt2kptGiHxQGsD9FeYF2Hgl4uFapqW"
CLIENT_SECRET = "BgYd2H0adW27negDIjGzRYYDzGwM0QFic7kkrVQn"
REDIRECT_URI = "http://localhost:8000/callback"

# QuickBooks Time OAuth endpoints
AUTH_URL = "https://accounts.intuit.com/connect/oauth2/authorizationcode"
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
SCOPE = "com.intuit.quickbooks.timetracking"

# Global variable to store the authorization code
auth_code = None
auth_error = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress log messages
        return
        
    def do_GET(self):
        global auth_code, auth_error
        
        # Parse the URL path and query parameters
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query
        params = parse_qs(query)
        
        print(f"Received callback: {path}")
        
        # Handle both /callback and /callback/ paths
        if path == "/callback" or path == "/callback/":
            if "code" in params:
                auth_code = params["code"][0]
                
                # Send a success response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                response = """
                <html>
                <head><title>Authorization Successful</title></head>
                <body>
                <h1>Authorization Successful!</h1>
                <p>You can now close this window and return to the script.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
            elif "error" in params:
                auth_error = params["error"][0]
                error_description = params.get("error_description", ["Unknown error"])[0]
                
                # Send an error response
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                response = f"""
                <html>
                <head><title>Authorization Failed</title></head>
                <body>
                <h1>Authorization Failed</h1>
                <p>Error: {auth_error}</p>
                <p>Description: {error_description}</p>
                <p>Please close this window and check the console for more information.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
            else:
                # Send an error response
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                response = """
                <html>
                <head><title>Authorization Failed</title></head>
                <body>
                <h1>Authorization Failed</h1>
                <p>No authorization code was received. Please try again.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
        else:
            # Handle other paths
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Not found")

def check_redirect_uri_registration():
    """Check if the redirect URI is properly registered"""
    print("\n⚠️ IMPORTANT: Make sure your redirect URI is registered in the QuickBooks Developer Portal")
    print(f"Your current redirect URI is: {REDIRECT_URI}")
    print("To register this URI:")
    print("1. Log in to https://developer.intuit.com/")
    print("2. Go to 'My Apps' and select your app")
    print("3. Click on the 'Development Settings' tab")
    print("4. Under 'Redirect URIs', add the exact URI shown above")
    print("5. Save your changes\n")
    
    response = input("Have you registered this redirect URI in the developer portal? (y/n): ")
    if response.lower() != 'y':
        print("\nPlease register the redirect URI first, then run this script again.")
        sys.exit(1)

def start_auth_server():
    """Start the authorization server and return the server object"""
    try:
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, OAuthCallbackHandler)
        print(f"Server started at http://localhost:8000")
        return httpd
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        if "Only one usage of each socket address" in str(e):
            print("\nPort 8000 is already in use. Please close any applications using this port and try again.")
        sys.exit(1)

def get_authorization_code():
    global auth_code, auth_error
    
    # Start the server first
    httpd = start_auth_server()
    
    # Construct the authorization URL with properly encoded parameters
    state = "state" + str(int(time.time()))  # Generate a unique state value
    
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "state": state
    }
    
    # Properly encode the URL parameters
    auth_url_params = urllib.parse.urlencode(auth_params)
    auth_url = f"{AUTH_URL}?{auth_url_params}"
    
    print(f"Opening browser to authorize the app...")
    print(f"Authorization URL: {auth_url}")
    
    # Open the browser
    try:
        webbrowser.open(auth_url)
    except Exception as e:
        print(f"Error opening browser: {str(e)}")
        print(f"Please manually open this URL in your browser: {auth_url}")
    
    print("Waiting for authorization (server listening on http://localhost:8000)...")
    print("If the browser doesn't open automatically, please copy and paste the URL above into your browser.")
    print("You may need to log in to your QuickBooks account and authorize the application.")
    
    # Handle one request
    try:
        httpd.handle_request()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    
    # Check if we got a code
    if auth_code:
        print("Authorization code received!")
        return auth_code
    elif auth_error:
        print(f"Authorization failed with error: {auth_error}")
        if "invalid_client" in auth_error:
            print("\nThis error typically occurs when your Client ID or Client Secret is incorrect.")
            print("Please verify your credentials in the QuickBooks Developer Portal.")
        elif "redirect_uri_mismatch" in auth_error:
            print("\nThis error occurs when the redirect URI in your code doesn't match what's registered in the QuickBooks Developer Portal.")
            print(f"Your code is using: {REDIRECT_URI}")
            print("Please make sure this exact URI is registered in the developer portal.")
        sys.exit(1)
    else:
        print("Failed to receive authorization code.")
        print("Please try again and make sure you complete the authorization process in the browser.")
        sys.exit(1)

def get_access_token(code, retry=True):
    # Encode client ID and secret for Basic Auth
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    
    # Prepare the token request
    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    print("\nSending token request to Intuit...")
    print(f"Token URL: {TOKEN_URL}")
    
    try:
        # Make the token request
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data
        else:
            print(f"Error getting access token: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text}")
            
            # Try to parse the error response
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
                
                # Check if the error is due to an expired code and retry if needed
                if retry and ("expired" in response.text.lower() or "invalid_grant" in response.text.lower()):
                    print("\nAuthorization code may have expired. Trying to get a new one...")
                    new_code = get_authorization_code()
                    return get_access_token(new_code, retry=False)  # Prevent infinite recursion
            except:
                pass
                
            sys.exit(1)
    except Exception as e:
        print(f"Exception during token request: {str(e)}")
        sys.exit(1)

def test_token(access_token):
    """Test the access token by making a simple API request"""
    print("\nTesting access token with a simple API request...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    # Try to get current user info as a simple test
    try:
        response = requests.get(
            "https://rest.tsheets.com/api/v1/current_user",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Token works! Retrieved current user information successfully.")
            return True
        else:
            print(f"❌ Token test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception during token test: {str(e)}")
        return False

def main():
    print("QuickBooks Time OAuth Helper")
    print("===========================")
    print(f"Client ID: {CLIENT_ID[:5]}...{CLIENT_ID[-5:]}")
    print(f"Client Secret: {CLIENT_SECRET[:5]}...{CLIENT_SECRET[-5:]}")
    print(f"Redirect URI: {REDIRECT_URI}")
    print(f"Scope: {SCOPE}")
    print("===========================")
    
    if CLIENT_ID == "YOUR_CLIENT_ID" or CLIENT_SECRET == "YOUR_CLIENT_SECRET":
        print("Error: You need to set your CLIENT_ID and CLIENT_SECRET in the script.")
        print("1. Register an app at https://developer.intuit.com/")
        print("2. Edit this script to set your client ID and secret")
        print("3. Run the script again")
        sys.exit(1)
    
    # Check if the redirect URI is registered
    check_redirect_uri_registration()
    
    try:
        # Get the authorization code
        code = get_authorization_code()
        
        print(f"\nAuthorization code: {code[:10]}...")
        
        # Exchange the code for an access token
        token_data = get_access_token(code)
        
        # Display the token information
        print("\nAccess Token Information:")
        print("========================")
        print(f"Access Token: {token_data['access_token'][:20]}...{token_data['access_token'][-20:]}")
        print(f"Refresh Token: {token_data['refresh_token'][:10]}...{token_data['refresh_token'][-10:]}")
        print(f"Expires In: {token_data['expires_in']} seconds")
        print(f"Token Type: {token_data.get('token_type', 'Bearer')}")
        
        # Test the token
        test_token(token_data['access_token'])
        
        # Save the token to a .env file
        with open(".env", "w") as f:
            f.write(f"QB_TIME_ACCESS_TOKEN={token_data['access_token']}\n")
            f.write("NODE_ENV=development\n")
        
        print("\nThe access token has been saved to .env file.")
        print("You can now run the QuickBooks Time MCP server.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 