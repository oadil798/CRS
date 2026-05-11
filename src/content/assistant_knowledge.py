from __future__ import annotations

RESPONSES = {
    "English": {
        "basic": "Basic Mode asks for temperature, humidity, and rainfall only. N, P, K, and pH are filled using dataset median values, so it is easier but less reliable.",
        "advanced": "Advanced Mode uses all seven inputs: N, P, K, temperature, humidity, pH, and rainfall. It is the preferred mode for accurate prediction.",
        "confidence": "Confidence shows how strongly the Random Forest model prefers the recommended crop. It is model confidence, not a guarantee of real farming success.",
        "nitrogen": "Nitrogen (N) is a soil nutrient. You can get it from a soil test report, agricultural lab, or soil testing kit.",
        "phosphorus": "Phosphorus (P) supports root development and is usually measured through soil testing.",
        "potassium": "Potassium (K) supports plant strength and stress tolerance. Soil tests usually provide this value.",
        "ph": "Soil pH measures acidity or alkalinity. Use a pH meter or soil testing kit.",
        "rainfall": "Rainfall can be checked from weather services, climate records, or agricultural weather stations.",
        "random forest": "Random Forest remains the deployed model because it matches the FYP investigation report and gives strong tabular classification performance.",
        "svm": "SVM is included for comparison only. It is not the deployed model.",
        "gaussian": "GaussianNB is included as a simple probabilistic comparison model.",
        "history": "Prediction History saves your inputs, recommended crop, confidence, and prediction mode in SQLite.",
        "crops": "The system only recommends the 22 crop labels available in the Kaggle crop recommendation dataset.",
        "default": "I can help with modes, input values, confidence, prediction history, model comparison, and general system usage. For real farming decisions, combine this system with local agricultural advice.",
        "empty": "Ask me about Basic Mode, Advanced Mode, NPK, pH, rainfall, confidence, or model comparison.",
        "greeting": "Hello! I can help explain how to use the Crop Recommendation System.",
    },
    "Bahasa Melayu": {
        "basic": "Mod Asas meminta suhu, kelembapan dan hujan sahaja. Nilai N, P, K dan pH diisi menggunakan median dataset, jadi ia lebih mudah tetapi kurang boleh dipercayai.",
        "advanced": "Mod Lanjutan menggunakan semua tujuh input: N, P, K, suhu, kelembapan, pH dan hujan. Ia ialah mod yang disyorkan untuk ramalan yang lebih tepat.",
        "confidence": "Keyakinan menunjukkan sejauh mana model Random Forest memilih tanaman yang dicadangkan. Ia ialah keyakinan model, bukan jaminan kejayaan pertanian sebenar.",
        "nitrogen": "Nitrogen (N) ialah nutrien tanah. Nilai ini boleh diperoleh daripada laporan ujian tanah, makmal pertanian atau kit ujian tanah.",
        "phosphorus": "Fosforus (P) membantu perkembangan akar dan biasanya diukur melalui ujian tanah.",
        "potassium": "Kalium (K) membantu kekuatan tanaman dan toleransi tekanan. Ujian tanah biasanya menyediakan nilai ini.",
        "ph": "pH tanah mengukur tahap keasidan atau kealkalian. Gunakan meter pH atau kit ujian tanah.",
        "rainfall": "Hujan boleh disemak melalui perkhidmatan cuaca, rekod iklim atau stesen cuaca pertanian.",
        "random forest": "Random Forest kekal sebagai model yang digunakan kerana ia sepadan dengan Investigation Report FYP dan sesuai untuk klasifikasi data berjadual.",
        "svm": "SVM dimasukkan untuk perbandingan sahaja. Ia bukan model yang digunakan dalam ramalan utama.",
        "gaussian": "GaussianNB dimasukkan sebagai model perbandingan probabilistik yang ringkas.",
        "history": "Sejarah Ramalan menyimpan input, tanaman dicadangkan, keyakinan dan mod ramalan dalam SQLite.",
        "crops": "Sistem hanya mencadangkan 22 label tanaman yang tersedia dalam dataset cadangan tanaman Kaggle.",
        "default": "Saya boleh membantu tentang mod, nilai input, keyakinan, sejarah ramalan, perbandingan model dan penggunaan sistem. Untuk keputusan pertanian sebenar, gabungkan sistem ini dengan nasihat pertanian tempatan.",
        "empty": "Tanya saya tentang Mod Asas, Mod Lanjutan, NPK, pH, hujan, keyakinan atau perbandingan model.",
        "greeting": "Helo! Saya boleh membantu menerangkan cara menggunakan Sistem Cadangan Tanaman.",
    },
}

KEYWORD_ALIASES = {
    "basic": ["basic", "asas"],
    "advanced": ["advanced", "lanjutan"],
    "confidence": ["confidence", "keyakinan"],
    "nitrogen": ["nitrogen", " n ", "n,"],
    "phosphorus": ["phosphorus", "fosforus", " p ", "p,"],
    "potassium": ["potassium", "kalium", " k ", "k,"],
    "ph": ["ph", "pH"],
    "rainfall": ["rainfall", "hujan"],
    "random forest": ["random forest"],
    "svm": ["svm"],
    "gaussian": ["gaussian", "naive", "nb"],
    "history": ["history", "sejarah"],
    "crops": ["crops", "tanaman"],
}


def answer_question(question: str, language: str = "English") -> str:
    lang = language if language in RESPONSES else "English"
    q = f" {question.lower().strip()} "
    if not q.strip():
        return RESPONSES[lang]["empty"]
    if any(greet in q for greet in [" hello ", " hi ", " hey ", "helo", "salam"]):
        return RESPONSES[lang]["greeting"]
    for key, aliases in KEYWORD_ALIASES.items():
        if any(alias.lower() in q for alias in aliases):
            return RESPONSES[lang].get(key, RESPONSES[lang]["default"])
    return RESPONSES[lang]["default"]
