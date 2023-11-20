# CiTrace_Demo

#Come fare deploy da Render.com
1.	Da Enviroment->Environment Variables->Inserire come Key = “PYTHON_VERSION“ e come value = “3.11.5” (Versione di python attualmente utilizzata in Spyder)
2.	Build Command: pip install -r requirements.txt
3.	Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000
