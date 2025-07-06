from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import secrets
import string

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "tickets.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kikker-band-secret-key-2025'

db = SQLAlchemy(app)

# Database Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_tickets = db.Column(db.Integer, default=100)
    orders = db.relationship('Order', backref='event', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    ticket_quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')

# Create tables
with app.app_context():
    db.create_all()
    
    # Add sample events if they don't exist
    if Event.query.count() == 0:
        events = [
            Event(
                name="Zomerfestival Groningen",
                date="15 Juli 2025 - 20:00",
                location="Stadspark, Groningen",
                price=25.0,
                available_tickets=200
            ),
            Event(
                name="Havenfestival Rotterdam",
                date="22 Juli 2025 - 19:30",
                location="Wilhelminapier, Rotterdam",
                price=30.0,
                available_tickets=300
            )
        ]
        for event in events:
            db.session.add(event)
        db.session.commit()

# Helper functions
def generate_order_number():
    """Generate a unique order number"""
    chars = string.ascii_uppercase + string.digits
    return 'KKR-' + ''.join(secrets.choice(chars) for _ in range(8))

def send_confirmation_email(order, event):
    """Send confirmation email to customer"""
    # In production, you would configure real SMTP settings
    # For now, we'll just return success
    email_content = f"""
    Beste {order.customer_name},
    
    Bedankt voor uw bestelling bij Kikker!
    
    Bestelnummer: {order.order_number}
    Evenement: {event.name}
    Datum: {event.date}
    Locatie: {event.location}
    Aantal tickets: {order.ticket_quantity}
    Totaal bedrag: €{order.total_amount},-
    
    Uw tickets zijn bijgevoegd als PDF.
    
    Tot ziens bij het evenement!
    
    Met vriendelijke groet,
    Kikker Band
    """
    
    # In production, implement actual email sending
    print(f"Email would be sent to: {order.customer_email}")
    print(email_content)
    return True

# API Routes
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all available events"""
    events = Event.query.all()
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'location': event.location,
            'price': event.price,
            'available_tickets': event.available_tickets
        })
    return jsonify({'events': events_data})

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get specific event details"""
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'name': event.name,
        'date': event.date,
        'location': event.location,
        'price': event.price,
        'available_tickets': event.available_tickets
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new ticket order"""
    data = request.json
    
    # Validate required fields
    required_fields = ['event_name', 'customer_name', 'customer_email', 'customer_phone', 'ticket_quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Find event by name
    event = Event.query.filter_by(name=data['event_name']).first()
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Check ticket availability
    ticket_quantity = int(data['ticket_quantity'])
    if ticket_quantity > event.available_tickets:
        return jsonify({'error': f'Only {event.available_tickets} tickets available'}), 400
    
    # Calculate total amount
    total_amount = ticket_quantity * event.price
    
    # Create order
    order = Order(
        order_number=generate_order_number(),
        event_id=event.id,
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone'],
        ticket_quantity=ticket_quantity,
        total_amount=total_amount
    )
    
    # Update available tickets
    event.available_tickets -= ticket_quantity
    
    # Save to database
    db.session.add(order)
    db.session.commit()
    
    # Send confirmation email
    send_confirmation_email(order, event)
    
    return jsonify({
        'success': True,
        'order_number': order.order_number,
        'message': 'Order confirmed! Check your email for tickets.',
        'order_details': {
            'event': event.name,
            'date': event.date,
            'quantity': ticket_quantity,
            'total': total_amount
        }
    }), 201

@app.route('/api/orders/<string:order_number>', methods=['GET'])
def get_order(order_number):
    """Get order details by order number"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    event = Event.query.get(order.event_id)
    
    return jsonify({
        'order_number': order.order_number,
        'event': event.name,
        'date': event.date,
        'location': event.location,
        'customer_name': order.customer_name,
        'customer_email': order.customer_email,
        'ticket_quantity': order.ticket_quantity,
        'total_amount': order.total_amount,
        'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': order.status
    })

@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders():
    """Admin endpoint to get all orders"""
    orders = Order.query.all()
    orders_data = []
    
    for order in orders:
        event = Event.query.get(order.event_id)
        orders_data.append({
            'order_number': order.order_number,
            'event': event.name,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'ticket_quantity': order.ticket_quantity,
            'total_amount': order.total_amount,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': order.status
        })
    
    return jsonify({'orders': orders_data})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Kikker Tickets API'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)