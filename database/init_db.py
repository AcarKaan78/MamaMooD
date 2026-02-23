"""
Mamamood Database Initialization
Creates tables and inserts sample data.
Safe to run multiple times.
"""

import sqlite3
import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


def init_db():
    """Initialize the database with tables and sample data."""
    conn = sqlite3.connect(config.DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("[OK] users tablosu oluşturuldu.")

    # Create videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            thumbnail TEXT,
            category TEXT DEFAULT 'Genel',
            duration TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("[OK] videos tablosu oluşturuldu.")

    # Insert sample users if table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ('demo', 'demo123'),
            ('ayse', 'sifre123'),
            ('elif', 'sifre123'),
        ]
        cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', sample_users)
        print(f"[OK] {len(sample_users)} demo kullanıcı eklendi.")
    else:
        print("[BILGI] Kullanıcılar zaten mevcut, atlandı.")

    # Insert sample videos if table is empty
    cursor.execute('SELECT COUNT(*) FROM videos')
    if cursor.fetchone()[0] == 0:
        sample_videos = [
            (
                "Doğum Öncesi Yoga — İlk Trimester",
                "İlk trimesteriniz için mükemmel, nazik yoga pozları. Vücudunuz bu güzel yolculuğa başlarken esnek ve rahat kalın.",
                "1.1.mp4",
                None,
                "1. Trimester",
                "15:00"
            ),
            (
                "Doğum İçin Nefes Egzersizleri",
                "Doğum sırasında sakin ve odaklanmış kalmanıza yardımcı olacak temel nefes tekniklerini öğrenin.",
                "3.3.mp4",
                None,
                "Doğum Hazırlığı",
                "12:30"
            ),
            (
                "İki Kişilik Sağlıklı Yemekler",
                "Bebeğinizin gelişimini destekleyen ve sizi enerjik tutan besleyici ve lezzetli tarifler.",
                "5.mp4",
                None,
                "Beslenme",
                "20:00"
            ),
            (
                "İkinci Trimester Esneme Hareketleri",
                "Bel ağrısını hafifletmek ve esnekliği artırmak için ikinci trimestere özel güvenli esneme rutinleri.",
                "6.3.mp4",
                None,
                "2. Trimester",
                "18:00"
            ),
            (
                "Anne Adayları İçin Meditasyon",
                "Huzur arayan hamile kadınlar için özel olarak tasarlanmış sakinleştirici rehberli meditasyon seansı.",
                "6.5.mp4",
                None,
                "Sağlık",
                "10:00"
            ),
            (
                "Bebek Odasını Hazırlama",
                "Minik bebeğiniz için mükemmel odayı kurmaya yönelik pratik ipuçları ve yaratıcı fikirler.",
                "6.6.mp4",
                None,
                "Hazırlık",
                "25:00"
            ),
            (
                "Üçüncü Trimester Konforu",
                "Üçüncü trimesterda rahat kalmak için egzersizler, uyku pozisyonları ve günlük ipuçları.",
                "8.1.mp4",
                None,
                "3. Trimester",
                "16:00"
            ),
            (
                "Doğum Sonrası İyileşme Rehberi",
                "Doğum sonrası neler beklemeniz gerektiği ve iyileşme sürecinde kendinize nasıl bakacağınız.",
                "8.2.mp4",
                None,
                "Doğum Sonrası",
                "22:00"
            ),
        ]
        cursor.executemany(
            'INSERT INTO videos (title, description, filename, thumbnail, category, duration) VALUES (?, ?, ?, ?, ?, ?)',
            sample_videos
        )
        print(f"[OK] {len(sample_videos)} örnek video eklendi.")
    else:
        print("[BILGI] Videolar zaten mevcut, atlandı.")

    conn.commit()
    conn.close()
    print("\n[OK] Veritabanı başarıyla başlatıldı!")


if __name__ == '__main__':
    init_db()
