document.addEventListener("DOMContentLoaded", function () {
    const balanceCanvas = document.querySelectorAll('.balance-line');

    balanceCanvas.forEach(canvas => {
        const balanceMonths = JSON.parse(canvas.dataset.labels).reverse();
        const balanceData = JSON.parse(canvas.dataset.values).reverse();

        new Chart(canvas, {
            type: 'line',
            data: {
                labels: balanceMonths,
                datasets: [{
                    label: 'Balance',
                    data: balanceData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.3,
                    fill: true,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: 'rgba(75, 192, 192, 1)',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#fff' },
                        display: false
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#fff' },
                        grid: { color: '#444' }
                    },
                    y: {
                        ticks: { color: '#fff' },
                        grid: { color: '#444' }
                    }
                }
            }
        });
    })
});
