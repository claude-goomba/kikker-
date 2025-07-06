# Kikker Band Ticket System Backend

Dit is de Python Flask backend voor het Kikker band ticket systeem.

## Installatie

1. Maak een virtuele omgeving aan:
```bash
python3 -m venv venv
```

2. Activeer de virtuele omgeving:
```bash
# Op Linux/Mac:
source venv/bin/activate

# Op Windows:
venv\Scripts\activate
```

3. Installeer de vereiste packages:
```bash
pip install -r requirements.txt
```

## Backend Starten

1. Ga naar de backend directory:
```bash
cd kikker-website/backend
```

2. Start de Flask applicatie:
```bash
python app.py
```

De backend draait nu op http://localhost:5000

## API Endpoints

### Publieke Endpoints:
- `GET /api/events` - Haal alle evenementen op
- `GET /api/events/<id>` - Haal specifiek evenement op
- `POST /api/orders` - Maak nieuwe ticket bestelling
- `GET /api/orders/<order_number>` - Haal bestelling op met bestelnummer
- `GET /api/health` - Health check

### Admin Endpoints:
- `GET /api/admin/orders` - Haal alle bestellingen op

## Database

De applicatie gebruikt SQLite met de volgende tabellen:
- **Event**: Evenement informatie (naam, datum, locatie, prijs, beschikbare tickets)
- **Order**: Bestellingen (klantgegevens, aantal tickets, totaalbedrag)

De database wordt automatisch aangemaakt als `tickets.db` bij het eerste opstarten.

## Voorbeeld Bestelling

```json
POST /api/orders
{
    "event_name": "Zomerfestival Groningen",
    "customer_name": "Jan Jansen",
    "customer_email": "jan@example.com",
    "customer_phone": "06-12345678",
    "ticket_quantity": 2
}
```

## Email Configuratie

Voor productie moet je de SMTP instellingen configureren in `app.py` om echte emails te versturen.

## Frontend Connectie

De frontend is geconfigureerd om te verbinden met http://localhost:5000. 
CORS is ingeschakeld om cross-origin requests toe te staan.