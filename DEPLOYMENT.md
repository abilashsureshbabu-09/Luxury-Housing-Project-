# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions to deploy your Luxury Housing Dashboard to Streamlit Cloud.

## Prerequisites

- GitHub account (free)
- Streamlit Cloud account (free, sign up at [share.streamlit.io](https://share.streamlit.io))
- Your project pushed to a GitHub repository

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git (if not already done)

```bash
cd luxury_housing_project
git init
git add .
git commit -m "Initial commit: Luxury Housing Dashboard ready for Streamlit Cloud"
```

### 1.2 Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `luxury_housing_project` (or your preferred name)
3. Description: "Interactive Streamlit dashboard for luxury housing market analysis"
4. Choose "Public" (required for free Streamlit Cloud)
5. Click "Create repository"

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/luxury_housing_project.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Deploy on Streamlit Cloud

### 2.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" (or "Sign in" if you have an account)
3. Choose "Continue with GitHub"
4. Authorize Streamlit Cloud to access your GitHub repositories

### 2.2 Create New App

1. On the Streamlit Cloud dashboard, click **"New app"**
2. Fill in the deployment details:
   - **Repository**: Select `YOUR_USERNAME/luxury_housing_project`
   - **Branch**: `main`
   - **Main file path**: `src/streamlit_app.py`
3. Click **"Deploy"**

The deployment will start automatically. You'll see a log showing the build progress.

### 2.3 Wait for Deployment to Complete

- The app will build and deploy (usually takes 2-5 minutes)
- Once deployed, you'll see your app URL: `https://your-app-name.streamlit.app`
- Share this URL with anyone to view your dashboard!

## Step 3: Project Structure Verification

Ensure your GitHub repository has this structure:

```
luxury_housing_project/
├── src/
│   ├── streamlit_app.py          ← Main entry point for Streamlit Cloud
│   ├── data_cleaning.py
│   └── load_to_db.py
├── data/
│   └── cleaned_luxury_housing.csv  ← Required for app to work
├── .streamlit/
│   └── config.toml
├── requirements.txt                ← Must include all dependencies
├── .gitignore
├── README.md
└── DEPLOYMENT.md
```

## Step 4: Troubleshooting

### App shows "❌ Data file not found"

**Solution**: Ensure `data/cleaned_luxury_housing.csv` is committed to GitHub:

```bash
git add data/cleaned_luxury_housing.csv
git commit -m "Add cleaned data CSV"
git push
```

Then redeploy in Streamlit Cloud dashboard.

### Import Error: "No module named 'streamlit'"

**Solution**: Ensure `requirements.txt` contains all dependencies. Run from project root:

```bash
pip install -r requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Deployment Fails

**Solution**: 
1. Check the build logs in Streamlit Cloud dashboard
2. Common issues:
   - Missing `requirements.txt`
   - Wrong main file path (should be `src/streamlit_app.py`)
   - Uncommitted changes in GitHub repository

## Step 5: Managing Your Deployed App

### View Deployment Status
- Log in to [share.streamlit.io](https://share.streamlit.io)
- Click on your app to see logs and deployment history
- View app metrics and performance

### Update Your App

To push updates:

```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy your app with the new code!

### Delete Your App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click the three dots (...) on your app card
3. Select "Delete app"

## Step 6: Advanced Configuration

### Custom Domain (Streamlit for Teams)

Premium feature for custom domains like `app.yourcompany.com`

### Environment Variables

Add secrets in Streamlit Cloud:
1. Go to app settings (three dots)
2. Click "Manage secrets"
3. Add any API keys or database credentials needed

### Resource Allocation

- Free tier: 1 CPU, 512 MB RAM, 1 GB storage
- For larger deployments, consider Streamlit for Teams

## Step 7: Share Your App

Your deployed app is now live! Share the URL:
- **Direct Link**: `https://your-app-name.streamlit.app`
- **Embed in Website**: Use the embed code from Streamlit Cloud settings
- **Social Media**: Share the link on any platform

## Step 8: Monitoring and Maintenance

### Regular Updates

Keep your app maintained:
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Test locally
streamlit run src/streamlit_app.py

# Push changes
git add .
git commit -m "Update dependencies and features"
git push
```

### View App Logs

In Streamlit Cloud dashboard:
1. Click on your app
2. View real-time logs of user interactions and errors
3. Monitor CPU and memory usage

## Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud/get-started
- **GitHub Guides**: https://guides.github.com
- **Streamlit Community**: https://discuss.streamlit.io

## Example Deployment URL

After deployment, your app will be accessible at:
```
https://luxury-housing-dashboard.streamlit.app
```

Share this URL with colleagues, clients, or the public!

---

**Need Help?**
- Check [Streamlit Community Forums](https://discuss.streamlit.io)
- Review [GitHub Actions logs](https://github.com/YOUR_USERNAME/luxury_housing_project/actions) for deployment issues
- Contact Streamlit support at support@streamlit.io
