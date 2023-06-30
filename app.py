from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ddddocr
import base64

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ocr = ddddocr.DdddOcr()


class GetCaptchaRequest(BaseModel):
    img: str


@app.post("/captcha")
async def get_captcha(req: GetCaptchaRequest):
    try:
        return {"result": ocr.classification(base64.b64decode(req.img))}
    except Exception:
        raise HTTPException(status_code=400, detail="invalid image")
