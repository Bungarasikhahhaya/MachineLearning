Plant Growth Prediction (Machine Learning Web App)

Aplikasi ini merupakan sistem prediksi berbasis Machine Learning untuk menentukan apakah suatu tanaman dapat tumbuh berdasarkan kondisi lingkungan dan tanah.

Project ini terdiri dari:
🔹 Frontend: Streamlit (User Interface)
🔹 Backend: FastAPI (API & Model Serving)
🔹 Model: Random Forest Classifier

- Fitur Utama
Input data lingkungan & tanah oleh user
Feature engineering otomatis
Rule-based validation untuk kondisi ekstrem
Prediksi menggunakan Machine Learning (Random Forest)
Tampilan hasil prediksi secara real-time
UI modern dengan efek visual (glass + blur + glow)

Cara Kerja Sistem
Sistem bekerja dalam 3 tahap utama:

1. Input Data
User memasukkan parameter:
- Suhu udara & tanah
- Kelembapan tanah
- pH tanah
- Nutrisi (Nitrogen, Phosphorus, Potassium)
- Salinitas
- Jenis tanah
- Kategori tanaman

2. Feature Engineering (Otomatis)
Data akan diolah menjadi fitur baru:
- NP Ratio (Nitrogen / Phosphorus)
- NK Ratio (Nitrogen / Potassium)
- pH Deviation (selisih dari pH netral)
- Moisture Deficit & Excess
- Salinity Stress
Tujuannya untuk meningkatkan performa model.

3. Prediksi
🔹 Rule-Based System (Prioritas)
Jika kondisi ekstrem:
- pH < 4 atau > 9
- Kelembapan terlalu rendah / tinggi
- Suhu ekstrem
Sistem langsung memberikan hasil tanpa ML
🔹 Machine Learning
Jika kondisi normal:
Data diproses oleh Random Forest Model

Output:
✅ Tanaman Dapat Tumbuh
❌ Tanaman Tidak Dapat Tumbuh

Tech Stack
- Python
- FastAPI
- Streamlit
- Scikit-learn
- Pandas
- Joblib

Install & Setup
1. Clone Repository
- git clone https://github.com/username plant-growth-prediction.git
- cd plant-growth-prediction

2. Install Depedencies
- pip install -r requirements.txt
- pip install fastapi uvicorn streamlit scikit-learn pandas joblib requests

3. Jalankan Backend (FastAPI)
masuk ke folder backend:
- cd Backend
- uvicorn main:app --reload

4. Jalankan Frontend (Streamlit)
- cd Frontend
- streamlit run main.py

Outhor
Kelompok 4
1. Anisa Ramadhani
2. Akrimah Usri
3. Bunga Rasikhah Haya