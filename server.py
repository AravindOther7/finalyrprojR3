from ast import Bytes
from urllib.request import Request
from fastapi import FastAPI,Request,File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import joblib

app = FastAPI()

templates = Jinja2Templates(directory="template")

cat_s = ['Advocate', 'Arts', 'Automation Testing', 'Blockchain', 'Business Analyst', 'Civil Engineer', 'Data Science', 'Database', 'DevOps Engineer', 'DotNet Developer', 'ETL Developer', 'Electrical Engineering', 'HR', 'Hadoop', 'Health and fitness', 'Java Developer', 'Mechanical Engineer', 'Network Security Engineer', 'Operations Manager', 'PMO', 'Python Developer', 'SAP Developer', 'Sales', 'Testing', 'Web Designing']
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.get('/')
async def root(request:Request):
    return templates.TemplateResponse('index.html',{"request":request})




@app.post('/')
async def rooter(request:Request,file:bytes = File(...)):
    pages = convert_from_bytes(file,500,poppler_path="./poppler-0.68.0/bin")
    pages[0].save("saved.jpg","JPEG")
    text = str(((pytesseract.image_to_string(pages[0]))))
    text = text.replace('-\n', '')  
    print(text)
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    a = vectorizer.transform([text])
    tuple_result = sorted(list(zip(cat_s,list(map(lambda x:round(x*100,0),model.predict_proba(a)[0])))),key=lambda x:x[-1],reverse=True)
    for i in tuple_result:
        print(i)
    return templates.TemplateResponse('output-test.html',{"request":request})
