document.getElementById('studyForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const subjects = document.getElementById('subjects').value.split(',').map(s => s.trim());
    const deadlines = document.getElementById('deadlines').value.split(',').map(d => d.trim());
    const freeTime = parseFloat(document.getElementById('freeTime').value);

    fetch('/generate-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            subjects: subjects,
            deadlines: deadlines,
            freeTime: freeTime
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            const plan = data.plan.map(item => `
                <div>
                    <strong>${item.subject}</strong>: ${item.hours_per_day} hours/day, ${item.days_remaining} days remaining
                </div>
            `).join('');
            document.getElementById('result').innerHTML = `<h2>Study Plan</h2>${plan}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});