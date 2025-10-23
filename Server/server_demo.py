
# TODO server demo with api 'http://127.0.0.1:8001/generate

import requests
import os
from fastapi import FastAPI
app = FastAPI()

@app.post('/generate')
def generate_text(prompt):
    return 'echo :{prompt}'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
    