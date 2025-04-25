document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('random-btn')
    const container = document.getElementById('random-entities')

    if (!btn || !container) return;

    btn.addEventListener('click', async function (e) {
        e.preventDefault()

        const originalText = btn.textContent
        btn.textContent = 'Loading...'
        btn.disabled = true;

        try {
            const resp = await fetch('/whale/entites')
            if (!resp.ok) throw new Error(resp.statusText)
            const { entities } = await resp.json()

            container.innerHTML = ''
            entities.forEach(val => {
                const span = document.createElement('span')
                span.className = 'entity'
                span.textContent = val
                span.onclick = () => updateEntitySubmit(val)
                container.appendChild(span)
            })
        } catch (err) {
            console.error('Failed to load entites:', err)
        } finally {
            btn.textContent = originalText
            btn.disabled = false;
        }
    })
})