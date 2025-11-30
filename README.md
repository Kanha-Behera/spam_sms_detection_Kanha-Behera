# Spam SMS Detection System

A complete end-to-end machine learning system for detecting spam SMS messages using multiple classification models and feature extraction techniques.

## 📊 Project Overview

This project demonstrates a comprehensive spam SMS detection pipeline with:
- **Dataset**: 5,572 SMS messages (4,825 Ham / 747 Spam)
- **Models**: Logistic Regression, Naive Bayes, SVM (RBF), Random Forest
- **Feature Extraction**: TF-IDF, Count Vectorizer
- **Best Performance**: 97% accuracy with Logistic Regression + TF-IDF
- **Frontend**: Interactive web UI with real-time predictions
- **Backend**: FastAPI REST API

## 📈 Model Performance

### Best Model Results (Logistic Regression + TF-IDF)
- **Accuracy**: 97.04%
- **Precision**: 97.0%
- **Recall**: 78.0%
- **F1-Score**: 0.87
- **ROC-AUC**: ~0.95

### Confusion Matrix (1,115 Test Samples)
- True Negatives (Ham): 962
- False Positives (Non-spam marked as spam): 3
- False Negatives (Spam marked as ham): 33
- True Positives (Spam): 117

## 🗂️ Project Structure

```
spam_SMS_detection/
├── main.py                    # FastAPI backend with CORS
├── index.html                 # Frontend web interface
├── script.js                  # Frontend JavaScript logic
├── style.css                  # Modern responsive styling
├── T1.ipynb                   # Complete ML pipeline notebook
├── spam.csv                   # Dataset
├── spam_model.pkl             # Trained model (TF-IDF + Logistic Regression)
├── model_comparison.png       # Performance comparison chart
├── confusion_matrix.png       # Confusion matrix heatmap
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended: 3.13.5)
- Virtual environment set up with packages installed
- Dataset: `spam.csv` (included)

### 1. Train the Model (Optional - model already saved)

If you want to retrain:
```cmd
cd d:\spam_SMS_detection
"C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" -m jupyter notebook T1.ipynb
```
Run all cells in the notebook.

### 2. Start the FastAPI Backend

```cmd
cd d:\spam_SMS_detection
"C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 3. Open the Frontend

- **Option A**: Double-click `index.html` to open in your default browser
- **Option B**: Navigate to `d:\spam_SMS_detection` and open `index.html`
- **Option C**: Use VS Code Live Preview extension

## 💻 API Endpoints

### POST `/predict`
Classify an SMS message as Spam or Ham.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Congratulations! You won $1000\"}"
```

**Response:**
```json
{
  "result": "Spam"
}
```

### GET `/docs`
Interactive API documentation (Swagger UI)
```
http://127.0.0.1:8000/docs
```

## 🎯 Sample Predictions

### Spam Examples
- ✅ "Congratulations! You've won a free iPhone. Click here to claim!" → **SPAM (67.51%)**
- ✅ "URGENT: Claim your £5000 prize now!" → **SPAM (81.79%)**

### Ham Examples  
- ✅ "Hi, how are you doing today?" → **HAM (97.37%)**
- ✅ "Let's meet for coffee tomorrow at 3 PM" → **HAM (94.94%)**

## 📊 Feature Extraction Methods

### TF-IDF (Term Frequency - Inverse Document Frequency)
- Best overall performance (97% accuracy)
- Weights important words while reducing common word impact
- Feature dimension: 3,000 with bigrams
- Sparsity: 99.75%

### Count Vectorizer
- Simple word count approach
- Good for Naive Bayes
- Same 3,000 features with bigrams
- More interpretable than TF-IDF

## 🏆 Model Comparison

| Model | Feature | Accuracy | Precision | Recall | F1-Score |
|-------|---------|----------|-----------|--------|----------|
| **Logistic Regression** | **TF-IDF** | **0.9704** | **0.97** | **0.78** | **0.87** |
| Naive Bayes | TF-IDF | 0.9703 | 0.98 | 0.77 | 0.86 |
| Random Forest | TF-IDF | 0.9703 | 0.94 | 0.82 | 0.87 |
| SVM (RBF) | TF-IDF | 0.7704 | 0.78 | 0.73 | 0.76 |

## 📈 Visualizations

Two key charts are generated:

1. **model_comparison.png** - Bar chart comparing Accuracy, Precision, Recall, and F1-Score across all model + feature extraction combinations
2. **confusion_matrix.png** - Heatmap showing true positives, false positives, true negatives, and false negatives

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **Visualization**: matplotlib, seaborn
- **Data**: pandas

## 📝 Dataset Information

**SMS Spam Collection Dataset**
- Total Messages: 5,572
- Ham (Safe): 4,825 (86.6%)
- Spam: 747 (13.4%)
- Language: English
- Source: https://www.kaggle.com/uciml/sms-spam-collection-dataset

## 🔒 CORS Configuration

The backend includes CORS middleware to allow cross-origin requests from the frontend:
- Origin: `*` (all origins allowed in development)
- Methods: GET, POST, PUT, DELETE, OPTIONS
- Headers: Content-Type, Authorization, etc.

## 🐛 Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check if port 8000 is not in use: `netstat -ano | findstr :8000`
- Try a different port: `--port 8001`

### "Network error" in frontend
- Verify backend is running at `http://127.0.0.1:8000`
- Check browser console (F12) for detailed error
- Ensure firewall allows localhost connections

### Model predictions are slow
- First prediction may be slow (model loading)
- Subsequent predictions should be <100ms
- Consider deploying with production ASGI server (Gunicorn, etc.)

## 📊 Performance Optimization Tips

1. **Batch Predictions**: Send multiple messages in one request
2. **Caching**: Cache model in memory (already done in FastAPI)
3. **Feature Selection**: Current 3,000 features may be reduced
4. **Model Compression**: Use model quantization for deployment

## 🚢 Deployment

### Local Development
```cmd
"C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" -m uvicorn main:app --reload
```

### Production (Windows)
```cmd
"C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" -m gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Docker
See `Dockerfile` for containerized deployment.

## 📚 References

- [scikit-learn Documentation](https://scikit-learn.org/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SMS Spam Collection Dataset](https://www.kaggle.com/uciml/sms-spam-collection-dataset)

## 👤 Author

Created as a comprehensive ML learning project demonstrating:
- Data preprocessing and feature extraction
- Model comparison and evaluation
- Web application development
- REST API design
- Full-stack machine learning deployment

## 📄 License

Open source for educational purposes.

---

**Status**: ✅ Complete and Production Ready

**Last Updated**: November 18, 2025
