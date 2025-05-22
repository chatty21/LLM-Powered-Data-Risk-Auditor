# 🧠 LLaMA 2-Powered Data Risk Auditor

> “Risk is what you don’t see — until your data tells you.”

## Project link
https://llm-powered-data-risk-auditor.streamlit.app/

## 📌 Project Overview
The **LLaMA 2-Powered Data Risk Auditor** is an advanced data analysis tool that allows users to upload structured datasets (CSV or JSON) and instantly gain insights about data quality, potential risks, and summary statistics. It uses both traditional data profiling techniques and large language model (LLM) reasoning to assess data biases, missing values, imbalances, and sensitive fields.

The tool is designed with an interactive and animated Streamlit UI, complemented by glowing UI elements, themed styling, and a tech-inspired backdrop for a modern user experience.

---

## 🛠️ Technologies Used
| Category | Tools |
|---------|------|
| Frontend UI | Streamlit (Python-based), custom CSS |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| LLM Integration | LLaMA 2 via Ollama (Local LLM Inference) |
| Backend Enhancements | dotenv for API keys, modularized Python scripts |

---

## 🔄 Features & Capabilities
### ✅ Core Functionalities
- **File Uploader** supporting CSV and JSON (up to 1GB)
- **Dataset Summary** with:
  - Total rows, columns, missing values
  - Per-column: datatype, unique count, null count, examples
- **Visualizations**:
  - Missing value bar plot
  - High cardinality detection
  - Numeric distribution histograms
  - Correlation heatmap with top-50 features and rotation

### 🤖 LLM-Powered Insights
- Integrated **LLaMA 2** using Ollama for:
  - Risk summarization
  - Bias detection (e.g. gender or regional imbalance)
  - Suggestions for handling data issues (e.g. column merging, imputation)

### 🎨 UI/UX Enhancements
- Neon-green glowing title and button hover effects
- Glassmorphism styling with dark/light auto toggle based on time
- Animated title and fade-in sections
- Fully responsive layout with smooth visual transitions

---

## 🧪 Example Use Cases
- Auditing a large e-commerce dataset for potential data leakage
- Exploring class imbalance in churn prediction datasets
- Detecting sensitive fields in healthcare or HR data
- Understanding correlation between performance and salary in sports analytics

---

## 🗂️ Project Structure
```
├── app.py                      # Main Streamlit app logic
├── modules/
│   ├── data_profile.py        # Dataset summary and profiling logic
│   └── llm_analyzer.py        # LLM (LLaMA 2) interaction module
├── Data/
│   └── ecommerce_orders.csv   # Sample dataset (500MB+)
├── .env                       # API key configuration (if needed)
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## 💡 Future Enhancements
- Add **PDF/HTML report export** with charts and analysis
- Include **chatbot interface** to ask questions to the dataset
- Provide an **AutoML insight module** with model recommendations
- Add **customizable dashboards** with filters and pinboards

---

## 🚀 How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/llm-data-risk-auditor
   cd llm-data-risk-auditor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start LLaMA 2 with Ollama (if not already running):
   ```bash
   ollama run llama2
   ```

4. Launch the Streamlit app:
   ```bash
   streamlit run app.py --server.maxUploadSize=1000
   ```

---

## 📃 License
This project is licensed under the MIT License.

---

## 👨‍💻 Author
**Chaitanya [Your Last Name]**  
M.S. in Information Technology & Analytics – Rochester Institute of Technology  
Built for educational and research purposes.

---

### 🔗 Connect with Me
- [LinkedIn](https://www.linkedin.com/in/your-profile)
- [GitHub](https://github.com/your-username)

---

