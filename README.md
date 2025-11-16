# Luxury Housing Dashboard - Bangalore

An interactive Streamlit dashboard for analyzing the luxury housing market in Bangalore. Visualize property prices, distributions, and key metrics with an intuitive web interface.

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/luxury_housing_project.git
   cd luxury_housing_project
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run src/streamlit_app.py
   ```

The dashboard will open at `http://localhost:8501`

## 📊 Features

- **Interactive Price Analysis**: Filter and analyze luxury housing prices
- **Statistical Insights**: View distribution, median, average, and max prices
- **Data Visualization**: Histograms, box plots, and comprehensive statistics
- **Data Overview**: Explore dataset structure and data types
- **Raw Data Access**: Download and inspect raw data directly in the dashboard

## 📁 Project Structure

```
luxury_housing_project/
├── src/
│   ├── streamlit_app.py        # Main Streamlit application
│   ├── data_cleaning.py        # Data cleaning script
│   └── load_to_db.py           # Database loading script
├── data/
│   └── cleaned_luxury_housing.csv
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore file
├── README.md                  # This file
└── DEPLOYMENT.md              # Deployment instructions
```

## 🌐 Deploy to Streamlit Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Streamlit Cloud.

### Quick Deploy:
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repository
4. Set main file to `src/streamlit_app.py`
5. Deploy!

## 🛠 Data Pipeline

### 1. Clean Data
Run the data cleaning script to standardize and prepare the raw data:
```bash
python src/data_cleaning.py --input data/Luxury_Housing_Bangalore.csv --output data/cleaned_luxury_housing.csv
```

### 2. Load to Database
Load cleaned data to a database:
```bash
python src/load_to_db.py --input data/cleaned_luxury_housing.csv --db_url sqlite:///data/luxury_housing.sqlite
```

## 📋 Requirements

- Python 3.8+
- Streamlit >= 1.28.0
- Pandas >= 1.5.0
- Plotly >= 5.14.0
- NumPy >= 1.24.0
- SQLAlchemy >= 2.0.0

## 🔧 Configuration

The `.streamlit/config.toml` file contains Streamlit settings:
- Theme colors and fonts
- Client configurations
- Server settings
- Logging level

## 📝 Notes

- Data is cached for 1 hour to improve performance
- The app supports both local file paths and cloud deployments
- Missing values are automatically checked and reported

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---
**Last Updated**: November 2025

