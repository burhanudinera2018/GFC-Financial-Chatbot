"""
Utility functions for chatbot
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_revenue_chart(data):
    """Create revenue trend chart"""
    years = list(data['financials']['revenue'].keys())
    revenues = list(data['financials']['revenue'].values())
    
    df = pd.DataFrame({
        'Year': years,
        'Revenue': [r/1e6 for r in revenues]  # Convert to millions
    })
    
    fig = px.line(
        df, x='Year', y='Revenue',
        title='Tren Pendapatan GFC (dalam Juta USD)',
        markers=True
    )
    fig.update_layout(
        xaxis_title='Tahun',
        yaxis_title='Pendapatan (Juta USD)',
        height=400
    )
    return fig

def create_income_chart(data):
    """Create net income trend chart"""
    years = list(data['financials']['net_income'].keys())
    incomes = list(data['financials']['net_income'].values())
    
    df = pd.DataFrame({
        'Year': years,
        'Net Income': [i/1e6 for i in incomes]  # Convert to millions
    })
    
    fig = px.bar(
        df, x='Year', y='Net Income',
        title='Laba Bersih GFC (dalam Juta USD)',
        color='Net Income',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        xaxis_title='Tahun',
        yaxis_title='Laba Bersih (Juta USD)',
        height=400
    )
    return fig

def format_message(role, content):
    """Format message for chat display"""
    if role == "user":
        return f"👤 **Anda:** {content}"
    else:
        return f"🤖 **Chatbot:** {content}"

def sanitize_input(text):
    """Sanitize user input"""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    # Limit length
    return text[:500]