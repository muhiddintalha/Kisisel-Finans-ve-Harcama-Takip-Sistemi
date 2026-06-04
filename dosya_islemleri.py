# -*- coding: utf-8 -*-
"""
dosya_islemleri.py
==================
Dosya işlemleri (CSV okuma / yazma + Excel raporu).

Gelir ve gider verileri, oturumlar arasında kaybolmaması için bir CSV
dosyasında kalıcı olarak saklanır. Türkçe karakterlerin Excel'de de sorunsuz
görünmesi amacıyla dosyalar 'utf-8-sig' kodlamasıyla yazılır.

Ayrıca ``excel_kaydet`` fonksiyonu, verileri ve özet analizleri çok sayfalı
(.xlsx) bir Excel raporu olarak dışa aktarır.
"""

import csv
import os

from finans_modeli import Islem

# CSV dosyasının sütun (başlık) sırası.
BASLIKLAR = ["id", "tutar", "tarih", "aciklama", "tip"]


def csv_kaydet(dosya_adi, gelirler, giderler):
    """Tüm gelir ve gider verilerini belirtilen CSV dosyasına kaydeder.

    Parametreler
    ------------
    dosya_adi : str
        Yazılacak CSV dosyasının yolu/adı.
    gelirler, giderler : list[Islem]
        Kaydedilecek işlem listeleri.

    Dönüş
    -----
    bool
        Kayıt başarılıysa True, hata oluşursa False.
    """
    try:
        # Hedef klasör (ör. "ciktilar/") yoksa otomatik oluşturulur.
        klasor = os.path.dirname(dosya_adi)
        if klasor and not os.path.exists(klasor):
            os.makedirs(klasor)

        with open(dosya_adi, mode="w", newline="", encoding="utf-8-sig") as dosya:
            yazici = csv.DictWriter(dosya, fieldnames=BASLIKLAR)
            yazici.writeheader()
            for islem in (gelirler + giderler):
                yazici.writerow(islem.sozluge_cevir())

        toplam = len(gelirler) + len(giderler)
        print(f"  [OK] {toplam} işlem '{dosya_adi}' dosyasına kaydedildi.")
        return True
    except (OSError, IOError) as hata:
        print(f"  [!] CSV kaydedilirken hata oluştu: {hata}")
        return False


def csv_oku(dosya_adi):
    """CSV dosyasındaki verileri okuyarak gelir ve gider listelerini oluşturur.

    Parametre
    ---------
    dosya_adi : str
        Okunacak CSV dosyasının yolu/adı.

    Dönüş
    -----
    tuple[list[Islem], list[Islem]]
        (gelirler, giderler) ikilisi. Dosya yoksa iki boş liste döner.
    """
    gelirler = []
    giderler = []
    try:
        with open(dosya_adi, mode="r", newline="", encoding="utf-8-sig") as dosya:
            okuyucu = csv.DictReader(dosya)
            for satir in okuyucu:
                islem = Islem.sozlukten_olustur(satir)
                if islem.tip == "gelir":
                    gelirler.append(islem)
                else:
                    giderler.append(islem)
        print(f"  [OK] '{dosya_adi}' dosyasından {len(gelirler)} gelir, "
              f"{len(giderler)} gider okundu.")
    except FileNotFoundError:
        print(f"  [i] '{dosya_adi}' bulunamadı. Boş listelerle başlanıyor.")
    except Exception as hata:
        print(f"  [!] CSV okunurken hata oluştu: {hata}")
    return gelirler, giderler


def excel_kaydet(dosya_adi, gelirler, giderler):
    """Verileri ve özet analizleri çok sayfalı bir Excel (.xlsx) raporuna aktarır.

    Oluşturulan çalışma kitabı üç sayfadan oluşur:
        1. "Tum Islemler"  : Bütün gelir/gider kayıtları
        2. "Aylik Ozet"    : Aya göre toplam gelir, gider ve net bakiye
        3. "Istatistikler" : NumPy ile hesaplanan ortalama, min, max, std vb.

    Not: Bu fonksiyon ``pandas`` ve ``openpyxl`` kütüphanelerine ihtiyaç duyar.
    İçe aktarmalar, döngüsel bağımlılığı önlemek için fonksiyon içinde yapılır.

    Parametreler
    ------------
    dosya_adi : str
        Yazılacak .xlsx dosyasının yolu/adı.
    gelirler, giderler : list[Islem]
        Rapora aktarılacak işlem listeleri.

    Dönüş
    -----
    bool
        Rapor başarıyla oluşturulduysa True, aksi halde False.
    """
    try:
        import pandas as pd
        # analiz modülü yalnızca burada kullanıldığı için yerel olarak alınır.
        from analiz import (
            verileri_dataframe_yap,
            aylik_analiz,
            numpy_istatistik,
        )

        klasor = os.path.dirname(dosya_adi)
        if klasor and not os.path.exists(klasor):
            os.makedirs(klasor)

        df = verileri_dataframe_yap(gelirler, giderler)
        if df.empty:
            print("  [i] Excel için kayıt bulunamadı.")
            return False

        # 1) Tüm işlemler tablosu (okunabilir Türkçe başlıklarla).
        tum = df[["id", "tarih", "tip", "tutar", "aciklama"]].copy()
        tum["tarih"] = tum["tarih"].dt.strftime("%Y-%m-%d")
        tum.columns = ["ID", "Tarih", "Tür", "Tutar (TL)", "Açıklama"]

        # 2) Aylık özet tablosu.
        aylik = aylik_analiz(df).rename(
            columns={"ay": "Ay", "gelir": "Gelir (TL)",
                     "gider": "Gider (TL)", "net": "Net (TL)"}
        )

        # 3) İstatistik tablosu (NumPy sonuçlarından düz bir tablo üretilir).
        istat = numpy_istatistik(df)
        istat_df = pd.DataFrame(
            [
                {
                    "Tür": tip.capitalize(),
                    "Adet": deger["adet"],
                    "Toplam (TL)": round(deger["toplam"], 2),
                    "Ortalama (TL)": round(deger["ortalama"], 2),
                    "Minimum (TL)": round(deger["min"], 2),
                    "Maksimum (TL)": round(deger["max"], 2),
                    "Std. Sapma": round(deger["std"], 2),
                }
                for tip, deger in istat.items()
            ]
        )

        # Üç tabloyu üç ayrı sayfaya yazıyoruz.
        with pd.ExcelWriter(dosya_adi, engine="openpyxl") as yazici:
            tum.to_excel(yazici, sheet_name="Tum Islemler", index=False)
            aylik.to_excel(yazici, sheet_name="Aylik Ozet", index=False)
            istat_df.to_excel(yazici, sheet_name="Istatistikler", index=False)

            # Basit biçimlendirme: sütun genişliklerini içeriğe göre ayarla.
            for sayfa in yazici.sheets.values():
                for sutun in sayfa.columns:
                    en_uzun = max(
                        (len(str(h.value)) for h in sutun if h.value is not None),
                        default=10,
                    )
                    harf = sutun[0].column_letter
                    sayfa.column_dimensions[harf].width = en_uzun + 4

        print(f"  [OK] Excel raporu oluşturuldu: {dosya_adi}")
        return True
    except ImportError:
        print("  [!] Excel için 'openpyxl' gerekli. Kurulum: pip install openpyxl")
        return False
    except Exception as hata:
        print(f"  [!] Excel kaydedilirken hata oluştu: {hata}")
        return False
