# pokusduls-be
<<<<<<< HEAD
=======

Backend FastAPI untuk aplikasi PokusDuls.

## YOLO model

Backend sekarang mencari model YOLO di beberapa lokasi lokal:

- `services/yolov8n.pt`
- `model/yolov8n.pt`
- `../YOLO/yolov8n.pt`

Jika tidak ada file model lokal, backend akan mencoba memuat `yolov8n.pt` secara default dari Ultralytics, yang dapat mengunduh model secara otomatis jika terhubung ke internet.

## Cara gunakan

1. Pastikan backend dijalankan dari folder project:
   - `cd C:\Users\Akmal\Documents\IMPAL\pokusduls-be-main`
2. Jalankan server:
   - `uvicorn main:app --reload --port 8000`
3. Pastikan frontend diarahkan ke `http://localhost:8000`.

## Jika kamu ingin menyimpan model di repo backend

Letakkan file `yolov8n.pt` di:

- `pokusduls-be-main/model/yolov8n.pt`

atau set environment variable:

- `YOLO_MODEL_PATH=C:\path\to\yolov8n.pt`
>>>>>>> 1925e27 (Penambahan YOLO)
