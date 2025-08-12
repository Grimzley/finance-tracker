document.addEventListener('DOMContentLoaded', function () {
    const pieCanvas = document.getElementById('budget-pie');
    const pieLabels = JSON.parse(pieCanvas.dataset.labels);
    const rawData = JSON.parse(pieCanvas.dataset.values).map(Number);

    const pieData = rawData.map(v => v === 0 ? 0.0001 : v);

    const categoryColors = [
        '#b1b1b4', // Food
        '#26a69a', // Bills
        '#5d4037', // Transportation
        '#607d8b', // Shopping
        '#ff9800', // Entertainment
        '#f44336', // Healthcare
        '#f8bbd0', // Savings
        '#17171c'  // Other
    ];

    console.log("Pie Labels:", pieLabels);
    console.log("Pie Data (Chart):", pieData);
    console.log("Raw Data (Tooltip):", rawData);

    new Chart(pieCanvas, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: categoryColors
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const total = rawData.reduce((a, b) => a + b, 0);
                            const actualValue = rawData[context.dataIndex];
                            const percentage = total > 0 ? ((actualValue / total) * 100).toFixed(1) : 0;
                            return `${context.label}: $${actualValue} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
});
