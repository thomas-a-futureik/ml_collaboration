# Onboarding Guide for Interns

Welcome to the Image Classification Project! This guide will help you get started with your assigned task (Age/Gender/Expression/Race classification).

## 🚀 Getting Started

### 1. Repository Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ml_collaboration
   ```

2. **Set up the environment**
   ```bash
   # Create and activate a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### 2. Project Structure

```
ml_collaboration/
├── data/
│   └── processed/
│       ├── age/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       ├── gender/
│       ├── expression/
│       └── race/
├── notebooks/
│   ├── age/
│   │   └── main.ipynb
│   ├── gender/
│   ├── expression/
│   └── race/
├── models/
└── README.md
```

## 🖥️ Working with Notebooks

### 1. Starting Jupyter

```bash
# Activate your virtual environment first
jupyter notebook
# or
jupyter lab
```

### 2. Notebook Workflow

1. **Data Loading**
   - Load your dataset from the appropriate directory
   - Example: `data/processed/age/train/`

2. **Model Development**
   - Use the provided template in your task's notebook
   - Follow MLflow for experiment tracking

3. **Saving Outputs**
   - Save models to the `models/` directory
   - Log all experiments using MLflow

## 📊 MLflow Integration

### 1. Starting MLflow UI

```bash
mlflow ui
```

### 2. Logging Parameters and Metrics

```python
import mlflow

with mlflow.start_run():
    # Log parameters (key-value pairs)
    mlflow.log_param("learning_rate", 0.01)
    
    # Log metrics (e.g., accuracy, loss)
    mlflow.log_metric("accuracy", 0.95)
    
    # Log artifacts (plots, models, etc.)
    mlflow.log_artifact("confusion_matrix.png")
```

## 📁 Data Versioning with DVC (Optional)

### 1. Tracking Large Files

```bash
# Add data to DVC
dvc add data/processed/age

# Track changes with git
git add data/processed/age.dvc data/.gitignore
git commit -m "Add processed age data"

# Push to remote storage
dvc push
```

## 🔄 Version Control Best Practices

1. **Before Starting Work**
   ```bash
   git pull origin main
   ```

2. **Creating a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Committing Changes**
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   git push origin your-branch-name
   ```

## 📋 Task Checklist

- [ ] Set up the development environment
- [ ] Familiarize yourself with the project structure
- [ ] Review the notebook template for your task
- [ ] Start with data exploration
- [ ] Implement and train your model
- [ ] Log experiments with MLflow
- [ ] Document your findings

## 🆘 Getting Help

- For technical issues, check the project's issue tracker
- Reach out to your mentor for guidance
- Document any problems you encounter and how you solved them

## 📝 Best Practices

1. **Code Organization**
   - Keep your code modular
   - Add comments explaining complex logic
   - Use meaningful variable names

2. **Documentation**
   - Update the notebook with your findings
   - Document any assumptions or decisions made

3. **Reproducibility**
   - Pin package versions in requirements.txt
   - Document any manual setup steps

Happy coding! 🚀
