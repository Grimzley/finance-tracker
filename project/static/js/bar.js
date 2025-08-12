document.addEventListener('DOMContentLoaded', function () {
    const barCanvas = document.getElementById('month-bar');
    const labels = JSON.parse(barCanvas.dataset.labels);
    const incomeData = JSON.parse(barCanvas.dataset.income).map(Number);
    const savedData = JSON.parse(barCanvas.dataset.saved).map(Number);
    const expensesData = JSON.parse(barCanvas.dataset.expenses).map(Number);

    new Chart(barCanvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Income',
                    data: incomeData,
                    backgroundColor: '#198754'
                },
                {
                    label: 'Saved',
                    data: savedData,
                    backgroundColor: '#adb5bd'
                },
                {
                    label: 'Expenses',
                    data: expensesData,
                    backgroundColor: '#dc3545'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.dataset.label}: $${ctx.formattedValue}`
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: '#444',
                        borderColor: '#888'
                    }
                },
                y: {
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: '#444',
                        borderColor: '#888'
                    }
                }
            }
        }
    });
});
