# End-to-End Network Security / Phishing Website Detection ML Pipeline

## 📌 Project Overview
This project is an end-to-end, production-ready Machine Learning pipeline designed to classify websites as malicious (phishing) or safe based on their network data features. The project strictly adheres to industry best practices, featuring a highly modular object-oriented programming (OOP) architecture, custom exception handling, and custom logging. 

The application incorporates a complete MLOps lifecycle—from an automated ETL data pipeline connected to a cloud database, to remote experiment tracking, cloud artifact storage, and a fully automated CI/CD deployment on AWS.

## 🛠️ Tech Stack & Tools
* **Language:** Python 3.10
* **Database:** MongoDB Atlas (Cloud)
* **Machine Learning:** Scikit-Learn (Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost, KNN Imputer)
* **MLOps & Tracking:** MLflow, DAGsHub
* **Web Framework:** FastAPI, Uvicorn, Jinja2 Templates
* **Cloud & DevOps:** Docker, AWS ECR (Elastic Container Registry), AWS EC2, AWS S3, AWS CLI
* **CI/CD:** GitHub Actions (with Self-Hosted App Runner)

## 🚀 Pipeline Architecture & Workflow

1. **ETL Pipeline:** Extracts local raw network data (CSV), transforms it into JSON (key-value pairs), and loads it into a remote MongoDB Atlas database.
   
2. **Data Ingestion:** Reads the JSON data from MongoDB, converts it into a pandas DataFrame, splits the data into training and testing sets (80/20 ratio), and stores them in a local feature store artifact folder.
   
3. **Data Validation:** Validates the dataset schema (ensuring correct column count and numerical data types). Most importantly, it detects **Data Drift** by comparing the distribution of training and incoming test data using the `ks_2samp` statistical hypothesis test from SciPy, generating a YAML report.
   
4. **Data Transformation:** Applies feature engineering by dropping the target column, mapping the target variables (converting -1 to 0), and handling any missing values dynamically using a `KNNImputer` pipeline. The fitted preprocessor is saved as a `preprocessor.pkl` file.
   
5. **Model Training & Hyperparameter Tuning:** Trains multiple classification models and performs hyperparameter tuning utilizing `GridSearchCV`. The best-performing model is selected based on evaluated metrics.
    
6. **Model Evaluation & MLOps Tracking:** Calculates the F1 Score, Precision, and Recall. Evaluated metrics and model parameters are logged and tracked remotely using **MLflow** connected to **DAGsHub** for team collaboration.
    
7. **Model Pusher (AWS S3):** Automatically syncs and uploads the generated pipeline artifacts, the final `model.pkl`, and the `preprocessor.pkl` to an **AWS S3 Bucket** using the AWS CLI, ensuring remote model versioning and storage.
    
8. **FastAPI Web Interface:** Exposes the pipeline via two main API routes:
   * `/train`: Triggers the entire ML training pipeline from ingestion to pushing the model to S3.
   * `/predict`: Accepts an uploaded CSV file containing testing data and performs **batch prediction**, outputting an HTML table and a downloadable CSV of the predictions.
     
9. **CI/CD Deployment:** Contains a complete GitHub Actions workflow. On every push to the `main` branch, the pipeline performs Continuous Integration (code checkout, environment setup), Continuous Delivery (building a Docker image and pushing it to AWS ECR), and Continuous Deployment (pulling the latest image to an AWS EC2 instance via a self-hosted runner and serving it on port 8080).

## 📁 Project Structure
The project maintains a highly modular structure suitable for enterprise environments:
```text
├── .github/workflows/      # GitHub Actions CI/CD YAML files
├── network_security/       # Main project package
│   ├── components/         # Ingestion, Validation, Transformation, Trainer modules
│   ├── constant/           # Hardcoded training and pipeline variables
│   ├── entity/             # Config and Artifact entities (Data classes)
│   ├── exception/          # Custom Exception handling script
│   ├── logging/            # Custom Logger setup
│   ├── pipeline/           # Training and batch prediction pipelines
│   ├── cloud/              # AWS S3 sync scripts
│   └── utils/              # Generic helper functions (save/load pickle, read yaml)
├── templates/              # Jinja2 HTML templates for FastAPI front-end
├── network_data/           # Raw CSV source data
├── app.py                  # FastAPI application entry point
├── main.py                 # Pipeline execution script
├── Dockerfile              # Docker container configurations
├── setup.py                # Setup script to initialize the project as a package
└── requirements.txt        # Python dependencies
```

## ⚙️ Installation & Local Setup

**1. Clone the repository and navigate to the project directory:**
```bash
git clone <your-github-repo-url>
cd <repository-folder>
```

**2. Create and activate a virtual environment:**
```bash
conda create -p venv python=3.10 -y
conda activate ./venv
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Environment Variables Setup:**
Create a `.env` file in the root directory and add your credentials:
```env
MONGO_DB_URL="your_mongodb_atlas_connection_string"
AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
```
*(Ensure AWS CLI is installed and configured on your machine if you plan to sync artifacts to S3)*

**5. Start the FastAPI Application:**
```bash
uvicorn app:app --reload
```
Navigate to `http://localhost:8000/docs` to view the Swagger UI and test the `/train` and `/predict` endpoints.
