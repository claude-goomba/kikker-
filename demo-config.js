// Demo Configuration for GitHub Pages
// This version provides demo data when backend is not available

const DEMO_EVENTS = [
    {
        id: 1,
        name: "Zomerfestival Groningen",
        date: "15 Juli 2025 - 20:00",
        location: "Stadspark, Groningen",
        price: 25.0,
        available_tickets: 180
    },
    {
        id: 2,
        name: "Havenfestival Rotterdam", 
        date: "22 Juli 2025 - 19:30",
        location: "Wilhelminapier, Rotterdam",
        price: 30.0,
        available_tickets: 250
    },
    {
        id: 3,
        name: "Muziekfestival Utrecht",
        date: "10 Augustus 2025 - 21:00", 
        location: "Griftpark, Utrecht",
        price: 28.0,
        available_tickets: 320
    }
];

const DEMO_ORDERS = [
    {
        order_number: "KKR-DEMO001",
        event: "Zomerfestival Groningen",
        customer_name: "Jan Jansen",
        customer_email: "jan@example.com",
        ticket_quantity: 2,
        total_amount: 50.0,
        order_date: "2025-07-01 14:30:00",
        status: "confirmed"
    },
    {
        order_number: "KKR-DEMO002", 
        event: "Havenfestival Rotterdam",
        customer_name: "Marie de Vries",
        customer_email: "marie@example.com",
        ticket_quantity: 4,
        total_amount: 120.0,
        order_date: "2025-07-02 16:45:00",
        status: "confirmed"
    },
    {
        order_number: "KKR-DEMO003",
        event: "Muziekfestival Utrecht", 
        customer_name: "Piet Bakker",
        customer_email: "piet@example.com",
        ticket_quantity: 1,
        total_amount: 28.0,
        order_date: "2025-07-03 09:15:00",
        status: "confirmed"
    }
];

// Configuration for demo vs production
const CONFIG = {
    PRODUCTION: {
        WEBSITE_URL: 'https://kikker-website.nl',
        BACKEND_URL: 'https://kikker-backend.herokuapp.com',
        API_BASE: 'https://kikker-backend.herokuapp.com/api',
        USE_DEMO_DATA: false
    },
    
    GITHUB_PAGES: {
        WEBSITE_URL: window.location.origin,
        BACKEND_URL: null,
        API_BASE: null, 
        USE_DEMO_DATA: true
    },
    
    DEVELOPMENT: {
        WEBSITE_URL: 'http://localhost:8000',
        BACKEND_URL: 'http://localhost:5000',
        API_BASE: 'http://localhost:5000/api',
        USE_DEMO_DATA: false
    }
};

// Auto-detect environment
function detectEnvironment() {
    const hostname = window.location.hostname;
    
    if (hostname.includes('github.io') || hostname.includes('githubpages')) {
        return 'GITHUB_PAGES';
    } else if (hostname === 'kikker-website.nl' || hostname === 'www.kikker-website.nl') {
        return 'PRODUCTION';
    } else {
        return 'DEVELOPMENT';
    }
}

const CURRENT_ENV = detectEnvironment();
const CURRENT_CONFIG = CONFIG[CURRENT_ENV];

// Demo API functions for GitHub Pages
window.DEMO_API = {
    async getEvents() {
        return { events: DEMO_EVENTS };
    },
    
    async createOrder(orderData) {
        const orderNumber = 'KKR-DEMO' + Math.random().toString(36).substr(2, 6).toUpperCase();
        return {
            success: true,
            order_number: orderNumber,
            message: 'Dit is een demo! Voor echte tickets, neem contact op met Kikker.',
            is_demo: true,
            contact_info: {
                email: 'info@kikkerband.nl',
                phone: '06-12345678',
                booking_form: 'https://forms.gle/kikker-booking'
            },
            order_details: {
                event: orderData.event_name,
                date: DEMO_EVENTS.find(e => e.name === orderData.event_name)?.date || 'Demo datum',
                quantity: orderData.ticket_quantity,
                total: orderData.ticket_quantity * (DEMO_EVENTS.find(e => e.name === orderData.event_name)?.price || 25)
            }
        };
    },
    
    async getOrders() {
        return { orders: DEMO_ORDERS };
    },
    
    async createEvent(eventData) {
        return {
            success: true,
            message: 'Demo evenement toegevoegd! In productie zou dit opgeslagen worden.',
            event_id: Math.floor(Math.random() * 1000)
        };
    }
};

// Export configuration
window.KIKKER_CONFIG = CURRENT_CONFIG;
window.IS_DEMO = CURRENT_CONFIG.USE_DEMO_DATA;

console.log(`🐸 Kikker Website - Environment: ${CURRENT_ENV}`, CURRENT_CONFIG);