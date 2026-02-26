"""
Main Streamlit Application for Financial Chatbot
Run with: streamlit run src/app.py --server.port 8503
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_financial_data, get_financial_dataframe
from src.chatbot_logic import FinancialChatbot
from src.utils import create_revenue_chart, create_income_chart, format_message

# Page config
st.set_page_config(
    page_title="GFC Financial Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        font-weight: semi-bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
    }
    .bot-message {
        background-color: #F3F4F6;
        border-left: 4px solid #10B981;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    .suggestion-btn {
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Halo! Saya asisten keuangan GFC. Saya bisa membantu Anda menganalisis data keuangan perusahaan. Silakan tanya tentang pendapatan, laba, pertumbuhan, atau insight keuangan lainnya!"}
    ]
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

# Header
st.markdown('<p class="main-header">💰 GFC Financial Chatbot</p>', unsafe_allow_html=True)
st.markdown("Asisten AI untuk analisis keuangan Global Finance Corp")

# Load data
with st.spinner("Loading financial data..."):
    financial_data = load_financial_data()

# Initialize chatbot
if st.session_state.chatbot is None:
    st.session_state.chatbot = FinancialChatbot(financial_data)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/bank.png", width=80)
    st.markdown("## 🤖 Chatbot Settings")
    st.markdown("---")
    
    # Company info
    st.markdown("### 📊 Company Info")
    st.markdown(f"**Company:** {financial_data['company']}")
    st.markdown(f"**Period:** {financial_data['period']}")
    
    st.markdown("---")
    
    # Model selection
    st.markdown("### 🧠 AI Model")
    model_options = ['mistral:latest', 'llama2:latest']
    selected_model = st.selectbox(
        "Pilih Model LLM",
        model_options,
        index=0,
        help="Pilih model yang tersedia di Ollama"
    )
    
    # Update model if changed
    if selected_model != st.session_state.chatbot.model_name:
        st.session_state.chatbot.model_name = selected_model
        st.success(f"Model diubah ke {selected_model}")
    
    # LLM toggle
    use_llm = st.checkbox("Gunakan AI untuk pertanyaan umum", value=True, 
                          help="Jika nonaktif, hanya akan menjawab pertanyaan yang sudah ditentukan")
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📈 Quick Stats")
    df = get_financial_dataframe(financial_data)
    latest_year = df['Year'].iloc[-1]
    prev_year = df['Year'].iloc[-2]
    
    revenue_growth = ((df['Revenue'].iloc[-1] - df['Revenue'].iloc[-2]) / df['Revenue'].iloc[-2]) * 100
    
    st.metric("Pendapatan 2023", f"${df['Revenue'].iloc[-1]/1e6:.1f}M", 
              f"{revenue_growth:.1f}%")
    st.metric("Laba Bersih 2023", f"${df['Net Income'].iloc[-1]/1e6:.1f}M")
    st.metric("Profit Margin", f"{df['Profit Margin'].iloc[-1]}%")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Halo! Saya asisten keuangan GFC. Silakan tanya tentang data keuangan perusahaan!"}
        ]
        st.rerun()

# Main content - Chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="sub-header">💬 Chat dengan Asisten Keuangan</p>', unsafe_allow_html=True)
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 **Anda:** {message["content"]}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">🤖 **Chatbot:** {message["content"]}</div>', 
                          unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Suggested questions
    st.markdown("**📝 Pertanyaan yang disarankan:**")
    suggested = st.session_state.chatbot.get_suggested_questions()
    cols = st.columns(3)
    for i, question in enumerate(suggested[:3]):
        with cols[i]:
            if st.button(question[:20] + "...", key=f"sugg_{i}", use_container_width=True):
                # Process this question
                user_input = question
                
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get response
                with st.spinner("Chatbot sedang berpikir..."):
                    result = st.session_state.chatbot.get_response(user_input, use_llm=use_llm)
                    response = result["response"]
                    
                    # Add confidence indicator
                    if result["confidence"] == "high":
                        response += "\n\n_✅ Berdasarkan data yang tersedia_"
                    elif result["confidence"] == "medium":
                        response += "\n\n_🤖 Dihasilkan oleh AI_"
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
    
    # Text input
    user_input = st.chat_input("Ketik pertanyaan Anda di sini...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response
        with st.spinner("Chatbot sedang berpikir..."):
            result = st.session_state.chatbot.get_response(user_input, use_llm=use_llm)
            response = result["response"]
            
            # Add confidence indicator
            if result["confidence"] == "high":
                response += "\n\n_✅ Berdasarkan data yang tersedia_"
            elif result["confidence"] == "medium":
                response += "\n\n_🤖 Dihasilkan oleh AI_"
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

with col2:
    st.markdown('<p class="sub-header">📊 Visualisasi Data</p>', unsafe_allow_html=True)
    
    # Charts
    with st.expander("📈 Tren Pendapatan", expanded=True):
        fig1 = create_revenue_chart(financial_data)
        st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("📊 Laba Bersih", expanded=True):
        fig2 = create_income_chart(financial_data)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Key insights
    with st.expander("💡 Key Insights", expanded=True):
        insights = financial_data.get('key_insights', [])
        for insight in insights:
            st.markdown(f"- {insight}")
    
    # Quick info
    with st.expander("ℹ️ Cara Menggunakan", expanded=False):
        st.markdown("""
        **Pertanyaan yang bisa dijawab:**
        - Pendapatan per tahun
        - Laba bersih
        - Pertumbuhan revenue
        - Profit margin
        - Insight keuangan
        
        **Tips:**
        - Gunakan bahasa Indonesia atau Inggris
        - Tanyakan tahun spesifik (contoh: "revenue 2023")
        - Klik pertanyaan yang disarankan untuk demo
        """)

# Footer
st.markdown("---")
st.markdown("© 2024 GFC Financial Chatbot | Powered by Streamlit + Ollama")