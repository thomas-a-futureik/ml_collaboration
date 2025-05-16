# Image Classification Internship Project

This repository is designed for interns to collaboratively build image classification models for age, gender, expression, and race using processed datasets. It integrates MLflow for experiment tracking and DVC for optional data/model versioning. Each task has its own notebook for clarity and modularity.

## Structure
- `/notebooks/<task>/main.ipynb`: One notebook per task (age, gender, expression, race)
- `/data/processed/`: Processed datasets for each task
- `/models/`: Exported models (TFLite, ONNX, etc.)
- `/docs/`: Onboarding and guides

## Getting Started
1. Clone this repo (from GitHub or DagsHub)
2. Install dependencies: `pip install -r requirements.txt`
3. Follow onboarding in `/docs/onboarding.md`
4. Work in the relevant notebook under `/notebooks/<task>/`

## Tracking
- Use MLflow to log experiments and models
- Use DVC to track processed data and models if needed

## Contribution
- Beginner-friendly; see `/docs/onboarding.md` for step-by-step instructions.