# -*- coding: utf-8 -*-
"""
analiz.py
=========
Veri analizi (Pandas & NumPy).

Bu modül, ``Islem`` nesnelerinden oluşan gelir/gider listelerini bir pandas
``DataFrame`` yapısına dönüştürür ve bu yapı üzerinde çeşitli finansal
analizler (toplamlar, aylık özet, istatistikler) gerçekleştirir.

Kullanılan kütüphaneler:
    - pandas : Tablo (DataFrame) işlemleri ve gruplama
    - numpy  : İstatistiksel hesaplamalar (ortalama, std, min, max)
"""

import numpy as np
import pandas as pd

# DataFrame'de kullanılacak standart sütun adları.
SUTUNLAR = ["id", "tutar", "tarih", "aciklama", "tip"]


def verileri_dataframe_yap(gelirler, giderler):
    """Gelir ve gider listelerini birleştirerek pandas DataFrame'e dönüştürür.

    Her ``Islem`` nesnesi önce sözlüğe çevrilir, ardından tüm sözlükler tek bir
    DataFrame'de toplanır. ``tarih`` sütunu tarih tipine, ``tutar`` sütunu
    sayısal tipe dönüştürülür ve gruplama kolaylığı için ``ay`` (YYYY-MM)
    sütunu eklenir.

    Parametreler
    ------------
    gelirler, giderler : list[Islem]
        İşlem nesnelerinden oluşan listeler.

    Dönüş
    -----
    pandas.DataFrame
        ``id, tutar, tarih, aciklama, tip, ay`` sütunlarını içerir.
        Veri yoksa boş bir DataFrame döner.
    """
    tum_kayitlar = [islem.sozluge_cevir() for islem in (gelirler + giderler)]

    # Hiç kayıt yoksa, sütun yapısı korunmuş boş bir DataFrame döndürülür.
    if not tum_kayitlar:
        return pd.DataFrame(columns=SUTUNLAR + ["ay"])

    df = pd.DataFrame(tum_kayitlar, columns=SUTUNLAR)

    # Tür dönüşümleri: hatalı değerler NaT/NaN olur, sonra temizlenir.
    df["tarih"] = pd.to_datetime(df["tarih"], format="%Y-%m-%d", errors="coerce")
    df["tutar"] = pd.to_numeric(df["tutar"], errors="coerce")
    df = df.dropna(subset=["tarih", "tutar"]).reset_index(drop=True)

    # Aylık analizler için "YYYY-MM" biçiminde yardımcı sütun.
    df["ay"] = df["tarih"].dt.strftime("%Y-%m")

    # Kronolojik sıralama (en eskiden en yeniye).
    df = df.sort_values("tarih").reset_index(drop=True)
    return df


def toplam_gelir_gider(df):
    """DataFrame üzerinden toplam gelir ve toplam gider değerlerini hesaplar.

    Parametre
    ---------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.

    Dönüş
    -----
    tuple[float, float]
        (toplam_gelir, toplam_gider) ikilisi.
    """
    if df.empty:
        return 0.0, 0.0

    toplam_gelir = df.loc[df["tip"] == "gelir", "tutar"].sum()
    toplam_gider = df.loc[df["tip"] == "gider", "tutar"].sum()
    return float(toplam_gelir), float(toplam_gider)


def aylik_analiz(df):
    """Verileri aya göre gruplayarak aylık bazda özet analiz oluşturur.

    Her ay için toplam gelir, toplam gider ve net bakiye (gelir - gider)
    hesaplanır.

    Parametre
    ---------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.

    Dönüş
    -----
    pandas.DataFrame
        ``ay, gelir, gider, net`` sütunlarını içerir.
    """
    if df.empty:
        return pd.DataFrame(columns=["ay", "gelir", "gider", "net"])

    # Ay ve tip kırılımında toplam tutarlar (pivot tablo).
    ozet = df.pivot_table(
        index="ay",
        columns="tip",
        values="tutar",
        aggfunc="sum",
        fill_value=0,
    )

    # Yalnızca gelir veya yalnızca gider varsa eksik sütunu 0 ile tamamla.
    for tip in ("gelir", "gider"):
        if tip not in ozet.columns:
            ozet[tip] = 0.0

    ozet = ozet[["gelir", "gider"]]
    ozet["net"] = ozet["gelir"] - ozet["gider"]
    return ozet.reset_index()


def numpy_istatistik(df):
    """NumPy kullanarak gelir ve gider tutarları üzerinde istatistik hesaplar.

    Her işlem türü için ortalama, minimum, maksimum, standart sapma, toplam ve
    adet değerleri hesaplanır.

    Parametre
    ---------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.

    Dönüş
    -----
    dict
        ``{"gelir": {...}, "gider": {...}}`` biçiminde iç içe sözlük.
        Her alt sözlük: ortalama, min, max, std, toplam, adet anahtarlarını taşır.
    """
    sonuc = {}
    for tip in ("gelir", "gider"):
        # İlgili türe ait tutarları bir NumPy dizisine alıyoruz.
        tutarlar = df.loc[df["tip"] == tip, "tutar"].to_numpy(dtype=float)

        if tutarlar.size == 0:
            sonuc[tip] = {
                "ortalama": 0.0, "min": 0.0, "max": 0.0,
                "std": 0.0, "toplam": 0.0, "adet": 0,
            }
        else:
            sonuc[tip] = {
                "ortalama": float(np.mean(tutarlar)),
                "min": float(np.min(tutarlar)),
                "max": float(np.max(tutarlar)),
                "std": float(np.std(tutarlar)),
                "toplam": float(np.sum(tutarlar)),
                "adet": int(tutarlar.size),
            }
    return sonuc
