# kpu_tps
Python script untuk mengambil data KPU per TPS menggunakan Selenium

## Instalasi
### Di Ubuntu Desktop, Linux Mint, dan turunan Debian lainnya
1. Install python3 dan unzip
   ```sudo apt-get install -y python3 python3-pip unzip```
2. Install selenium.
   `sudo pip3 install selenium`
3. Install chromedriver.
   Cek versi Chrome.
   Unduh chromedriver yang sama/mirip dengan versi Chrome di [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
   Setelah diunduh, jalankan ini:
   `unzip chromedriver_linux64.zip`
   `sudo cp chromedriver /usr/bin`

### Di _virtual environment_ Python 3
1. Aktifkan virtual environment.
   `source /direktori/virtual_environment/bin/activate`
2. Install selenium
   `pip3 install selenium`
3. Install chromedriver seperti di atas

## Instalasi di Ubuntu Server atau turunan Debian Non-Desktop lainnya
1. Lakukan salah satu dari dua cara instalasi di atas
2. Install xvfb (X video frame buffer), x11vnc, dan fluxbox
   `sudo apt-get install -y xvfb x11vnc fluxbox`
   
## Menjalankan di Ubuntu Desktop, Linux Mint, dan turunan Debian lainnya
1. Unduh file dan ekstrak
2. Jalankan:
   `python3 tps.py`

## Menjalankan di Ubuntu Server atau turunan Debian Non-Desktop lainnya
1. Unduh file dan ekstrak
2. Jalankan xvfb, x11vnc, dan fluxbox
   `Xvfb :1 -screen 0 1024x768x16 &`
   `x11vnc -display :1 -forever -shared &`
   `DISPLAY=:1 fluxbox &`
3. Jalankan:
   `DISPLAY=:1 python3 tps.py`
