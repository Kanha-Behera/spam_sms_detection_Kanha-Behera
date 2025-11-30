document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('checkBtn');
    const input = document.getElementById('smsInput');
    const result = document.getElementById('result');

    async function checkSpam() {
        const text = input.value.trim();
        result.className = '';
        result.textContent = '';

        if (!text) {
            result.textContent = 'Please enter a message to check.';
            result.classList.add('result-error');
            return;
        }

        if (text.length < 5) {
            result.textContent = 'Message too short. Please enter at least 5 characters.';
            result.classList.add('result-error');
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Checking...';

        try {
            const res = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            if (!res.ok) {
                const textErr = await res.text().catch(() => '');
                result.textContent = `Server error: ${res.status} ${res.statusText} ${textErr}`;
                return;
            }

            const data = await res.json();

            if (data.result === 'Spam') {
                result.classList.add('result-spam');
                result.textContent = '🚨 Spam Message Detected!';
            } else {
                result.classList.add('result-ham');
                result.textContent = '✔️ Ham (Safe Message)';
            }
        } catch (err) {
            result.textContent = 'Network error: Could not reach the backend. Is the server running?';
            console.error(err);
        } finally {
            btn.disabled = false;
            btn.textContent = 'Check';
        }
    }

    btn.addEventListener('click', checkSpam);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            checkSpam();
        }
    });
});
