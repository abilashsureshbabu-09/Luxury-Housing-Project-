#!/bin/bash

# Complete Git Push Script for Streamlit Cloud
# This script initializes git, commits all files, and pushes to GitHub

set -e

echo "🚀 Pushing Luxury Housing Dashboard to GitHub"
echo "=============================================="
echo ""

REPO_URL="https://github.com/abilashsureshbabu-09/Luxury-Housing-Project-.git"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "📦 Step 1: Checking Git configuration..."
# Check git user configuration
if ! git config --global user.name &> /dev/null; then
    echo "⚠️  Git user not configured. Setting up..."
    read -p "Enter your GitHub username: " git_user
    read -p "Enter your GitHub email: " git_email
    git config --global user.name "$git_user"
    git config --global user.email "$git_email"
    echo "✅ Git user configured"
else
    echo "✅ Git user already configured: $(git config --global user.name)"
fi

echo ""
echo "📋 Step 2: Initializing Git repository..."
if [ -d .git ]; then
    echo "✅ Git repository already initialized"
else
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "📝 Step 3: Staging all files..."
git add .
echo "✅ Files staged"

echo ""
echo "💾 Step 4: Creating initial commit..."
git commit -m "Initial commit: Luxury Housing Dashboard - Streamlit Cloud Ready

- Streamlit configuration (.streamlit/config.toml)
- Cloud-compatible app (src/streamlit_app.py)
- Complete documentation (README.md, DEPLOYMENT.md)
- All dependencies in requirements.txt
- Ready for Streamlit Cloud deployment" || echo "⚠️  Note: Repository may already have commits"

echo ""
echo "🔗 Step 5: Adding GitHub remote..."
# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "✅ Remote added: $REPO_URL"

echo ""
echo "📤 Step 6: Pushing to GitHub..."
echo "Note: You may be prompted for GitHub credentials or to use SSH key"
echo ""

# Try to push with main branch
git branch -M main 2>/dev/null || true
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "✅ SUCCESS! Your project has been pushed to GitHub"
    echo "=============================================="
    echo ""
    echo "📊 Repository URL:"
    echo "   $REPO_URL"
    echo ""
    echo "🌐 Next Step - Deploy to Streamlit Cloud:"
    echo "   1. Go to https://share.streamlit.io"
    echo "   2. Click 'New app'"
    echo "   3. Select your repository: abilashsureshbabu-09/Luxury-Housing-Project-"
    echo "   4. Set main file path to: src/streamlit_app.py"
    echo "   5. Click 'Deploy'"
    echo ""
    echo "📚 For more details, see DEPLOYMENT.md"
    echo "=============================================="
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. You have internet connection"
    echo "   2. Your GitHub credentials are correct"
    echo "   3. The repository URL is correct"
    echo "   4. You have push permissions to the repository"
    echo ""
    echo "💡 Try authenticating with GitHub:"
    echo "   gh auth login"
    exit 1
fi
