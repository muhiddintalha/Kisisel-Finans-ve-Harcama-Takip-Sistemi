# -*- coding: utf-8 -*-
"""
main.py
=======
Kişisel Finans ve Harcama Takip Sistemi  --  ANA PROGRAM (Giriş Noktası)

Bu dosya, projenin tüm modüllerini bir araya getiren ana programdır. Diğer
modüllerdeki sınıf ve fonksiyonları ``import`` ederek menü tabanlı bir konsol
uygulaması çalıştırır.

Modül haritası:
    finans_modeli.py    -> Islem sınıfı (OOP)
    utils.py            -> Yardımcı fonksiyonlar (ID, tarih/sayı kontrolü, menü)
    islem_yonetimi.py   -> Gelir/gider ekleme, listeleme, silme
    dosya_islemleri.py  -> CSV okuma/yazma + Excel raporu
    analiz.py           -> Pandas & NumPy analizleri
    gorsellestirme.py   -> Matplotlib & Seaborn grafikleri

Çalıştırma:
    python main.py

------------------------------------------------------------------------------
Öğrenci : Muhiddin Talha Yılmaz
Numara  : 24083002
Bölüm   : Bilgi Güvenliği Teknolojisi (BGT)
Ders    : BGY210 - Python Programlama II
Öğretim Elemanı : Dr. Öğr. Üyesi Tohid YOUSEFİ
------------------------------------------------------------------------------
"""

import os

# --- Proje modüllerinin içe aktarılması (import) ---
from utils import menu_goster, sayi_kontrol
from islem_yonetimi import (
    gelir_ekle,
    gider_ekle,
    islemleri_listele,
    islem_sil,
)
from dosya_islemleri import csv_kaydet, csv_oku, excel_kaydet
from analiz import (
    verileri_dataframe_yap,
    toplam_gelir_gider,
    aylik_analiz,
    numpy_istatistik,
)
from gorsellestirme import aylik_grafik, gelir_gider_bar, pasta_grafik

# --- Sabit dosya yolları ---
CSV_DOSYA = "veriler.csv"                            # ana veri dosyası
CIKTI_KLASORU = "ciktilar"                           # çıktı (grafik/Excel) klasörü
EXCEL_DOSYA = os.path.join(CIKTI_KLASORU, "finans_raporu.xlsx")


def analiz_yap(gelirler, giderler):
    """4. menü seçeneği: Pandas & NumPy ile finansal analizleri ekrana yazdırır."""
    df = verileri_dataframe_yap(gelirler, giderler)
    if df.empty:
        print("  [i] Analiz için kayıtlı veri bulunmuyor.")
        return

    toplam_gelir, toplam_gider = toplam_gelir_gider(df)
    bakiye = toplam_gelir - toplam_gider

    print("\n" + "=" * 52)
    print("                 FİNANSAL ANALİZ")
    print("=" * 52)
    print(f"  Toplam Gelir : {toplam_gelir:>14,.2f} TL")
    print(f"  Toplam Gider : {toplam_gider:>14,.2f} TL")
    print(f"  Net Bakiye   : {bakiye:>14,.2f} TL")
    durum = "POZİTİF (artıda)" if bakiye >= 0 else "NEGATİF (ekside)"
    print(f"  Durum        : {durum}")

    # --- Aylık özet tablosu ---
    print("\n  --- Aylık Özet ---")
    aylik = aylik_analiz(df)
    print(f"  {'Ay':<9}{'Gelir':>14}{'Gider':>14}{'Net':>14}")
    print("  " + "-" * 49)
    for _, satir in aylik.iterrows():
        print(f"  {satir['ay']:<9}{satir['gelir']:>14,.2f}"
              f"{satir['gider']:>14,.2f}{satir['net']:>14,.2f}")

    # --- NumPy istatistikleri ---
    print("\n  --- İstatistikler (NumPy) ---")
    istat = numpy_istatistik(df)
    for tip, deger in istat.items():
        print(f"  > {tip.capitalize()} (adet: {deger['adet']})")
        print(f"      Ortalama : {deger['ortalama']:>12,.2f} TL")
        print(f"      Minimum  : {deger['min']:>12,.2f} TL")
        print(f"      Maksimum : {deger['max']:>12,.2f} TL")
        print(f"      Std.Sapma: {deger['std']:>12,.2f} TL")
    print("=" * 52)


def grafik_goster(gelirler, giderler):
    """5. menü seçeneği: Üç farklı grafiği oluşturur, gösterir ve kaydeder."""
    df = verileri_dataframe_yap(gelirler, giderler)
    if df.empty:
        print("  [i] Grafik için kayıtlı veri bulunmuyor.")
        return

    print("  Grafikler oluşturuluyor (pencereyi kapatınca menüye dönülür)...")
    # Hem ekranda gösterilir hem de 'ciktilar/' klasörüne PNG olarak kaydedilir.
    aylik_grafik(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "aylik_grafik.png"))
    gelir_gider_bar(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "gelir_gider_bar.png"))
    pasta_grafik(df, kaydet_yolu=os.path.join(CIKTI_KLASORU, "pasta_grafik.png"))


def listele_ve_sil(gelirler, giderler):
    """3. menü seçeneği: Kayıtları listeler ve isteğe bağlı silme imkânı sunar.

    Şartnamedeki ``islem_sil`` fonksiyonu bu akış içinde aktif olarak kullanılır.
    """
    islemleri_listele(gelirler, giderler)

    if not (gelirler or giderler):
        return  # silinecek kayıt yok

    secim = input("\n  Silmek için işlem ID'si girin (boş bırak = geri dön): ").strip()
    if secim == "":
        return
    if not sayi_kontrol(secim):
        print("  [!] Geçersiz ID. Sayısal bir değer girilmelidir.")
        return
    islem_sil(gelirler, giderler, int(float(secim)))


def main():
    """Programın ana akışı: verileri yükler ve menü döngüsünü çalıştırır."""
    print("Kişisel Finans ve Harcama Takip Sistemine hoş geldiniz!")

    # Program açılışında varsa önceki veriler CSV'den yüklenir.
    gelirler, giderler = csv_oku(CSV_DOSYA)

    while True:
        menu_goster()
        try:
            secim = input("Seçiminiz (1-7): ").strip()

            if secim == "1":
                # Her iki liste de verilerek benzersiz ID üretimi sağlanır.
                gelir_ekle(gelirler, giderler)

            elif secim == "2":
                gider_ekle(giderler, gelirler)

            elif secim == "3":
                listele_ve_sil(gelirler, giderler)

            elif secim == "4":
                analiz_yap(gelirler, giderler)

            elif secim == "5":
                grafik_goster(gelirler, giderler)

            elif secim == "6":
                # Veriler hem CSV hem de Excel raporu olarak kaydedilir.
                csv_kaydet(CSV_DOSYA, gelirler, giderler)
                excel_kaydet(EXCEL_DOSYA, gelirler, giderler)

            elif secim == "7":
                # Çıkıştan önce kullanıcıya kaydetme imkânı sunulur.
                cevap = input("  Çıkmadan önce kaydedilsin mi? (E/H): ").strip().lower()
                if cevap == "e":
                    csv_kaydet(CSV_DOSYA, gelirler, giderler)
                    excel_kaydet(EXCEL_DOSYA, gelirler, giderler)
                print("  Programdan çıkılıyor. İyi günler!")
                break

            else:
                print("  [!] Geçersiz seçim. Lütfen 1-7 arasında bir değer girin.")

        except KeyboardInterrupt:
            # Kullanıcı Ctrl+C ile çıkmak isterse program çökmek yerine kapanır.
            print("\n  Program kullanıcı tarafından sonlandırıldı.")
            break
        except Exception as hata:
            # Beklenmeyen tüm hatalar burada yakalanır (program çökmez).
            print(f"  [!] Beklenmeyen bir hata oluştu: {hata}")


# Bu dosya doğrudan çalıştırıldığında main() devreye girer.
# (Başka bir modülden import edilirse otomatik çalışmaz.)
if __name__ == "__main__":
    main()
