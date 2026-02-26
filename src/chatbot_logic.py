"""
Module untuk logika chatbot - Rule-based + LLM integration
"""
import streamlit as st
import requests
import json
import re
from src.financial_analyzer import FinancialAnalyzer

class FinancialChatbot:
    def __init__(self, financial_data, model_name='mistral:latest'):
        self.analyzer = FinancialAnalyzer(financial_data)
        self.model_name = model_name
        self.ollama_url = 'http://localhost:11434'
        
        # Define predefined queries and their mappings
        self.predefined_queries = {
            # English queries
            "total revenue": {"type": "total_revenue", "description": "Total pendapatan"},
            "revenue": {"type": "total_revenue", "description": "Total pendapatan"},
            "net income": {"type": "net_income", "description": "Laba bersih"},
            "profit": {"type": "net_income", "description": "Laba bersih"},
            "revenue growth": {"type": "revenue_growth", "description": "Pertumbuhan pendapatan"},
            "growth": {"type": "revenue_growth", "description": "Pertumbuhan"},
            "profit margin": {"type": "profit_margin", "description": "Margin keuntungan"},
            "margin": {"type": "profit_margin", "description": "Margin"},
            "insights": {"type": "key_insights", "description": "Insight utama"},
            "key insights": {"type": "key_insights", "description": "Insight utama"},
            
            # Indonesian queries
            "pendapatan": {"type": "total_revenue", "description": "Total pendapatan"},
            "laba bersih": {"type": "net_income", "description": "Laba bersih"},
            "keuntungan": {"type": "net_income", "description": "Keuntungan"},
            "pertumbuhan": {"type": "revenue_growth", "description": "Pertumbuhan"},
            "margin": {"type": "profit_margin", "description": "Margin keuntungan"},
            "insight": {"type": "key_insights", "description": "Insight"}
        }
        
        # Year pattern for queries like "revenue 2023"
        self.year_pattern = r'\b(19|20)\d{2}\b'
    
    def check_ollama(self):
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def extract_year(self, query):
        """Extract year from query if present"""
        years = re.findall(self.year_pattern, query)
        return years[0] if years else None
    
    def match_predefined_query(self, query):
        """Match user query to predefined query types"""
        query_lower = query.lower()
        
        # Check for year in query
        year = self.extract_year(query)
        
        # Try to match with predefined queries
        for key, mapping in self.predefined_queries.items():
            if key in query_lower:
                return mapping['type'], year
        
        return None, None
    
    def get_rule_based_response(self, query):
        """Generate response using rule-based logic"""
        query_type, year = self.match_predefined_query(query)
        
        if query_type:
            return self.analyzer.get_response_for_query(query_type, year=year)
        
        return None
    
    def get_llm_response(self, query, context_data):
        """Generate response using Ollama LLM"""
        if not self.check_ollama():
            return None
        
        # Prepare context for LLM
        prompt = f"""You are a financial analyst chatbot for Global Finance Corp (GFC). 
Answer the user's question based on the financial data provided.

FINANCIAL DATA CONTEXT:
Company: {context_data['company']}
Period: {context_data['period']}

Key Financials (in millions):
- Revenue 2023: ${context_data['financials']['revenue']['2023']/1e6:.1f}M
- Revenue 2022: ${context_data['financials']['revenue']['2022']/1e6:.1f}M  
- Net Income 2023: ${context_data['financials']['net_income']['2023']/1e6:.1f}M
- Net Income 2022: ${context_data['financials']['net_income']['2022']/1e6:.1f}M
- Profit Margin: {context_data['financials']['profit_margin']['2023']}%

Key Insights:
{chr(10).join(['- ' + i for i in context_data.get('key_insights', [])])}

USER QUESTION: {query}

INSTRUCTIONS:
1. Answer in Indonesian language
2. Be concise but informative (2-3 sentences)
3. Use the financial data provided
4. If the question is not related to financial data, politely redirect
5. Format numbers appropriately (use M for millions, B for billions)

ANSWER:"""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                return None
                
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return None
    
    def get_response(self, query, use_llm=True):
        """Main method to get response - combines rule-based and LLM"""
        
        # First try rule-based (for predefined queries)
        rule_response = self.get_rule_based_response(query)
        
        if rule_response:
            return {
                "type": "rule_based",
                "response": rule_response,
                "confidence": "high"
            }
        
        # If not found and LLM is enabled, try LLM
        if use_llm:
            llm_response = self.get_llm_response(query, self.data)
            if llm_response:
                return {
                    "type": "llm",
                    "response": llm_response,
                    "confidence": "medium"
                }
        
        # Fallback response
        return {
            "type": "fallback",
            "response": "Maaf, saya hanya bisa menjawab pertanyaan tentang data keuangan GFC. Coba tanyakan tentang pendapatan, laba, pertumbuhan, atau insight keuangan lainnya.",
            "confidence": "low"
        }
    
    @property
    def data(self):
        return self.analyzer.data
    
    def get_suggested_questions(self):
        """Get list of suggested questions"""
        return [
            "Berapa total pendapatan tahun 2023?",
            "Bagaimana laba bersih tahun ini?",
            "Pertumbuhan pendapatan year-over-year",
            "Profit margin perusahaan",
            "Insight keuangan utama",
            "Bandingkan pendapatan 2022 dan 2023"
        ]