@echo off
REM Direct push to GitHub - Luxury Housing Project

set REPO_URL=https://github.com/abilashsureshbabu-09/Luxury-Housing-Project-.git

echo 🚀 Pushing to GitHub: %REPO_URL%
echo.

REM Initialize if needed
if not exist .git (
  echo Initializing git...
  git init
)

REM Configure git if needed
git config user.name "Abilash" 2>nul
git config user.email "abilash@example.com" 2>nul

REM Stage all files
echo Adding files...
git add -A

REM Commit
echo Committing...
git commit -m "Luxury Housing Dashboard - Streamlit Cloud Ready" --allow-empty

REM Add remote
git remote remove origin 2>nul
git remote add origin %REPO_URL%

REM Set main branch and push
echo Pushing to GitHub...
git branch -M main
git push -u origin main -f

if %errorlevel% equ 0 (
  echo.
  echo ✅ SUCCESS! Code pushed to GitHub
  echo 📊 Repository: %REPO_URL%
  echo.
  echo 🌐 Next: Deploy on Streamlit Cloud
  echo    1. Go to https://share.streamlit.io
  echo    2. Click 'New app'
  echo    3. Select: abilashsureshbabu-09/Luxury-Housing-Project-
  echo    4. Main file: src/streamlit_app.py
  echo    5. Click Deploy
  echo.
) else (
  echo ❌ Push failed - Check credentials and try again
)

pause
