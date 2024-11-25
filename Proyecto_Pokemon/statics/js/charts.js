// Función para mostrar/ocultar secciones
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`${sectionId}-section`).classList.add('active');

    if (sectionId === 'charts') {
        loadCharts();
    }
}

// Función para cargar todos los gráficos
async function loadCharts() {
    try {
        const response = await fetch('/api/pokemon');
        const pokemon = await response.json();

        createTypeDistributionChart(pokemon);
        createTopStatsChart(pokemon, 'HP', 'topHPChart');
        createTopStatsChart(pokemon, 'Attack', 'topAttackChart');
        createTopStatsChart(pokemon, 'Defense', 'topDefenseChart');
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// Función para crear el gráfico de distribución por tipo
function createTypeDistributionChart(pokemon) {
    const typeCount = {};
    pokemon.forEach(p => {
        typeCount[p['Type 1']] = (typeCount[p['Type 1']] || 0) + 1;
        if (p['Type 2']) {
            typeCount[p['Type 2']] = (typeCount[p['Type 2']] || 0) + 1;
        }
    });

    const ctx = document.getElementById('typeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(typeCount),
            datasets: [{
                label: 'Cantidad de Pokémon por Tipo',
                data: Object.values(typeCount),
                backgroundColor: 'rgba(76, 175, 80, 0.6)',
                borderColor: 'rgba(76, 175, 80, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribución de Pokémon por Tipo'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Función para crear los gráficos de top 10 estadísticas
function createTopStatsChart(pokemon, stat, chartId) {
    const sortedPokemon = [...pokemon].sort((a, b) => b[stat] - a[stat]).slice(0, 10);

    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: sortedPokemon.map(p => p.Name),
            datasets: [{
                label: `Top 10 Pokémon por ${stat}`,
                data: sortedPokemon.map(p => p[stat]),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `Top 10 Pokémon con mayor ${stat}`
                }
            },
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Inicializar mostrando la Pokédex
document.addEventListener('DOMContentLoaded', function() {
    showSection('pokedex');
});