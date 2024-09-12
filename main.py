from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

images_folder = "images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
):

    file_location = os.path.join(images_folder, file.filename)

    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
    }
