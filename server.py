from fastapi import FastAPI,Request,File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pdf2image import convert_from_bytes
from PIL import Image
from cosine_sim import cos_similarity
from answers import data
from preprocessor import cleanResume
import joblib,pytesseract,qrcode,spacy,os


app = FastAPI()
nlp = spacy.load("en_core_web_sm")

app.mount("/static", StaticFiles(directory="static"), name="static")

domain = ""
templates = Jinja2Templates(directory="template")

cat_s = ['Advocate', 'Arts', 'Automation Testing', 'Blockchain', 'Business Analyst', 'Civil Engineer', 'Data Science', 'Database', 'DevOps Engineer', 'DotNet Developer', 'ETL Developer', 'Electrical Engineering', 'HR', 'Hadoop', 'Health and fitness', 'Java Developer', 'Mechanical Engineer', 'Network Security Engineer', 'Operations Manager', 'PMO', 'Python Developer', 'SAP Developer', 'Sales', 'Testing', 'Web Designing']
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.get('/')
async def getter(request:Request):
    return templates.TemplateResponse('home.html',{"request":request})


@app.get('/upload')
async def root(request:Request):
    if os.path.exists("./static/images/saved.jpg"):
            os.remove("./static/images/saved.jpg")
    return templates.TemplateResponse('upload.html',{"request":request})


@app.post('/upload')
async def rooter(request:Request,file:bytes = File(...)):
    pages = convert_from_bytes(file,500,poppler_path="./poppler-0.68.0/bin")
    image = pages[0]
    image.save("./static/images/saved.jpg","JPEG")
    text = str(((pytesseract.image_to_string(pages[0]))))
    text = text.replace('-\n', '')  
    model = joblib.load('./models/model.pkl')
    vectorizer = joblib.load('./models/vectorizer.pkl')
    afterText = vectorizer.transform([text])
    tuple_result = sorted(list(zip(cat_s,list(map(lambda x:round(x*100,0),model.predict_proba(afterText)[0])))),key=lambda x:x[-1],reverse=True)
    for i in tuple_result:
        print(i)
    global domain
    domain = tuple_result[0][0]
    endpoint = tuple_result[0][0].replace(" ",'')
    return templates.TemplateResponse(f'domains/{endpoint}.html',{"request":request,"domain":tuple_result[0][0]})

@app.post('/test')
async def test(request:Request,answer1:str = Form(...),answer2:str = Form(...),answer3:str = Form(...)):
    image = Image.open('./static/images/saved.jpg')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    print(cos_similarity(nlp(answer1).vector,nlp(data[domain][0]).vector),cos_similarity(nlp(answer2).vector,nlp(data[domain][1]).vector),cos_similarity(nlp(answer3).vector,nlp(data[domain][2]).vector))
    overall_sim = round((cos_similarity(nlp(answer1).vector,nlp(data[domain][0]).vector)+cos_similarity(nlp(answer2).vector,nlp(data[domain][1]).vector)+cos_similarity(nlp(answer3).vector,nlp(data[domain][2]).vector))/3,2)*100
    qr.add_data({"tag":domain,"simal":str(overall_sim)+'%'})
    img = qr.make_image(fill_color="black", back_color="white")
    image.paste(img,(1000,200))
    if os.path.exists("./static/images/saved.jpg"):
            os.remove("./static/images/saved.jpg")
    image.save('./static/images/saved.jpg')
    return templates.TemplateResponse('output-test.html',{"request":request,"image":'./static/images/saved.jpg'})
    

