#!/bin/bash
# Direct push to GitHub - Luxury Housing Project

cd "$(dirname "$0")" || exit

REPO_URL="https://github.com/abilashsureshbabu-09/Luxury-Housing-Project-.git"

echo "🚀 Pushing to GitHub: $REPO_URL"
echo ""

# Initialize if needed
if [ ! -d .git ]; then
  echo "Initializing git..."
  git init
fi

# Configure git if needed
if ! git config user.name &>/dev/null; then
  git config user.name "Abilash"
  git config user.email "abilash@example.com"
fi

# Stage all files
echo "Adding files..."
git add -A

# Commit
echo "Committing..."
git commit -m "Luxury Housing Dashboard - Streamlit Cloud Ready" --allow-empty

# Add remote
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

# Set main branch and push
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main -f

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ SUCCESS! Code pushed to GitHub"
  echo "📊 Repository: $REPO_URL"
  echo ""
  echo "🌐 Next: Deploy on Streamlit Cloud"
  echo "   1. Go to https://share.streamlit.io"
  echo "   2. Click 'New app'"
  echo "   3. Select: abilashsureshbabu-09/Luxury-Housing-Project-"
  echo "   4. Main file: src/streamlit_app.py"
  echo "   5. Click Deploy"
  echo ""
else
  echo "❌ Push failed - Check credentials and try again"
fi
