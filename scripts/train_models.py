from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ml.train_models import train_all_models

if __name__ == "__main__":
    train_all_models()
    print("Models and artifacts created successfully.")
