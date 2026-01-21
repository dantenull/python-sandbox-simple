FROM python-sandbox-simple-base

WORKDIR /app

RUN mkdir -p ~/.pip && \
    echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./sandbox_requirements.txt .
RUN python -m venv .venv
RUN .venv/bin/pip install -r ./sandbox_requirements.txt

COPY ./src ./src
COPY run.py .

EXPOSE 8009

CMD [ "python", "run.py" ]
