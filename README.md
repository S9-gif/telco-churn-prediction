# Telco Customer Churn Prediction

🌐 [Live Demo](https://telco-churn-prediction-fb63.onrender.com/) · 📓 [Development Diary](https://wwwsercankuru.notion.site/ML-dev-diary-3b69e0171b4480e6a9d5c5a5cc7670db)

> Note: hosted on Render's free tier — the server may take up to a minute to wake up if it has been idle.

---

## 🇬🇧 English

An end-to-end machine learning project that predicts customer churn for a telecommunications company — from raw data to a working, deployable web application. The goal is to identify customers at risk of leaving in advance, providing a data-driven foundation for the company's customer retention strategies.

### Dataset
[Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
7,043 customers, 21 features (demographics, service details, account/billing information).

### Project Structure
```
telco-churn-prediction/
├── data/raw/              # Raw dataset
├── notebooks/              # Data analysis, cleaning, model training
├── models/                 # Saved trained model (joblib)
├── api/                    # FastAPI application
│   ├── main.py              # API endpoint, encoding logic, prediction
│   └── schemas.py           # Pydantic input/output schemas
├── frontend/                # HTML/CSS/JS web interface
└── requirements.txt
```

### Machine Learning Pipeline

**1. Data Cleaning**
- Hidden whitespace characters in `TotalCharges` were identified and the column was converted to a numeric type
- Missing values (new customers with `tenure=0`) were filled based on a reasonable assumption

**2. Feature Engineering**
- Binary categorical variables (Yes/No) were encoded as 0/1
- Redundant categories such as "No internet/phone service" were simplified
- Nominal variables (Contract, InternetService, PaymentMethod) were transformed using One-Hot Encoding

**3. Modeling**
- **Logistic Regression** (scikit-learn) was used as the baseline model
- Data was split into 80/20 train/test sets using `stratify` to preserve the churn ratio

**4. Evaluation**
- Accuracy: 80%
- Due to class imbalance (73% No Churn / 27% Churn), Precision, Recall, F1-Score, and the Confusion Matrix were used for a deeper analysis
- The ROC curve and AUC score were used to evaluate the model's threshold-independent discriminative power

**5. Threshold Tuning**
- Given the business context (the cost of losing a customer outweighs the cost of a false alarm), a Recall-prioritized threshold (~0.32) was chosen instead of the default 0.5
- This change increased Recall from 53% to 75%, while also improving the F1 score (0.586 → 0.626)
- Multiple threshold values were systematically tested to confirm the point that maximizes F1

### Deployment — API & Frontend

The trained model was deployed as a working web application:

- **Model serialization**: the trained model is saved with `joblib` and loaded once at API startup
- **API**: built with **FastAPI**, exposing a single `POST /predict` endpoint
  - Request/response validated with **Pydantic** schemas (`CustomerData` input, `PredictionResult` output)
  - Incoming raw customer data is encoded (binary + one-hot) inside the API, then aligned to the model's expected column order (`reindex` against `model.feature_names_in_`) before prediction
- **Frontend**: a custom HTML/CSS/JS interface (no framework) lets users fill in customer details and get an instant churn prediction with a visual probability bar
  - Served directly by FastAPI via a static file mount — frontend and API run on the same origin, avoiding any CORS configuration
- Interactive API documentation available at `/docs` (FastAPI's built-in Swagger UI)

**A notable debugging story**: an early version of the deployed model produced unexpectedly uncertain predictions on manually tested profiles. Investigation revealed a `train_test_split` misconfiguration (`test_size=0.8` instead of `0.2`), meaning the model had been trained on only 20% of the data. Fixing this single parameter significantly sharpened the model's predictions across all test cases — a good reminder that a model can look fine on aggregate metrics while still hiding a upstream data-splitting bug.

### Result
The model successfully identifies 75% of customers at risk of churning and is accessible through a working web interface where anyone can input customer details and get a real-time prediction.

### Tech Stack
Python, pandas, NumPy, scikit-learn, matplotlib, seaborn, FastAPI, Pydantic, Uvicorn, HTML/CSS/JavaScript

### Status
✅ Baseline model completed
✅ API & frontend deployed live on Render

---

## 🇹🇷 Türkçe

Bir telekom şirketinin müşteri kaybını (churn) tahmin eden, ham veriden çalışan bir web uygulamasına kadar uzanan uçtan uca bir makine öğrenmesi projesi. Amaç, hangi müşterilerin ayrılma riski taşıdığını önceden tespit ederek şirketin müşteri elde tutma stratejilerine veri destekli bir temel sağlamak.

### Veri Seti
[Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
7.043 müşteri, 21 değişken (demografik bilgiler, hizmet detayları, hesap/fatura bilgileri).

### Proje Yapısı
```
telco-churn-prediction/
├── data/raw/              # Ham veri seti
├── notebooks/              # Veri analizi, temizleme, model eğitimi
├── models/                 # Kaydedilmiş eğitilmiş model (joblib)
├── api/                    # FastAPI uygulaması
│   ├── main.py              # API endpoint, encoding mantığı, tahmin
│   └── schemas.py           # Pydantic giriş/çıkış şemaları
├── frontend/                # HTML/CSS/JS web arayüzü
└── requirements.txt
```

### Makine Öğrenmesi Süreci

**1. Veri Temizleme**
- `TotalCharges` sütunundaki gizli boşluk karakterleri tespit edilip sayısal tipe dönüştürüldü
- Eksik değerler (`tenure=0` olan yeni müşteriler) mantıklı bir varsayımla dolduruldu

**2. Feature Engineering**
- Binary kategorik değişkenler (Yes/No) 0/1 olarak encode edildi
- "No internet/phone service" gibi redundant kategoriler sadeleştirildi
- Nominal değişkenler (Contract, InternetService, PaymentMethod) One-Hot Encoding ile dönüştürüldü

**3. Modelleme**
- Baseline model olarak **Logistic Regression** (scikit-learn) kullanıldı
- Veri, `stratify` parametresiyle churn oranını koruyacak şekilde %80/%20 train/test olarak ayrıldı

**4. Değerlendirme**
- Accuracy: %80
- Dengesiz sınıf dağılımı (%73 No Churn / %27 Churn) nedeniyle Precision, Recall, F1-Score ve Confusion Matrix ile detaylı analiz yapıldı
- ROC eğrisi ve AUC skoru ile modelin eşikten bağımsız ayırt etme gücü değerlendirildi

**5. Threshold Tuning (Karar Eşiği Optimizasyonu)**
- İş bağlamı gereği (kaybedilen müşterinin maliyeti, yanlış alarmdan daha yüksek), varsayılan 0.5 eşiği yerine Recall'a öncelik veren bir eşik (~0.32) seçildi
- Bu değişiklik Recall'u %53'ten %75'e çıkarırken, F1 skorunu da iyileştirdi (0.586 → 0.626)
- Farklı eşik değerleri sistematik olarak taranarak F1'i maksimize eden nokta doğrulandı

### Deployment — API ve Frontend

Eğitilmiş model, çalışan bir web uygulaması olarak deploy edildi:

- **Model serileştirme**: eğitilmiş model `joblib` ile kaydediliyor, API başlangıcında bir kez yükleniyor
- **API**: **FastAPI** ile geliştirildi, tek bir `POST /predict` endpoint'i sunuyor
  - İstek/cevap, **Pydantic** şemalarıyla (`CustomerData` giriş, `PredictionResult` çıkış) doğrulanıyor
  - Gelen ham müşteri verisi API içinde encode ediliyor (binary + one-hot), tahmin öncesinde modelin beklediği sütun sırasına hizalanıyor (`model.feature_names_in_` ile `reindex`)
- **Frontend**: framework kullanılmadan, özel HTML/CSS/JS ile geliştirilen bir arayüz; kullanıcı müşteri bilgilerini girip anlık churn tahmini ve görsel bir olasılık çubuğu görüyor
  - FastAPI tarafından statik dosya mount'u ile doğrudan sunuluyor — frontend ve API aynı origin'den çalıştığı için CORS ayarına gerek kalmadı
  - `/docs` adresinde FastAPI'nin otomatik oluşturduğu interaktif API dokümantasyonu mevcut

**Dikkate değer bir hata ayıklama hikayesi**: deploy edilen modelin ilk versiyonu, manuel test edilen profillerde beklenmedik derecede belirsiz tahminler üretti. İnceleme sonucunda `train_test_split` parametresinde bir hata bulundu (`test_size=0.2` yerine yanlışlıkla `0.8` girilmişti) — yani model, verinin sadece %20'siyle eğitilmişti. Bu tek parametrenin düzeltilmesi, tüm test senaryolarında modelin tahminlerini belirgin şekilde netleştirdi — toplu metrikler iyi görünse bile, arka planda bir veri bölme hatasının gizlenebileceğinin iyi bir hatırlatıcısı oldu.

### Sonuç
Model, ayrılma riski taşıyan müşterilerin %75'ini başarıyla tespit edebiliyor ve herkesin müşteri bilgilerini girip gerçek zamanlı tahmin alabileceği çalışan bir web arayüzü üzerinden erişilebilir durumda.

### Kullanılan Teknolojiler
Python, pandas, NumPy, scikit-learn, matplotlib, seaborn, FastAPI, Pydantic, Uvicorn, HTML/CSS/JavaScript

### Durum
✅ Baseline model tamamlandı
✅ API ve frontend Render üzerinde canlı olarak deploy edildi