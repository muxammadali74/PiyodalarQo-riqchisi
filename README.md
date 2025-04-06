# 🚩 Piyodalar Qo‘riqchisi

🚗 YOLOv8 va OpenCV asosida qurilgan piyodalar yo‘lidan o‘tishdagi qoidabuzarliklarni aniqlovchi avtomatik tizim.

![Logo](/logo/logo.png)

---

## 📌 Imkoniyatlar

- Piyodalar va avtomobillarni aniqlash
- Piyodalar o‘tish zonasini belgilash (zonani chizish)
- Qoidabuzarlik holatini aniqlash (piyoda + avtomobil bir zonada)
- Qoidabuzarlik holatlarini rasmga olish
- Qoidabuzarlikdan oldin va keyingi qisqa videoni saqlab qolish (~10 soniya)
- FPS (frame per second) va vaqtni ko‘rsatish

---

## 🎩 Misollar

### Qoidabuzarlik holati:

![Example](/output_image/violation_detected_20250406-123732.png)

### Video lavha:

https://github.com/muxammadali74/PiyodalarQo-riqchisi/blob/main/output_video/output_Trim.mp4

---

## 🛠 O‘rnatish

```bash
git clone https://github.com/foydalanuvchi_nomi/PiyodalarQoriqchisi.git
cd PiyodalarQoriqchisi
pip install -r requirements.txt
```

---

## 🚀 Ishga tushirish

```bash
python main.py
```

---

## ⚙️ Sozlamalar

`config.py` faylida video yo‘li, ekran o‘lchami va modelni sozlashingiz mumkin:

```python
video_path = 'videoingiz.mp4'
model_path = 'yolov8n.pt'
```

---

## 📄 Litsenziya

Ushbu loyiha **MIT litsenziyasi** asosida tarqatiladi.

---

## 👤 Muallif

- **Ochilov Muxammad Ali** — Dasturchi / Talaba / Sun’iy intellekt tadqiqotchisi
- Telegram: [@ali7432](https://t.me/ali7432)

---

## 🌟 Loyihani qo‘llab-quvvatlang

Agar loyiha foydali bo‘lgan bo‘lsa, yulduzcha ⭐️ bosing va repo'ga obuna bo‘ling!

