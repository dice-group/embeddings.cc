document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('count');
    let running = true;
    let spinStart = 0;

    const MIN = 100_000_000;
    const MAX = 999_999_999;
    const SPIN_PERIOD = 3000;

    function easeOutQuad(t) {
        return t * (2 - t);
    }

    function parseNumber(str) {
        return Number(str.replace(/,/g, '')) || 0;
    }

    function spin() {
        if (!running) return;
        if (!spinStart) spinStart = timestamp;

        const elapsed = (timestamp - spinStart) % SPIN_PERIOD;
        const progress = elapsed / SPIN_PERIOD;
        const value = Math.floor(MIN +progress * (MAX - MIN));

        el.textContent = value.toLocaleString();
        requestAnimationFrame(spin)
    }
    requestAnimationFrame(spin)

    function animateTo(finalValue) {
        const startValue = parseNumber(el.textContent)
        const DURATION = 1000;
        const tweenStart = performance.now()

        function step(now) {
            const t = Math.min((now - tweenStart) / DURATION, 1)
            const eased = easeOutQuad(t);
            const current = Math.floor(startValue + (finalValue - startValue) * eased)
            el.textContent = current.toLocaleString()

            if (t < 1) {
                requestAnimationFrame(step)
            }
        }
        requestAnimationFrame(step)
    }

    fetch('/whale/count')
        .then(r => r.json())
        .then(data => {
            running = false;
            const real = data.count
            if (real != null) {
                animateTo(real)
            } else {
                el.textContent = 'millions of';
            }
        })
        .catch(() => {
            running = false;
            el.textContent = 'millions of'
        });
});