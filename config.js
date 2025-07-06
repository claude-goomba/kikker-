// Configuration for Kikker website
const CONFIG = {
    // Production settings
    PRODUCTION: {
        WEBSITE_URL: 'https://kikker-website.nl',
        BACKEND_URL: 'https://kikker-backend.herokuapp.com',
        API_BASE: 'https://kikker-backend.herokuapp.com/api'
    },
    
    // Development settings  
    DEVELOPMENT: {
        WEBSITE_URL: 'http://localhost:8000',
        BACKEND_URL: 'http://localhost:5000',
        API_BASE: 'http://localhost:5000/api'
    }
};

// Auto-detect environment
const IS_PRODUCTION = window.location.hostname === 'kikker-website.nl' || 
                     window.location.hostname === 'www.kikker-website.nl';

const CURRENT_CONFIG = IS_PRODUCTION ? CONFIG.PRODUCTION : CONFIG.DEVELOPMENT;

// Export for use in other scripts
window.KIKKER_CONFIG = CURRENT_CONFIG;