from fastapi import FastAPI

app = FastAPI(title="yolo-perception-agent")


@app.get("/health")
def health():
    return {"status": "ok"}
