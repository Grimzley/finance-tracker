document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('budget-radar');
    const labels = JSON.parse(canvas.dataset.labels);
    const thisMonth = JSON.parse(canvas.dataset.thisMonth);
    const lastMonth = JSON.parse(canvas.dataset.lastMonth);

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Expenses This Month',
                    data: thisMonth,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                },
                {
                    label: "Expenses Last Month",
                    data: lastMonth,
                    fill: true,
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    pointBackgroundColor: "rgba(255, 99, 132, 1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(255, 99, 132, 1)",
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#fff",
                    },
                },
            },
            scales: {
                r: {
                    angleLines: { color: '#fff' },
                    grid: { color: '#fff' },
                    ticks: { display: false },
                    pointLabels: { color: '#fff' },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
});
