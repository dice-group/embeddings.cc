document.addEventListener('DOMContentLoaded', () => {
    const embedBtn = document.getElementById('embed-btn')
    const entityInput = document.getElementById('entity-input')
    const embedOutput = document.getElementById('embeddings-output')

    if (embedBtn && entityInput && embedOutput) {
        embedBtn.addEventListener('click', async e => {
            e.preventDefault()
            const origText = embedBtn.textContent
            embedBtn.textContent = 'Loading...'
            embedBtn.disabled = true

            try {
                const resp = await fetch('/whale/embeddings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        "Accept": 'application/json'
                    },
                    body: JSON.stringify({ entity: entityInput.value })
                })
                if (!resp.ok) throw new Error(resp.statusText)
                const { embeddings } = await resp.json()
                embedOutput.style.display = 'block'
                embedOutput.value = embeddings
            } catch (err) {
            console.error('Failed to load embeddings:', err)
            } finally {
            embedBtn.textContent = origText
            embedBtn.disabled = false
            }
        })
    }
})