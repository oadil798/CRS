from __future__ import annotations
from pathlib import Path
from typing import Dict
from src.config import CROP_IMAGES_DIR
from src.utils.formatting import title_crop

IMAGE_FILES = {
    "apple": "Apple.jpg", "banana": "Banana.jpg", "blackgram": "Blackgram.jpg", "chickpea": "Chickpea.jpg",
    "coconut": "Coconut.jpg", "coffee": "Coffee.jpg", "cotton": "Cotton.jpg", "grapes": "Grapes.jpg",
    "jute": "Jute.jpg", "kidneybeans": "Kidneybeans.jpg", "lentil": "Lentil.jpg", "maize": "Maize.jpg",
    "mango": "Mango.jpg", "mothbeans": "Mothbeans.jpg", "mungbean": "Mungbeans.jpg", "muskmelon": "Muskmelon.jpg",
    "orange": "Orange.jpg", "papaya": "Papaya.jpg", "pigeonpeas": "Pigeonpeas.jpg", "pomegranate": "Pomegranate.jpg",
    "rice": "Rice.jpg", "watermelon": "Watermelon.jpg",
}

SUMMARY = {
    "rice": ("Rice usually prefers warm conditions and high water availability.", "Useful for areas with good rainfall or irrigation. Avoid drought stress."),
    "maize": ("Maize is a widely grown cereal crop for food and feed.", "Requires balanced nutrients, sunlight, and moderate rainfall."),
    "chickpea": ("Chickpea is a pulse crop suitable for relatively dry and moderate climates.", "Avoid excessive moisture and waterlogged soil."),
    "kidneybeans": ("Kidney beans are protein-rich legume crops.", "Prefer moderate temperature and well-drained soil."),
    "pigeonpeas": ("Pigeon pea is a warm-season pulse crop with some drought tolerance.", "Avoid waterlogging and monitor pests."),
    "mothbeans": ("Moth bean is a hardy legume crop that can tolerate dry conditions.", "Suitable for dry areas with limited water."),
    "mungbean": ("Mung bean is a short-duration pulse crop grown in warm climates.", "Needs well-drained soil and moderate moisture."),
    "blackgram": ("Black gram is a pulse crop commonly used in South Asian agriculture.", "Prefers warm conditions and controlled moisture."),
    "lentil": ("Lentil is a protein-rich cool-season pulse crop.", "Avoid waterlogging and maintain moderate fertility."),
    "pomegranate": ("Pomegranate is a fruit crop that can tolerate relatively dry conditions.", "Needs sunlight, drainage, and controlled irrigation."),
    "banana": ("Banana is a tropical fruit crop that prefers warm and humid conditions.", "Requires nutrient-rich soil and consistent moisture."),
    "mango": ("Mango is a tropical fruit crop suitable for warm climates.", "Requires sunlight, drainage, and management during flowering."),
    "grapes": ("Grapes are fruit crops used for fresh consumption and processing.", "Require pruning, sunlight, and disease control."),
    "watermelon": ("Watermelon is a warm-season fruit crop.", "Needs sunlight, space, and sufficient moisture."),
    "muskmelon": ("Muskmelon is a warm-season fruit crop grown in well-drained soil.", "Needs sunlight and careful irrigation."),
    "apple": ("Apple is a temperate fruit crop.", "Requires climate suitability, pruning, and disease management."),
    "orange": ("Orange is a citrus fruit crop suitable for warm regions.", "Requires balanced nutrients, sunlight, and irrigation control."),
    "papaya": ("Papaya is a fast-growing tropical fruit crop.", "Avoid waterlogging and protect from strong wind."),
    "coconut": ("Coconut is a tropical plantation crop.", "Needs warm, humid, and consistently moist conditions."),
    "cotton": ("Cotton is a fibre crop that prefers warm climates.", "Requires pest monitoring and dry conditions near harvest."),
    "jute": ("Jute is a fibre crop that prefers warm and humid conditions.", "Requires sufficient rainfall and fertile soil."),
    "coffee": ("Coffee is a plantation crop grown in suitable tropical/shaded environments.", "Requires shade, moisture, and disease management."),
}

def get_crop_info(crop: str) -> Dict[str, str]:
    key = crop.lower().strip()
    summary, care = SUMMARY.get(key, (f"{title_crop(crop)} is one of the supported dataset crops.", "Use local soil testing and agricultural advice before real farming decisions."))
    return {"name": title_crop(key), "summary": summary, "care": care}

def get_crop_image_path(crop: str) -> Path | None:
    filename = IMAGE_FILES.get(crop.lower().strip())
    if not filename:
        return None
    path = CROP_IMAGES_DIR / filename
    return path if path.exists() else None
