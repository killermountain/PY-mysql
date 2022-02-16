# from fileinput import filename
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
# import uvicorn

# pip install python-multipart

api = FastAPI()
cwd = os.getcwd()
hospital_name = "Broomfield"
ouput_json = cwd + "/output-json/" + hospital_name + "/"

@api.get("/")
def welcome():
    return {"msg": "Welcome to HTML to Database API"}

@api.get("/getfilnames/")
def getAlljsons():
    print(cwd)
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

@api.post("/uploadfile/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


# if __name__ == "__main__":
#     uvicorn.run("FastApi:api", host="127.0.0.1", port=5000, reload=True, log_level="info")