# 📰 News Summarization & Sentiment Analysis App  
### **Extract, Analyze, and Summarize News Effortlessly**  

🚀 This project scrapes the latest news articles, performs sentiment analysis, extracts trending words, and generates a Hindi speech summary using **BeautifulSoup, NLTK, Google TTS, and Streamlit**.  

---

## 📌 **Features**
✅ **News Extraction** – Scrapes at least 10 articles for a given company using **BeautifulSoup**.  
✅ **Sentiment Analysis** – Classifies news as **Positive, Negative, or Neutral** using **NLTK's VADER**.  
✅ **Comparative Analysis** – Analyzes sentiment trends across different sources.  
✅ **Text-to-Speech (TTS)** – Converts news summaries to **Hindi speech** using **gTTS**.  
✅ **User Interface** – Interactive **Streamlit UI** for news analysis.  
✅ **API Development** – Ensures frontend-backend communication via **Flask API**.  
✅ **Deployment Ready** – Can be deployed on **Hugging Face Spaces** or **Heroku**.  

---

## 📂 **Project Structure**
```bash
news-summarization-app/
│── app.py                  # Streamlit UI (Frontend)
│── api.py                  # Flask API (Backend)
│── utils.py                 # Helper functions (Scraping, Sentiment Analysis, TTS)
│── requirements.txt         # Dependencies list
│── README.md               # Documentation
│── deployment/             # Deployment scripts/configs
│── data/                   # (Optional) Sample news data for testing
│── models/                 # (Optional) Pre-trained models (if needed)
│── .gitignore              # Ignore unnecessary files (if using Git)
│── venv/                   # Virtual environment (ignored in Git)
```

---

## 🛠 **Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/news-summarization-app.git
cd news-summarization-app
```

### **2️⃣ Set Up a Virtual Environment**
For **Windows**:
```sh
python -m venv env
env\Scripts\activate
```
For **macOS/Linux**:
```sh
python3 -m venv env
source env/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Run the Application**
Run using **Streamlit**:
```sh
python -m streamlit run app.py
```
Or:
```sh
streamlit run app.py
```
(If `streamlit` command fails, see the troubleshooting section below.)

---

## 🚀 **Usage**
1. **Enter a company name** (e.g., "Tesla") in the text input.  
2. Click **"Analyze News"** to fetch and summarize articles.  
3. View **sentiment analysis, trending words, and article details**.  
4. Click **"Generate Hindi News Summary"** to create and play a Hindi speech summary.  

---

## 🔧 **Troubleshooting**
### **1️⃣ Streamlit Command Not Found**
If `streamlit run app.py` fails, try:
```sh
python -m streamlit run app.py
```
If the issue persists, add Streamlit to the system PATH:
```sh
where streamlit  # Windows
which streamlit  # macOS/Linux
```
Then add the output path to your environment variables.

### **2️⃣ Virtual Environment Issues**
Ensure your environment is activated:
```sh
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows
```

---

## 🌍 **Deployment**
### **Hugging Face Spaces**
1. Create a **Hugging Face Space** (select **Streamlit** template).  
2. Upload the project files.  
3. Define `requirements.txt` for dependencies.  
4. Deploy! 🚀  

### **Heroku (For Flask API)**
1. Install **Heroku CLI** and log in:
   ```sh
   heroku login
   ```
2. Create a new app:
   ```sh
   heroku create news-summarization-app
   ```
3. Deploy:
   ```sh
   git push heroku main
   ```

---

## 🤝 **Contributing**
Feel free to contribute by:
- Reporting issues
- Suggesting improvements
- Adding new features  

---

## 📜 **License**
This project is **open-source** and available under the **MIT License**.  

