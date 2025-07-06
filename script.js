// Global variables for ticket info
let currentEvent = '';
let currentDate = '';
let ticketPrice = 0;

// Mobile menu functions
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    
    navMenu.classList.toggle('active');
    menuToggle.classList.toggle('active');
}

function closeMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    
    navMenu.classList.remove('active');
    menuToggle.classList.remove('active');
}

// Open ticket modal
function openTicketModal(eventName, eventDate, price) {
    currentEvent = eventName;
    currentDate = eventDate;
    ticketPrice = price;
    
    // Update modal content
    document.querySelector('.event-name').textContent = eventName;
    document.querySelector('.event-date').textContent = eventDate;
    document.querySelector('.ticket-price').textContent = `Prijs per ticket: €${price},-`;
    
    // Reset form
    document.getElementById('ticketForm').reset();
    updateTotalPrice();
    
    // Show modal
    document.getElementById('ticketModal').style.display = 'block';
}

// Close ticket modal
function closeTicketModal() {
    document.getElementById('ticketModal').style.display = 'none';
}

// Update total price based on ticket amount
function updateTotalPrice() {
    const amount = document.getElementById('ticketAmount').value;
    const total = amount * ticketPrice;
    document.getElementById('totalPrice').textContent = `€${total},-`;
}

// Process ticket order
async function processTicketOrder(event) {
    event.preventDefault();
    
    const amount = document.getElementById('ticketAmount').value;
    const name = document.getElementById('customerName').value;
    const email = document.getElementById('customerEmail').value;
    const phone = document.getElementById('customerPhone').value;
    const total = amount * ticketPrice;
    
    // Prepare order data
    const orderData = {
        event_name: currentEvent,
        customer_name: name,
        customer_email: email,
        customer_phone: phone,
        ticket_quantity: parseInt(amount)
    };
    
    try {
        let result;
        
        if (window.IS_DEMO) {
            // Use demo API for GitHub Pages
            result = await window.DEMO_API.createOrder(orderData);
        } else {
            // Send order to real backend
            const response = await fetch(`${window.KIKKER_CONFIG.API_BASE}/orders`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderData)
            });
            
            result = await response.json();
        }
        
        if (result.success) {
            // Close ticket modal
            closeTicketModal();
            
            // Show confirmation with order number or demo message
            let orderDetails;
            
            if (result.is_demo) {
                orderDetails = `
                    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 1rem; margin-bottom: 1rem;">
                        <h3 style="color: #856404; margin: 0 0 1rem 0;">🐸 Dit is een Demo!</h3>
                        <p style="color: #856404; margin: 0;">Voor <strong>echte tickets</strong> voor ${currentEvent}, neem contact op met Kikker:</p>
                    </div>
                    
                    <div style="background-color: #e8f5e9; border: 1px solid #4caf50; border-radius: 5px; padding: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: #2c5530; margin: 0 0 1rem 0;">📞 Contact Kikker Band:</h4>
                        <p style="margin: 0.5rem 0;"><strong>📧 Email:</strong> <a href="mailto:${result.contact_info.email}" style="color: #2c5530;">${result.contact_info.email}</a></p>
                        <p style="margin: 0.5rem 0;"><strong>📱 Telefoon:</strong> <a href="tel:${result.contact_info.phone}" style="color: #2c5530;">${result.contact_info.phone}</a></p>
                        <p style="margin: 0.5rem 0;"><strong>📋 WhatsApp:</strong> <a href="https://wa.me/31612345678?text=Hallo%2C%20ik%20wil%20graag%20tickets%20voor%20${encodeURIComponent(currentEvent)}" target="_blank" style="color: #2c5530;">Stuur WhatsApp</a></p>
                    </div>
                    
                    <div style="background-color: #f8f8f8; padding: 1rem; border-radius: 5px;">
                        <p><strong>Uw aanvraag:</strong></p>
                        <p>📅 <strong>Evenement:</strong> ${currentEvent}</p>
                        <p>🗓️ <strong>Datum:</strong> ${currentDate}</p>
                        <p>🎫 <strong>Aantal tickets:</strong> ${amount}</p>
                        <p>💰 <strong>Totaal bedrag:</strong> €${total},-</p>
                        <p>📧 <strong>Uw email:</strong> ${email}</p>
                    </div>
                `;
            } else {
                orderDetails = `
                    <strong>Bestelnummer:</strong> ${result.order_number}<br>
                    <strong>Evenement:</strong> ${currentEvent}<br>
                    <strong>Datum:</strong> ${currentDate}<br>
                    <strong>Aantal tickets:</strong> ${amount}<br>
                    <strong>Totaal bedrag:</strong> €${total},-<br>
                    <strong>Email:</strong> ${email}<br><br>
                    <em>Controleer uw email voor de tickets!</em>
                `;
            }
            
            document.querySelector('.order-details').innerHTML = orderDetails;
            document.getElementById('confirmationModal').style.display = 'block';
        } else {
            // Show error message
            alert(`Er is een fout opgetreden: ${result.error || 'Probeer het later opnieuw.'}`);
        }
    } catch (error) {
        console.error('Error processing order:', error);
        alert('Er is een fout opgetreden bij het verwerken van uw bestelling. Probeer het later opnieuw.');
    }
}

// Close confirmation modal
function closeConfirmationModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const ticketModal = document.getElementById('ticketModal');
    const confirmationModal = document.getElementById('confirmationModal');
    const navMenu = document.querySelector('.nav-menu');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    
    if (event.target == ticketModal) {
        closeTicketModal();
    }
    if (event.target == confirmationModal) {
        closeConfirmationModal();
    }
    
    // Close mobile menu when clicking outside
    if (navMenu && navMenu.classList.contains('active')) {
        if (!event.target.closest('.nav-menu') && !event.target.closest('.mobile-menu-toggle')) {
            closeMobileMenu();
        }
    }
}

// Show loading screen
function showLoading() {
    const loadingScreen = document.getElementById('loadingScreen');
    const pageContent = document.getElementById('pageContent');
    
    if (loadingScreen) {
        loadingScreen.classList.remove('hidden');
    }
    if (pageContent) {
        pageContent.classList.remove('loaded');
    }
}

// Hide loading screen
function hideLoading() {
    const loadingScreen = document.getElementById('loadingScreen');
    const pageContent = document.getElementById('pageContent');
    
    setTimeout(() => {
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
        if (pageContent) {
            pageContent.classList.add('loaded');
        }
    }, 1000); // Show loading for at least 1 second
}

// Load events from backend or demo data
async function loadEvents(showLoadingScreen = false) {
    if (showLoadingScreen) {
        showLoading();
    }
    
    try {
        let data;
        
        if (window.IS_DEMO) {
            // Use demo data for GitHub Pages
            data = await window.DEMO_API.getEvents();
        } else {
            // Use real backend
            const response = await fetch(`${window.KIKKER_CONFIG.API_BASE}/events`);
            data = await response.json();
        }
        
        if (data.events && data.events.length > 0) {
            const performanceGrid = document.querySelector('.performance-grid');
            performanceGrid.innerHTML = '';
            
            data.events.forEach(event => {
                const eventCard = document.createElement('div');
                eventCard.className = 'performance-card';
                eventCard.innerHTML = `
                    <h3>${event.name}</h3>
                    <p class="date">${event.date}</p>
                    <p class="location">${event.location}</p>
                    <p class="type">Festival</p>
                    <p class="price">€${event.price},- per ticket</p>
                    <p class="availability">Nog ${event.available_tickets} tickets beschikbaar</p>
                    <button class="buy-ticket-btn" onclick="openTicketModal('${event.name}', '${event.date}', ${event.price})">Koop Tickets</button>
                `;
                performanceGrid.appendChild(eventCard);
            });
            
            // Add private event (not from database)
            const privateEvent = document.createElement('div');
            privateEvent.className = 'performance-card';
            privateEvent.innerHTML = `
                <h3>Bedrijfsfeest Amsterdam</h3>
                <p class="date">5 Augustus 2025 - 21:00</p>
                <p class="location">Privé locatie</p>
                <p class="type">Besloten evenement</p>
                <p class="price">Alleen op uitnodiging</p>
            `;
            performanceGrid.appendChild(privateEvent);
        }
        
        if (showLoadingScreen) {
            hideLoading();
        }
    } catch (error) {
        console.error('Error loading events:', error);
        if (showLoadingScreen) {
            hideLoading();
        }
    }
}

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    
    // Load events on page load with loading screen
    loadEvents(true);
    
    // Refresh events every 30 seconds (without loading screen)
    setInterval(() => loadEvents(false), 30000);
});