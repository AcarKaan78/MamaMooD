"""
Mamamood — Hamile kadınlar için video platformu
"""

import sqlite3
import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_from_directory, jsonify
)
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    """Get a database connection with Row factory."""
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed data on startup."""
    conn = sqlite3.connect(config.DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            thumbnail TEXT,
            category TEXT DEFAULT 'Genel',
            duration TEXT,
            duration_seconds INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watch_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_id INTEGER NOT NULL,
            watched_seconds REAL DEFAULT 0,
            time_spent REAL DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            UNIQUE(user_id, video_id)
        )
    ''')

    # Seed users
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        users = [
            ('admin', 'admin123', 1),
            ('demo', 'demo123', 0),
            ('ayse', 'sifre123', 0),
            ('elif', 'sifre123', 0),
        ]
        cursor.executemany('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', users)

    # Seed videos
    cursor.execute('SELECT COUNT(*) FROM videos')
    if cursor.fetchone()[0] == 0:
        videos = [
            # --- 1. Trimester (1.1 - 1.5) ---
            ("Doğum Öncesi Yoga — İlk Trimester",
             "İlk trimesteriniz için mükemmel, nazik yoga pozları. Vücudunuz bu güzel yolculuğa başlarken esnek ve rahat kalın.",
             "1.1.mp4", "1.1.jpg", "1. Trimester", "6:36", 396),
            ("İlk Trimester Beslenme Rehberi",
             "İlk üç ayda hangi besinlere öncelik vermelisiniz? Sağlıklı bir başlangıç için beslenme önerileri.",
             "1.2.mp4", "1.2.jpg", "1. Trimester", "5:09", 309),
            ("Erken Dönem Belirtileri ve Öneriler",
             "İlk trimesterde yaşanan yaygın belirtiler ve bunlarla başa çıkma yolları.",
             "1.3.mp4", "1.3.jpg", "1. Trimester", "6:22", 382),
            ("İlk Trimester Egzersiz Rutini",
             "İlk üç ay için güvenli ve etkili egzersiz hareketleri.",
             "1.4.mp4", "1.4.jpg", "1. Trimester", "4:40", 280),
            ("İlk Trimester Sık Sorulan Sorular",
             "Hamileliğin ilk döneminde en çok merak edilen soruların yanıtları.",
             "1.5.mp4", "1.5.jpg", "1. Trimester", "1:11", 71),
            # --- 2. Trimester — Giriş (2) ---
            ("İkinci Trimester Genel Bakış",
             "İkinci trimesterde vücudunuzda neler değişiyor? Bilmeniz gereken her şey.",
             "2.mp4", "2.jpg", "2. Trimester", "5:41", 341),
            # --- Doğum Hazırlığı (3.1 - 3.5) ---
            ("Doğum Planı Hazırlama",
             "Doğum planınızı nasıl oluşturabilirsiniz? Adım adım rehber.",
             "3.1.mp4", "3.1.jpg", "Doğum Hazırlığı", "1:22", 82),
            ("Hastane Çantası Hazırlığı",
             "Doğum için hastane çantanızda neler olmalı? Eksiksiz kontrol listesi.",
             "3.2.mp4", "3.2.jpg", "Doğum Hazırlığı", "1:22", 82),
            ("Doğum İçin Nefes Egzersizleri",
             "Doğum sırasında sakin ve odaklanmış kalmanıza yardımcı olacak temel nefes tekniklerini öğrenin.",
             "3.3.mp4", "3.3.jpg", "Doğum Hazırlığı", "2:30", 150),
            ("Doğum Pozisyonları",
             "Doğum sırasında deneyebileceğiniz farklı pozisyonlar ve faydaları.",
             "3.4.mp4", "3.4.jpg", "Doğum Hazırlığı", "1:34", 94),
            ("Eşinizle Doğuma Hazırlık",
             "Partnerinizle birlikte doğum sürecine nasıl hazırlanabilirsiniz?",
             "3.5.mp4", "3.5.jpg", "Doğum Hazırlığı", "2:45", 165),
            # --- 2. Trimester — Egzersizler (4.1 - 4.3) ---
            ("İkinci Trimester Yoga Serisi",
             "Büyüyen karnınıza uygun, ikinci trimestere özel yoga pozları ve esneme hareketleri.",
             "4.1.mp4", "4.1.jpg", "2. Trimester", "4:58", 298),
            ("İkinci Trimester Güçlendirme Egzersizleri",
             "Sırt ve kalça kaslarını güçlendiren, ikinci trimester için güvenli egzersizler.",
             "4.2.mp4", "4.2.jpg", "2. Trimester", "4:16", 256),
            ("İkinci Trimester Esneme Hareketleri",
             "Bel ağrısını hafifletmek ve esnekliği artırmak için ikinci trimestere özel güvenli esneme rutinleri.",
             "4.3.mp4", "4.3.jpg", "2. Trimester", "5:09", 309),
            # --- Beslenme (5) ---
            ("İki Kişilik Sağlıklı Yemekler",
             "Bebeğinizin gelişimini destekleyen ve sizi enerjik tutan besleyici ve lezzetli tarifler.",
             "5.mp4", "5.jpg", "Beslenme", "5:11", 311),
            # --- Sağlık (6.1 - 6.6) ---
            ("Hamilelikte Ruh Sağlığı",
             "Hamilelikte duygusal değişimler ve ruh sağlığınızı korumak için öneriler.",
             "6.1.mp4", "6.1.jpg", "Sağlık", "1:37", 97),
            ("Hamilelikte Uyku Düzeni",
             "Rahat bir uyku için pozisyon önerileri ve uyku hijyeni ipuçları.",
             "6.2.mp4", "6.2.jpg", "Sağlık", "2:44", 164),
            ("Hamilelikte Cilt Bakımı",
             "Hamilelik döneminde cilt değişimleri ve güvenli bakım rutinleri.",
             "6.3.mp4", "6.3.jpg", "Sağlık", "1:59", 119),
            ("Hamilelikte Bel ve Sırt Ağrısı",
             "Bel ve sırt ağrılarını hafifletmek için pratik egzersizler ve öneriler.",
             "6.4.mp4", "6.4.jpg", "Sağlık", "1:38", 98),
            ("Anne Adayları İçin Meditasyon",
             "Huzur arayan hamile kadınlar için özel olarak tasarlanmış sakinleştirici rehberli meditasyon seansı.",
             "6.5.mp4", "6.5.jpg", "Sağlık", "3:04", 184),
            ("Hamilelikte Sağlıklı Kilo Yönetimi",
             "Hamilelik süresince sağlıklı kilo almak için beslenme ve hareket önerileri.",
             "6.6.mp4", "6.6.jpg", "Sağlık", "1:24", 84),
            # --- 3. Trimester (7.1 - 7.11) ---
            ("Üçüncü Trimestere Hoş Geldiniz",
             "Son trimesterde neler beklemeniz gerektiği ve hazırlık ipuçları.",
             "7.1.mp4", "7.1.jpg", "3. Trimester", "2:22", 142),
            ("Üçüncü Trimester Yoga",
             "Son trimester için güvenli ve rahatlatıcı yoga hareketleri.",
             "7.2.mp4", "7.2.jpg", "3. Trimester", "2:19", 139),
            ("Doğuma Hazır Vücut Egzersizleri",
             "Doğum için vücudunuzu hazırlayan güçlendirme ve esneme hareketleri.",
             "7.3.mp4", "7.3.jpg", "3. Trimester", "2:17", 137),
            ("Üçüncü Trimester Nefes Çalışmaları",
             "Son trimester ve doğum için nefes teknikleri ve gevşeme egzersizleri.",
             "7.4.mp4", "7.4.jpg", "3. Trimester", "2:35", 155),
            ("Pelvik Taban Egzersizleri",
             "Pelvik taban kaslarını güçlendiren Kegel egzersizleri ve daha fazlası.",
             "7.5.mp4", "7.5.jpg", "3. Trimester", "2:37", 157),
            ("Üçüncü Trimester Uyku Pozisyonları",
             "Büyük karnınızla rahat uyumak için en iyi pozisyonlar ve yastık kullanımı.",
             "7.6.mp4", "7.6.jpg", "3. Trimester", "2:40", 160),
            ("Son Haftalarda Beslenme",
             "Doğuma yakın dönemde enerji ve dayanıklılık için beslenme önerileri.",
             "7.7.mp4", "7.7.jpg", "3. Trimester", "2:51", 171),
            ("Doğum Belirtilerini Tanıma",
             "Gerçek doğum belirtilerini nasıl anlarsınız? Ne zaman hastaneye gitmelisiniz?",
             "7.8.mp4", "7.8.jpg", "3. Trimester", "3:00", 180),
            ("Bebeğinizin Gelişimi — Son Dönem",
             "Üçüncü trimesterde bebeğiniz nasıl gelişiyor? Hafta hafta gelişim rehberi.",
             "7.9.mp4", "7.9.jpg", "3. Trimester", "2:56", 176),
            ("Üçüncü Trimester Rahatlama Teknikleri",
             "Son trimesterde stres ve gerginlikle başa çıkmak için rahatlama yöntemleri.",
             "7.10.mp4", "7.10.jpg", "3. Trimester", "3:03", 183),
            ("Doğum Öncesi Son Kontrol Listesi",
             "Doğumdan önce yapmanız gereken son hazırlıkların eksiksiz listesi.",
             "7.11.mp4", "7.11.jpg", "3. Trimester", "3:31", 211),
            # --- Doğum Sonrası (8.1 - 8.3) ---
            ("Doğum Sonrası İyileşme Rehberi",
             "Doğum sonrası neler beklemeniz gerektiği ve iyileşme sürecinde kendinize nasıl bakacağınız.",
             "8.1.mp4", "8.1.jpg", "Doğum Sonrası", "3:51", 231),
            ("Emzirme Rehberi",
             "Emzirmeye başlangıç, doğru pozisyonlar ve sık karşılaşılan sorunların çözümleri.",
             "8.2.mp4", "8.2.jpg", "Doğum Sonrası", "0:54", 54),
            ("Doğum Sonrası Egzersizler",
             "Doğum sonrası vücudunuzu yeniden güçlendirmek için güvenli egzersiz programı.",
             "8.3.mp4", "8.3.jpg", "Doğum Sonrası", "3:46", 226),
            # --- Bebek Bakımı (9.1 - 9.6) ---
            ("Yenidoğan Bakımı Temelleri",
             "İlk günlerde bebeğinize nasıl bakmalısınız? Temel bilgiler ve ipuçları.",
             "9.1.mp4", "9.1.jpg", "Bebek Bakımı", "1:37", 97),
            ("Bebek Banyosu Nasıl Yaptırılır",
             "Yenidoğan bebeğinizi güvenle yıkamak için adım adım rehber.",
             "9.2.mp4", "9.2.jpg", "Bebek Bakımı", "3:24", 204),
            ("Bebek Masajı Teknikleri",
             "Bebeğinizle bağ kuran ve rahatlamasını sağlayan masaj teknikleri.",
             "9.3.mp4", "9.3.jpg", "Bebek Bakımı", "1:33", 93),
            ("Bebeğinizin Uyku Düzeni",
             "Güvenli uyku ortamı oluşturma ve sağlıklı uyku alışkanlıkları kazandırma.",
             "9.4.mp4", "9.4.jpg", "Bebek Bakımı", "1:39", 99),
            ("Bebek Giysileri ve Giydirme",
             "Bebeğinizi mevsime uygun giydirme ve kıyafet seçimi ipuçları.",
             "9.5.mp4", "9.5.jpg", "Bebek Bakımı", "1:16", 76),
            ("Bebeğinizle İlk Hafta",
             "Hastaneden eve döndükten sonra ilk hafta neler yapmalısınız?",
             "9.6.mp4", "9.6.jpg", "Bebek Bakımı", "1:19", 79),
        ]
        cursor.executemany(
            'INSERT INTO videos (title, description, filename, thumbnail, category, duration, duration_seconds) VALUES (?, ?, ?, ?, ?, ?, ?)',
            videos
        )

    conn.commit()
    conn.close()


# Run DB init on import
init_db()


# ---------------------------------------------------------------------------
# Auth decorator
# ---------------------------------------------------------------------------

def login_required(f):
    """Redirect to login if user is not authenticated."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Redirect to home if user is not admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Bu sayfaya erişim yetkiniz yok.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hakkinda')
def hakkinda():
    return render_template('hakkinda.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash(f"Tekrar hoş geldiniz, {user['username']}!", 'success')
            if user['is_admin']:
                return redirect(url_for('admin_panel'))
            return redirect(url_for('video_list'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('home'))


def get_first_unwatched(db, user_id):
    """Return the first video (by id) that the user has NOT completed, or None if all done."""
    row = db.execute('''
        SELECT v.* FROM videos v
        LEFT JOIN watch_progress wp ON wp.video_id = v.id AND wp.user_id = ?
        WHERE COALESCE(wp.completed, 0) = 0
        ORDER BY v.id ASC LIMIT 1
    ''', (user_id,)).fetchone()
    return row


@app.route('/videos')
@login_required
def video_list():
    db = get_db()
    videos = db.execute('SELECT * FROM videos ORDER BY id ASC').fetchall()

    # Get set of completed video IDs for this user
    completed_rows = db.execute(
        'SELECT video_id FROM watch_progress WHERE user_id = ? AND completed = 1',
        (session['user_id'],)
    ).fetchall()
    completed_ids = {row['video_id'] for row in completed_rows}

    # First unwatched video (this is the one they should watch next)
    first_unwatched = get_first_unwatched(db, session['user_id'])
    first_unwatched_id = first_unwatched['id'] if first_unwatched else None

    db.close()

    return render_template(
        'video_list.html',
        videos=videos,
        completed_ids=completed_ids,
        first_unwatched_id=first_unwatched_id
    )


@app.route('/watch/<int:video_id>')
@login_required
def video_watch(video_id):
    db = get_db()
    video = db.execute('SELECT * FROM videos WHERE id = ?', (video_id,)).fetchone()

    if not video:
        db.close()
        flash('Video bulunamadı.', 'error')
        return redirect(url_for('video_list'))

    # Check lock: user must complete all prior videos first
    is_locked = False
    required_video = None
    first_unwatched = get_first_unwatched(db, session['user_id'])
    if first_unwatched and first_unwatched['id'] < video_id:
        is_locked = True
        required_video = first_unwatched

    # Get next video (next by id, or wrap to first)
    next_video = db.execute(
        'SELECT * FROM videos WHERE id > ? ORDER BY id ASC LIMIT 1',
        (video_id,)
    ).fetchone()
    if not next_video:
        next_video = db.execute(
            'SELECT * FROM videos ORDER BY id ASC LIMIT 1'
        ).fetchone()
        if next_video and next_video['id'] == video_id:
            next_video = None

    # Get current progress for resume + check if already completed
    progress = db.execute(
        'SELECT watched_seconds, completed FROM watch_progress WHERE user_id = ? AND video_id = ?',
        (session['user_id'], video_id)
    ).fetchone()
    resume_time = progress['watched_seconds'] if progress else 0
    is_current_completed = bool(progress and progress['completed'])

    db.close()

    return render_template(
        'video_watch.html',
        video=video,
        next_video=next_video,
        is_locked=is_locked,
        required_video=required_video,
        resume_time=resume_time,
        is_current_completed=is_current_completed
    )


@app.route('/serve_video/<filename>')
@login_required
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    """Update watch progress for current user. Called by JS during playback."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    video_id = data.get('video_id')
    watched_seconds = data.get('current_time', 0)
    time_spent = data.get('time_spent', 0)
    wants_complete = data.get('completed', False)

    db = get_db()

    # Server-side validation: only allow completion if time_spent >= 75% of video duration
    completed = 0
    if wants_complete:
        video = db.execute('SELECT duration_seconds FROM videos WHERE id = ?', (video_id,)).fetchone()
        if video and video['duration_seconds'] > 0:
            required = video['duration_seconds'] * 0.75
            if time_spent >= required:
                completed = 1
            # else: reject completion silently, just save progress
        else:
            # No duration data — allow completion as fallback
            completed = 1

    db.execute('''
        INSERT INTO watch_progress (user_id, video_id, watched_seconds, time_spent, completed)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, video_id) DO UPDATE SET
            watched_seconds = MAX(watch_progress.watched_seconds, excluded.watched_seconds),
            time_spent = MAX(watch_progress.time_spent, excluded.time_spent),
            completed = MAX(watch_progress.completed, excluded.completed)
    ''', (session['user_id'], video_id, watched_seconds, time_spent, completed))
    db.commit()
    db.close()

    return jsonify({'ok': True, 'completed': bool(completed)})


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.route('/admin')
@admin_required
def admin_panel():
    db = get_db()

    # All users (exclude admin from stats display if desired, but show all)
    users = db.execute('SELECT * FROM users ORDER BY id ASC').fetchall()

    # Total video count
    total_videos = db.execute('SELECT COUNT(*) as cnt FROM videos').fetchone()['cnt']

    # Per-user stats
    user_stats = []
    for user in users:
        stats = db.execute('''
            SELECT
                COUNT(CASE WHEN completed = 1 THEN 1 END) as completed_count,
                COALESCE(SUM(time_spent), 0) as total_time
            FROM watch_progress WHERE user_id = ?
        ''', (user['id'],)).fetchone()

        user_stats.append({
            'id': user['id'],
            'username': user['username'],
            'password': user['password'],
            'is_admin': user['is_admin'],
            'created_at': user['created_at'],
            'completed_count': stats['completed_count'],
            'total_time': stats['total_time'],
        })

    db.close()

    return render_template(
        'admin.html',
        user_stats=user_stats,
        total_videos=total_videos
    )


@app.route('/admin/create-user', methods=['POST'])
@admin_required
def admin_create_user():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        flash('Kullanıcı adı ve şifre gereklidir.', 'error')
        return redirect(url_for('admin_panel'))

    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        flash(f"'{username}' kullanıcısı başarıyla oluşturuldu.", 'success')
    except sqlite3.IntegrityError:
        flash(f"'{username}' kullanıcı adı zaten mevcut.", 'error')
    finally:
        db.close()

    return redirect(url_for('admin_panel'))


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
