# Telco Customer Churn Prediction

📓 [Development Diary](https://wwwsercankuru.notion.site/ML-dev-diary-3b69e0171b4480e6a9d5c5a5cc7670db)

---

## 🇬🇧 English

An end-to-end machine learning project predicting customer churn for a telecommunications company. The goal is to identify customers at risk of leaving in advance, providing a data-driven foundation for the company's customer retention strategies.

### Dataset
[Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
7,043 customers, 21 features (demographics, service details, account/billing information).

### Process

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

### Result
The model successfully identifies 75% of customers at risk of churning, serving as an early-warning system the company can use to intervene before losing them.

### Tech Stack
Python, pandas, NumPy, scikit-learn, matplotlib, seaborn

### Status
✅ Baseline model completed

---

## 🇹🇷 Türkçe

Bir telekom şirketinin müşteri kaybını (churn) tahmin eden uçtan uca bir makine öğrenmesi projesi. Amaç, hangi müşterilerin ayrılma riski taşıdığını önceden tespit ederek şirketin müşteri elde tutma stratejilerine veri destekli bir temel sağlamak.

### Veri Seti
[Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
7.043 müşteri, 21 değişken (demografik bilgiler, hizmet detayları, hesap/fatura bilgileri).

### Süreç

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

### Sonuç
Model, ayrılma riski taşıyan müşterilerin %75'ini başarıyla tespit edebiliyor. Bu, şirketin müşteri kaybı öncesinde müdahale edebileceği bir erken uyarı sistemi olarak kullanılabilir.

### Kullanılan Teknolojiler
Python, pandas, NumPy, scikit-learn, matplotlib, seaborn

### Durum
✅ Baseline model tamamlandı