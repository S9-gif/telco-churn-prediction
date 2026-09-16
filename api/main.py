
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.schemas import PredictionResult, CustomerData
import joblib
import pandas as pd

# main.py'nin bulunduğu dizinden bağımsız, dosyanın kendi konumuna göre mutlak yol kuruyoruz.
# "../models" gibi göreli yollar, uvicorn'un hangi dizinden çalıştırıldığına bağlı olduğu için
# Render'da (repo kökünden çalıştırıldığında) yanlış klasöre bakıp hata veriyordu.
BASE_DIR = Path(__file__).resolve().parent.parent

muhittin = joblib.load(BASE_DIR / "models" / "model.pkl")   #Modelimi burda yükledim adı muhittin :)



app= FastAPI()



@app.post("/predict",response_model=PredictionResult)   #Burda post'un dönmesi gereken schema'yı ona belirtiyorum uzantısı ile birlikte
def predict(customer:CustomerData):     #Parametre olarak da CustomerData almalı alınan ve işlenecek olan veriler onlar çünkü




    #1-customer schemasına uygun parametre verileri encode etmeli ki model tahmin yapabilsin.
    #2-bu veriler yüklenen modele verilip bir sonuç alınmalı
    #3- alınan sonuç yine schemaya uygun şekilde kullanıcıya geri verilmeli

#1-Encode etme:
    def encode_customer(customer: CustomerData):
        # 1. Pydantic nesnesini tek satırlık DataFrame'e çevir bu sayede modele paramtetre olarak tek bir argüman vermiş oluyoruz.
        data = pd.DataFrame([customer.dict()])                              #!dict'in üstü neden çizilmiş neden?-->yakında versiyon değişikliğinde dict yerine model_dump kullanılması gerekecekmiş.

        # 2. Redundant "No xxx service" değerlerini sadeleştir
        cols_to_fix = [
            'OnlineSecurity',
            'OnlineBackup',
            'DeviceProtection',
            'TechSupport',
            'StreamingTV',
            'StreamingMovies'
        ]

        for col in cols_to_fix:
            data[col] = data[col].replace("No internet service", "No")

        data['MultipleLines'] = data['MultipleLines'].replace(
            "No phone service", "No"
        )

        # 3. Binary encoding (No/Yes -> 0/1)
        binary_cols = [
            'MultipleLines',
            'OnlineSecurity',
            'OnlineBackup',
            'DeviceProtection',
            'TechSupport',
            'StreamingTV',
            'StreamingMovies',
            'Partner',
            'Dependents',
            'PhoneService',
            'PaperlessBilling'
        ]

        for col in binary_cols:
            data[col] = data[col].replace({
                "No": 0,
                "Yes": 1
            })

        # 4. Gender encoding
        data['gender'] = data['gender'].replace({
            "Female": 0,
            "Male": 1
        })

        # 5. InternetService One-Hot Encoding benim bulduğum yöntem kod içinde one hot encoding
        internet_service = data['InternetService'].iloc[0]          

        data['InternetService_DSL'] = 1 if internet_service == "DSL" else 0
        data['InternetService_Fiber optic'] = 1 if internet_service == "Fiber optic" else 0
        data['InternetService_No'] = 1 if internet_service == "No" else 0

        # Artık ham InternetService kolonuna ihtiyacımız yok
        data.drop(columns=['InternetService'], inplace=True)

        # 6. Contract One-Hot Encoding
        contract = data['Contract'].iloc[0]

        data['Contract_Month-to-month'] = 1 if contract == "Month-to-month" else 0
        data['Contract_One year'] = 1 if contract == "One year" else 0
        data['Contract_Two year'] = 1 if contract == "Two year" else 0

        # Ham Contract kolonunu kaldır
        data.drop(columns=['Contract'], inplace=True)

        # 7. PaymentMethod One-Hot Encoding
        payment_method = data['PaymentMethod'].iloc[0]

        data['PaymentMethod_Bank transfer (automatic)'] = (
            1 if payment_method == "Bank transfer (automatic)" else 0
        )

        data['PaymentMethod_Credit card (automatic)'] = (
            1 if payment_method == "Credit card (automatic)" else 0
        )

        data['PaymentMethod_Electronic check'] = (
            1 if payment_method == "Electronic check" else 0
        )

        data['PaymentMethod_Mailed check'] = (
            1 if payment_method == "Mailed check" else 0
        )

        # Ham PaymentMethod kolonunu kaldır
        data.drop(columns=['PaymentMethod'], inplace=True)


        expected_columns = muhittin.feature_names_in_.tolist()  #Her ne kadar muhittine parametreleri manuel vermiş olsak da ne olur ne olmaz claude'dan böyle otomatik bir acil durum bloğu eklettirdim.
        data = data.reindex(columns=expected_columns, fill_value=0) 

        return data

    encoded_data = encode_customer(customer) #Fonksiyonu çağırmadan kullanamayız


#Birinci adım bu sayede bitmiş olmalı.Elimde kullanıcının verdiği encode edilmiş data var şuanda bunu modele vereceğim yani muhittine:
    



#2-Modeleden sonuç elde etme:




    probability_pre=muhittin.predict_proba(encoded_data)
    probability_pre=float(probability_pre[0,1])

    # sklearn'ün predict() metodu sabit 0.5 eşik kullanır. Notebook'taki analizde
    # recall'u önceliklendirmek için ~0.32 eşiği seçildi (recall %53 -> %75),
    # bu yüzden sınıfı 0.5 yerine o eşikle belirliyoruz.
    CHURN_THRESHOLD = 0.32      #Burda bir debugging işlemi gerçekleştirdik belirlediğimthreshold predict fonksiyonunda tanınmıyordu o yüzden kodda bir daha tanımladık.
    churn_pre = "1" if probability_pre >= CHURN_THRESHOLD else "0"



#3- Alınan sonuç yine schemaya uygun şekilde kullanıcıya geri verilmeli
    return PredictionResult(Churn=churn_pre, PredictionRate=probability_pre)


# Frontend'i aynı origin'den servis ediyoruz (CORS'a gerek kalmadan).
# Bu mount /predict route'undan SONRA tanımlanmalı, yoksa "/" her isteği yakalar.
app.mount("/", StaticFiles(directory=BASE_DIR / "frontend", html=True), name="frontend")
#   app API objeme frontendi ekliyorum.
#   Farklı originden geliyor olsaydı da apı'ın buna izin veriyor olması gerekiyordu.
