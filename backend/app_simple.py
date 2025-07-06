#!/usr/bin/env python3
"""
Simplified Kikker Band Ticket Backend
This version works without external dependencies
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import secrets
import string

# Database setup
DB_FILE = 'tickets.db'

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            price REAL NOT NULL,
            available_tickets INTEGER DEFAULT 100
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            event_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            ticket_quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'confirmed',
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    
    # Check if events exist
    cursor.execute('SELECT COUNT(*) FROM events')
    if cursor.fetchone()[0] == 0:
        # Add sample events
        events = [
            ("Zomerfestival Groningen", "15 Juli 2025 - 20:00", "Stadspark, Groningen", 25.0, 200),
            ("Havenfestival Rotterdam", "22 Juli 2025 - 19:30", "Wilhelminapier, Rotterdam", 30.0, 300)
        ]
        cursor.executemany(
            'INSERT INTO events (name, date, location, price, available_tickets) VALUES (?, ?, ?, ?, ?)',
            events
        )
    
    conn.commit()
    conn.close()

def generate_order_number():
    """Generate a unique order number"""
    chars = string.ascii_uppercase + string.digits
    return 'KKR-' + ''.join(secrets.choice(chars) for _ in range(8))

class TicketHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/events':
            self.get_events()
        elif parsed_path.path == '/api/admin/orders':
            self.get_all_orders()
        elif parsed_path.path == '/api/health':
            self.health_check()
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/orders':
            self.create_order()
        elif self.path == '/api/admin/events':
            self.create_event()
        else:
            self.send_error(404, 'Not Found')
    
    def send_json_response(self, data, status=200):
        """Send JSON response with CORS headers"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_events(self):
        """Get all events"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = []
        for row in cursor.fetchall():
            events.append({
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'location': row[3],
                'price': row[4],
                'available_tickets': row[5]
            })
        conn.close()
        self.send_json_response({'events': events})
    
    def get_all_orders(self):
        """Get all orders for admin"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, e.name as event_name 
            FROM orders o 
            JOIN events e ON o.event_id = e.id
            ORDER BY o.order_date DESC
        ''')
        orders = []
        for row in cursor.fetchall():
            orders.append({
                'order_number': row[1],
                'event': row[11],
                'customer_name': row[3],
                'customer_email': row[4],
                'ticket_quantity': row[6],
                'total_amount': row[7],
                'order_date': row[8],
                'status': row[9]
            })
        conn.close()
        self.send_json_response({'orders': orders})
    
    def create_order(self):
        """Create a new order"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Validate required fields
        required_fields = ['event_name', 'customer_name', 'customer_email', 'customer_phone', 'ticket_quantity']
        for field in required_fields:
            if field not in data:
                self.send_json_response({'error': f'Missing field: {field}'}, 400)
                return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Find event
        cursor.execute('SELECT * FROM events WHERE name = ?', (data['event_name'],))
        event = cursor.fetchone()
        if not event:
            conn.close()
            self.send_json_response({'error': 'Event not found'}, 404)
            return
        
        event_id, name, date, location, price, available = event
        ticket_quantity = int(data['ticket_quantity'])
        
        # Check availability
        if ticket_quantity > available:
            conn.close()
            self.send_json_response({'error': f'Only {available} tickets available'}, 400)
            return
        
        # Create order
        order_number = generate_order_number()
        total_amount = ticket_quantity * price
        
        cursor.execute('''
            INSERT INTO orders (order_number, event_id, customer_name, customer_email, 
                              customer_phone, ticket_quantity, total_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_number, event_id, data['customer_name'], data['customer_email'],
              data['customer_phone'], ticket_quantity, total_amount))
        
        # Update available tickets
        cursor.execute('UPDATE events SET available_tickets = ? WHERE id = ?',
                      (available - ticket_quantity, event_id))
        
        conn.commit()
        conn.close()
        
        self.send_json_response({
            'success': True,
            'order_number': order_number,
            'message': 'Order confirmed! Check your email for tickets.',
            'order_details': {
                'event': name,
                'date': date,
                'quantity': ticket_quantity,
                'total': total_amount
            }
        }, 201)
    
    def health_check(self):
        """Health check endpoint"""
        self.send_json_response({'status': 'healthy', 'service': 'Kikker Tickets API'})
    
    def create_event(self):
        """Create a new event (admin only)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Validate required fields
        required_fields = ['name', 'date', 'location', 'price', 'available_tickets']
        for field in required_fields:
            if field not in data:
                self.send_json_response({'error': f'Missing field: {field}'}, 400)
                return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO events (name, date, location, price, available_tickets)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['name'], data['date'], data['location'], 
                  float(data['price']), int(data['available_tickets'])))
            
            event_id = cursor.lastrowid
            conn.commit()
            
            self.send_json_response({
                'success': True,
                'message': 'Event created successfully',
                'event_id': event_id
            }, 201)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
        finally:
            conn.close()

def main():
    """Main function to start the server"""
    # Initialize database
    init_db()
    
    # Start server
    port = 5000
    server = HTTPServer(('localhost', port), TicketHandler)
    print(f"Kikker Band Ticket Backend gestart op http://localhost:{port}")
    print("Druk op Ctrl+C om te stoppen")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestopt")
        server.shutdown()

if __name__ == '__main__':
    main()