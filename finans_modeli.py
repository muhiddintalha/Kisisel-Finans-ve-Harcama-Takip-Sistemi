# -*- coding: utf-8 -*-
"""
finans_modeli.py
================
Kişisel Finans ve Harcama Takip Sistemi  --  Veri Modeli (OOP)

Bu modül, sistemdeki her bir finansal hareketi temsil eden ``Islem`` sınıfını
içerir. Hem gelir hem de gider kayıtları aynı sınıf üzerinden, ``tip``
özniteliği ("gelir" / "gider") ile ayrıştırılarak modellenir.

Öğrenci : Muhiddin Talha Yılmaz
Numara  : 24083002
Bölüm   : Bilgi Güvenliği Teknolojisi (BGT)
Ders    : BGY210 - Python Programlama II
"""


class Islem:
    """Tek bir finansal işlemi (gelir veya gider) temsil eden sınıf.

    Öznitelikler
    ------------
    id : int
        İşlemin benzersiz kimlik numarası.
    tutar : float
        İşlem tutarı (her zaman pozitif tutulur; yön ``tip`` ile belirlenir).
    tarih : str
        İşlem tarihi, "YYYY-MM-DD" biçiminde.
    aciklama : str
        İşlemin kısa açıklaması (ör. "Maaş", "Market alışverişi").
    tip : str
        İşlem türü; yalnızca "gelir" veya "gider" değerini alır.
    """

    # Sınıf düzeyinde sabit: sistemde kabul edilen geçerli işlem türleri.
    GECERLI_TIPLER = ("gelir", "gider")

    def __init__(self, id, tutar, tarih, aciklama, tip):
        """Yeni bir İşlem nesnesi oluşturur.

        Parametreler teknik şartnamedeki imza ile birebir aynıdır:
        ``__init__(self, id, tutar, tarih, aciklama, tip)``

        Gelen değerler, güvenli kullanım için uygun türlere dönüştürülür.
        """
        self.id = int(id)
        self.tutar = float(tutar)
        self.tarih = str(tarih)
        self.aciklama = str(aciklama).strip()
        self.tip = str(tip).strip().lower()

    def sozluge_cevir(self):
        """Nesneyi bir sözlüğe (dict) dönüştürür.

        CSV'ye yazma ve pandas DataFrame oluşturma adımlarında kullanılır.

        Dönüş
        -----
        dict
            "id", "tutar", "tarih", "aciklama", "tip" anahtarlarını içerir.
        """
        return {
            "id": self.id,
            "tutar": self.tutar,
            "tarih": self.tarih,
            "aciklama": self.aciklama,
            "tip": self.tip,
        }

    @classmethod
    def sozlukten_olustur(cls, veri):
        """Bir sözlükten yeni bir ``Islem`` nesnesi üretir.

        CSV'den veri okurken her satırı tekrar nesneye çevirmek için kullanılır.

        Parametre
        ---------
        veri : dict
            "id", "tutar", "tarih", "aciklama", "tip" anahtarlarını içerir.
        """
        return cls(
            id=veri["id"],
            tutar=veri["tutar"],
            tarih=veri["tarih"],
            aciklama=veri["aciklama"],
            tip=veri["tip"],
        )

    def __str__(self):
        """Listeleme ekranı için okunabilir, hizalanmış metin gösterimi."""
        isaret = "+" if self.tip == "gelir" else "-"
        return (
            f"#{self.id:<4}| {self.tarih} | {self.tip.upper():<5} | "
            f"{isaret}{self.tutar:>12,.2f} TL | {self.aciklama}"
        )

    def __repr__(self):
        """Hata ayıklama (debug) için teknik gösterim."""
        return (
            f"Islem(id={self.id}, tutar={self.tutar}, tarih='{self.tarih}', "
            f"aciklama='{self.aciklama}', tip='{self.tip}')"
        )
