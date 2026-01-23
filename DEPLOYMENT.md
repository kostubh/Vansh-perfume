# Deployment Guide for PUREN

## Quick Start - Local Development

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to that URL

## Deploying to Streamlit Cloud (Free)

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Push this code to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Puren luxury perfume website"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select:
   - **Repository:** Your GitHub repo
   - **Branch:** main
   - **Main file path:** app.py
5. Click "Deploy"
6. Wait 2-3 minutes for deployment to complete

### Step 3: Access Your Live App

- Your app will be available at: `https://YOUR_USERNAME-YOUR_REPO-RANDOM.streamlit.app`
- Share this URL with customers!

## Deploying to Other Platforms

### Heroku

1. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Google Cloud Run / AWS / Azure

Use the official Streamlit Docker image:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Environment Variables (Optional)

For future enhancements with payment processing or email:

```bash
STRIPE_API_KEY=your_key_here
SENDGRID_API_KEY=your_key_here
```

Add these in Streamlit Cloud under "Advanced settings" → "Secrets"

## Custom Domain (Optional)

### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Update your DNS records as instructed

### Recommended DNS Settings:
- Type: CNAME
- Name: www (or your subdomain)
- Value: Your Streamlit app URL

## Performance Optimization

1. **Caching**: Already implemented with `@st.cache_data`
2. **Images**: Using external URLs (Unsplash) for fast loading
3. **Session State**: Efficient state management implemented

## Monitoring

- **Streamlit Cloud**: Built-in analytics available in dashboard
- **Google Analytics**: Add tracking code to `app.py` if needed

## Security Considerations

- No sensitive data stored in session state
- All external images from trusted sources (Unsplash)
- No user authentication required for browsing

## Troubleshooting

### Common Issues:

1. **Module not found:**
   - Ensure all packages are in `requirements.txt`
   - Run `pip install -r requirements.txt`

2. **Port already in use:**
   - Kill existing Streamlit processes
   - Or specify different port: `streamlit run app.py --server.port=8502`

3. **Slow loading:**
   - Check internet connection (images load from Unsplash)
   - Consider caching images locally if needed

## Updating the Live App

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Streamlit Cloud will auto-redeploy in 1-2 minutes

## Support

For Streamlit-specific issues:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)

---

**Ready to launch your luxury perfume brand!**
