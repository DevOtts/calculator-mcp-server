from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from asteval import Interpreter

app = FastAPI()

aeval = Interpreter()

class CalculationRequest(BaseModel):
    expression: str

class CalculationResponse(BaseModel):
    result: float | str

@app.post("/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest):
    try:
        result = aeval(request.expression)
        if aeval.error:
            raise ValueError(aeval.error[0].get_error())
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 