import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import random
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="PUREN - Essence of Luxury",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'custom_blend' not in st.session_state:
    st.session_state.custom_blend = {'top': [], 'middle': [], 'base': []}
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = None
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Luxury color palette
COLORS = {
    'primary': '#D4AF37',      # Gold
    'secondary': '#1a1a1a',    # Deep black
    'accent': '#8B7355',       # Bronze
    'background': '#FAF9F6',   # Off-white
    'text': '#2C2C2C',
    'light_gold': '#F4E4C1'
}

# Custom CSS for luxury aesthetic
def load_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Cormorant+Garamond:wght@300;400;500&family=Montserrat:wght@300;400;500&display=swap');

    .stApp {{
        background: linear-gradient(135deg, {COLORS['background']} 0%, #FFFFFF 100%);
    }}

    h1, h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: {COLORS['secondary']};
        letter-spacing: 3px;
    }}

    p, .stMarkdown {{
        font-family: 'Cormorant Garamond', serif;
        color: {COLORS['text']};
        font-size: 1.1rem;
        line-height: 1.8;
    }}

    .luxury-card {{
        background: linear-gradient(145deg, #FFFFFF 0%, {COLORS['background']} 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.15);
        border: 1px solid {COLORS['light_gold']};
        margin: 20px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .luxury-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(212, 175, 55, 0.25);
    }}

    .product-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        height: 100%;
    }}

    .product-card:hover {{
        border: 2px solid {COLORS['primary']};
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.2);
    }}

    .gold-divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
        margin: 30px 0;
    }}

    .hero-text {{
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 300;
        letter-spacing: 10px;
        color: {COLORS['secondary']};
        text-align: center;
        margin: 50px 0;
        text-shadow: 2px 2px 4px rgba(212, 175, 55, 0.2);
    }}

    .tagline {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        letter-spacing: 5px;
        color: {COLORS['accent']};
        text-align: center;
        margin-bottom: 50px;
        font-weight: 300;
    }}

    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 50px;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 2px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(212, 175, 55, 0.3);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.5);
    }}

    .note-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['light_gold']} 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        margin: 5px;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 1px;
        box-shadow: 0 3px 10px rgba(212, 175, 55, 0.3);
    }}

    .price-tag {{
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: {COLORS['primary']};
        font-weight: 600;
    }}

    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, {COLORS['secondary']} 0%, {COLORS['accent']} 100%);
    }}

    /* Animated gradient background for hero sections */
    .animated-bg {{
        background: linear-gradient(-45deg, #FAF9F6, #F4E4C1, #D4AF37, #C5A572);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}

    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .quiz-option {{
        background: white;
        border: 2px solid {COLORS['light_gold']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }}

    .quiz-option:hover {{
        background: {COLORS['light_gold']};
        border-color: {COLORS['primary']};
        transform: scale(1.02);
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS['primary']};
        border-radius: 5px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['accent']};
    }}
    </style>
    """, unsafe_allow_html=True)

# Load logo
def load_logo():
    try:
        with open('logo.svg', 'r') as f:
            logo_svg = f.read()
        return logo_svg
    except:
        return None

# Product data with placeholder information
PRODUCTS = [
    {
        'id': 1,
        'name': 'Mystic Rose',
        'description': 'A timeless blend of Bulgarian rose and oud wood, creating an aura of mystery and elegance.',
        'price': 295,
        'category': 'Floral',
        'notes': {
            'top': ['Bergamot', 'Pink Pepper', 'Mandarin'],
            'middle': ['Bulgarian Rose', 'Jasmine', 'Peony'],
            'base': ['Oud Wood', 'Amber', 'Musk']
        },
        'mood': ['Romantic', 'Elegant', 'Evening'],
        'season': 'All Season',
        'intensity': 85,
        'longevity': 10,
        'image_url': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'
    },
    {
        'id': 2,
        'name': 'Velvet Noir',
        'description': 'Dark, sensual, and captivating. A sophisticated blend for those who dare to be bold.',
        'price': 325,
        'category': 'Oriental',
        'notes': {
            'top': ['Black Currant', 'Saffron', 'Cardamom'],
            'middle': ['Leather', 'Violet', 'Tobacco'],
            'base': ['Vanilla', 'Patchouli', 'Sandalwood']
        },
        'mood': ['Mysterious', 'Seductive', 'Night'],
        'season': 'Fall/Winter',
        'intensity': 95,
        'longevity': 12,
        'image_url': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400'
    },
    {
        'id': 3,
        'name': 'Citrus Symphony',
        'description': 'A vibrant celebration of Mediterranean citrus groves, fresh and invigorating.',
        'price': 245,
        'category': 'Citrus',
        'notes': {
            'top': ['Lemon', 'Orange Blossom', 'Grapefruit'],
            'middle': ['Neroli', 'Petitgrain', 'Green Tea'],
            'base': ['Vetiver', 'Cedar', 'White Musk']
        },
        'mood': ['Fresh', 'Energetic', 'Daytime'],
        'season': 'Spring/Summer',
        'intensity': 65,
        'longevity': 6,
        'image_url': 'https://images.unsplash.com/photo-1588405748880-12d1d2a59cfc?w=400'
    },
    {
        'id': 4,
        'name': 'Ocean Breeze',
        'description': 'Experience the crisp, refreshing essence of coastal winds and sea salt.',
        'price': 265,
        'category': 'Aquatic',
        'notes': {
            'top': ['Sea Salt', 'Mint', 'Lemon'],
            'middle': ['Marine Accord', 'Lavender', 'Sage'],
            'base': ['Driftwood', 'Ambergris', 'Moss']
        },
        'mood': ['Clean', 'Fresh', 'Casual'],
        'season': 'Spring/Summer',
        'intensity': 70,
        'longevity': 7,
        'image_url': 'https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400'
    },
    {
        'id': 5,
        'name': 'Golden Amber',
        'description': 'Warm, luxurious, and utterly captivating. Pure indulgence in a bottle.',
        'price': 350,
        'category': 'Amber',
        'notes': {
            'top': ['Cinnamon', 'Clove', 'Honey'],
            'middle': ['Amber', 'Labdanum', 'Benzoin'],
            'base': ['Tonka Bean', 'Vanilla', 'Incense']
        },
        'mood': ['Warm', 'Luxurious', 'Evening'],
        'season': 'Fall/Winter',
        'intensity': 90,
        'longevity': 11,
        'image_url': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400'
    },
    {
        'id': 6,
        'name': 'Ethereal Bloom',
        'description': 'A delicate bouquet of white flowers, evoking purity and grace.',
        'price': 285,
        'category': 'Floral',
        'notes': {
            'top': ['Freesia', 'Lily of the Valley', 'Pear'],
            'middle': ['White Gardenia', 'Magnolia', 'Tuberose'],
            'base': ['Cashmeran', 'White Musk', 'Sandalwood']
        },
        'mood': ['Romantic', 'Feminine', 'Daytime'],
        'season': 'Spring',
        'intensity': 75,
        'longevity': 8,
        'image_url': 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400'
    },
    {
        'id': 7,
        'name': 'Spice Caravan',
        'description': 'An exotic journey through ancient spice routes, rich and intoxicating.',
        'price': 310,
        'category': 'Spicy',
        'notes': {
            'top': ['Nutmeg', 'Star Anise', 'Ginger'],
            'middle': ['Cinnamon', 'Clove', 'Rose'],
            'base': ['Sandalwood', 'Frankincense', 'Myrrh']
        },
        'mood': ['Exotic', 'Mysterious', 'Evening'],
        'season': 'Fall/Winter',
        'intensity': 88,
        'longevity': 10,
        'image_url': 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400'
    },
    {
        'id': 8,
        'name': 'Lunar Garden',
        'description': 'Night-blooming flowers under moonlight, ethereal and enchanting.',
        'price': 295,
        'category': 'Floral',
        'notes': {
            'top': ['Night Jasmine', 'Moonflower', 'Dewdrops'],
            'middle': ['Tuberose', 'Ylang Ylang', 'Iris'],
            'base': ['White Amber', 'Musk', 'Cashmere Wood']
        },
        'mood': ['Dreamy', 'Romantic', 'Night'],
        'season': 'All Season',
        'intensity': 80,
        'longevity': 9,
        'image_url': 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?w=400'
    }
]

# Fragrance notes database
FRAGRANCE_NOTES = {
    'top': ['Bergamot', 'Lemon', 'Orange', 'Grapefruit', 'Mandarin', 'Pink Pepper',
            'Cardamom', 'Lavender', 'Mint', 'Apple', 'Pear', 'Black Currant',
            'Sea Salt', 'Saffron', 'Cinnamon', 'Nutmeg'],
    'middle': ['Rose', 'Jasmine', 'Ylang Ylang', 'Iris', 'Violet', 'Geranium',
               'Neroli', 'Tuberose', 'Peony', 'Leather', 'Tobacco', 'Cinnamon',
               'Marine Accord', 'Lavender', 'Green Tea', 'Magnolia'],
    'base': ['Vanilla', 'Musk', 'Amber', 'Sandalwood', 'Cedar', 'Oud',
             'Patchouli', 'Vetiver', 'Tonka Bean', 'Benzoin', 'Moss',
             'Frankincense', 'Myrrh', 'Ambergris', 'Cashmere Wood']
}

# Scent profile quiz questions
QUIZ_QUESTIONS = [
    {
        'question': 'Which environment resonates with you most?',
        'options': {
            'A sun-drenched garden full of blooming flowers': 'floral',
            'A mysterious forest at twilight': 'woody',
            'A bustling spice market in Morocco': 'oriental',
            'A pristine beach with ocean breeze': 'fresh'
        }
    },
    {
        'question': 'What describes your personality best?',
        'options': {
            'Romantic and graceful': 'floral',
            'Bold and confident': 'oriental',
            'Free-spirited and adventurous': 'fresh',
            'Sophisticated and mysterious': 'woody'
        }
    },
    {
        'question': 'When do you typically wear fragrance?',
        'options': {
            'Daily, as part of my routine': 'fresh',
            'Special occasions and evenings': 'oriental',
            'Romantic dates and intimate settings': 'floral',
            'Professional settings and important meetings': 'woody'
        }
    },
    {
        'question': 'Which scent memory appeals to you?',
        'options': {
            'Fresh laundry and clean linen': 'fresh',
            'Antique wooden furniture and leather books': 'woody',
            'Rose garden after rain': 'floral',
            'Warm spices and vanilla from baking': 'oriental'
        }
    },
    {
        'question': 'What intensity do you prefer?',
        'options': {
            'Subtle and close to skin': 'fresh',
            'Moderate and noticeable': 'floral',
            'Strong and long-lasting': 'oriental',
            'Rich and enveloping': 'woody'
        }
    }
]

def create_fragrance_wheel():
    """Create an interactive fragrance wheel visualization"""
    categories = ['Floral', 'Oriental', 'Woody', 'Fresh', 'Citrus', 'Aquatic', 'Spicy', 'Amber']
    values = [3, 2, 2, 2, 1, 1, 1, 1]

    colors = ['#FF69B4', '#8B4513', '#8B7355', '#00CED1',
              '#FFD700', '#4682B4', '#DC143C', '#DAA520']

    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textfont=dict(size=14, family='Playfair Display'),
        hovertemplate='<b>%{label}</b><br>Explore fragrances<extra></extra>'
    )])

    fig.update_layout(
        title={
            'text': 'Fragrance Families',
            'font': {'size': 24, 'family': 'Playfair Display', 'color': COLORS['secondary']}
        },
        showlegend=True,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Cormorant Garamond')
    )

    return fig

def create_note_pyramid(product):
    """Create a visual pyramid of fragrance notes"""
    fig = go.Figure()

    # Create pyramid layers
    layers = [
        {'name': 'Top Notes', 'notes': product['notes']['top'], 'y': 3, 'color': COLORS['light_gold']},
        {'name': 'Middle Notes', 'notes': product['notes']['middle'], 'y': 2, 'color': COLORS['primary']},
        {'name': 'Base Notes', 'notes': product['notes']['base'], 'y': 1, 'color': COLORS['accent']}
    ]

    for layer in layers:
        fig.add_trace(go.Bar(
            name=layer['name'],
            x=[layer['name']],
            y=[layer['y']],
            text=[f"<br>".join(layer['notes'])],
            textposition='inside',
            marker=dict(color=layer['color']),
            hovertemplate=f"<b>{layer['name']}</b><br>" + "<br>".join(layer['notes']) + "<extra></extra>"
        ))

    fig.update_layout(
        title='Fragrance Pyramid',
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        font=dict(family='Cormorant Garamond', color='white', size=12)
    )

    return fig

def create_scent_evolution():
    """Create an animated timeline showing how fragrance evolves"""
    time_points = ['0-15 min', '15-60 min', '1-4 hours', '4-12 hours']
    intensity = [100, 85, 60, 30]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_points,
        y=intensity,
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=4, shape='spline'),
        marker=dict(size=15, color=COLORS['accent'], line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor=f'rgba(212, 175, 55, 0.2)',
        hovertemplate='<b>%{x}</b><br>Intensity: %{y}%<extra></extra>'
    ))

    # Add annotations for notes
    annotations = [
        dict(x=0, y=100, text='Top Notes<br>Bloom', showarrow=False, yshift=20),
        dict(x=1, y=85, text='Heart Notes<br>Develop', showarrow=False, yshift=20),
        dict(x=2, y=60, text='Base Notes<br>Emerge', showarrow=False, yshift=20),
        dict(x=3, y=30, text='Base Notes<br>Linger', showarrow=False, yshift=20)
    ]

    fig.update_layout(
        title={
            'text': 'Scent Evolution Journey',
            'font': {'size': 20, 'family': 'Playfair Display'}
        },
        xaxis_title='Time',
        yaxis_title='Intensity',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=annotations,
        font=dict(family='Cormorant Garamond'),
        hovermode='x unified'
    )

    return fig

def create_mood_radar(product):
    """Create a radar chart for fragrance mood profile"""
    categories = ['Romantic', 'Fresh', 'Mysterious', 'Energetic', 'Luxurious', 'Casual']

    # Generate values based on product characteristics
    values = []
    for cat in categories:
        if cat.lower() in [m.lower() for m in product['mood']]:
            values.append(random.randint(70, 95))
        else:
            values.append(random.randint(10, 40))

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba(212, 175, 55, 0.3)',
        line=dict(color=COLORS['primary'], width=2),
        marker=dict(size=8, color=COLORS['accent'])
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
            bgcolor='rgba(255, 255, 255, 0.5)'
        ),
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Cormorant Garamond', size=12)
    )

    return fig

def get_recommendations_by_mood(mood):
    """Get fragrance recommendations based on mood"""
    recommendations = []
    for product in PRODUCTS:
        if any(m.lower() in [pm.lower() for pm in product['mood']] for m in mood):
            recommendations.append(product)
    return recommendations[:3]  # Return top 3

def calculate_scent_profile(answers):
    """Calculate personalized scent profile from quiz answers"""
    profile_scores = {'floral': 0, 'woody': 0, 'oriental': 0, 'fresh': 0}

    for answer in answers:
        profile_scores[answer] += 1

    dominant_profile = max(profile_scores, key=profile_scores.get)

    # Map profiles to product categories
    profile_to_category = {
        'floral': 'Floral',
        'woody': ['Woody', 'Amber'],
        'oriental': ['Oriental', 'Spicy'],
        'fresh': ['Fresh', 'Citrus', 'Aquatic']
    }

    return dominant_profile, profile_to_category

def show_header():
    """Display the luxury header with logo"""
    logo_svg = load_logo()

    if logo_svg:
        st.markdown(f'<div style="text-align: center; padding: 20px;">{logo_svg}</div>',
                   unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="hero-text">PUREN</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline">ESSENCE OF LUXURY</p>', unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

def home_page():
    """Main home page with hero section"""
    show_header()

    # Hero section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="luxury-card" style="text-align: center;">
            <h2 style="font-size: 2.5rem; margin-bottom: 20px;">Discover Your Signature Scent</h2>
            <p style="font-size: 1.3rem; margin-bottom: 30px;">
                Each fragrance tells a story. Each bottle holds a memory.
                Experience the art of perfumery refined through generations of mastery.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Features showcase
    st.markdown("<h2 style='text-align: center; margin: 50px 0;'>Experience Puren</h2>",
               unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>🌸</h3>
            <h3>Scent Finder</h3>
            <p>Take our personalized quiz to discover fragrances that match your unique personality and style.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>⚗️</h3>
            <h3>Create Your Blend</h3>
            <p>Become a perfumer. Design your own custom fragrance by selecting from our exquisite note collection.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>✨</h3>
            <h3>Curated Collection</h3>
            <p>Explore our signature fragrances, each crafted with the finest ingredients from around the world.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Fragrance wheel
    st.markdown("<h2 style='text-align: center; margin: 50px 0;'>Explore Fragrance Families</h2>",
               unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig = create_fragrance_wheel()
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Featured products preview
    st.markdown("<h2 style='text-align: center; margin: 50px 0;'>Featured Fragrances</h2>",
               unsafe_allow_html=True)

    featured = random.sample(PRODUCTS, 3)
    cols = st.columns(3)

    for idx, product in enumerate(featured):
        with cols[idx]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{product['image_url']}" style="width: 100%; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="text-align: center; margin: 15px 0;">{product['name']}</h3>
                <p style="text-align: center; font-size: 0.95rem; min-height: 80px;">{product['description'][:100]}...</p>
                <p class="price-tag" style="text-align: center; margin: 20px 0;">${product['price']}</p>
            </div>
            """, unsafe_allow_html=True)

def shop_page():
    """Product catalog with filters"""
    show_header()

    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Our Collection</h2>",
               unsafe_allow_html=True)

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        categories = ['All'] + list(set([p['category'] for p in PRODUCTS]))
        selected_category = st.selectbox('Category', categories)

    with col2:
        seasons = ['All', 'Spring', 'Summer', 'Fall/Winter', 'All Season']
        selected_season = st.selectbox('Season', seasons)

    with col3:
        price_range = st.slider('Price Range', 0, 400, (0, 400))

    with col4:
        intensity_filter = st.slider('Intensity', 0, 100, (0, 100))

    # Filter products
    filtered_products = PRODUCTS

    if selected_category != 'All':
        filtered_products = [p for p in filtered_products if p['category'] == selected_category]

    if selected_season != 'All':
        filtered_products = [p for p in filtered_products
                           if p['season'] == selected_season or p['season'] == 'All Season']

    filtered_products = [p for p in filtered_products
                        if price_range[0] <= p['price'] <= price_range[1]
                        and intensity_filter[0] <= p['intensity'] <= intensity_filter[1]]

    st.markdown(f"<p style='text-align: center; margin: 30px 0;'>Showing {len(filtered_products)} fragrances</p>",
               unsafe_allow_html=True)

    # Display products in grid
    for i in range(0, len(filtered_products), 3):
        cols = st.columns(3)
        for idx, product in enumerate(filtered_products[i:i+3]):
            with cols[idx]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product['image_url']}" style="width: 100%; border-radius: 10px;">
                    <h3 style="text-align: center; margin: 20px 0 10px 0;">{product['name']}</h3>
                    <p style="text-align: center; color: {COLORS['accent']}; margin-bottom: 15px;">
                        {product['category']} • {product['season']}
                    </p>
                    <p style="text-align: center; min-height: 100px;">{product['description']}</p>
                    <p class="price-tag" style="text-align: center; margin: 20px 0;">${product['price']}</p>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button('View Details', key=f'view_{product["id"]}'):
                        st.session_state.selected_product = product['id']
                        st.rerun()

                with col_b:
                    if product['id'] in st.session_state.favorites:
                        if st.button('♥ Saved', key=f'fav_{product["id"]}'):
                            st.session_state.favorites.remove(product['id'])
                            st.rerun()
                    else:
                        if st.button('♡ Save', key=f'unfav_{product["id"]}'):
                            st.session_state.favorites.append(product['id'])
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # Product detail modal
    if 'selected_product' in st.session_state and st.session_state.selected_product:
        product = next(p for p in PRODUCTS if p['id'] == st.session_state.selected_product)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; margin: 40px 0;'>{product['name']}</h2>",
                   unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.image(product['image_url'], use_container_width=True)

            st.markdown(f"""
            <div class="luxury-card">
                <h3>Notes</h3>
                <p><strong>Top Notes:</strong><br>
                {"".join([f'<span class="note-badge">{note}</span>' for note in product['notes']['top']])}</p>
                <p><strong>Middle Notes:</strong><br>
                {"".join([f'<span class="note-badge">{note}</span>' for note in product['notes']['middle']])}</p>
                <p><strong>Base Notes:</strong><br>
                {"".join([f'<span class="note-badge">{note}</span>' for note in product['notes']['base']])}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="luxury-card">
                <p class="price-tag">${product['price']}</p>
                <p style="font-size: 1.2rem; line-height: 2;">{product['description']}</p>
                <p><strong>Category:</strong> {product['category']}</p>
                <p><strong>Best Season:</strong> {product['season']}</p>
                <p><strong>Intensity:</strong> {product['intensity']}/100</p>
                <p><strong>Longevity:</strong> {product['longevity']} hours</p>
                <p><strong>Perfect For:</strong> {', '.join(product['mood'])}</p>
            </div>
            """, unsafe_allow_html=True)

            # Visualizations
            st.plotly_chart(create_note_pyramid(product), use_container_width=True)
            st.plotly_chart(create_mood_radar(product), use_container_width=True)
            st.plotly_chart(create_scent_evolution(), use_container_width=True)

            if st.button('← Back to Collection', use_container_width=True):
                st.session_state.selected_product = None
                st.rerun()

def scent_finder_page():
    """Interactive scent profile quiz"""
    show_header()

    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Find Your Perfect Scent</h2>",
               unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align: center;">
        <p style="font-size: 1.2rem;">
            Answer a few questions about your preferences and personality,
            and we'll recommend fragrances that are perfect for you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Quiz
    answers = []

    for idx, q in enumerate(QUIZ_QUESTIONS):
        st.markdown(f"""
        <div class="luxury-card">
            <h3>Question {idx + 1} of {len(QUIZ_QUESTIONS)}</h3>
            <p style="font-size: 1.3rem; margin: 20px 0;">{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)

        answer = st.radio(
            'Select your answer:',
            list(q['options'].keys()),
            key=f'q_{idx}',
            label_visibility='collapsed'
        )

        answers.append(q['options'][answer])
        st.markdown('<br>', unsafe_allow_html=True)

    if st.button('✨ Discover My Scent Profile ✨', use_container_width=True):
        dominant_profile, category_map = calculate_scent_profile(answers)
        st.session_state.quiz_results = {
            'profile': dominant_profile,
            'categories': category_map[dominant_profile]
        }
        st.rerun()

    # Show results if quiz completed
    if st.session_state.quiz_results:
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        profile = st.session_state.quiz_results['profile']

        profile_descriptions = {
            'floral': {
                'title': 'The Romantic',
                'description': 'You are drawn to beauty, elegance, and timeless grace. Floral fragrances with their soft, romantic character perfectly complement your refined taste.',
                'characteristics': ['Graceful', 'Romantic', 'Elegant', 'Feminine']
            },
            'woody': {
                'title': 'The Sophisticate',
                'description': 'You appreciate depth, complexity, and understated luxury. Woody and amber fragrances with their rich, warm character match your sophisticated nature.',
                'characteristics': ['Sophisticated', 'Mysterious', 'Confident', 'Timeless']
            },
            'oriental': {
                'title': 'The Enigma',
                'description': 'You are bold, passionate, and unapologetically unique. Oriental and spicy fragrances with their intense, exotic character reflect your captivating personality.',
                'characteristics': ['Bold', 'Passionate', 'Exotic', 'Intense']
            },
            'fresh': {
                'title': 'The Free Spirit',
                'description': 'You embrace life with energy and optimism. Fresh, citrus, and aquatic fragrances with their vibrant, uplifting character match your free-spirited nature.',
                'characteristics': ['Energetic', 'Fresh', 'Optimistic', 'Adventurous']
            }
        }

        info = profile_descriptions[profile]

        st.markdown(f"""
        <div class="luxury-card" style="text-align: center;">
            <h2 style="color: {COLORS['primary']}; font-size: 3rem; margin-bottom: 20px;">
                {info['title']}
            </h2>
            <p style="font-size: 1.3rem; margin: 30px 0;">
                {info['description']}
            </p>
            <div style="margin: 30px 0;">
                {"".join([f'<span class="note-badge">{char}</span>' for char in info['characteristics']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; margin: 40px 0;'>Your Recommended Fragrances</h3>",
                   unsafe_allow_html=True)

        # Get recommendations
        categories = st.session_state.quiz_results['categories']
        if isinstance(categories, str):
            categories = [categories]

        recommendations = [p for p in PRODUCTS if p['category'] in categories][:3]

        cols = st.columns(3)
        for idx, product in enumerate(recommendations):
            with cols[idx]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product['image_url']}" style="width: 100%; border-radius: 10px;">
                    <h3 style="text-align: center; margin: 20px 0;">{product['name']}</h3>
                    <p style="text-align: center; min-height: 100px;">{product['description']}</p>
                    <p class="price-tag" style="text-align: center;">${product['price']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button('View Details', key=f'rec_{product["id"]}'):
                    st.session_state.selected_product = product['id']
                    st.rerun()

        if st.button('↻ Retake Quiz', use_container_width=True):
            st.session_state.quiz_results = None
            st.rerun()

def blend_creator_page():
    """Interactive custom blend creator"""
    show_header()

    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Create Your Custom Blend</h2>",
               unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align: center;">
        <p style="font-size: 1.2rem;">
            Design your perfect fragrance by selecting notes from each layer of the fragrance pyramid.
            Combine up to 3 notes per layer to create your unique signature scent.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Note selection
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="luxury-card" style="text-align: center;">
            <h3>Top Notes</h3>
            <p>The first impression - fresh and volatile</p>
            <p style="font-size: 0.9rem; color: #888;">Lasts 15-60 minutes</p>
        </div>
        """, unsafe_allow_html=True)

        top_notes = st.multiselect(
            'Select up to 3 top notes',
            FRAGRANCE_NOTES['top'],
            default=st.session_state.custom_blend['top'],
            max_selections=3,
            key='top'
        )
        st.session_state.custom_blend['top'] = top_notes

    with col2:
        st.markdown("""
        <div class="luxury-card" style="text-align: center;">
            <h3>Middle Notes</h3>
            <p>The heart - character and personality</p>
            <p style="font-size: 0.9rem; color: #888;">Lasts 2-4 hours</p>
        </div>
        """, unsafe_allow_html=True)

        middle_notes = st.multiselect(
            'Select up to 3 middle notes',
            FRAGRANCE_NOTES['middle'],
            default=st.session_state.custom_blend['middle'],
            max_selections=3,
            key='middle'
        )
        st.session_state.custom_blend['middle'] = middle_notes

    with col3:
        st.markdown("""
        <div class="luxury-card" style="text-align: center;">
            <h3>Base Notes</h3>
            <p>The foundation - depth and longevity</p>
            <p style="font-size: 0.9rem; color: #888;">Lasts 4-12 hours</p>
        </div>
        """, unsafe_allow_html=True)

        base_notes = st.multiselect(
            'Select up to 3 base notes',
            FRAGRANCE_NOTES['base'],
            default=st.session_state.custom_blend['base'],
            max_selections=3,
            key='base'
        )
        st.session_state.custom_blend['base'] = base_notes

    # Show blend preview
    if top_notes or middle_notes or base_notes:
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin: 40px 0;'>Your Custom Blend Preview</h3>",
                   unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            # Create custom pyramid visualization
            custom_product = {
                'notes': {
                    'top': top_notes if top_notes else ['Not selected'],
                    'middle': middle_notes if middle_notes else ['Not selected'],
                    'base': base_notes if base_notes else ['Not selected']
                }
            }

            st.plotly_chart(create_note_pyramid(custom_product), use_container_width=True)

        with col2:
            st.markdown(f"""
            <div class="luxury-card">
                <h3 style="text-align: center; margin-bottom: 30px;">Your Blend</h3>

                <div style="margin: 20px 0;">
                    <h4>Top Notes</h4>
                    {"".join([f'<span class="note-badge">{note}</span>' for note in top_notes]) if top_notes else '<p>No notes selected</p>'}
                </div>

                <div style="margin: 20px 0;">
                    <h4>Middle Notes</h4>
                    {"".join([f'<span class="note-badge">{note}</span>' for note in middle_notes]) if middle_notes else '<p>No notes selected</p>'}
                </div>

                <div style="margin: 20px 0;">
                    <h4>Base Notes</h4>
                    {"".join([f'<span class="note-badge">{note}</span>' for note in base_notes]) if base_notes else '<p>No notes selected</p>'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Blend name input
            blend_name = st.text_input('Name your creation', placeholder='My Signature Scent')

            total_notes = len(top_notes) + len(middle_notes) + len(base_notes)

            if total_notes >= 5:
                estimated_price = 400 + (total_notes - 5) * 25

                st.markdown(f"""
                <div style="text-align: center; margin: 30px 0;">
                    <p class="price-tag">Estimated Price: ${estimated_price}</p>
                    <p style="font-size: 0.9rem; color: #888;">
                        Based on {total_notes} selected notes<br>
                        50ml Eau de Parfum
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if st.button('🌟 Request Custom Creation 🌟', use_container_width=True):
                    st.success(f"""
                    Thank you for creating "{blend_name if blend_name else 'Your Custom Blend'}"!
                    Our master perfumer will review your composition.
                    Custom blends typically take 3-4 weeks to craft.
                    """)
                    st.balloons()
            else:
                st.info('Select at least 5 notes (minimum 1 from each layer) to create your custom blend.')

def mood_recommendations_page():
    """Mood-based fragrance recommendations"""
    show_header()

    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Fragrance by Mood & Moment</h2>",
               unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align: center;">
        <p style="font-size: 1.2rem;">
            Every moment deserves the perfect scent. Tell us about your mood or occasion,
            and we'll recommend the ideal fragrance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Mood selection
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### How are you feeling?")
        mood = st.radio(
            'mood',
            ['Romantic & Dreamy', 'Confident & Powerful', 'Fresh & Energized',
             'Mysterious & Alluring', 'Calm & Peaceful', 'Playful & Fun'],
            label_visibility='collapsed'
        )

    with col2:
        st.markdown("### What's the occasion?")
        occasion = st.radio(
            'occasion',
            ['Date Night', 'Business Meeting', 'Casual Day Out',
             'Special Event', 'Evening Party', 'Weekend Brunch'],
            label_visibility='collapsed'
        )

    time_of_day = st.select_slider(
        'Time of Day',
        options=['Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night']
    )

    season = st.selectbox(
        'Current Season',
        ['Spring', 'Summer', 'Fall', 'Winter']
    )

    if st.button('Find Perfect Fragrance', use_container_width=True):
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # Smart recommendations based on inputs
        mood_map = {
            'Romantic & Dreamy': ['Romantic', 'Feminine'],
            'Confident & Powerful': ['Elegant', 'Mysterious'],
            'Fresh & Energized': ['Fresh', 'Energetic'],
            'Mysterious & Alluring': ['Mysterious', 'Seductive'],
            'Calm & Peaceful': ['Clean', 'Casual'],
            'Playful & Fun': ['Energetic', 'Daytime']
        }

        time_map = {
            'Early Morning': ['Fresh', 'Clean'],
            'Morning': ['Fresh', 'Energetic'],
            'Afternoon': ['Casual', 'Daytime'],
            'Evening': ['Elegant', 'Romantic'],
            'Night': ['Mysterious', 'Seductive', 'Night']
        }

        # Combine mood and time preferences
        preferred_moods = mood_map.get(mood, []) + time_map.get(time_of_day, [])

        recommendations = get_recommendations_by_mood(preferred_moods)

        if not recommendations:
            recommendations = random.sample(PRODUCTS, 3)

        st.markdown(f"""
        <div class="luxury-card" style="text-align: center;">
            <h3>Perfect for {mood} • {occasion} • {time_of_day}</h3>
            <p style="font-size: 1.1rem; margin-top: 20px;">
                Based on your selections, here are our top recommendations:
            </p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for idx, product in enumerate(recommendations):
            with cols[idx]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product['image_url']}" style="width: 100%; border-radius: 10px;">
                    <h3 style="text-align: center; margin: 20px 0;">{product['name']}</h3>
                    <p style="text-align: center; color: {COLORS['accent']};">
                        {product['category']}
                    </p>
                    <p style="text-align: center; min-height: 100px;">{product['description']}</p>
                    <p style="text-align: center;">
                        {"".join([f'<span class="note-badge" style="font-size: 0.7rem; padding: 4px 10px;">{m}</span>' for m in product['mood'][:2]])}
                    </p>
                    <p class="price-tag" style="text-align: center; margin: 20px 0;">${product['price']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button('View Details', key=f'mood_rec_{product["id"]}'):
                    st.session_state.selected_product = product['id']
                    st.rerun()

def about_page():
    """About Puren brand story"""
    show_header()

    st.markdown("""
    <div class="luxury-card">
        <h2 style="text-align: center; margin-bottom: 30px;">The Puren Story</h2>

        <p style="font-size: 1.2rem; line-height: 2; text-align: center; margin: 40px 0;">
            Born from a passion for the art of perfumery, Puren represents the perfect marriage
            of tradition and innovation. Each fragrance is a testament to our commitment to
            excellence, crafted with the finest ingredients sourced from around the world.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>🌍</h3>
            <h3>Global Sourcing</h3>
            <p style="line-height: 1.8;">
                We travel the world to source the most exquisite raw materials -
                from Bulgarian rose valleys to Indonesian patchouli forests,
                from Italian bergamot groves to Arabian oud distilleries.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>🔬</h3>
            <h3>Master Craftsmanship</h3>
            <p style="line-height: 1.8;">
                Our master perfumers combine traditional techniques passed down through
                generations with cutting-edge extraction methods to capture the purest
                essence of each ingredient.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="luxury-card" style="text-align: center; min-height: 300px;">
            <h3>♻️</h3>
            <h3>Sustainable Luxury</h3>
            <p style="line-height: 1.8;">
                We believe luxury and sustainability go hand in hand. Our ingredients
                are ethically sourced, our bottles are refillable, and our packaging
                is completely recyclable.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align: center;">
        <h3 style="margin-bottom: 30px;">Our Philosophy</h3>
        <p style="font-size: 1.2rem; line-height: 2;">
            "A fragrance is more than a scent - it's a memory, an emotion, a story waiting to unfold.
            At Puren, we don't just create perfumes; we craft olfactory experiences that become
            an intimate part of your personal narrative."
        </p>
        <p style="margin-top: 30px; font-style: italic; color: {COLORS['accent']};">
            - The Puren Atelier
        </p>
    </div>
    """.replace('{COLORS[\'accent\']}', COLORS['accent']), unsafe_allow_html=True)

# Main app navigation
def main():
    load_css()

    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['accent']} 100%); border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: {COLORS['primary']}; margin: 0; font-family: 'Playfair Display', serif; letter-spacing: 5px;">PUREN</h2>
            <p style="color: {COLORS['light_gold']}; margin: 5px 0 0 0; font-size: 0.8rem; letter-spacing: 2px;">NAVIGATION</p>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            'Navigate',
            ['Home', 'Shop Collection', 'Scent Finder', 'Create Blend', 'Mood & Moment', 'About Puren'],
            label_visibility='collapsed'
        )

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # Favorites counter
        if st.session_state.favorites:
            st.markdown(f"""
            <div style="background: {COLORS['light_gold']}; padding: 15px; border-radius: 10px; text-align: center;">
                <p style="margin: 0; color: {COLORS['secondary']};">♥ {len(st.session_state.favorites)} Saved Favorites</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p style="font-size: 0.9rem; color: #CCC;">
                Crafting luxury fragrances<br>
                since your first creation
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Page routing
    if page == 'Home':
        home_page()
    elif page == 'Shop Collection':
        shop_page()
    elif page == 'Scent Finder':
        scent_finder_page()
    elif page == 'Create Blend':
        blend_creator_page()
    elif page == 'Mood & Moment':
        mood_recommendations_page()
    elif page == 'About Puren':
        about_page()

    # Footer
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: {COLORS['accent']};">
        <p style="font-family: 'Playfair Display', serif; font-size: 1.5rem; letter-spacing: 5px; margin-bottom: 10px;">PUREN</p>
        <p style="font-size: 0.9rem; letter-spacing: 2px;">ESSENCE OF LUXURY</p>
        <p style="font-size: 0.8rem; margin-top: 20px;">
            © 2024 Puren. All rights reserved.<br>
            Crafted with passion for perfume lovers worldwide.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
