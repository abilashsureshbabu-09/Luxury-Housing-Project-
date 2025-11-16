@echo off
REM Complete Git Push Script for Streamlit Cloud (Windows)
REM This script initializes git, commits all files, and pushes to GitHub

setlocal enabledelayedexpansion

echo.
echo 🚀 Pushing Luxury Housing Dashboard to GitHub
echo ==============================================
echo.

set REPO_URL=https://github.com/abilashsureshbabu-09/Luxury-Housing-Project-.git

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    exit /b 1
)

echo 📦 Step 1: Checking Git configuration...
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Git user not configured. Setting up...
    set /p git_user="Enter your GitHub username: "
    set /p git_email="Enter your GitHub email: "
    git config --global user.name "!git_user!"
    git config --global user.email "!git_email!"
    echo ✅ Git user configured
) else (
    echo ✅ Git user already configured
)

echo.
echo 📋 Step 2: Initializing Git repository...
if exist .git (
    echo ✅ Git repository already initialized
) else (
    git init
    echo ✅ Git initialized
)

echo.
echo 📝 Step 3: Staging all files...
git add .
echo ✅ Files staged

echo.
echo 💾 Step 4: Creating initial commit...
git commit -m "Initial commit: Luxury Housing Dashboard - Streamlit Cloud Ready"
if errorlevel 1 (
    echo ⚠️  Note: Repository may already have commits
)

echo.
echo 🔗 Step 5: Adding GitHub remote...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
echo ✅ Remote added: %REPO_URL%

echo.
echo 📤 Step 6: Pushing to GitHub...
echo Note: You may be prompted for GitHub credentials or to use SSH key
echo.

REM Try to set main branch if needed
git branch -M main 2>nul

REM Push to GitHub
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed. Please check:
    echo    1. You have internet connection
    echo    2. Your GitHub credentials are correct
    echo    3. The repository URL is correct
    echo    4. You have push permissions to the repository
    echo.
    echo 💡 Try authenticating with GitHub:
    echo    gh auth login
    pause
    exit /b 1
)

echo.
echo ==============================================
echo ✅ SUCCESS! Your project has been pushed to GitHub
echo ==============================================
echo.
echo 📊 Repository URL:
echo    %REPO_URL%
echo.
echo 🌐 Next Step - Deploy to Streamlit Cloud:
echo    1. Go to https://share.streamlit.io
echo    2. Click 'New app'
echo    3. Select your repository: abilashsureshbabu-09/Luxury-Housing-Project-
echo    4. Set main file path to: src/streamlit_app.py
echo    5. Click 'Deploy'
echo.
echo 📚 For more details, see DEPLOYMENT.md
echo ==============================================
pause
