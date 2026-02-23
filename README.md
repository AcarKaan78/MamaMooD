<p align="center">
  <img src="static/images/mascot.png" alt="MamaMooD Mascot" width="280">
</p>

<h1 align="center">MamaMooD</h1>

<p align="center">
  <strong>Yeni Nesil Anne Adayları İcin Psikolojik Destek Portali</strong><br>
  <em>Gebelik Yolculugunuzda Yalniz Degilsiniz!</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/flask-3.x-lightgrey?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/database-SQLite-green?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/TUBITAK-2209--A-red" alt="TUBITAK 2209-A">
  <img src="https://img.shields.io/badge/license-Academic%20Research-purple" alt="License">
</p>

---

## Hakkinda

**MamaMooD**, TUBITAK 2209-A programi kapsaminda Saglik Bilimleri Universitesi bunyesinde gelistirilen, gebelik donemindeki kadinlarin stres ve depresyon duzeylerini online egitim yoluyla azaltmayi hedefleyen bir web platformudur.

Arastirmalar, anne adaylarinin yaklasik **%20'sinin** gebelik surecinde depresif semptomlar yasadigini gostermektedir. MamaMooD, bu hassas donemde anne adaylarina evlerinin konforunda, uzman hekimler ve psikologlar tarafindan hazirlanan video icerikleriyle psikolojik destek sunmaktadir.

## Ozellikler

| Ozellik | Aciklama |
|---------|----------|
| **Video Platformu** | 38+ uzman icerigi, trimester bazli kategorilendirme |
| **Sirasal Ilerleme** | Kullanici onceki videoyu tamamlamadan sonrakine gecemez |
| **Izleme Takibi** | Sunucu tarafli dogrulama ile gercek izleme suresi kontrolu (%75 kural) |
| **Kaldigi Yerden Devam** | Video izleme sureci kaydedilir, kaldigi yerden devam edilir |
| **Admin Paneli** | Kullanici yonetimi, ilerleme istatistikleri, toplam izleme suresi |
| **Responsive Tasarim** | Mobil, tablet ve masaustu uyumlu modern arayuz |
| **Hakkinda Sayfasi** | Proje ekibi, danisman bilgileri ve proje detaylari |

## Egitim Modulleri

| Kategori | Video Sayisi | Konu |
|----------|:------------:|------|
| 1. Trimester | 5 | Yoga, beslenme, belirtiler, egzersiz, SSS |
| 2. Trimester | 4 | Genel bakis, yoga, guclendirme, esneme |
| Dogum Hazirligi | 5 | Dogum plani, hastane cantasi, nefes, pozisyonlar |
| Beslenme | 1 | Saglikli tarifler ve besin onerileri |
| Saglik | 6 | Ruh sagligi, uyku, cilt bakimi, meditasyon, kilo |
| 3. Trimester | 11 | Yoga, egzersiz, nefes, uyku, beslenme, belirtiler |
| Dogum Sonrasi | 3 | Iyilesme, emzirme, egzersiz |
| Bebek Bakimi | 6 | Yenidogan bakimi, banyo, masaj, uyku, giydirme |

> Toplam: **41 video** | Toplam sure: ~**100+ dakika** uzman icerigi

## Teknoloji

```
Backend:   Python 3.10+ / Flask
Database:  SQLite (dosya tabanli, sunucu gerektirmez)
Frontend:  HTML5 / CSS3 / Vanilla JavaScript
Fontlar:   Playfair Display + Nunito (Google Fonts)
```

## Proje Yapisi

```
mamamood/
  app.py                  # Ana Flask uygulamasi ve route'lar
  config.py               # Yapilandirma dosyasi
  requirements.txt        # Python bagimliliklari
  mamamood.db             # SQLite veritabani (otomatik olusur)
  templates/
    base.html             # Ana sablon (navbar, footer)
    home.html             # Ana sayfa
    hakkinda.html         # Hakkinda sayfasi
    login.html            # Giris sayfasi
    video_list.html       # Video listesi
    video_watch.html      # Video izleme sayfasi
    admin.html            # Admin paneli
  static/
    css/style.css         # Tum stiller
    js/main.js            # JavaScript islevleri
    images/               # Logo ve maskot
    videos/               # Video dosyalari (.mp4)
    thumbnails/           # Video onizleme gorselleri (.jpg)
  database/
    init_db.py            # Veritabani baslatma scripti
```

## Kurulum

### Gereksinimler
- Python 3.10 veya ustu
- pip (Python paket yoneticisi)

### Adimlar

**1. Repoyu klonlayin:**
```bash
git clone https://github.com/AcarKaan78/MamaMooD.git
cd MamaMooD
```

**2. Bagimliliklari yukleyin:**
```bash
pip install -r requirements.txt
```

**3. Video dosyalarini ekleyin:**
```
static/videos/ klasorune .mp4 dosyalarini yerlestirin
static/thumbnails/ klasorune .jpg onizleme gorsellerini yerlestirin
```

**4. Uygulamayi calistirin:**
```bash
python app.py
```

**5. Tarayicida acin:**
```
http://localhost:5000
```

> Veritabani ilk calistirmada otomatik olarak olusturulur ve ornek verilerle doldurulur.

## Kullanim

### Kullanici Girisi
| Rol | Kullanici Adi | Sifre |
|-----|:-------------:|:-----:|
| Admin | `admin` | `admin123` |
| Demo | `demo` | `demo123` |
| Kullanici | `ayse` | `sifre123` |
| Kullanici | `elif` | `sifre123` |

### Sayfalar
- **/** — Ana sayfa (tanitim)
- **/hakkinda** — Proje hakkinda, ekip bilgileri
- **/login** — Kullanici girisi
- **/videos** — Video listesi (giris gerekli)
- **/watch/\<id\>** — Video izleme (giris gerekli)
- **/admin** — Admin paneli (admin girisi gerekli)

## Proje Ekibi

| Isim | Rol | Kurum |
|------|-----|-------|
| **Sevda Rezaei** | Proje Yurutucusu | Saglik Bilimleri Uni. - Hemsirelik |
| **Rumeysa Cakir** | Proje Arastirmacisi | Ankara Uni. - Psikoloji |
| **Didem Sezer** | Proje Arastirmacisi | Ankara Uni. - Psikoloji |

### Danisman ve Destekci

| Isim | Rol |
|------|-----|
| **Prof. Dr. Kazim Emre Karasahin** | Proje Danismani — Kadin Hastaliklari ve Dogum Uzmani, Saglik Bilimleri Uni. |
| **Uzm. Psikiyatrist Dr. Emel Koyuncu Kutuk** | Proje Destekcisi — Psikiyatri Uzmani, Toplum Ruh Sagligi |

## Destekleyen Kurum

<p align="center">
  <strong>TUBITAK 2209-A Universite Ogrencileri Arastirma Projeleri Destekleme Programi</strong><br>
  Saglik Bilimleri Universitesi
</p>

---

<p align="center">
  Sevgiyle yapildi | MamaMooD 2025
</p>
