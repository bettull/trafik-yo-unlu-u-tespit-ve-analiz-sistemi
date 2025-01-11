import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import datetime
import csv
import os
from threading import Thread
import time

class TrafikYogunlukTespiti:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Trafik Yoğunluğu Tespit Sistemi")
        self.pencere.geometry("1200x800")
        
        # Video kaynağı
        self.video_kaynagi = None
        self.video_aktif = False
        
        # Araç sayım değişkenleri
        self.toplam_arac = 0
        self.anlik_arac = 0
        self.yogunluk_seviyesi = "Düşük"
        
        # Arkaplan çıkarıcı
        self.arkaplan_cikarici = cv2.createBackgroundSubtractorMOG2(
            history=100, varThreshold=40, detectShadows=True)
        
        # Kayıt değişkenleri
        self.kayit_aktif = False
        self.kayit_dosyasi = None
        
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        # Kontrol paneli
        kontrol_panel = ttk.LabelFrame(self.pencere, text="Kontrol Paneli")
        kontrol_panel.pack(fill="x", padx=5, pady=5)
        
        # Video seçme butonu
        self.video_sec_buton = ttk.Button(kontrol_panel, 
                                        text="Video Seç",
                                        command=self.video_sec)
        self.video_sec_buton.pack(side="left", padx=5, pady=5)
        
        # Kamera başlat butonu
        self.kamera_buton = ttk.Button(kontrol_panel,
                                     text="Kamera Başlat",
                                     command=self.kamera_baslat)
        self.kamera_buton.pack(side="left", padx=5, pady=5)
        
        # Kayıt butonu
        self.kayit_buton = ttk.Button(kontrol_panel,
                                    text="Kayıt Başlat",
                                    command=self.kayit_toggle)
        self.kayit_buton.pack(side="left", padx=5, pady=5)
        
        # Video görüntüleme alanı
        self.video_cerceve = ttk.LabelFrame(self.pencere, text="Video Görüntüsü")
        self.video_cerceve.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.video_alani = ttk.Label(self.video_cerceve)
        self.video_alani.pack(pady=5)
        
        # Bilgi paneli
        bilgi_panel = ttk.LabelFrame(self.pencere, text="Trafik Bilgileri")
        bilgi_panel.pack(fill="x", padx=5, pady=5)
        
        # Anlık araç sayısı
        self.anlik_arac_label = ttk.Label(bilgi_panel,
                                        text="Anlık Araç Sayısı: 0")
        self.anlik_arac_label.pack(pady=5)
        
        # Toplam araç sayısı
        self.toplam_arac_label = ttk.Label(bilgi_panel,
                                         text="Toplam Araç Sayısı: 0")
        self.toplam_arac_label.pack(pady=5)
        
        # Yoğunluk seviyesi
        self.yogunluk_label = ttk.Label(bilgi_panel,
                                      text="Yoğunluk Seviyesi: Düşük")
        self.yogunluk_label.pack(pady=5)
        
    def video_sec(self):
        dosya_yolu = filedialog.askopenfilename(
            filetypes=[("Video Dosyaları", "*.mp4 *.avi *.mkv")]
        )
        
        if dosya_yolu:
            if self.video_aktif:
                self.video_durdur()
            
            self.video_kaynagi = cv2.VideoCapture(dosya_yolu)
            self.video_aktif = True
            Thread(target=self.video_isleme).start()
    
    def kamera_baslat(self):
        if self.video_aktif:
            self.video_durdur()
            self.kamera_buton.config(text="Kamera Başlat")
        else:
            self.video_kaynagi = cv2.VideoCapture(0)  # Varsayılan kamera
            self.video_aktif = True
            self.kamera_buton.config(text="Kamera Durdur")
            Thread(target=self.video_isleme).start()
    
    def video_durdur(self):
        self.video_aktif = False
        if self.video_kaynagi:
            self.video_kaynagi.release()
        
        if self.kayit_aktif:
            self.kayit_toggle()
    
    def kayit_toggle(self):
        if not self.kayit_aktif:
            # Kayıt klasörü oluştur
            if not os.path.exists("kayitlar"):
                os.makedirs("kayitlar")
            
            # Kayıt dosyası oluştur
            tarih = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.kayit_dosyasi = open(f"kayitlar/trafik_kayit_{tarih}.csv", "w", newline="")
            self.csv_yazici = csv.writer(self.kayit_dosyasi)
            self.csv_yazici.writerow(["Zaman", "Anlık Araç", "Toplam Araç", "Yoğunluk"])
            
            self.kayit_aktif = True
            self.kayit_buton.config(text="Kayıt Durdur")
        else:
            self.kayit_aktif = False
            self.kayit_buton.config(text="Kayıt Başlat")
            if self.kayit_dosyasi:
                self.kayit_dosyasi.close()
    
    def arac_tespiti(self, frame):
        # Gri tonlamaya çevir
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Arkaplan çıkarma
        maske = self.arkaplan_cikarici.apply(gri)
        
        # Gürültü temizleme
        maske = cv2.morphologyEx(maske, cv2.MORPH_OPEN, 
                               np.ones((5,5), np.uint8))
        maske = cv2.morphologyEx(maske, cv2.MORPH_CLOSE,
                               np.ones((20,20), np.uint8))
        
        # Konturları bul
        konturlar, _ = cv2.findContours(maske, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
        
        # Araç sayısını güncelle
        self.anlik_arac = 0
        min_alan = 500  # Minimum araç alanı
        
        for kontur in konturlar:
            alan = cv2.contourArea(kontur)
            if alan > min_alan:
                self.anlik_arac += 1
                x, y, w, h = cv2.boundingRect(kontur)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Toplam araç sayısını güncelle
        if self.anlik_arac > 0:
            self.toplam_arac += 1
        
        # Yoğunluk seviyesini belirle
        if self.anlik_arac < 3:
            self.yogunluk_seviyesi = "Dusuk"
        elif self.anlik_arac < 6:
            self.yogunluk_seviyesi = "Orta"
        else:
            self.yogunluk_seviyesi = "Yuksek"
        
        return frame
    
    def video_isleme(self):
        while self.video_aktif:
            ret, frame = self.video_kaynagi.read()
            if not ret:
                break
            
            # Boyut ayarlama
            frame = cv2.resize(frame, (800, 600))
            
            # Araç tespiti
            islenmus_frame = self.arac_tespiti(frame)
            
            # Bilgileri ekrana yaz
            cv2.putText(islenmus_frame, f"Anlik Arac: {self.anlik_arac}",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(islenmus_frame, f"Toplam Arac: {self.toplam_arac}",
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(islenmus_frame, f"Yogunluk: {self.yogunluk_seviyesi}",
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Görüntüyü GUI'de göster
            rgb_frame = cv2.cvtColor(islenmus_frame, cv2.COLOR_BGR2RGB)
            foto = Image.fromarray(rgb_frame)
            foto_tk = ImageTk.PhotoImage(image=foto)
            self.video_alani.config(image=foto_tk)
            self.video_alani.image = foto_tk
            
            # Bilgi etiketlerini güncelle
            self.anlik_arac_label.config(text=f"Anlık Araç Sayısı: {self.anlik_arac}")
            self.toplam_arac_label.config(text=f"Toplam Araç Sayısı: {self.toplam_arac}")
            self.yogunluk_label.config(text=f"Yoğunluk Seviyesi: {self.yogunluk_seviyesi}")
            
            # Kayıt
            if self.kayit_aktif:
                zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.csv_yazici.writerow([zaman, self.anlik_arac,
                                        self.toplam_arac, self.yogunluk_seviyesi])
            
            time.sleep(0.03)  # FPS kontrolü
        
        self.video_kaynagi.release()
    
    def baslat(self):
        self.pencere.mainloop()

if __name__ == "__main__":
    uygulama = TrafikYogunlukTespiti()
    uygulama.baslat()

