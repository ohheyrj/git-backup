FROM python:3.8-alpine

RUN adduser -D -g "gitbackup" gitbackup

USER gitbackup

COPY gitbackup /data/gitbackup

RUN pip install --no-cache-dir -r /data/gitbackup/requirements.txt

CMD ["python", "/data/gitbackup/gitbackup.py"]
