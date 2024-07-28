#!/usr/bin/env python3
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import subprocess
import datetime
import math
import cv2
import os

def loop(path, out):
    process = subprocess.Popen([
        'ffmpeg', '-i', path, '-f', 'image2pipe', '-pix_fmt', 'rgb24', '-vcodec', 'rawvideo', '-'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    video = cv2.VideoCapture(path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video.release()

    best = None
    first = None
    frames = 0

    while True:
        image = process.stdout.read(width * height * 3)
        if len(image) != (width * height * 3):
            break
        if frames % (fps / 10) != 0:
            frames += 1
            continue
        if frames > fps * 5:
            break
        frame = np.frombuffer(image, dtype=np.uint8).reshape((height, width, 3))
        if first is None:
            first = frame
        elif frames > fps / 2:
            first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            score, _ = ssim(first_gray, frame_gray, full=True)
            if best == None or score > best[1]:
                best = (frames, score)
        frames += 1

    process.terminate()
    if best == None:
        print(f'[{path}] no best frame somehow')
        return
    end = datetime.timedelta(seconds=best[0] / fps)
    print(f'[{path}] score {score} at {end}')
    subprocess.call([
        'ffmpeg', '-i', path, '-filter:v', 'fps=30,scale=1080:-2,setsar=1:1', '-to', str(end), '-y', out
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check(filename):
    path = Path(filename)
    if path.suffix not in [ '.mp4', '.mkv' ]:
        return
    out = f'{path.stem}.webp'
    if os.path.isfile(out):
        return
    loop(filename, out)

with ThreadPoolExecutor(max_workers = 8) as executor:
    executor.map(check, os.listdir())
    executor.shutdown(wait=True)
