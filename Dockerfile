FROM jjanzic/docker-python3-opencv:opencv-4.0.0
RUN git clone --progress --verbose https://github.com/d4rk-lucif3r/DeOldify.git DeOldify && cd DeOldify && pip install -r requirements.txt
RUN mkdir models && wget https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth --no-check-certificate -O ./models/ColorizeArtistic_gen.pth
RUN cd ..
COPY . ./app
WORKDIR app
ENTRYPOINT python app.py