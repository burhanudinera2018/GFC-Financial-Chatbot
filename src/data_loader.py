"""
Module untuk load data keuangan dari JSON
"""
import json
import pandas as pd
import streamlit as st

@st.cache_data
def load_financial_data(file_path='data/financial_data.json'):
    """Load financial data from JSON file"""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {file_path}")
        # Return dummy data for testing
        return create_dummy_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return create_dummy_data()

def create_dummy_data():
    """Create dummy financial data for testing"""
    return {
        "company": "Global Finance Corp (GFC)",
        "period": "2020-2023",
        "financials": {
            "revenue": {"2020": 125000000, "2021": 142000000, "2022": 168000000, "2023": 195000000},
            "net_income": {"2020": 18750000, "2021": 21300000, "2022": 25200000, "2023": 29250000},
            "profit_margin": {"2020": 15.0, "2021": 15.0, "2022": 15.0, "2023": 15.0}
        },
        "key_insights": [
            "Pendapatan tumbuh konsisten 13-18% setiap tahun",
            "Profit margin stabil di 15% selama 4 tahun"
        ]
    }

def get_financial_dataframe(data):
    """Convert financial data to pandas DataFrame for analysis"""
    financials = data['financials']
    
    # Create DataFrame from years
    years = list(financials['revenue'].keys())
    df = pd.DataFrame({
        'Year': years,
        'Revenue': [financials['revenue'][y] for y in years],
        'Net Income': [financials['net_income'][y] for y in years],
        'Profit Margin': [financials['profit_margin'][y] for y in years]
    })
    
    # Add calculated fields
    df['Revenue Growth'] = df['Revenue'].pct_change() * 100
    df['Income Growth'] = df['Net Income'].pct_change() * 100
    
    return df