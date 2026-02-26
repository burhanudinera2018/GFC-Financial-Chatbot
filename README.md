```markdown
# 💰 GFC Financial Chatbot

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral%20%7C%20Llama2-green)](https://ollama.ai/)

## 📋 Deskripsi Proyek
Chatbot AI untuk analisis keuangan Global Finance Corp (GFC) yang dapat menjawab pertanyaan tentang data keuangan perusahaan. Menggabungkan **rule-based logic** untuk query spesifik dan **Local LLM (Ollama)** untuk pertanyaan umum.


## 🏗️ Struktur Proyek
```
GFC-Financial-Chatbot/
├── src/
│   ├── app.py                 # Main Streamlit app
│   ├── chatbot_logic.py       # Rule-based + LLM logic
│   ├── data_loader.py         # Load financial data
│   ├── financial_analyzer.py  # Financial calculations
│   └── utils.py               # Helper functions
├── data/
│   └── financial_data.json    # Data dari Tugas 1
├── requirements.txt
└── README.md
```
### **Komponen Utama:**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Input    │────▶│  Pattern Match  │────▶│ Rule-based Resp │
│  (Streamlit UI) │     │                 │     │  (Predefined)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                        │
         │                       ▼                        │
         │              ┌─────────────────┐               │
         └─────────────▶│   Ollama LLM    │◀──────────────┘
                        │  (Mistral/Llama)│
                        └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Financial Data │
                        │    (JSON/CSV)   │
                        └─────────────────┘
```

### **Teknologi yang Digunakan:**
- **Frontend**: Streamlit (Python-based web framework)
- **Backend Logic**: Python dengan pattern matching
- **LLM Integration**: Ollama dengan model Mistral/Llama2
- **Data Processing**: Pandas, NumPy
- **Visualisasi**: Plotly untuk charts interaktif

## ✨ **Fitur-Fitur Utama**

### **1. Rule-Based Query System**
Chatbot memiliki 5 kategori query yang telah didefinisikan:

| Kategori | Contoh Query | Response |
|----------|--------------|----------|
| **Total Revenue** | "Pendapatan 2023" | Nilai spesifik dengan format mata uang |
| **Net Income** | "Laba bersih" | Tabel laba semua tahun |
| **Revenue Growth** | "Pertumbuhan pendapatan" | Persentase YoY dengan indikator 📈/📉 |
| **Profit Margin** | "Margin keuntungan" | Margin per tahun |
| **Key Insights** | "Insight keuangan" | Poin-poin penting dari analisis |

### **2. Multi-Language Support**
- **Bahasa Indonesia**: "pendapatan 2023", "laba bersih"
- **English**: "revenue 2023", "net income"
- **Campuran**: Chatbot memahami kedua bahasa

### **3. Year-Specific Queries**
- Query tahun spesifik: "revenue 2022" → return nilai tunggal
- Query umum: "revenue" → return semua tahun

### **4. LLM Integration untuk Pertanyaan Kompleks**
Ketika query tidak cocok dengan pattern yang ada, chatbot menggunakan Ollama untuk:
- Analisis tren ("Bagaimana performa GFC dalam 3 tahun terakhir?")
- Perbandingan ("Bandingkan 2022 dengan 2023")
- Interpretasi ("Apa arti margin 15% bagi perusahaan?")

### **5. Confidence Indicators**
- ✅ **High Confidence**: Berdasarkan data langsung
- 🤖 **Medium Confidence**: Dihasilkan oleh AI dengan konteks data
- ⚠️ **Low Confidence**: Fallback response

### **6. Interactive Visualizations**
- **Line Chart**: Tren pendapatan
- **Bar Chart**: Laba bersih per tahun
- **Sidebar Metrics**: Ringkasan cepat

## 🚀 Cara Install dan Menjalankan

### Prasyarat
- Python 3.11
- Ollama (https://ollama.ai)
- Data keuangan dari Tugas 1

### Langkah-langkah

1. **Clone repository**
```bash
git clone https://github.com/burhanudinera2018/GFC-Financial-Chatbot.git
cd GFC-Financial-Chatbot
```

2. **Buat virtual environment**
```bash
python3.11 -m venv venv_chatbot
source venv_chatbot/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Setup Ollama**
```bash
# Terminal 1: Jalankan Ollama
ollama serve

# Terminal 2: Download model
ollama pull mistral:latest
```

5. **Siapkan data**  
   Copy file JSON dari Tugas 1 ke folder `data/financial_data.json`

6. **Jalankan aplikasi**
```bash
streamlit run src/app.py --server.port 8503
```

7. **Buka browser**
```
http://localhost:8503
```

## 📊 Query yang Didukung

### Rule-based Queries (High Confidence)
| Pertanyaan | Response |
|------------|----------|
| "Total revenue" | Menampilkan pendapatan semua tahun |
| "Revenue 2023" | Pendapatan tahun 2023 |
| "Net income" | Laba bersih semua tahun |
| "Profit margin" | Margin keuntungan |
| "Revenue growth" | Pertumbuhan year-over-year |
| "Key insights" | Insight utama dari data |

### LLM-powered Queries (Medium Confidence)
- Pertanyaan umum tentang keuangan
- Perbandingan antar tahun
- Analisis tren
- Pertanyaan dalam bahasa Indonesia

## 🧪 Testing

**Test Case 1: Rule-based Query**
```
User: Berapa total pendapatan 2023?
Bot: Total pendapatan tahun 2023 adalah $195.00M
```

**Test Case 2: LLM Query**
```
User: Bagaimana performa keuangan GFC dalam 3 tahun terakhir?
Bot: Berdasarkan data, GFC menunjukkan pertumbuhan yang konsisten...
```

**Test Case 3: Year-specific**
```
User: pendapatan 2022
Bot: Total pendapatan tahun 2022 adalah $168.00M
```

## 📝 Dokumentasi Tugas

### Pertanyaan yang Telah Didefinisikan (Predefined Queries)
1. **Total Revenue** - Menampilkan pendapatan semua tahun atau tahun spesifik
2. **Net Income** - Menampilkan laba bersih
3. **Revenue Growth** - Menghitung pertumbuhan year-over-year
4. **Profit Margin** - Menampilkan margin keuntungan per tahun
5. **Key Insights** - Menampilkan insight utama dari analisis

### Cara Kerja Chatbot
1. **Input Processing**: Membersihkan input user dan mengekstrak tahun jika ada
2. **Pattern Matching**: Mencocokkan dengan pattern query yang sudah didefinisikan
3. **Rule-based Response**: Jika cocok, ambil data dari analyzer dan format response
4. **LLM Fallback**: Jika tidak cocok dan opsi LLM aktif, gunakan Ollama
5. **Confidence Indicator**: Menandai sumber response (data vs AI)


## 📄 Lisensi
Proyek ini dibuat untuk keperluan penyelesaian tugas Virtual Internship Job simulation involving AI-powered financial chatbot development for BCG's GenAI Consulting team..

## 👨‍💻 Author
**Burhanudin Badiuzaman** - Data Analyst

```