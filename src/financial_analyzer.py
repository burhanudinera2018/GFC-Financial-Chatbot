"""
Module untuk analisis keuangan dan persiapan respons
"""
import pandas as pd
import numpy as np
from datetime import datetime

class FinancialAnalyzer:
    def __init__(self, data):
        self.data = data
        self.df = self._create_dataframe()
        
    def _create_dataframe(self):
        """Create DataFrame from financial data"""
        financials = self.data['financials']
        years = list(financials['revenue'].keys())
        
        df = pd.DataFrame({'Year': years})
        for metric, values in financials.items():
            # Handle both dictionary and direct values
            if isinstance(values, dict):
                df[metric.capitalize()] = [values.get(y, 0) for y in years]
            else:
                df[metric.capitalize()] = values
        
        return df
    
    def get_total_revenue(self, year=None):
        """Get total revenue for specific year or all years"""
        revenue_data = self.data['financials']['revenue']
        
        if year:
            year_str = str(year)
            if year_str in revenue_data:
                # Return single value for specific year
                return revenue_data[year_str]
            else:
                return f"Data tahun {year} tidak tersedia"
        
        # Return all years data
        return revenue_data
    
    def get_net_income(self, year=None):
        """Get net income for specific year or all years"""
        income_data = self.data['financials']['net_income']
        
        if year:
            year_str = str(year)
            if year_str in income_data:
                # Return single value for specific year
                return income_data[year_str]
            else:
                return f"Data tahun {year} tidak tersedia"
        
        # Return all years data
        return income_data
    
    def get_revenue_growth(self):
        """Calculate year-over-year revenue growth"""
        revenue = self.data['financials']['revenue']
        years = sorted(revenue.keys())
        growth = {}
        
        for i in range(1, len(years)):
            prev_year = years[i-1]
            curr_year = years[i]
            growth[f"{prev_year}-{curr_year}"] = round(
                ((revenue[curr_year] - revenue[prev_year]) / revenue[prev_year]) * 100, 1
            )
        
        return growth
    
    def get_profit_margin_trend(self):
        """Get profit margin trend"""
        return self.data['financials']['profit_margin']
    
    def get_key_insights(self):
        """Get predefined key insights"""
        return self.data.get('key_insights', [])
    
    def format_currency(self, amount):
        """Format number as currency - FIXED: handles both number and string"""
        # Handle jika amount adalah string (error message)
        if isinstance(amount, str):
            return amount
        
        # Handle jika amount adalah dict (seharusnya tidak terjadi setelah perbaikan)
        if isinstance(amount, dict):
            return "Data tidak tersedia dalam format yang benar"
        
        # Handle numeric values
        try:
            amount = float(amount)
            if amount >= 1e9:
                return f"${amount/1e9:.2f}B"
            elif amount >= 1e6:
                return f"${amount/1e6:.2f}M"
            elif amount >= 1e3:
                return f"${amount/1e3:.2f}K"
            else:
                return f"${amount:,.0f}"
        except:
            return str(amount)
    
    def get_response_for_query(self, query_type, **kwargs):
        """Generate response based on query type - FIXED version"""
        try:
            if query_type == "total_revenue":
                if 'year' in kwargs and kwargs['year']:
                    amount = self.get_total_revenue(kwargs['year'])
                    # Check if amount is a number or error message
                    if isinstance(amount, (int, float)):
                        return f"Total pendapatan tahun {kwargs['year']} adalah {self.format_currency(amount)}"
                    else:
                        return amount  # Return error message
                else:
                    revenues = self.get_total_revenue()
                    if isinstance(revenues, dict):
                        response = "📊 **Pendapatan per tahun:**\n\n"
                        for year, amount in revenues.items():
                            response += f"• **{year}**: {self.format_currency(amount)}\n"
                        return response
                    else:
                        return str(revenues)
            
            elif query_type == "net_income":
                if 'year' in kwargs and kwargs['year']:
                    amount = self.get_net_income(kwargs['year'])
                    if isinstance(amount, (int, float)):
                        return f"Laba bersih tahun {kwargs['year']} adalah {self.format_currency(amount)}"
                    else:
                        return amount
                else:
                    incomes = self.get_net_income()
                    if isinstance(incomes, dict):
                        response = "📊 **Laba bersih per tahun:**\n\n"
                        for year, amount in incomes.items():
                            response += f"• **{year}**: {self.format_currency(amount)}\n"
                        return response
                    else:
                        return str(incomes)
            
            elif query_type == "revenue_growth":
                growth = self.get_revenue_growth()
                if growth:
                    response = "📈 **Pertumbuhan pendapatan year-over-year:**\n\n"
                    for period, percentage in growth.items():
                        arrow = "📈" if percentage > 0 else "📉"
                        response += f"• {arrow} **{period}**: {percentage}%\n"
                    return response
                else:
                    return "Data pertumbuhan tidak tersedia"
            
            elif query_type == "profit_margin":
                margins = self.get_profit_margin_trend()
                if isinstance(margins, dict):
                    response = "📊 **Profit margin per tahun:**\n\n"
                    for year, margin in margins.items():
                        response += f"• **{year}**: {margin}%\n"
                    return response
                else:
                    return str(margins)
            
            elif query_type == "key_insights":
                insights = self.get_key_insights()
                if insights:
                    response = "💡 **Insight Utama:**\n\n"
                    for i, insight in enumerate(insights, 1):
                        response += f"{i}. {insight}\n"
                    return response
                else:
                    return "Tidak ada insight yang tersedia"
            
            else:
                return None
                
        except Exception as e:
            return f"Maaf, terjadi kesalahan dalam memproses pertanyaan: {str(e)}"
    
    def calculate_growth_percentage(self, current, previous):
        """Calculate growth percentage between two values"""
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100, 1)
    
    def get_financial_summary(self):
        """Get summary of all financial data"""
        summary = "📋 **Ringkasan Keuangan GFC**\n\n"
        
        # Add revenue summary
        revenues = self.get_total_revenue()
        if isinstance(revenues, dict):
            summary += "**Pendapatan:**\n"
            for year, amount in revenues.items():
                summary += f"  • {year}: {self.format_currency(amount)}\n"
        
        # Add net income summary
        incomes = self.get_net_income()
        if isinstance(incomes, dict):
            summary += "\n**Laba Bersih:**\n"
            for year, amount in incomes.items():
                summary += f"  • {year}: {self.format_currency(amount)}\n"
        
        # Add growth
        growth = self.get_revenue_growth()
        if growth:
            summary += "\n**Pertumbuhan:**\n"
            for period, percentage in growth.items():
                summary += f"  • {period}: {percentage}%\n"
        
        return summary