function renderPokemonCards(pokemon) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Limpia resultados anteriores

    pokemon.forEach(p => {
        const card = document.createElement('div');
        card.className = 'pokemon-card';

        const maxStat = 255; // Valor máximo posible para estadísticas
        const stats = {
            HP: p.HP,
            Attack: p.Attack,
            Defense: p.Defense,
            'Sp. Atk': p['Sp. Atk'],
            'Sp. Def': p['Sp. Def'],
            Speed: p.Speed
        };

        // Crear las barras de estadísticas con tooltips
        const statBars = Object.entries(stats).map(([stat, value]) => `
            <span class="stat-label">${stat}:</span>
            <div class="stat-bar">
                <div class="stat-fill" style="width: ${(value / maxStat) * 100}%;">
                    <div class="tooltip">${stat}: ${value}</div>
                </div>
            </div>
        `).join('');

        // Contenido de la tarjeta del Pokémon
        card.innerHTML = `
            <h3>#${p['#']} ${p.Name}</h3>
            <div class="stats">
                <span class="stat-label">Tipo:</span>
                <span>${p['Type 1']}${p['Type 2'] ? ' / ' + p['Type 2'] : ''}</span>

                ${statBars}

                <span class="stat-label">Generación:</span>
                <span>${p.Generation}</span>

                <span class="stat-label">Legendario:</span>
                <span>${p.Legendary ? 'Sí' : 'No'}</span>
            </div>
        `;

        resultsDiv.appendChild(card);
    });
}
