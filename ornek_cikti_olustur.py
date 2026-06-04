# -*- coding: utf-8 -*-
"""
ornek_cikti_olustur.py
======================
Örnek (demo) çıktı üretici.

Bu yardımcı betik; menüden tek tek veri girmeye gerek kalmadan, gerçekçi
örnek gelir/gider kayıtları oluşturur ve projenin tüm çıktılarını otomatik
olarak üretir:

    - veriler.csv                  (CSV verisi)
    - ciktilar/finans_raporu.xlsx  (çok sayfalı Excel raporu)
    - ciktilar/aylik_grafik.png    (çizgi grafik)
    - ciktilar/gelir_gider_bar.png (sütun grafik)
    - ciktilar/pasta_grafik.png    (pasta grafik)

Çalıştırma:
    python ornek_cikti_olustur.py
"""

import os

# Grafikler ekran (pencere) açmadan dosyaya kaydedilsin diye 'Agg' arka ucu.
import matplotlib
matplotlib.use("Agg")

from finans_modeli import Islem
from dosya_islemleri import csv_kaydet, excel_kaydet
from gorsellestirme import aylik_grafik, gelir_gider_bar, pasta_grafik

CIKTI_KLASORU = "ciktilar"

# (tutar, tarih, aciklama, tip) biçiminde gerçekçi örnek veriler (6 ay).
ORNEK_VERILER = [
    # Ocak 2025
    (32000.00, "2025-01-05", "Maaş", "gelir"),
    (4500.00,  "2025-01-12", "Freelance yazılım işi", "gelir"),
    (9500.00,  "2025-01-03", "Ev kirası", "gider"),
    (3200.50,  "2025-01-09", "Market alışverişi", "gider"),
    (1450.00,  "2025-01-15", "Elektrik + su + doğalgaz", "gider"),
    (850.00,   "2025-01-22", "Ulaşım (akbil)", "gider"),
    # Şubat 2025
    (32000.00, "2025-02-05", "Maaş", "gelir"),
    (2000.00,  "2025-02-18", "İkinci el eşya satışı", "gelir"),
    (9500.00,  "2025-02-03", "Ev kirası", "gider"),
    (2950.75,  "2025-02-11", "Market alışverişi", "gider"),
    (1600.00,  "2025-02-14", "Sevgililer günü", "gider"),
    (1200.00,  "2025-02-20", "İnternet + telefon", "gider"),
    # Mart 2025
    (33500.00, "2025-03-05", "Maaş (zam)", "gelir"),
    (6000.00,  "2025-03-21", "Freelance web sitesi", "gelir"),
    (9500.00,  "2025-03-03", "Ev kirası", "gider"),
    (3400.00,  "2025-03-10", "Market alışverişi", "gider"),
    (2200.00,  "2025-03-16", "Giyim", "gider"),
    (950.00,   "2025-03-25", "Eğlence (sinema, kafe)", "gider"),
    # Nisan 2025
    (33500.00, "2025-04-05", "Maaş", "gelir"),
    (9500.00,  "2025-04-03", "Ev kirası", "gider"),
    (3100.25,  "2025-04-12", "Market alışverişi", "gider"),
    (4800.00,  "2025-04-19", "Tatil rezervasyonu", "gider"),
    (1500.00,  "2025-04-27", "Faturalar", "gider"),
    # Mayıs 2025
    (33500.00, "2025-05-05", "Maaş", "gelir"),
    (5200.00,  "2025-05-23", "Freelance mobil uygulama", "gelir"),
    (9500.00,  "2025-05-03", "Ev kirası", "gider"),
    (3650.00,  "2025-05-13", "Market alışverişi", "gider"),
    (2750.00,  "2025-05-18", "Teknolojik ürün (kulaklık)", "gider"),
    # Haziran 2025
    (34000.00, "2025-06-05", "Maaş", "gelir"),
    (9500.00,  "2025-06-03", "Ev kirası", "gider"),
    (3300.00,  "2025-06-11", "Market alışverişi", "gider"),
    (1850.00,  "2025-06-20", "Spor salonu üyeliği", "gider"),
]


def ornek_listeleri_olustur():
    """Örnek verilerden gelir ve gider listelerini (Islem nesneleri) üretir.

    Kayıtlara, çakışmayan benzersiz kimlik (ID) numaraları sırayla verilir.

    Dönüş
    -----
    tuple[list[Islem], list[Islem]]
        (gelirler, giderler) ikilisi.
    """
    gelirler = []
    giderler = []
    siradaki_id = 1
    for tutar, tarih, aciklama, tip in ORNEK_VERILER:
        islem = Islem(siradaki_id, tutar, tarih, aciklama, tip)
        if islem.tip == "gelir":
            gelirler.append(islem)
        else:
            giderler.append(islem)
        siradaki_id += 1
    return gelirler, giderler


def main():
    """Örnek verileri üretip tüm çıktı dosyalarını oluşturur."""
    print("Örnek veriler oluşturuluyor...")
    gelirler, giderler = ornek_listeleri_olustur()
    print(f"  -> {len(gelirler)} gelir, {len(giderler)} gider kaydı hazırlandı.\n")

    # 1) CSV ve Excel çıktıları
    csv_kaydet("veriler.csv", gelirler, giderler)
    excel_kaydet(os.path.join(CIKTI_KLASORU, "finans_raporu.xlsx"), gelirler, giderler)

    # 2) Grafik çıktıları (ekran açmadan doğrudan dosyaya)
    from analiz import verileri_dataframe_yap
    df = verileri_dataframe_yap(gelirler, giderler)
    aylik_grafik(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "aylik_grafik.png"), goster=False)
    gelir_gider_bar(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "gelir_gider_bar.png"), goster=False)
    pasta_grafik(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "pasta_grafik.png"), goster=False)

    print("\nTüm örnek çıktılar başarıyla oluşturuldu.")


if __name__ == "__main__":
    main()
