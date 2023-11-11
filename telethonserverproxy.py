from fastapi import FastAPI
from pydantic import BaseModel
import lmql
import pandas as pd
import subprocess


app = FastAPI()

@lmql.query(model="llama.cpp:/local/llama-2-70b.Q5_K_M.gguf",endpoint="localhost:8080") #use served model
async def extract_date(question):
    '''lmql
    "You are given this context: {question}" 
    "The month that the context took place in is: [MONTH]" where MONTH in ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    "The day the context took place in is: [DAY]" where DAY in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    return MONTH,DAY
    '''

class LQMLRequest(BaseModel):
    question: str

@app.get("/execute")
def execute_lqml(request: LQMLRequest):
    return extract_date(request.question)


if __name__ == "__main__":
    cmd = ["uvicorn", "lmqlserverproxy:app", "--reload", "--host", "0.0.0.0", "--port", f"{8000}"]
    subprocess.run(cmd)
