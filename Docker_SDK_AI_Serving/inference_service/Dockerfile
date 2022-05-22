FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install fastapi uvicorn requests docker six

EXPOSE 82

COPY ./app /app

CMD ["uvicorn", "Inference_Service:app", "--host", "0.0.0.0", "--port", "8002"]