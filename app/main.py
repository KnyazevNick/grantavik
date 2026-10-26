from fastapi import FastAPI



grantavik = FastAPI(title="Grantavik")



@grantavik.get('/health')
def health():
    return {"status": "ok"}
