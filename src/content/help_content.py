from __future__ import annotations

HELP_ITEMS = {
    "English": [
        ("Nitrogen (N)", "A major soil nutrient. Usually obtained from a soil test report or soil testing kit."),
        ("Phosphorus (P)", "Supports root development. Usually measured through soil testing."),
        ("Potassium (K)", "Supports plant strength and stress tolerance. Usually measured through soil testing."),
        ("pH", "Shows whether soil is acidic, neutral, or alkaline. Measured using a pH meter or test kit."),
        ("Temperature", "Can be taken from local weather reports, sensors, or a thermometer."),
        ("Humidity", "Can be obtained from weather apps, weather stations, or online meteorological reports."),
        ("Rainfall", "Can be obtained from weather services, climate records, or local agricultural reports."),
    ],
    "Bahasa Melayu": [
        ("Nitrogen (N)", "Nutrien tanah utama. Biasanya diperoleh daripada laporan ujian tanah atau kit ujian tanah."),
        ("Fosforus (P)", "Membantu perkembangan akar. Biasanya diukur melalui ujian tanah."),
        ("Kalium (K)", "Membantu kekuatan tanaman dan ketahanan terhadap tekanan. Biasanya diukur melalui ujian tanah."),
        ("pH", "Menunjukkan sama ada tanah berasid, neutral atau beralkali. Diukur menggunakan meter pH atau kit ujian."),
        ("Suhu", "Boleh diperoleh daripada laporan cuaca tempatan, sensor atau termometer."),
        ("Kelembapan", "Boleh diperoleh daripada aplikasi cuaca, stesen cuaca atau laporan meteorologi dalam talian."),
        ("Hujan", "Boleh diperoleh daripada perkhidmatan cuaca, rekod iklim atau laporan pertanian tempatan."),
    ],
}


def get_help_items(language: str):
    return HELP_ITEMS.get(language, HELP_ITEMS["English"])
