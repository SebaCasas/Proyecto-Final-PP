from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
from pokemon_class import PokemonCollection
from functools import reduce
from pyDatalog import pyDatalog
import os


app = Flask(__name__)
CORS(app)

# Diccionario de relaciones de tipo
TYPE_EFFECTIVENESS = {
    'Water': ['Fire'],
    'Fire': ['Grass'],
    'Grass': ['Water']
    # Puedes añadir más relaciones aquí
}

# Cargar el dataset
df = pd.read_csv('Pokemon.csv')
pokemon_collection = PokemonCollection(df.to_dict('records'))

@app.route('/')
def index():
    # Obtener listas únicas para los filtros
    types = sorted(set(df['Type 1'].tolist() + df['Type 2'].dropna().tolist()))
    generations = sorted(df['Generation'].unique())

    return render_template('index.html', 
                         types=types,
                         generations=generations)

@app.route('/api/pokemon')
@app.route('/api/pokemon')
def get_pokemon():
    # Obtener filtros del front-end
    name = request.args.get('name', '')
    type_filter = request.args.get('type', '')
    generation = request.args.get('generation', '')
    legendary = request.args.get('legendary', '')
    min_hp = request.args.get('min_hp', None)
    min_attack = request.args.get('min_attack', None)

    # Construir filtros para aplicar
    filters = {}
    if name: filters['name'] = name
    if type_filter: filters['type'] = type_filter
    if generation: filters['generation'] = generation
    if legendary: filters['legendary'] = legendary
    if min_hp: filters['stat_min'] = ('hp', min_hp)
    if min_attack: filters['stat_min'] = ('attack', min_attack)

    # Filtrar los Pokémon
    filtered_pokemon = pokemon_collection.filter_pokemon(filters)

    return jsonify(filtered_pokemon)

    return jsonify(filtered_pokemon)

@app.route('/api/type-effectiveness/<type_name>')
def get_type_effectiveness(type_name):
    # Obtener tipos efectivos del diccionario
    effective = TYPE_EFFECTIVENESS.get(type_name, [])
    return jsonify(effective)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Agregar estas rutas a tu app.py existente

@app.route('/api/stats')
def get_stats():
    # Leer el dataset
    pokemon_data = df.to_dict('records')

    # Obtener estadísticas por tipo
    type_stats = {}
    for p in pokemon_data:
        type_stats[p['Type 1']] = type_stats.get(p['Type 1'], 0) + 1
        if pd.notnull(p['Type 2']):
            type_stats[p['Type 2']] = type_stats.get(p['Type 2'], 0) + 1

    # Obtener top 10 por diferentes estadísticas
    top_hp = df.nlargest(10, 'HP')[['Name', 'HP']].to_dict('records')
    top_attack = df.nlargest(10, 'Attack')[['Name', 'Attack']].to_dict('records')
    top_defense = df.nlargest(10, 'Defense')[['Name', 'Defense']].to_dict('records')

    return jsonify({
        'type_distribution': type_stats,
        'top_hp': top_hp,
        'top_attack': top_attack,
        'top_defense': top_defense
    })