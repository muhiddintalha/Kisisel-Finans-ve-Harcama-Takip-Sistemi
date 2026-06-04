# -*- coding: utf-8 -*-
"""
gorsellestirme.py
=================
Veri görselleştirme (Matplotlib & Seaborn).

Bu modül, analiz sonuçlarını anlaşılır grafiklere dönüştürür:
    - aylik_grafik     : Aylık gelir/gider karşılaştırması (çizgi grafik)
    - gelir_gider_bar  : Toplam gelir/gider karşılaştırması (sütun grafik)
    - pasta_grafik     : Gelir/gider oranı (pasta grafik)

Her fonksiyon, isteğe bağlı olarak grafiği bir dosyaya kaydedebilir
(``kaydet_yolu``) ve/veya ekranda gösterebilir (``goster``). Böylece hem
menüden interaktif kullanım hem de otomatik çıktı üretimi desteklenir.
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns

from analiz import aylik_analiz, toplam_gelir_gider

# Seaborn ile tutarlı, modern bir görünüm.
sns.set_theme(style="whitegrid")

# Proje genelinde kullanılan kurumsal renk paleti.
RENK_GELIR = "#16a34a"   # yeşil
RENK_GIDER = "#dc2626"   # kırmızı


def _grafigi_bitir(kaydet_yolu, goster):
    """Grafiği (varsa) dosyaya kaydeder ve (isteniyorsa) ekranda gösterir.

    Tüm grafik fonksiyonlarında tekrar eden bitiş adımlarını tek yerde toplar.
    """
    plt.tight_layout()
    if kaydet_yolu:
        klasor = os.path.dirname(kaydet_yolu)
        if klasor and not os.path.exists(klasor):
            os.makedirs(klasor)
        plt.savefig(kaydet_yolu, dpi=120, bbox_inches="tight")
        print(f"  [OK] Grafik kaydedildi: {kaydet_yolu}")
    if goster:
        plt.show()
    plt.close()


def aylik_grafik(df, kaydet_yolu=None, goster=True):
    """Aylık gelir ve giderleri karşılaştıran çizgi grafiği oluşturur.

    Parametreler
    ------------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.
    kaydet_yolu : str, optional
        Verilirse grafik bu yola PNG olarak kaydedilir.
    goster : bool, optional
        True ise grafik ekranda gösterilir (varsayılan: True).
    """
    ozet = aylik_analiz(df)
    if ozet.empty:
        print("  [i] Grafik için yeterli veri yok.")
        return

    plt.figure(figsize=(10, 5.5))
    plt.plot(ozet["ay"], ozet["gelir"], marker="o", linewidth=2.5,
             color=RENK_GELIR, label="Gelir")
    plt.plot(ozet["ay"], ozet["gider"], marker="s", linewidth=2.5,
             color=RENK_GIDER, label="Gider")

    plt.title("Aylık Gelir / Gider Karşılaştırması", fontsize=14, fontweight="bold")
    plt.xlabel("Ay")
    plt.ylabel("Tutar (TL)")
    plt.xticks(rotation=45)
    plt.legend()
    _grafigi_bitir(kaydet_yolu, goster)


def gelir_gider_bar(df, kaydet_yolu=None, goster=True):
    """Toplam gelir ve toplam gideri karşılaştıran sütun grafiği oluşturur.

    Parametreler
    ------------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.
    kaydet_yolu : str, optional
        Verilirse grafik bu yola PNG olarak kaydedilir.
    goster : bool, optional
        True ise grafik ekranda gösterilir (varsayılan: True).
    """
    toplam_gelir, toplam_gider = toplam_gelir_gider(df)
    if toplam_gelir == 0 and toplam_gider == 0:
        print("  [i] Grafik için yeterli veri yok.")
        return

    etiketler = ["Toplam Gelir", "Toplam Gider"]
    degerler = [toplam_gelir, toplam_gider]

    plt.figure(figsize=(8, 5.5))
    cubuklar = plt.bar(etiketler, degerler,
                       color=[RENK_GELIR, RENK_GIDER], width=0.55)

    # Her çubuğun üzerine değerini yazdırıyoruz (okunabilirlik için).
    for cubuk, deger in zip(cubuklar, degerler):
        plt.text(cubuk.get_x() + cubuk.get_width() / 2, deger,
                 f"{deger:,.0f} TL", ha="center", va="bottom", fontweight="bold")

    plt.title("Toplam Gelir ve Gider", fontsize=14, fontweight="bold")
    plt.ylabel("Tutar (TL)")
    plt.margins(y=0.15)  # üstte yazı için boşluk
    _grafigi_bitir(kaydet_yolu, goster)


def pasta_grafik(df, kaydet_yolu=None, goster=True):
    """Gelir ve gider oranlarını gösteren pasta grafiği oluşturur.

    Parametreler
    ------------
    df : pandas.DataFrame
        ``verileri_dataframe_yap`` çıktısı.
    kaydet_yolu : str, optional
        Verilirse grafik bu yola PNG olarak kaydedilir.
    goster : bool, optional
        True ise grafik ekranda gösterilir (varsayılan: True).
    """
    toplam_gelir, toplam_gider = toplam_gelir_gider(df)
    if toplam_gelir == 0 and toplam_gider == 0:
        print("  [i] Grafik için yeterli veri yok.")
        return

    plt.figure(figsize=(7, 7))
    plt.pie(
        [toplam_gelir, toplam_gider],
        labels=["Gelir", "Gider"],
        colors=[RENK_GELIR, RENK_GIDER],
        autopct="%1.1f%%",
        startangle=90,
        explode=(0.03, 0.03),
        textprops={"fontsize": 12, "fontweight": "bold", "color": "white"},
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    plt.title("Gelir / Gider Oranı", fontsize=14, fontweight="bold")
    plt.axis("equal")  # daireyi yuvarlak tutar
    _grafigi_bitir(kaydet_yolu, goster)
