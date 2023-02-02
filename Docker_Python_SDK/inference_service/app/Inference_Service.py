from fastapi import FastAPI
from random import *
import json
from starlette.responses import JSONResponse

app = FastAPI()

## Inference Results 반환
# start_inference Code가 와야됨

path = '/mnt/result.json'

@app.get("/inference_result")
async def read_root():
    # inference ~~~~~~~
    n = randint(1, 100)
    result = dict({
        'result:' : n
    })
    print('inference 값:',result)
    with open(path, 'w+') as f:
        json.dump(result, f)
        print(path, '에 inference 결과 기록완료')
    return JSONResponse(result)
