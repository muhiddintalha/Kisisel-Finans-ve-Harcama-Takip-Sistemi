# 📦 Teslim Rehberi (GitHub + ALMS)

Bu rehber, projeyi şartnameye uygun biçimde **GitHub'a yüklemen** ve **ALMS'ye
teslim etmen** için adım adım hazırlanmıştır. Komutları sırayla kopyalayıp
çalıştırman yeterli.

---

## 1. Hazırlık

Bilgisayarında **Git** kurulu olmalı (`git --version` ile kontrol et) ve bir
**GitHub hesabın** olmalı. Projeyi bir klasöre çıkar ve o klasörde bir terminal aç:

```bash
cd Muhiddin_Talha_Yilmaz_24083002_BGT
```

---

## 2. GitHub'da Private Repo Oluştur

1. GitHub'a gir → sağ üstten **New repository**.
2. **Repository name:** `24083002-MuhiddinTalhaYilmaz-PythonProje`
3. **Visibility:** **Private (Gizli)** ✅ *(şartname zorunluluğu)*
4. "Add a README" / ".gitignore" / "license" seçeneklerini **işaretleme**
   (projede zaten mevcutlar).
5. **Create repository** de ve açılan sayfadaki repo adresini (HTTPS) kopyala.

---

## 3. Git Geçmişini Oluştur — En Az 4 Commit (Checkpoint)

Şartname **en az 4 farklı aşamada, açıklayıcı commit** ister. Aşağıdaki komutlar,
projeyi mantıklı aşamalara bölerek tam olarak bunu yapar:

```bash
git init
git branch -M main

# ── Commit 1: Proje iskeleti ve OOP veri modeli ───────────────────────
git add finans_modeli.py utils.py .gitignore requirements.txt
git commit -m "Adim 1: Proje iskeleti, Islem sinifi (OOP) ve yardimci fonksiyonlar"

# ── Commit 2: İşlem yönetimi ve dosya (CSV/Excel) işlemleri ────────────
git add islem_yonetimi.py dosya_islemleri.py
git commit -m "Adim 2: Gelir/gider islemleri ve CSV/Excel dosya islemleri"

# ── Commit 3: Analiz, görselleştirme ve ana program ───────────────────
git add analiz.py gorsellestirme.py main.py ornek_cikti_olustur.py
git commit -m "Adim 3: Pandas/NumPy analizleri, grafikler ve ana menu (main.py)"

# ── Commit 4: Çıktılar, web arayüzü ve dokümantasyon ──────────────────
git add veriler.csv ciktilar/ docs/ README.md TESLIM_REHBERI.md
git commit -m "Adim 4: Ornek ciktilar (CSV/Excel/grafik), web arayuzu ve README"
```

> 💡 Commit mesajlarında Türkçe çizgili harfler yerine sade harfler (i, s, c)
> kullanmak, bazı terminallerde kodlama sorunlarını önler. İçerik dosyalarında
> ise tam Türkçe karakterler korunmuştur.

---

## 4. Repo'ya Gönder (Push)

`<REPO-ADRESI>` kısmını 2. adımda kopyaladığın adresle değiştir:

```bash
git remote add origin <REPO-ADRESI>
git push -u origin main
```

---

## 5. Öğretim Elemanını Collaborator Olarak Ekle (Zorunlu)

1. Repo sayfasında **Settings → Collaborators** (veya *Collaborators and teams*).
2. **Add people** → kullanıcı adı: **`tohid.yousefi`**
3. Davet et ve onay bekle.

---

## 6. (Ekstra) Web Arayüzünü Canlı Yayınla — Paylaşılabilir Link

Şık web arayüzünü "internet sitesi gibi" paylaşmak için **GitHub Pages** kullanılır.

> ⚠️ **Önemli:** Ücretsiz GitHub hesaplarında **Pages yalnızca public (herkese
> açık) repolarda** yayınlanabilir. Ödev reposu ise **private** olmak zorundadır.
> Bu yüzden iki seçeneğin var:

### Seçenek A — Ayrı bir public repo (önerilen)
1. Yeni bir **public** repo oluştur: ör. `finans-takip-web`.
2. Sadece `docs/index.html` dosyasını bu repoya `index.html` olarak yükle.
3. **Settings → Pages → Branch: `main` / (root)** seç → **Save**.
4. Birkaç dakika sonra link hazır olur:
   `https://<kullanici-adi>.github.io/finans-takip-web/`

### Seçenek B — Sadece yerelde çalıştır
`docs/index.html` dosyasına çift tıklayarak tarayıcıda doğrudan açabilirsin
(internet/sunucu gerektirmez).

Yayınladıktan sonra linki **README.md** dosyasındaki ilgili alana yapıştır,
ardından küçük bir commit at:

```bash
git add README.md
git commit -m "Adim 5: Canli web arayuzu ve repo linkleri README'ye eklendi"
git push
```

---

## 7. ALMS'ye Teslim

Şartname; **GitHub repo linki**, **.py dosyaları (zip içinde)** ve **proje
çıktılarının** ALMS'ye yüklenmesini ister. Proje modüler olduğu için **.zip**
biçiminde gönderilir.

1. `Muhiddin_Talha_Yilmaz_24083002_BGT` klasörünün tamamını **.zip** yap
   (içinde `.py` modülleri, `veriler.csv`, `ciktilar/`, `docs/`, `README.md`).
   > Bu pakette hazır bir `Muhiddin_Talha_Yilmaz_24083002_BGT.zip` dosyası da bulunur.
2. ALMS'ye:
   - ✅ `.zip` dosyasını yükle
   - ✅ Açıklama/yorum alanına **GitHub repo linkini** yapıştır
   - ✅ (varsa) canlı web arayüzü linkini de ekle

---

## ✅ Teslim Öncesi Son Kontrol Listesi

- [ ] Repo **private** ve adı `24083002-MuhiddinTalhaYilmaz-PythonProje`
- [ ] **`tohid.yousefi`** collaborator olarak eklendi
- [ ] En az **4 açıklayıcı commit** var
- [ ] `README.md` içinde **repo linki** mevcut
- [ ] `python main.py` sorunsuz çalışıyor
- [ ] `ciktilar/` içinde CSV, Excel ve 3 grafik mevcut
- [ ] ALMS'ye **.zip** + repo linki yüklendi
