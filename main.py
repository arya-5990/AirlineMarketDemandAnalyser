import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import numpy as np
import time
from typing import Dict, List, Optional, Tuple
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Load environment variables
load_dotenv()

# Page configuration with dark theme
st.set_page_config(
    page_title="✈️ Airline Market Demand Analyzer | Professional Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/airline-analyzer',
        'Report a bug': "https://github.com/yourusername/airline-analyzer/issues",
        'About': "# Airline Market Demand Analyzer\n\nProfessional dashboard for analyzing airline market trends, demand patterns, and revenue optimization opportunities.\n\nBuilt with Streamlit, Plotly, and AI-powered insights."
    }
)

# Set Streamlit theme to dark
st.markdown("""
<style>
    /* Override Streamlit's default theme */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* Force dark theme on page load */
    .main .block-container {
        background-color: #0e1117 !important;
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)

# Apply dark theme
st.markdown("""
<style>
    /* Dark theme base colors */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1c23;
        --bg-tertiary: #262730;
        --text-primary: #fafafa;
        --text-secondary: #c1c1c1;
        --accent-primary: #00d4aa;
        --accent-secondary: #ff4b4b;
        --border-color: #3a3a3a;
        --shadow-color: rgba(0, 0, 0, 0.3);
    }
    
    /* Global dark theme */
    .main .block-container {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: var(--text-primary) !important;
    }
    
    /* Streamlit default elements */
    .stMarkdown, .stText, .stDataFrame {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar dark theme */
    .css-1d391kg, .css-1lcbmhc {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }
    
    .css-1d391kg .css-1lcbmhc {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Sidebar text */
    .css-1d391kg .css-1lcbmhc .css-1lcbmhc {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar widgets */
    .stSelectbox, .stSlider, .stDateInput, .stButton {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Main header styling with dark theme */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px var(--shadow-color);
    }
    
    /* Metric cards with dark theme */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px var(--shadow-color);
        backdrop-filter: blur(4px);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-card h3 {
        color: var(--text-primary);
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: var(--accent-primary);
    }
    
    /* Insight boxes with dark theme */
    .insight-box {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px var(--shadow-color);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
        color: var(--text-primary);
    }
    
    /* Chart containers with dark theme */
    .chart-container {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px var(--shadow-color);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Tab styling with dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--bg-secondary);
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--bg-tertiary);
        border-radius: 4px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-primary);
        color: var(--bg-primary);
        font-weight: bold;
    }
    
    /* Button styling with dark theme */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        color: var(--bg-primary);
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.6);
    }
    
    /* Dataframe styling with dark theme */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 4px 15px var(--shadow-color);
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }
    
    /* Dataframe headers and cells */
    .dataframe th {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    
    .dataframe td {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Custom scrollbar with dark theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00b894 0%, #e74c3c 100%);
    }
    
    /* Streamlit specific elements */
    .stAlert {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSuccess {
        background-color: rgba(0, 212, 170, 0.1) !important;
        border: 1px solid var(--accent-primary) !important;
        color: var(--accent-primary) !important;
    }
    
    .stInfo {
        background-color: rgba(0, 123, 255, 0.1) !important;
        border: 1px solid #007bff !important;
        color: #007bff !important;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid #ffc107 !important;
        color: #ffc107 !important;
    }
    
    .stError {
        background-color: rgba(220, 53, 69, 0.1) !important;
        border: 1px solid #dc3545 !important;
        color: #dc3545 !important;
    }
    
    /* Plotly chart backgrounds */
    .js-plotly-plot {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Additional dark theme improvements */
    .stExpander {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stExpander > div > div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit metrics styling */
    .stMetric {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        color: var(--text-primary) !important;
    }
    
    .stMetric > div > div {
        color: var(--text-primary) !important;
    }
    
    .stMetric > div > div > div {
        color: var(--text-primary) !important;
    }
    
    /* Streamlit spinner styling */
    .stSpinner > div {
        color: var(--accent-primary) !important;
    }
    
    /* Streamlit info/warning/error boxes */
    .stAlert > div {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Dataframe specific dark theme */
    .stDataFrame > div > div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Ensure all text is visible */
    .stMarkdown > div > div {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar text color override */
    .css-1d391kg .css-1lcbmhc .css-1lcbmhc {
        color: var(--text-primary) !important;
    }
    
    /* Force dark theme on all elements */
    * {
        color: var(--text-primary) !important;
    }
    
    /* Override Streamlit's default white backgrounds */
    .stApp > div > div > div > div > div > div {
        background-color: var(--bg-primary) !important;
    }
</style>
""", unsafe_allow_html=True)



# Constants
AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Sample data for demonstration when APIs are not available
SAMPLE_CITIES = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
    'Miami', 'Atlanta', 'Denver', 'Seattle', 'Portland'
]

def generate_sample_data(days: int = 30) -> pd.DataFrame:
    """
    Generate sample airline data for demonstration purposes.
    
    Args:
        days: Number of days to generate data for
        
    Returns:
        DataFrame with sample airline data
    """
    np.random.seed(42)
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    # Define popular routes that should always have flights
    popular_routes = [
        ('New York', 'Los Angeles'),
        ('New York', 'Chicago'),
        ('Los Angeles', 'Chicago'),
        ('Chicago', 'Miami'),
        ('Denver', 'Seattle'),
        ('New York', 'Miami'),
        ('Los Angeles', 'Miami'),
        ('Atlanta', 'New York'),
        ('Dallas', 'Los Angeles'),
        ('Houston', 'Chicago')
    ]
    
    for date in dates:
        # Generate 20-50 flights per day
        num_flights = np.random.randint(20, 51)
        
        # Ensure popular routes always have at least 1 flight per day
        for departure, destination in popular_routes:
            # Random flight details
            airline = np.random.choice(['American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue'])
            flight_number = f"{airline[:2].upper()}{np.random.randint(100, 9999)}"
            
            # Simulate price based on route popularity and date
            base_price = np.random.uniform(200, 800)
            # Weekend and holiday premiums
            if date.weekday() >= 5:  # Weekend
                base_price *= 1.3
            # Summer months premium
            if date.month in [6, 7, 8]:
                base_price *= 1.2
            price = round(base_price + np.random.uniform(-50, 100), 2)
            
            # Random capacity and occupancy
            capacity = np.random.randint(100, 300)
            occupancy = np.random.randint(50, capacity)
            
            data.append({
                'date': date,
                'departure_city': departure,
                'destination_city': destination,
                'airline': airline,
                'flight_number': flight_number,
                'price': price,
                'capacity': capacity,
                'occupancy': occupancy,
                'route': f"{departure} → {destination}"
            })
        
        # Generate additional random flights
        remaining_flights = num_flights - len(popular_routes)
        for _ in range(remaining_flights):
            # Random route
            departure = np.random.choice(SAMPLE_CITIES)
            destination = np.random.choice([city for city in SAMPLE_CITIES if city != departure])
            
            # Random flight details
            airline = np.random.choice(['American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue'])
            flight_number = f"{airline[:2].upper()}{np.random.randint(100, 9999)}"
            
            # Simulate price based on route popularity and date
            base_price = np.random.uniform(200, 800)
            # Weekend and holiday premiums
            if date.weekday() >= 5:  # Weekend
                base_price *= 1.3
            # Summer months premium
            if date.month in [6, 7, 8]:
                base_price *= 1.2
            price = round(base_price + np.random.uniform(-50, 100), 2)
            
            # Random capacity and occupancy
            capacity = np.random.randint(100, 300)
            occupancy = np.random.randint(50, capacity)
            
            data.append({
                'date': date,
                'departure_city': departure,
                'destination_city': destination,
                'airline': airline,
                'flight_number': flight_number,
                'price': price,
                'capacity': capacity,
                'occupancy': occupancy,
                'route': f"{departure} → {destination}"
            })
    
    df = pd.DataFrame(data)
    st.info(f"📊 Generated {len(df)} sample flights for demonstration")
    return df

def fetch_aviationstack_data() -> Optional[pd.DataFrame]:
    """
    Fetch data from AviationStack API.
    
    Returns:
        DataFrame with flight data or None if API is not available
    """
    if not AVIATIONSTACK_API_KEY:
        return None
    
    try:
        # AviationStack API endpoint
        url = "http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': AVIATIONSTACK_API_KEY,
            'limit': 100  # Free tier limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and data['data']:
                flights = []
                for flight in data['data']:
                    if flight.get('departure') and flight.get('arrival'):
                        flights.append({
                            'date': datetime.now().date(),
                            'departure_city': flight['departure'].get('airport', 'Unknown'),
                            'destination_city': flight['arrival'].get('airport', 'Unknown'),
                            'airline': flight.get('airline', {}).get('name', 'Unknown'),
                            'flight_number': flight.get('flight', {}).get('iata', 'Unknown'),
                            'price': np.random.uniform(200, 800),  # Simulated price
                            'capacity': np.random.randint(100, 300),
                            'occupancy': np.random.randint(50, 300),
                            'route': f"{flight['departure'].get('airport', 'Unknown')} → {flight['arrival'].get('airport', 'Unknown')}"
                        })
                
                return pd.DataFrame(flights)
        
        return None
        
    except Exception as e:
        st.warning(f"AviationStack API error: {e}")
        return None

def fetch_opensky_data() -> Optional[pd.DataFrame]:
    """
    Fetch data from OpenSky Network API.
    
    Returns:
        DataFrame with flight data or None if API is not available
    """
    try:
        # OpenSky Network API endpoint (no API key required for basic usage)
        end_time = int(time.time())
        start_time = end_time - (24 * 60 * 60)  # Last 24 hours
        
        url = f"https://opensky-network.org/api/flights/all"
        params = {
            'begin': start_time,
            'end': end_time
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                flights = []
                for flight in data[:100]:  # Limit to 100 flights
                    if flight.get('estDepartureAirport') and flight.get('estArrivalAirport'):
                        flights.append({
                            'date': datetime.fromtimestamp(flight.get('firstSeen', time.time())).date(),
                            'departure_city': flight['estDepartureAirport'],
                            'destination_city': flight['estArrivalAirport'],
                            'airline': flight.get('callsign', 'Unknown')[:3],
                            'flight_number': flight.get('callsign', 'Unknown'),
                            'price': np.random.uniform(200, 800),  # Simulated price
                            'capacity': np.random.randint(100, 300),
                            'occupancy': np.random.randint(50, 300),
                            'route': f"{flight['estDepartureAirport']} → {flight['estArrivalAirport']}"
                        })
                
                return pd.DataFrame(flights)
        
        return None
        
    except Exception as e:
        st.warning(f"OpenSky API error: {e}")
        return None

def fetch_flight_data() -> pd.DataFrame:
    """
    Fetch flight data from available APIs or generate sample data.
    
    Returns:
        DataFrame with flight data
    """
    # Try AviationStack API first
    df = fetch_aviationstack_data()
    
    if df is not None and not df.empty:
        st.success("✅ Data fetched from AviationStack API")
        return df
    
    # Try OpenSky Network API
    df = fetch_opensky_data()
    
    if df is not None and not df.empty:
        st.success("✅ Data fetched from OpenSky Network API")
        return df
    
    # Generate sample data if no APIs available
    st.info("📊 Using sample data for demonstration (no API keys configured)")
    sample_df = generate_sample_data()
    st.success(f"✅ Sample data generated successfully: {len(sample_df)} flights")
    return sample_df

def process_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Process the flight data to extract insights.
    
    Args:
        df: Raw flight data DataFrame
        
    Returns:
        Tuple of (processed DataFrame, insights dictionary)
    """
    # Make a copy to avoid modifying original
    processed_df = df.copy()
    
    # Convert date to datetime if it's not already
    if 'date' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['date'])
    
    # Calculate additional metrics if required columns exist
    if 'occupancy' in processed_df.columns and 'capacity' in processed_df.columns:
        processed_df['occupancy_rate'] = (processed_df['occupancy'] / processed_df['capacity'] * 100).round(2)
    else:
        processed_df['occupancy_rate'] = 0
    
    if 'price' in processed_df.columns and 'occupancy' in processed_df.columns:
        processed_df['revenue'] = processed_df['price'] * processed_df['occupancy']
    else:
        processed_df['revenue'] = 0
    
    # Extract insights
    insights = {}
    
    # Top 5 popular routes
    if 'route' in processed_df.columns and not processed_df.empty:
        route_counts = processed_df['route'].value_counts().head(5)
        insights['popular_routes'] = route_counts.to_dict()
    else:
        insights['popular_routes'] = {}
    
    # Price trends over time
    if 'date' in processed_df.columns and 'price' in processed_df.columns and not processed_df.empty:
        daily_avg_price = processed_df.groupby('date')['price'].mean().reset_index()
        insights['price_trends'] = daily_avg_price
    else:
        insights['price_trends'] = pd.DataFrame()
    
    # High-demand periods
    if 'date' in processed_df.columns and not processed_df.empty:
        daily_flights = processed_df.groupby('date').size().reset_index(name='flight_count')
        insights['demand_periods'] = daily_flights
    else:
        insights['demand_periods'] = pd.DataFrame()
    
    # Average prices by route
    if 'route' in processed_df.columns and 'price' in processed_df.columns and not processed_df.empty:
        route_prices = processed_df.groupby('route')['price'].mean().sort_values(ascending=False).head(10)
        insights['route_prices'] = route_prices.to_dict()
    else:
        insights['route_prices'] = {}
    
    # Occupancy analysis
    if 'occupancy_rate' in processed_df.columns:
        insights['avg_occupancy'] = processed_df['occupancy_rate'].mean()
    else:
        insights['avg_occupancy'] = 0
    
    insights['total_flights'] = len(processed_df)
    
    if 'revenue' in processed_df.columns:
        insights['total_revenue'] = processed_df['revenue'].sum()
    else:
        insights['total_revenue'] = 0
    
    return processed_df, insights

def create_charts(df: pd.DataFrame, insights: Dict) -> None:
    """
    Create and display interactive charts using Plotly with professional styling.
    
    Args:
        df: Processed flight data DataFrame
        insights: Dictionary containing processed insights
    """
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Interactive Charts & Analytics")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different chart types
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Popular Routes", "💰 Price Trends", "📈 Demand Patterns", "🛫 Route Analysis", "🎯 Market Overview"])
    
    with tab1:
        # Popular routes chart with improved styling
        if 'popular_routes' in insights and insights['popular_routes']:
            routes_df = pd.DataFrame(list(insights['popular_routes'].items()), 
                                   columns=['Route', 'Flight Count'])
            
            fig = px.bar(routes_df, x='Route', y='Flight Count',
                        title="Top 5 Most Popular Routes",
                        color='Flight Count',
                        color_continuous_scale='viridis',
                        template='plotly_dark')
            
            # Enhanced chart styling with dark theme
            fig.update_layout(
                title_font_size=20,
                title_font_color='#fafafa',
                plot_bgcolor='#1a1c23',
                paper_bgcolor='#1a1c23',
                xaxis=dict(
                    title="Route",
                    title_font_size=16,
                    tickfont_size=12,
                    tickangle=-45,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                yaxis=dict(
                    title="Number of Flights",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                margin=dict(l=50, r=50, t=80, b=100),
                height=500
            )
            
            # Add hover template
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Flights: %{y}<extra></extra>",
                marker_line_color='white',
                marker_line_width=2
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
        else:
            st.info("📊 No route data available for visualization.")
    
    with tab2:
        # Price trends chart with improved styling
        if 'price_trends' in insights and not insights['price_trends'].empty:
            fig = px.line(insights['price_trends'], x='date', y='price',
                         title="Average Price Trends Over Time",
                         labels={'price': 'Average Price ($)', 'date': 'Date'},
                         template='plotly_dark')
            
            # Enhanced chart styling with dark theme
            fig.update_layout(
                title_font_size=20,
                title_font_color='#fafafa',
                plot_bgcolor='#1a1c23',
                paper_bgcolor='#1a1c23',
                xaxis=dict(
                    title="Date",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                yaxis=dict(
                    title="Average Price ($)",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                margin=dict(l=50, r=50, t=80, b=80),
                height=500
            )
            
            # Add hover template and line styling with dark theme colors
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>",
                line=dict(width=3, color='#00d4aa'),
                mode='lines+markers',
                marker=dict(size=6, color='#667eea')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
        else:
            st.info("💰 No price trend data available for visualization.")
    
    with tab3:
        # Demand patterns chart with improved styling
        if 'demand_periods' in insights and not insights['demand_periods'].empty:
            fig = px.bar(insights['demand_periods'], x='date', y='flight_count',
                        title="Daily Flight Demand Patterns",
                        labels={'flight_count': 'Number of Flights', 'date': 'Date'},
                        template='plotly_dark')
            
            # Enhanced chart styling with dark theme
            fig.update_layout(
                title_font_size=20,
                title_font_color='#fafafa',
                plot_bgcolor='#1a1c23',
                paper_bgcolor='#1a1c23',
                xaxis=dict(
                    title="Date",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                yaxis=dict(
                    title="Number of Flights",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                margin=dict(l=50, r=50, t=80, b=80),
                height=500
            )
            
            # Add hover template and bar styling with dark theme colors
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Flights: %{y}<extra></extra>",
                marker_color='#00d4aa',
                marker_line_color='#1a1c23',
                marker_line_width=2
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
        else:
            st.info("📈 No demand pattern data available for visualization.")
    
    with tab4:
        # Route price analysis with improved styling
        if 'route_prices' in insights and insights['route_prices']:
            route_prices_df = pd.DataFrame(list(insights['route_prices'].items()),
                                         columns=['Route', 'Average Price'])
            route_prices_df = route_prices_df.head(10)
            
            fig = px.bar(route_prices_df, x='Route', y='Average Price',
                        title="Average Prices by Route (Top 10)",
                        color='Average Price',
                        color_continuous_scale='plasma',
                        template='plotly_dark')
            
            # Enhanced chart styling with dark theme
            fig.update_layout(
                title_font_size=20,
                title_font_color='#fafafa',
                plot_bgcolor='#1a1c23',
                paper_bgcolor='#1a1c23',
                xaxis=dict(
                    title="Route",
                    title_font_size=16,
                    tickfont_size=12,
                    tickangle=-45,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                yaxis=dict(
                    title="Average Price ($)",
                    title_font_size=16,
                    tickfont_size=12,
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title_font_color='#fafafa',
                    tickfont_color='#c1c1c1'
                ),
                margin=dict(l=50, r=50, t=80, b=100),
                height=500
            )
            
            # Add hover template with dark theme colors
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>",
                marker_line_color='#1a1c23',
                marker_line_width=2
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
        else:
            st.info("🛫 No route price data available for visualization.")
    
    with tab5:
        # Market overview dashboard
        st.subheader("🎯 Market Overview Dashboard")
        
        # Create a summary grid
        col1, col2 = st.columns(2)
        
        with col1:
            if 'avg_occupancy' in insights:
                st.metric(
                    label="Average Occupancy Rate",
                    value=f"{insights['avg_occupancy']:.1f}%",
                    delta=f"{insights['avg_occupancy'] - 70:.1f}%" if insights['avg_occupancy'] > 70 else f"{insights['avg_occupancy'] - 70:.1f}%"
                )
            
            if 'total_revenue' in insights:
                st.metric(
                    label="Total Revenue",
                    value=f"${insights['total_revenue']:,.0f}",
                    delta=f"${insights['total_revenue'] * 0.1:,.0f}"
                )
        
        with col2:
            if 'total_flights' in insights:
                st.metric(
                    label="Total Flights",
                    value=f"{insights['total_flights']:,}",
                    delta=f"{insights['total_flights'] * 0.05:.0f}"
                )
            
            if 'route_prices' in insights and insights['route_prices']:
                avg_price = np.mean(list(insights['route_prices'].values()))
                st.metric(
                    label="Average Route Price",
                    value=f"${avg_price:.0f}",
                    delta=f"${avg_price * 0.05:.0f}"
                )
        
        # Additional insights
        if 'popular_routes' in insights and insights['popular_routes']:
            st.subheader("🏆 Top Performing Routes")
            top_routes = pd.DataFrame(list(insights['popular_routes'].items())[:3], 
                                    columns=['Route', 'Flight Count'])
            st.dataframe(top_routes, use_container_width=True, hide_index=True)

def display_tables(df: pd.DataFrame, insights: Dict) -> None:
    """
    Display data tables with enhanced styling.
    
    Args:
        df: Processed flight data DataFrame
        insights: Dictionary containing processed insights
    """
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 Data Tables & Export")
    st.markdown("</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Raw Data", "🛫 Route Summary", "📅 Daily Summary", "📈 Performance Metrics"])
    
    with tab1:
        if not df.empty:
            st.markdown("**📊 Raw Flight Data**")
            st.markdown(f"*Showing {len(df)} records*")
            
            # Enhanced dataframe with better styling
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "price": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
                    "occupancy_rate": st.column_config.NumberColumn("Occupancy (%)", format="%.1f%%"),
                    "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.2f")
                }
            )
            
            # Enhanced download section
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"airline_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Excel export (if openpyxl is available)
                try:
                    import openpyxl
                    from io import BytesIO
                    
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Flight Data', index=False)
                        # Add summary sheet
                        if 'route' in df.columns:
                            route_summary = df.groupby('route').agg({
                                'price': ['mean', 'min', 'max'],
                                'occupancy_rate': 'mean',
                                'flight_number': 'count'
                            }).round(2)
                            route_summary.to_excel(writer, sheet_name='Route Summary')
                    
                    buffer.seek(0)
                    st.download_button(
                        label="📊 Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"airline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except ImportError:
                    st.info("💡 Install openpyxl for Excel export: `pip install openpyxl`")
        else:
            st.info("📊 No data available to display.")
    
    with tab2:
        # Enhanced route summary table
        if 'route' in df.columns and not df.empty:
            try:
                st.markdown("**🛫 Route Performance Summary**")
                
                agg_dict = {}
                if 'price' in df.columns:
                    agg_dict['price'] = ['mean', 'min', 'max']
                if 'occupancy_rate' in df.columns:
                    agg_dict['occupancy_rate'] = 'mean'
                if 'flight_number' in df.columns:
                    agg_dict['flight_number'] = 'count'
                if 'revenue' in df.columns:
                    agg_dict['revenue'] = 'sum'
                
                if agg_dict:
                    route_summary = df.groupby('route').agg(agg_dict).round(2)
                    # Flatten column names
                    route_summary.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in route_summary.columns]
                    route_summary = route_summary.sort_values('flight_number_count' if 'flight_number_count' in route_summary.columns else route_summary.columns[0], ascending=False)
                    
                    # Add performance indicators
                    if 'price_mean' in route_summary.columns and 'occupancy_rate_mean' in route_summary.columns:
                        route_summary['performance_score'] = (
                            (route_summary['price_mean'] / route_summary['price_mean'].max()) * 0.4 +
                            (route_summary['occupancy_rate_mean'] / 100) * 0.6
                        ).round(3)
                    
                    st.dataframe(route_summary, use_container_width=True, hide_index=True)
                else:
                    st.info("📊 No data available for route summary.")
            except Exception as e:
                st.error(f"❌ Unable to generate route summary: {str(e)}")
        else:
            st.info("🛫 No route data available for summary.")
    
    with tab3:
        # Enhanced daily summary table
        if 'date' in df.columns and not df.empty:
            try:
                st.markdown("**📅 Daily Performance Summary**")
                
                agg_dict = {}
                if 'price' in df.columns:
                    agg_dict['price'] = 'mean'
                if 'occupancy_rate' in df.columns:
                    agg_dict['occupancy_rate'] = 'mean'
                if 'flight_number' in df.columns:
                    agg_dict['flight_number'] = 'count'
                if 'revenue' in df.columns:
                    agg_dict['revenue'] = 'sum'
                
                if agg_dict:
                    daily_summary = df.groupby('date').agg(agg_dict).round(2)
                    
                    # Add day of week for better analysis
                    daily_summary['day_of_week'] = daily_summary.index.day_name()
                    daily_summary['weekend'] = daily_summary.index.weekday >= 5
                    
                    st.dataframe(daily_summary, use_container_width=True, hide_index=True)
                else:
                    st.info("📅 No data available for daily summary.")
            except Exception as e:
                st.error(f"❌ Unable to generate daily summary: {str(e)}")
        else:
            st.info("📅 No date data available for daily summary.")
    
    with tab4:
        # Performance metrics dashboard
        st.markdown("**📈 Performance Metrics Dashboard**")
        
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'price' in df.columns:
                    st.metric("💰 Price Performance", 
                             f"${df['price'].mean():.2f}",
                             f"{df['price'].std():.2f}")
                
                if 'occupancy_rate' in df.columns:
                    st.metric("👥 Occupancy Performance",
                             f"{df['occupancy_rate'].mean():.1f}%",
                             f"{df['occupancy_rate'].std():.1f}%")
            
            with col2:
                if 'revenue' in df.columns:
                    st.metric("💵 Revenue Performance",
                             f"${df['revenue'].sum():,.0f}",
                             f"${df['revenue'].mean():.0f}/flight")
                
                if 'route' in df.columns:
                    st.metric("🛫 Route Diversity",
                             f"{df['route'].nunique()}",
                             f"{df['airline'].nunique()} airlines")
            
            # Performance trends
            if 'date' in df.columns and len(df) > 1:
                st.markdown("**📊 Performance Trends**")
                
                # Calculate trends
                if 'price' in df.columns:
                    price_trend = df.groupby('date')['price'].mean()
                    if len(price_trend) > 1:
                        price_change = (price_trend.iloc[-1] - price_trend.iloc[0]) / price_trend.iloc[0] * 100
                        if price_change > 0:
                            st.success(f"📈 Average price increased by {price_change:.1f}%")
                        elif price_change < 0:
                            st.error(f"📉 Average price decreased by {abs(price_change):.1f}%")
                        else:
                            st.info("➡️ Average price remained stable")
        else:
            st.info("📈 No data available for performance metrics.")

def generate_insights(insights: Dict) -> str:
    """
    Generate natural language insights from the data.
    
    Args:
        insights: Dictionary containing processed insights
        
    Returns:
        String with natural language insights
    """
    insight_text = []
    
    # Popular routes
    if 'popular_routes' in insights and insights['popular_routes']:
        try:
            top_route = list(insights['popular_routes'].keys())[0]
            top_count = list(insights['popular_routes'].values())[0]
            insight_text.append(f"🎯 **Most Popular Route**: {top_route} with {top_count} flights")
        except (IndexError, KeyError):
            insight_text.append("🎯 **Popular Routes**: No route data available")
    else:
        insight_text.append("🎯 **Popular Routes**: No route data available")
    
    # Price analysis
    if 'route_prices' in insights and insights['route_prices']:
        try:
            avg_price = np.mean(list(insights['route_prices'].values()))
            insight_text.append(f"💰 **Average Route Price**: ${avg_price:.2f}")
        except (ValueError, TypeError):
            insight_text.append("💰 **Average Route Price**: No price data available")
    else:
        insight_text.append("💰 **Average Route Price**: No price data available")
    
    # Demand analysis
    if 'demand_periods' in insights and not insights['demand_periods'].empty:
        try:
            max_demand_date = insights['demand_periods'].loc[insights['demand_periods']['flight_count'].idxmax(), 'date']
            max_demand_count = insights['demand_periods']['flight_count'].max()
            insight_text.append(f"📈 **Peak Demand**: {max_demand_date.strftime('%Y-%m-%d')} with {max_demand_count} flights")
        except (KeyError, IndexError):
            insight_text.append("📈 **Peak Demand**: No demand data available")
    else:
        insight_text.append("📈 **Peak Demand**: No demand data available")
    
    # Overall statistics
    if 'total_flights' in insights:
        insight_text.append(f"✈️ **Total Flights Analyzed**: {insights.get('total_flights', 0):,}")
    
    if 'avg_occupancy' in insights and not pd.isna(insights.get('avg_occupancy')):
        insight_text.append(f"👥 **Average Occupancy Rate**: {insights['avg_occupancy']:.1f}%")
    else:
        insight_text.append("👥 **Average Occupancy Rate**: No occupancy data available")
    
    if 'total_revenue' in insights:
        insight_text.append(f"💵 **Total Revenue**: ${insights.get('total_revenue', 0):,.2f}")
    
    return "\n\n".join(insight_text)

def generate_gemini_insights(insights: Dict, df: pd.DataFrame) -> str:
    """
    Generate AI-powered insights using Google Gemini API.
    
    Args:
        insights: Dictionary containing processed insights
        df: Processed DataFrame with flight data
        
    Returns:
        String with AI-generated insights
    """
    try:
        if not GEMINI_API_KEY:
            return "🤖 Gemini AI not configured. Please add your API key to use AI-powered insights."
        
        # Prepare data summary for Gemini
        data_summary = {
            'total_flights': len(df),
            'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}" if 'date' in df.columns else "Unknown",
            'airlines': df['airline'].nunique() if 'airline' in df.columns else 0,
            'routes': df['route'].nunique() if 'route' in df.columns else 0,
            'avg_price': f"${df['price'].mean():.2f}" if 'price' in df.columns else "N/A",
            'avg_occupancy': f"{df['occupancy_rate'].mean():.1f}%" if 'occupancy_rate' in df.columns else "N/A"
        }
        
        prompt = f"""
        Analyze this airline market data and provide 3-5 key business insights:
        
        Data Summary:
        - Total Flights: {data_summary['total_flights']}
        - Date Range: {data_summary['date_range']}
        - Airlines: {data_summary['airlines']}
        - Routes: {data_summary['routes']}
        - Average Price: {data_summary['avg_price']}
        - Average Occupancy: {data_summary['avg_occupancy']}
        
        Please provide:
        1. Market trends and patterns
        2. Revenue optimization opportunities
        3. Route performance analysis
        4. Competitive insights
        5. Recommendations for airlines
        
        Format as bullet points with clear, actionable insights.
        """
        
        # Initialize Gemini
        import google.generativeai as genai
        
        # Configure Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response.text:
            return f"🤖 **AI-Powered Insights**\n\n{response.text}"
        else:
            return "🤖 **AI Insights**: Unable to generate insights at this time."
            
    except ImportError:
        return "🤖 **AI Insights**: Google Generative AI library not installed. Run: `pip install google-generativeai`"
    except Exception as e:
        return f"🤖 **AI Insights**: Error generating insights: {str(e)}"

def export_report(df: pd.DataFrame, insights: Dict, format_type: str = "csv") -> bytes:
    """
    Export flight data and insights in various formats.
    
    Args:
        df: Processed DataFrame with flight data
        insights: Dictionary containing processed insights
        format_type: Export format ("csv", "excel", or "pdf")
        
    Returns:
        Bytes object containing the exported file
    """
    try:
        if format_type == "csv":
            # Export filtered data to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            csv_buffer.close()
            return csv_data
            
        elif format_type == "excel":
            # Export to Excel with multiple sheets
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Flight Data', index=False)
                
                # Insights summary sheet
                insights_df = pd.DataFrame([
                    ['Total Flights', insights.get('total_flights', 0)],
                    ['Average Price', f"${insights.get('avg_price', 0):.2f}"],
                    ['Average Occupancy', f"{insights.get('avg_occupancy', 0):.1f}%"],
                    ['Total Revenue', f"${insights.get('total_revenue', 0):,.2f}"],
                    ['Unique Airlines', insights.get('unique_airlines', 0)],
                    ['Unique Routes', insights.get('unique_routes', 0)]
                ], columns=['Metric', 'Value'])
                insights_df.to_excel(writer, sheet_name='Insights Summary', index=False)
                
                # Popular routes sheet
                if 'popular_routes' in insights and insights['popular_routes']:
                    routes_df = pd.DataFrame(list(insights['popular_routes'].items()), 
                                          columns=['Route', 'Flight Count'])
                    routes_df.to_excel(writer, sheet_name='Popular Routes', index=False)
                
                # Price analysis sheet
                if 'route_prices' in insights and insights['route_prices']:
                    prices_df = pd.DataFrame(list(insights['route_prices'].items()), 
                                           columns=['Route', 'Average Price'])
                    prices_df.to_excel(writer, sheet_name='Route Prices', index=False)
            
            excel_buffer.seek(0)
            return excel_buffer.getvalue()
            
        elif format_type == "pdf":
            # Create a comprehensive PDF report
            pdf_buffer = io.BytesIO()
            
            # Create PDF using reportlab
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=getSampleStyleSheet()['Title'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("✈️ Airline Market Demand Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", getSampleStyleSheet()['Heading1']))
            story.append(Spacer(1, 12))
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Flights', str(insights.get('total_flights', 0))],
                ['Date Range', f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}" if 'date' in df.columns else "N/A"],
                ['Average Price', f"${insights.get('avg_price', 0):.2f}"],
                ['Average Occupancy', f"{insights.get('avg_occupancy', 0):.1f}%"],
                ['Total Revenue', f"${insights.get('total_revenue', 0):,.2f}"]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Key Insights
            story.append(Paragraph("Key Insights", getSampleStyleSheet()['Heading1']))
            story.append(Spacer(1, 12))
            
            if 'popular_routes' in insights and insights['popular_routes']:
                story.append(Paragraph("Most Popular Routes:", getSampleStyleSheet()['Heading2']))
                for i, (route, count) in enumerate(list(insights['popular_routes'].items())[:5]):
                    story.append(Paragraph(f"{i+1}. {route}: {count} flights", getSampleStyleSheet()['Normal']))
                story.append(Spacer(1, 12))
            
            if 'route_prices' in insights and insights['route_prices']:
                story.append(Paragraph("Route Price Analysis:", getSampleStyleSheet()['Heading2']))
                avg_price = np.mean(list(insights['route_prices'].values()))
                story.append(Paragraph(f"Average route price: ${avg_price:.2f}", getSampleStyleSheet()['Normal']))
                story.append(Spacer(1, 12))
            
            # Data Sample
            story.append(Paragraph("Data Sample (First 10 Records)", getSampleStyleSheet()['Heading1']))
            story.append(Spacer(1, 12))
            
            # Convert DataFrame to table format for PDF
            sample_df = df.head(10)
            if not sample_df.empty:
                # Get column names
                cols = list(sample_df.columns)
                table_data = [cols]  # Header row
                
                # Add data rows
                for _, row in sample_df.iterrows():
                    table_data.append([str(val) for val in row.values])
                
                data_table = Table(table_data)
                data_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                story.append(data_table)
            
            # Build PDF
            doc.build(story)
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()
            
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
    except Exception as e:
        st.error(f"Export error: {str(e)}")
        return None

def main():
    """
    Main function to run the Streamlit application.
    """
    # Initialize session state for data persistence
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Header
    st.markdown('<h1 class="main-header">✈️ Airline Market Demand Analyzer</h1>', unsafe_allow_html=True)
    
    # Theme toggle button
    st.sidebar.markdown("**🎨 Theme**")
    if st.sidebar.button("🌙 Dark Theme", use_container_width=True, key="dark_theme"):
        st.info("🌙 Dark theme is now active! The application will use a dark color scheme for better visibility.")
    
    st.sidebar.markdown("---")
    
    # Enhanced Sidebar with better styling
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 1rem; margin-bottom: 1rem;">
        <h2 style="color: white; text-align: center; margin: 0;">🔍 Data Filters</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range filter with better styling
    st.sidebar.markdown("**📅 Date Range**")
    default_start = datetime.now() - timedelta(days=30)
    default_end = datetime.now()
    
    start_date = st.sidebar.date_input("Start Date", value=default_start, key="start_date")
    end_date = st.sidebar.date_input("End Date", value=default_end, key="end_date")
    
    # City filters with enhanced styling
    st.sidebar.markdown("**🌍 City Filters**")
    all_cities = sorted(list(set(SAMPLE_CITIES)))
    
    departure_city = st.sidebar.selectbox("Departure City", ["All"] + all_cities, key="departure_city")
    destination_city = st.sidebar.selectbox("Destination City", ["All"] + all_cities, key="destination_city")
    
    # Show guaranteed routes info
    st.sidebar.info("💡 **Guaranteed Routes:** New York → Los Angeles, Chicago → Miami, Denver → Seattle")
    
    # Quick actions
    st.sidebar.markdown("**⚡ Quick Actions**")
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    # Export functionality (moved to after data processing)
    st.sidebar.markdown("**📊 Export Report**")
    export_format = st.sidebar.selectbox(
        "Export Format",
        ["CSV", "Excel", "PDF"],
        key="export_format",
        index=0  # Default to CSV
    )
    
    # Data source info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**ℹ️ Data Source**")
    if AVIATIONSTACK_API_KEY:
        st.sidebar.success("✅ AviationStack API")
    elif GEMINI_API_KEY:
        st.sidebar.info("🤖 Gemini AI Enabled")
    else:
        st.sidebar.warning("📊 Sample Data Mode")
    
    # Debug info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🐛 Debug Info**")
    if 'df' in st.session_state and st.session_state.df is not None:
        st.sidebar.info(f"📊 Raw data: {len(st.session_state.df)} flights")
        if not st.session_state.df.empty:
            st.sidebar.success("✅ Data loaded successfully")
        else:
            st.sidebar.error("❌ Data is empty")
    else:
        st.sidebar.warning("⚠️ No data in session state")
    
    # Fetch data
    with st.spinner("🔄 Fetching airline data..."):
        df = fetch_flight_data()
    
    # Store DataFrame in session state for export functionality
    st.session_state.df = df
    
    # Debug: Show data info
    st.sidebar.info(f"📊 Data loaded: {len(df)} flights")
    
    if df.empty:
        st.error("No data available. Please check your API configuration or try again later.")
        return
    
    # Additional filters (moved here after df is created)
    st.sidebar.markdown("**✈️ Flight Filters**")
    
    # Price range filter
    if 'price' in df.columns:
        # Filter out None/NaN values for price calculations
        price_values = df['price'].dropna()
        if not price_values.empty:
            min_price = float(price_values.min())
            max_price = float(price_values.max())
        else:
            min_price, max_price = 0, 1000
        
        price_range = st.sidebar.slider(
            "Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            key="price_range"
        )
    
    # Airline filter
    if 'airline' in df.columns:
        # Filter out None values and convert to list before sorting
        airline_values = [str(airline) for airline in df['airline'].unique() if airline is not None and pd.notna(airline)]
        all_airlines = ["All"] + sorted(airline_values)
        selected_airline = st.sidebar.selectbox("Airline", all_airlines, key="airline_filter")
    
    # Process data first to create occupancy_rate column
    with st.spinner("🔄 Processing data..."):
        processed_df, insights = process_data(df)
        st.sidebar.info(f"📊 Processed data: {len(processed_df)} flights, {len(insights)} insights")
    
    # Now create filters using the processed data
    # Occupancy filter (now occupancy_rate column exists)
    if 'occupancy_rate' in processed_df.columns:
        # Filter out None/NaN values for occupancy calculations
        occupancy_values = processed_df['occupancy_rate'].dropna()
        if not occupancy_values.empty:
            min_occupancy = float(occupancy_values.min())
            max_occupancy = float(occupancy_values.max())
        else:
            min_occupancy, max_occupancy = 0, 100
        
        occupancy_range = st.sidebar.slider(
            "Occupancy Rate (%)",
            min_value=min_occupancy,
            max_value=max_occupancy,
            value=(min_occupancy, max_occupancy),
            key="occupancy_range"
        )
    
    # Apply filters with enhanced logic (using processed_df for filtering)
    initial_count = len(processed_df)
    
    if departure_city != "All":
        processed_df = processed_df[processed_df['departure_city'] == departure_city]
        st.sidebar.info(f"🔍 Filtered by departure city: {len(processed_df)} flights remaining")
    
    if destination_city != "All":
        processed_df = processed_df[processed_df['destination_city'] == destination_city]
        st.sidebar.info(f"🔍 Filtered by destination city: {len(processed_df)} flights remaining")
    
    # Date filtering
    if 'date' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['date'])
        processed_df = processed_df[(processed_df['date'].dt.date >= start_date) & (processed_df['date'].dt.date <= end_date)]
        st.sidebar.info(f"🔍 Filtered by date range: {len(processed_df)} flights remaining")
    
    # Apply additional filters
    if 'price' in processed_df.columns and 'price_range' in locals():
        processed_df = processed_df[(processed_df['price'] >= price_range[0]) & (processed_df['price'] <= price_range[1])]
        st.sidebar.info(f"🔍 Filtered by price range: {len(processed_df)} flights remaining")
    
    if 'airline' in processed_df.columns and 'selected_airline' in locals() and selected_airline != "All":
        processed_df = processed_df[processed_df['airline'] == selected_airline]
        st.sidebar.info(f"🔍 Filtered by airline: {len(processed_df)} flights remaining")
    
    if 'occupancy_rate' in processed_df.columns and 'occupancy_range' in locals():
        processed_df = processed_df[(processed_df['occupancy_rate'] >= occupancy_range[0]) & (processed_df['occupancy_rate'] <= occupancy_range[1])]
        st.sidebar.info(f"🔍 Filtered by occupancy: {len(processed_df)} flights remaining")
    
    st.sidebar.success(f"✅ Final filtered data: {len(processed_df)} flights (from {initial_count} total)")
    
    # Check if all data was filtered out
    if len(processed_df) == 0:
        st.warning("⚠️ All data was filtered out. Please adjust your filters or refresh the data.")
        
        # Provide helpful suggestions
        st.info("💡 **Filtering Tips:**")
        if departure_city != "All" and destination_city != "All":
            st.info(f"• No flights found from **{departure_city}** to **{destination_city}**")
            st.info("• Try selecting 'All' for one of the cities to see available routes")
            st.info("• Popular routes include: New York → Los Angeles, Chicago → Miami, Denver → Seattle")
        elif departure_city != "All":
            st.info(f"• No flights found departing from **{departure_city}**")
            st.info("• Try selecting 'All' for departure city to see all available routes")
        elif destination_city != "All":
            st.info(f"• No flights found arriving at **{destination_city}**")
            st.info("• Try selecting 'All' for destination city to see all available routes")
        
        st.info("• Click '🔄 Refresh Data' to generate new sample data")
        return
    
    # Export functionality (after data processing and filtering)
    if len(processed_df) > 0:
        if st.sidebar.button("📥 Export Data", use_container_width=True):
            st.sidebar.info(f"🔍 Debug: processed_df empty: {processed_df.empty}, export_format: {export_format}")
            if not processed_df.empty and export_format:
                with st.spinner(f"🔄 Exporting data as {export_format}..."):
                    try:
                        # Export the data
                        export_data = export_report(processed_df, insights, export_format.lower())
                        
                        if export_data:
                            # Create download button
                            file_extension = {
                                "CSV": "csv",
                                "Excel": "xlsx", 
                                "PDF": "pdf"
                            }[export_format]
                            
                            filename = f"airline_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
                            
                            st.sidebar.download_button(
                                label=f"📥 Download {export_format}",
                                data=export_data,
                                file_name=filename,
                                mime={
                                    "CSV": "text/csv",
                                    "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    "PDF": "application/pdf"
                                }[export_format],
                                use_container_width=True
                            )
                            
                            st.sidebar.success(f"✅ {export_format} export ready for download!")
                        else:
                            st.sidebar.error("❌ Export failed. Please try again.")
                            
                    except Exception as e:
                        st.sidebar.error(f"❌ Export error: {str(e)}")
            else:
                st.sidebar.warning("⚠️ No data available for export. Please fetch data first.")
    else:
        st.sidebar.warning("⚠️ No data available for export. Please fetch data first.")
    
    # Display metrics with enhanced styling
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Key Performance Indicators")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✈️ Total Flights</h3>
            <div class="metric-value">{insights.get('total_flights', 0):,}</div>
            <small>Analyzed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate average price from route_prices or use 0 if not available
        avg_price = 0
        if 'route_prices' in insights and insights['route_prices']:
            avg_price = np.mean(list(insights['route_prices'].values()))
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Average Price</h3>
            <div class="metric-value">${avg_price:.0f}</div>
            <small>Per Route</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Avg Occupancy</h3>
            <div class="metric-value">{insights.get('avg_occupancy', 0):.1f}%</div>
            <small>Capacity Used</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💵 Total Revenue</h3>
            <div class="metric-value">${insights.get('total_revenue', 0):,.0f}</div>
            <small>Generated</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content tabs with enhanced styling
    tab1, tab2, tab3 = st.tabs(["📊 Charts & Analytics", "📋 Data Tables", "💡 AI Insights"])
    
    with tab1:
        create_charts(processed_df, insights)
    
    with tab2:
        display_tables(processed_df, insights)
    
    with tab3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💡 AI-Powered Insights & Analysis")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate and display insights with better styling
        insights_text = generate_insights(insights)
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**🔍 Key Insights**")
        st.markdown(insights_text)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AI-powered insights with Gemini
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**🤖 AI-Powered Analysis**")
        gemini_insights = generate_gemini_insights(insights, processed_df)
        st.markdown(gemini_insights)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Additional analysis with enhanced styling
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**📊 Detailed Market Analysis**")
        
        if 'popular_routes' in insights and insights['popular_routes']:
            st.markdown("**🏆 Top 5 Most Popular Routes:**")
            for i, (route, count) in enumerate(insights['popular_routes'].items(), 1):
                st.markdown(f"**{i}.** {route}: **{count} flights**")
        else:
            st.markdown("**🏆 Popular Routes:** No route data available")
        
        if 'demand_periods' in insights and not insights['demand_periods'].empty:
            st.markdown("**📈 Demand Analysis:**")
            try:
                avg_daily_flights = insights['demand_periods']['flight_count'].mean()
                st.markdown(f"**Average daily flights:** {avg_daily_flights:.1f}")
                
                # Identify peak and low demand days
                peak_day = insights['demand_periods'].loc[insights['demand_periods']['flight_count'].idxmax()]
                low_day = insights['demand_periods'].loc[insights['demand_periods']['flight_count'].idxmin()]
                
                st.markdown(f"**Peak demand day:** {peak_day['date'].strftime('%Y-%m-%d')} (**{peak_day['flight_count']} flights**)")
                st.markdown(f"**Lowest demand day:** {low_day['date'].strftime('%Y-%m-%d')} (**{low_day['flight_count']} flights**)")
                
                # Add demand trend analysis
                if len(insights['demand_periods']) > 1:
                    demand_trend = insights['demand_periods']['flight_count'].iloc[-1] - insights['demand_periods']['flight_count'].iloc[0]
                    if demand_trend > 0:
                        st.success(f"📈 **Demand Trend:** Increasing (+{demand_trend:.0f} flights)")
                    elif demand_trend < 0:
                        st.error(f"📉 **Demand Trend:** Decreasing ({demand_trend:.0f} flights)")
                    else:
                        st.info("➡️ **Demand Trend:** Stable")
                        
            except Exception as e:
                st.error(f"**Demand Analysis:** Unable to analyze demand patterns: {str(e)}")
        else:
            st.markdown("**📈 Demand Analysis:** No demand data available")
        
        # Revenue analysis
        if 'total_revenue' in insights and insights['total_revenue'] > 0:
            st.markdown("**💰 Revenue Analysis:**")
            avg_revenue_per_flight = insights['total_revenue'] / insights['total_flights'] if insights['total_flights'] > 0 else 0
            st.markdown(f"**Average revenue per flight:** ${avg_revenue_per_flight:.2f}")
            
            if 'avg_occupancy' in insights and insights['avg_occupancy'] > 0:
                revenue_per_passenger = insights['total_revenue'] / (insights['total_flights'] * insights['avg_occupancy'] / 100) if insights['total_flights'] > 0 else 0
                st.markdown(f"**Revenue per passenger:** ${revenue_per_passenger:.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 