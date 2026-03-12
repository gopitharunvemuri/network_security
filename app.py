import os, sys
from fastapi import FastAPI
import pymongo
from network_security.exception.CustomException import NetworkSecurityException
from dotenv import load_dotenv
load_dotenv()
from uvicorn import run as app_run
from network_security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from starlette.responses import RedirectResponse
from network_security.pipelines.training_pipeline import TrainingPipeline
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from network_security.utils.main_utils.utils import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile, Request
jinja = Jinja2Templates(directory='./templates')
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_db_url = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(mongo_db_url)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is successfull")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict(request:Request,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(model = model, preprocessor=preprocessor)
        y_pred = network_model.predict(x = df)
        print(y_pred)
        df['predicted_value'] = y_pred
        os.makedirs("predicted_output", exist_ok=True)
        df.to_csv("predicted_output/output.csv")
        table = df.to_html(classes = 'table table-striped')
        return jinja.TemplateResponse('table.html', {"request":request, "table":table})
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
if __name__=="__main__":
    app_run(app, host = "localhost", port=8000)