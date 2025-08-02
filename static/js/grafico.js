const ctx = document.getElementById('grafico').getContext('2d');
let grafico;

async function atualizarGrafico() {
    const res = await fetch('/api/precos?key=12345');
    const data = await res.json();

    const labels = Object.keys(data);
    const valores = labels.map(k => data[k].usd);

    if (grafico) {
        grafico.data.labels = labels;
        grafico.data.datasets[0].data = valores;
        grafico.update();
    } else {
        grafico = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Preço em USD',
                    data: valores,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}

atualizarGrafico();