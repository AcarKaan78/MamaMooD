/**
 * Mamamood — Main JavaScript
 */

/* ========== Mobile Menu Toggle ========== */
function toggleMobileMenu() {
    const hamburger = document.getElementById('hamburgerBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function (e) {
    const hamburger = document.getElementById('hamburgerBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenu && mobileMenu.classList.contains('open')) {
        if (!mobileMenu.contains(e.target) && !hamburger.contains(e.target)) {
            hamburger.classList.remove('open');
            mobileMenu.classList.remove('open');
        }
    }
});

/* ========== Flash Message Auto-Dismiss ========== */
document.addEventListener('DOMContentLoaded', function () {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.classList.add('fade-out');
            setTimeout(function () {
                flash.remove();
            }, 400);
        }, 4000);
    });
});

/* ========== Scroll-triggered Animations (IntersectionObserver) ========== */
document.addEventListener('DOMContentLoaded', function () {
    const animatedElements = document.querySelectorAll('.animate-in');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        });

        animatedElements.forEach(function (el) {
            // Pause animations until element is in view
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        });
    } else {
        // Fallback: just show all elements
        animatedElements.forEach(function (el) {
            el.style.opacity = '1';
        });
    }
});


/* ========== Video Progress Tracking (real wall-clock timer, server-validated) ========== */
document.addEventListener('DOMContentLoaded', function () {
    var player = document.getElementById('mainPlayer');
    if (!player) return;

    var videoId = parseInt(player.getAttribute('data-video-id'));
    var resumeTime = parseFloat(player.getAttribute('data-resume-time')) || 0;
    var durationSeconds = parseInt(player.getAttribute('data-duration-seconds')) || 0;
    var completed = false;
    var timeSpentPlaying = 0;
    var lastPlayTime = null;
    var requiredTime = durationSeconds * 0.75;

    console.log('[Mamamood] Video ID:', videoId, '| Duration:', durationSeconds + 's', '| Required:', Math.round(requiredTime) + 's');

    // Resume from where user left off
    if (resumeTime > 0) {
        player.addEventListener('loadedmetadata', function () {
            player.currentTime = resumeTime;
        }, { once: true });
    }

    // When user presses play, start the wall-clock timer
    player.addEventListener('play', function () {
        lastPlayTime = Date.now();
    });

    // When paused, accumulate elapsed real time
    player.addEventListener('pause', function () {
        if (lastPlayTime) {
            timeSpentPlaying += (Date.now() - lastPlayTime) / 1000;
            lastPlayTime = null;
        }
    });

    // Every second: accumulate time and check if 75% reached
    setInterval(function () {
        if (!player.paused && lastPlayTime && !completed) {
            var now = Date.now();
            timeSpentPlaying += (now - lastPlayTime) / 1000;
            lastPlayTime = now;

            // Check completion
            if (requiredTime > 0 && timeSpentPlaying >= requiredTime) {
                completed = true;
                console.log('[Mamamood] 75% time reached! Sending completion...');
                sendProgress(videoId, player.currentTime, timeSpentPlaying, true, function (ok) {
                    if (ok) {
                        unlockNextVideo();
                    } else {
                        completed = false;
                    }
                });
            }
        }
    }, 1000);

    // Save position every 5 seconds
    setInterval(function () {
        if (!player.paused && !completed) {
            sendProgress(videoId, player.currentTime, timeSpentPlaying, false);
        }
    }, 5000);

    // Video ended — flush timer, try completion one more time
    player.addEventListener('ended', function () {
        if (lastPlayTime) {
            timeSpentPlaying += (Date.now() - lastPlayTime) / 1000;
            lastPlayTime = null;
        }
        if (!completed && requiredTime > 0 && timeSpentPlaying >= requiredTime) {
            completed = true;
            sendProgress(videoId, player.currentTime, timeSpentPlaying, true, function (ok) {
                if (ok) unlockNextVideo();
                else completed = false;
            });
        }
    });

    function unlockNextVideo() {
        var locked = document.getElementById('nextVideoLocked');
        var card = document.getElementById('nextVideoCard');
        if (locked) locked.style.display = 'none';
        if (card) card.style.display = 'flex';
    }

    function sendProgress(vid, currentTime, timeSpent, isCompleted, callback) {
        fetch('/api/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                video_id: vid,
                current_time: currentTime,
                time_spent: timeSpent,
                completed: isCompleted
            })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (callback) callback(data.completed);
        })
        .catch(function () {
            if (callback) callback(false);
        });
    }
});

/* ========== Smooth scroll for category bar on mobile ========== */
document.addEventListener('DOMContentLoaded', function () {
    const categoryBar = document.querySelector('.category-bar');
    if (categoryBar) {
        const activeChip = categoryBar.querySelector('.category-pill.active');
        if (activeChip) {
            // Scroll active chip into view
            setTimeout(function () {
                activeChip.scrollIntoView({
                    behavior: 'smooth',
                    inline: 'center',
                    block: 'nearest'
                });
            }, 100);
        }
    }
});
