# Crop Recommendation System

A professional Streamlit-based Final Year Project rebuild for a machine learning crop recommendation system.

## Core ML Purpose

The system predicts the most suitable crop using:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall

The deployed model is **Random Forest** to match the FYP / Investigation Report. SVM and GaussianNB are included for academic model comparison.

## Version 2 Improvements

This build improves the first rebuild based on UI and privacy feedback:

- Normal users only see their own prediction history.
- Admin pages are separated from normal user pages.
- Model Comparison is admin/academic only, not shown in the normal user sidebar.
- Admin can edit users, reset passwords, delete users, view all prediction logs, delete logs, and clear a selected user's history.
- Sidebar no longer shows "2.0 FYP Rebuild".
- Google/Facebook login buttons were removed because they were not functional and were risky for FYP demo stability.
- Login page redesigned with a more polished agricultural dashboard style.
- Every major page has a faded agriculture background image and page-specific introduction.
- Sidebar options now include emojis.
- Green/brown agriculture theme, glass cards, hover effects, transitions, and improved spacing added.

## Demo Accounts

```text
Admin
Username: admin
Password: Admin@123

User
Username: demo
Password: Demo@123
```

## How to Run

```bash
cd crop_recommendation_rebuild
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Useful Scripts

```bash
python scripts/train_models.py
python scripts/create_demo_users.py
```

The model files are already included, so training is not required unless you want to regenerate the metrics and artifacts.

## Scope Notes

Real Google/Facebook OAuth and live email sending are intentionally not included in the working demo build. They can be described as future enhancements. The forgot username/password flow uses secure expiring SQLite tokens for a stable FYP demonstration.
