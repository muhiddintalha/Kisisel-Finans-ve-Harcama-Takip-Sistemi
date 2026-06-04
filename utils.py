# -*- coding: utf-8 -*-
"""
utils.py
========
Yardımcı (utility) fonksiyonlar.

Bu modül; benzersiz kimlik (ID) üretimi, tarih ve sayı doğrulaması ve ana
menüyü ekrana yazdırma gibi projenin genelinde sıkça tekrar kullanılan küçük
fonksiyonları barındırır. Böylece aynı kod birden fazla yerde tekrar
yazılmaz (Clean Code / DRY ilkesi).
"""

from datetime import datetime


def yeni_id_olustur(liste):
    """Verilen listedeki en büyük ID'yi bulup bir artırarak yeni ID üretir.

    Parametre
    ---------
    liste : list[Islem]
        İçinde ``Islem`` nesneleri bulunan liste.

    Dönüş
    -----
    int
        Liste boşsa 1; aksi halde (mevcut en büyük ID + 1).
    """
    if not liste:
        return 1
    return max(islem.id for islem in liste) + 1


def tarih_kontrol(tarih):
    """Girilen tarihin 'YYYY-MM-DD' biçiminde olup olmadığını kontrol eder.

    Parametre
    ---------
    tarih : str
        Kontrol edilecek tarih metni.

    Dönüş
    -----
    bool
        Biçim doğruysa True, değilse False.
    """
    try:
        datetime.strptime(tarih, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        # Hatalı biçim veya yanlış tür gelirse güvenle False döndürülür.
        return False


def sayi_kontrol(deger):
    """Verilen değerin sayıya (float) çevrilebilir olup olmadığını kontrol eder.

    Parametre
    ---------
    deger : str | int | float
        Kontrol edilecek değer.

    Dönüş
    -----
    bool
        Sayıya dönüştürülebiliyorsa True, aksi halde False.
    """
    try:
        float(deger)
        return True
    except (ValueError, TypeError):
        return False


def menu_goster():
    """Programın ana menüsünü kullanıcıya ekrana yazdırır."""
    print("\n" + "=" * 48)
    print("    KİŞİSEL FİNANS VE HARCAMA TAKİP SİSTEMİ")
    print("=" * 48)
    print("  1. Gelir Ekle")
    print("  2. Gider Ekle")
    print("  3. Listele")
    print("  4. Analiz Yap")
    print("  5. Grafik Göster")
    print("  6. CSV Kaydet")
    print("  7. Çıkış")
    print("=" * 48)
