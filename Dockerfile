FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv sync --no-default-groups

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
