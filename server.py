#!/usr/bin/env python3
"""
Simple HTTP server for the Kikker band website
This allows easy sharing and access to the website
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

# Change to the website directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow backend communication
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    """Open the website in the default browser after a short delay"""
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    # Create the server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print("=" * 50)
        print("🐸 KIKKER BAND WEBSITE GESTART! 🐸")
        print("=" * 50)
        print(f"Website URL: http://localhost:{PORT}")
        print(f"Admin panel: http://localhost:{PORT}/admin.html")
        print("")
        print("BELANGRIJK: Zorg dat de backend ook draait!")
        print("In een andere terminal, run: cd backend && python3 app_simple.py")
        print("")
        print("Druk op Ctrl+C om de server te stoppen")
        print("=" * 50)
        
        # Open browser after 2 seconds
        Timer(2.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🐸 Kikker website gestopt. Tot ziens!")
            httpd.shutdown()