# 🐸 Kikker Band Website

Een complete website voor de Nederlandse band Kikker met ticket verkoop systeem en admin dashboard.

## 🚀 Quick Start

### Optie 1: Automatisch starten (Aanbevolen)

1. **Start de website**:
   ```bash
   cd kikker-website
   ./start_website.sh
   ```

2. **Start de backend** (in een nieuwe terminal):
   ```bash
   cd kikker-website
   ./start_backend.sh
   ```

### Optie 2: Handmatig starten

1. **Website server**:
   ```bash
   cd kikker-website
   python3 server.py
   ```

2. **Backend server**:
   ```bash
   cd kikker-website/backend
   python3 app_simple.py
   ```

## 🌐 Website Links

- **Hoofdwebsite**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin.html
- **Backend API**: http://localhost:5000

## ✨ Features

### 🎵 Hoofdwebsite
- **Hopping logo loading screen** met Kikker logo animatie
- **Auto-refresh events** elke 30 seconden
- **Ticket verkoop systeem** met real-time beschikbaarheid
- **Responsive design** voor alle apparaten
- **Smooth scrolling** navigatie

### 🛠️ Admin Dashboard
- **Event management** - Voeg nieuwe evenementen toe
- **Order tracking** - Bekijk alle ticket bestellingen
- **Real-time statistics** - Totaal omzet, tickets verkocht
- **Auto-refresh data** elke 30 seconden

### 🔧 Backend API
- **SQLite database** voor events en orders
- **REST API endpoints** voor alle functionaliteit
- **Order number generatie** (KKR-XXXXXXXX formaat)
- **Email confirmatie** systeem (klaar voor productie)

## 📱 Hoe te gebruiken

### Voor bezoekers:
1. Ga naar http://localhost:8000
2. Bekijk komende evenementen
3. Klik "Koop Tickets" voor een evenement
4. Vul je gegevens in
5. Bevestig je bestelling

### Voor beheerders:
1. Ga naar http://localhost:8000/admin.html
2. Bekijk alle bestellingen en statistieken
3. Klik "Nieuw Evenement Toevoegen"
4. Vul event details in
5. Nieuw evenement verschijnt automatisch op de hoofdsite

## 🎯 Live Updates

Het systeem werkt volledig real-time:
- **Nieuwe events** verschijnen automatisch binnen 30 seconden
- **Ticket verkoop** updates direct de beschikbaarheid
- **Admin dashboard** toont live statistieken
- **No refresh needed** - alles werkt automatisch!

## 📂 Project Structuur

```
kikker-website/
├── index.html              # Hoofdwebsite
├── admin.html              # Admin dashboard
├── styles.css              # Website styling
├── script.js               # Frontend JavaScript
├── kikker-logo.svg         # Band logo
├── server.py               # Website HTTP server
├── start_website.sh        # Website starter script
├── start_backend.sh        # Backend starter script
└── backend/
    ├── app_simple.py       # Backend API server
    ├── tickets.db          # SQLite database
    └── README.md           # Backend documentatie
```

## 🔧 Technische Details

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3 (geen externe dependencies)
- **Database**: SQLite
- **Server**: Python HTTP server met CORS support
- **Animaties**: CSS keyframes voor hopping logo

## 🎨 Design Features

- **Kikker thema**: Groen kleurenpallet passend bij de bandnaam
- **Hopping frog logo**: Leuke animatie tijdens loading
- **Professional layout**: Clean, modern design
- **Dutch language**: Volledig Nederlandse interface

## 🚨 Troubleshooting

### Website niet toegankelijk?
```bash
# Check of de website server draait
curl http://localhost:8000
```

### Backend errors?
```bash
# Check of de backend server draait
curl http://localhost:5000/api/health
```

### Poort al in gebruik?
```bash
# Vind welk proces de poort gebruikt
lsof -i :8000
lsof -i :5000
```

## 📈 Next Steps

Voor productie gebruik:
1. **HTTPS configuratie** voor veilige payments
2. **Echte email service** (SMTP configuratie)
3. **Payment gateway** integratie
4. **Professional hosting** setup
5. **Domain naam** registratie

---

**Gemaakt voor Kikker Band** 🐸🎵
*De sprankelende Nederlandse band die uw evenement onvergetelijk maakt!*