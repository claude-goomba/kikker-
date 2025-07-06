#!/bin/bash

echo "🐸 GIT COMMANDS TO PUSH KIKKER WEBSITE"
echo "======================================"
echo ""
echo "Run these commands in your terminal (where git is available):"
echo ""

cat << 'EOF'
# Navigate to your kikker-website folder
cd /path/to/kikker-website

# Initialize git repository
git init

# Add all website files (excluding backend)
git add index.html
git add admin.html
git add styles.css
git add script.js
git add demo-config.js
git add kikker-logo.svg
git add README.md
git add GITHUB_PAGES_DEMO.md
git add DOMAIN_SETUP.md
git add CNAME
git add vercel.json
git add netlify.toml

# Create initial commit
git commit -m "🐸 Complete Kikker band website with hopping logo animations

Features:
- Hopping frog logo loading animations
- Professional Dutch band website
- Ticket purchasing system with demo mode
- Admin dashboard
- Real contact integration (email, phone, WhatsApp)
- Mobile responsive design
- Custom domain ready (kikker-website.nl)
- GitHub Pages demo ready"

# Set main branch
git branch -M main

# Add your GitHub repository
git remote add origin https://github.com/claude-goomba/kikker-.git

# Push to GitHub
git push -u origin main

echo ""
echo "✅ SUCCESS! Your Kikker website is now on GitHub!"
echo ""
echo "Next steps:"
echo "1. Go to https://github.com/claude-goomba/kikker-"
echo "2. Go to Settings → Pages"
echo "3. Source: 'Deploy from a branch' → 'main'"
echo "4. Your demo will be live at: https://claude-goomba.github.io/kikker-/"
echo ""
echo "🐸 Features that will work on GitHub Pages:"
echo "- Hopping logo loading animation"
echo "- Complete website design"
echo "- Ticket purchase forms with real contact info"
echo "- Admin dashboard demo"
echo "- WhatsApp integration for real bookings"
EOF