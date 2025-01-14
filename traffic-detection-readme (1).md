Trafik Yoğunluğu Algılama Sistemi
Bilgisayarlı görüş teknikleri kullanılarak gerçek zamanlı trafik izleme ve yoğunluk analizi için Python tabanlı bir uygulama. Sistem, araçları tespit etmek ve trafik modellerini analiz etmek için hem canlı kamera yayınlarını hem de kayıtlı video dosyalarını işleyebilir.
Özellikler

Gerçek zamanlı araç tespiti ve sayımı
Trafik yoğunluğu sınıflandırması (Düşük, Orta, Yüksek)
Hem video dosyaları hem de canlı kamera yayınları için destek
CSV dışa aktarımıyla veri kaydı yetenekleri
Kullanıcı dostu GUI arayüzü
Araç sınırlayıcı kutularla gerçek zamanlı görselleştirme
Doğru algılama için otomatik arka plan çıkarma

Gereksinimler

Python 3.8+
AçıkCV (cv2)
NumPy
Tkinter
Yastık (KÖP)

Kurulum

Depoyu klonlayın:

vuruşKopyalagit clone https://github.com/yourusername/traffic-density-detection.git
cd traffic-density-detection

Sanal bir ortam oluşturun (önerilir):

vuruşKopyalapython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Gerekli paketleri kurun:

vuruşKopyalapip install opencv-python numpy pillow
Kullanım

Ana uygulamayı çalıştırın:

vuruşKopyalapython traffic_detection.py

Uygulamayı kullanma:

Önceden kaydedilmiş bir video dosyasını analiz etmek için "Video Seç"e tıklayın
Canlı kamera yayınını kullanmak için "Kamera Başlat"a tıklayın
Trafik verilerini CSV'ye kaydetmeye başlamak için "Kayıt Başlat"a tıklayın



Sistem şunu gösterecektir:

Gerçek zamanlı araç sayımı
Toplam tespit edilen araç sayısı
Mevcut trafik yoğunluk seviyesi
Tanımlanan araçların etrafında görsel tespit kutuları

Veri Kaydı
Kayıt etkinleştirildiğinde, sistem dizinde recordingsaşağıdaki bilgileri içeren CSV dosyaları oluşturur:

Zaman damgası
Mevcut araç sayısı
Toplam tespit edilen araç sayısı
Trafik yoğunluk seviyesi

Teknik Detaylar
Sistem şunları kullanır:

Hareket algılama için MOG2 arka plan çıkarma
Gürültü azaltma için morfolojik işlemler
Araç tanımlama için kontur algılama
Sorunsuz video işleme için çoklu iş parçacığı

Yapılandırma
Kodda ayarlanabilen temel parametreler:

min_area = 500: Araç tespiti için minimum alan eşiği
history = 100: Arkaplan çıkarıcı geçmişi uzunluğu
varThreshold = 40: Arka plan çıkarma için varyans eşiği
Çerçeve yeniden boyutlandırma boyutları: 800x600 ( video_islemeyöntemde ayarlanabilir)

Bilinen Sınırlamalar

Tutarlı ışık koşullarında en iyi performans
Farklı kamera açıları için eşik ayarlamaları gerekebilir
Yukarıdan trafik görünümü için tasarlanmıştır
İşlem hızı donanım yeteneklerine bağlıdır

Katkıda bulunmak

Depoyu çatallandır
Özellik dalınızı oluşturun ( git checkout -b feature/AmazingFeature)
Değişikliklerinizi kaydedin ( git commit -m 'Add some AmazingFeature')
Şubeye it ( git push origin feature/AmazingFeature)
Bir Çekme İsteği Açın

Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.
Teşekkürler

Bilgisayar görüşü için OpenCV kütüphanesi kullanılarak oluşturuldu
GUI uygulaması için Tkinter'ı kullanır
Modern trafik yönetim sistemlerinden ilham alındı

Yazar
[BETÜL BAŞBOĞA]

GitHub: @bettull
E-posta: betulbasboga921@gmail.com
