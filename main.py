import shutil

import pandas as pd
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import mail
import topiis

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def input_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def process_and_send_mail(request: Request,
                                file: UploadFile = File(...),
                                weights: str = Form(...),
                                impacts: str = Form(...),
                                email: str = Form(...)):
    with open('data.csv', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    dataset, temp_dataset = pd.read_csv("data.csv"), pd.read_csv("data.csv")
    nCol = len(temp_dataset.columns.values)
    print(dataset)
    print(nCol)
    weights = [int(i) for i in weights.split(',')]
    impact = impacts.split(',')
    topiis.topsis_pipy(temp_dataset, dataset, nCol, weights, impact)
    mail.send_mail(email)
    return templates.TemplateResponse("form.html", {"request": request})
