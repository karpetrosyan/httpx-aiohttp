ARG PYTHON_IMAGE

FROM ${PYTHON_IMAGE}

VOLUME [ "/app/script" ]
ENV SERVER_URL="http://server:8000"

WORKDIR /app

RUN python3 -m pip install uv
