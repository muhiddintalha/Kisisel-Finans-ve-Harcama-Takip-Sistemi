# -*- coding: utf-8 -*-
"""
islem_yonetimi.py
=================
Gelir / gider işlemlerinin yönetimi.

Bu modül; kullanıcıdan veri alıp doğrulayarak yeni gelir/gider kaydı
oluşturma, tüm kayıtları listeleme ve ID'ye göre kayıt silme fonksiyonlarını
içerir. Girdi doğrulamaları için ``utils`` modülü, kayıtların modellenmesi
için ``finans_modeli.Islem`` sınıfı kullanılır.
"""

from datetime import date

from finans_modeli import Islem
from utils import yeni_id_olustur, tarih_kontrol, sayi_kontrol


def _tutar_iste(soru):
    """Kullanıcıdan geçerli (pozitif) bir tutar alana kadar tekrar tekrar sorar.

    Bu özel (private) yardımcı fonksiyon, gelir_ekle ve gider_ekle içinde
    kod tekrarını önlemek için kullanılır.
    """
    while True:
        # Virgüllü girişleri (1500,50) da kabul etmek için noktaya çeviriyoruz.
        deger = input(soru).strip().replace(",", ".")
        if not sayi_kontrol(deger):
            print("  [!] Geçersiz tutar. Sayısal bir değer girin (ör. 1500.50).")
            continue
        tutar = float(deger)
        if tutar <= 0:
            print("  [!] Tutar sıfırdan büyük olmalıdır.")
            continue
        return tutar


def _tarih_iste(soru):
    """Kullanıcıdan 'YYYY-MM-DD' biçiminde geçerli bir tarih alana kadar sorar.

    Giriş boş bırakılırsa bugünün tarihi otomatik olarak kullanılır.
    """
    while True:
        deger = input(soru).strip()
        if deger == "":
            return date.today().strftime("%Y-%m-%d")
        if tarih_kontrol(deger):
            return deger
        print("  [!] Geçersiz tarih. Biçim 'YYYY-MM-DD' olmalı (ör. 2025-03-15).")


def gelir_ekle(gelirler, giderler=None):
    """Kullanıcıdan alınan bilgileri doğrulayarak yeni bir gelir kaydı oluşturur.

    Oluşturulan ``Islem`` nesnesi ``gelirler`` listesine eklenir.

    Parametreler
    ------------
    gelirler : list[Islem]
        Gelir kayıtlarının tutulduğu liste (yerinde güncellenir).
    giderler : list[Islem], optional
        Verilirse, üretilen kimlik (ID) tüm sistemde benzersiz olacak biçimde
        gelir ve gider listeleri birlikte değerlendirilerek belirlenir.

    Dönüş
    -----
    Islem | None
        Eklenen gelir nesnesi; bir hata olursa None.
    """
    print("\n--- Yeni Gelir Ekle ---")
    try:
        tutar = _tutar_iste("  Tutar (TL): ")
        tarih = _tarih_iste("  Tarih (YYYY-MM-DD, boş=bugün): ")
        aciklama = input("  Açıklama: ").strip() or "Açıklama yok"

        # Kimliğin tüm sistemde benzersiz olması için (varsa) gelir ve gider
        # listeleri birlikte değerlendirilir; böylece aynı ID iki kez oluşmaz.
        mevcut_kayitlar = gelirler if giderler is None else gelirler + giderler
        yeni_islem = Islem(
            id=yeni_id_olustur(mevcut_kayitlar),
            tutar=tutar,
            tarih=tarih,
            aciklama=aciklama,
            tip="gelir",
        )
        gelirler.append(yeni_islem)
        print(f"  [+] Gelir başarıyla eklendi: {yeni_islem}")
        return yeni_islem
    except Exception as hata:
        print(f"  [!] Gelir eklenirken beklenmeyen bir hata oluştu: {hata}")
        return None


def gider_ekle(giderler, gelirler=None):
    """Kullanıcıdan alınan bilgileri doğrulayarak yeni bir gider kaydı oluşturur.

    Oluşturulan ``Islem`` nesnesi ``giderler`` listesine eklenir.

    Parametreler
    ------------
    giderler : list[Islem]
        Gider kayıtlarının tutulduğu liste (yerinde güncellenir).
    gelirler : list[Islem], optional
        Verilirse, üretilen kimlik (ID) tüm sistemde benzersiz olacak biçimde
        gelir ve gider listeleri birlikte değerlendirilerek belirlenir.

    Dönüş
    -----
    Islem | None
        Eklenen gider nesnesi; bir hata olursa None.
    """
    print("\n--- Yeni Gider Ekle ---")
    try:
        tutar = _tutar_iste("  Tutar (TL): ")
        tarih = _tarih_iste("  Tarih (YYYY-MM-DD, boş=bugün): ")
        aciklama = input("  Açıklama: ").strip() or "Açıklama yok"

        # Kimliğin tüm sistemde benzersiz olması için (varsa) gelir ve gider
        # listeleri birlikte değerlendirilir; böylece aynı ID iki kez oluşmaz.
        mevcut_kayitlar = giderler if gelirler is None else gelirler + giderler
        yeni_islem = Islem(
            id=yeni_id_olustur(mevcut_kayitlar),
            tutar=tutar,
            tarih=tarih,
            aciklama=aciklama,
            tip="gider",
        )
        giderler.append(yeni_islem)
        print(f"  [+] Gider başarıyla eklendi: {yeni_islem}")
        return yeni_islem
    except Exception as hata:
        print(f"  [!] Gider eklenirken beklenmeyen bir hata oluştu: {hata}")
        return None


def islemleri_listele(gelirler, giderler):
    """Tüm gelir ve gider kayıtlarını düzenli bir biçimde ekrana yazdırır.

    Kayıtlar tarihe göre kronolojik olarak sıralanır.
    """
    print("\n" + "=" * 72)
    print("                          TÜM İŞLEM KAYITLARI")
    print("=" * 72)

    tum_islemler = gelirler + giderler
    if not tum_islemler:
        print("  Henüz kayıtlı bir işlem bulunmuyor.")
        print("=" * 72)
        return

    # YYYY-MM-DD biçimindeki metin tarih, alfabetik sıralamada kronolojiktir.
    for islem in sorted(tum_islemler, key=lambda i: (i.tarih, i.tip, i.id)):
        print("  " + str(islem))

    print("-" * 72)
    print(f"  Toplam {len(gelirler)} gelir ve {len(giderler)} gider kaydı listelendi.")
    print("=" * 72)


def islem_sil(gelirler, giderler, id):
    """Verilen ID'ye sahip işlemi bularak ilgili listeden siler.

    Önce gelir listesi, ardından gider listesi taranır ve ilk eşleşen kayıt
    silinir.

    Parametreler
    ------------
    gelirler, giderler : list[Islem]
        İçinden silme yapılacak listeler.
    id : int
        Silinecek işlemin kimlik numarası.

    Dönüş
    -----
    bool
        Silme başarılıysa True, kayıt bulunamazsa False.
    """
    for liste, etiket in ((gelirler, "gelir"), (giderler, "gider")):
        for islem in liste:
            if islem.id == id:
                liste.remove(islem)
                print(f"  [-] {etiket.upper()} kaydı silindi: {islem}")
                return True
    print(f"  [!] {id} numaralı işlem bulunamadı.")
    return False
