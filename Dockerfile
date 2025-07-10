FROM linuxserver/ffmpeg:5.1.2 as ffmpeg-stage

FROM python:3.11

WORKDIR /app

COPY --from=ffmpeg-stage /usr/bin/ffmpeg /usr/bin/
COPY --from=ffmpeg-stage /usr/bin/ffprobe /usr/bin/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["python", "open_server.py"]