FROM python

COPY server.py /app/server.py

WORKDIR /app

RUN python3 -m pip install uvicorn==0.34.0 fastapi

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]