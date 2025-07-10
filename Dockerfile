FROM jrottenberg/ffmpeg:5.1-ubuntu2004 as ffmpeg-stage

FROM python:3.11

WORKDIR /app

COPY --from=ffmpeg-stage /usr/local/bin/ffmpeg /usr/local/bin/
COPY --from=ffmpeg-stage /usr/local/bin/ffprobe /usr/local/bin/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["python", "open_server.py"]