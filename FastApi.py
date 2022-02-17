# from fileinput import filename
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import uvicorn
from searchquery import searchDocs
from connDB import MySQLDB

# pip install python-multipart

api = FastAPI()
cwd = os.getcwd()
hospital_name = "Broomfield"
ouput_json = cwd + os.path.sep + "output-json"+ os.path.sep + hospital_name + os.path.sep

documents = None
last_doc_id = None
docs_count = None

@api.get("/")
def welcome():
    return {"msg": "Welcome to HTML to Database API"}

@api.get("/getfilnames/")
def getAlljsons():
    # print(cwd)
    filenames = []
    # filepath = os.path.join(cwd, "output-json/")
    files = os.listdir(ouput_json)
    
    for file in files:
        if file[-5:].lower() == ".json":
            filenames.append(file[:-5])
    return {"Hospital": hospital_name, "No of Files": len(filenames), "data":filenames}

@api.get("/getjson/{filename}")
def getjson(filename: str):
    filepath = ouput_json + filename + ".json"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="application/json")
    return {"error":"JSON not found."}

@api.get("/search/{query}")
def getjson(query: str):
    global documents, docs_count, last_doc_id
    
    results = searchDocs(query, documents, docs_count, last_doc_id, top_x=5)
    documents = results["docs"]
    docs_count = results["docCount"]
    last_doc_id = results["docLastID"]
    return results["matches"]

@api.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


def initialize():
    global documents, docs_count, last_doc_id
    conn_db = MySQLDB()
    docs_count, last_doc_id = conn_db.getDocInfo()
    documents = conn_db.getAllDocs()
    conn_db.disconnectDB()

initialize()

if __name__ == "__main__":
    uvicorn.run("FastApi:api", host="127.0.0.1", port=5000, reload=True, log_level="info")