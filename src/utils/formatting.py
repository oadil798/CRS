from __future__ import annotations

def title_crop(label: str) -> str:
    return str(label).replace("_", " ").title()

def as_percent(value: float) -> str:
    return f"{float(value) * 100:.2f}%"
