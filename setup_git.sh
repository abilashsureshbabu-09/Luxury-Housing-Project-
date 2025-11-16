#!/bin/bash

# Streamlit Cloud Deployment Setup Script
# This script initializes git and prepares your project for deployment

set -e

echo "🚀 Luxury Housing Dashboard - Git Setup"
echo "=========================================="
echo ""

# Check if git is already initialized
if [ -d .git ]; then
    echo "✅ Git repository already initialized"
else
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "📋 Staging files for commit..."
git add .

echo ""
echo "📝 Creating initial commit..."
git commit -m "Initial commit: Luxury Housing Dashboard ready for Streamlit Cloud deployment" || echo "⚠️  Commit failed - repository may already have commits"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo ""
echo "📌 Next Steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Add your GitHub repository as remote:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/luxury_housing_project.git"
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "4. Go to https://share.streamlit.io to deploy"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
echo "=========================================="
