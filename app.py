from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ddddocr
import base64
import uvicorn
import argparse

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("captcha resolver")
    parser.add_argument("--host", help="host", default="127.0.0.1")
    parser.add_argument("--port", help="port", default="8000")
    args = parser.parse_args()
    uvicorn.run(app="app:app", host=args.host, port=int(args.port))
