import pandas as pd  # Asegurarse de importar pandas

class Pokemon:
    def __init__(self, data):
        self.id = data['#']
        self.name = data['Name']
        self.type1 = data['Type 1']
        self.type2 = data['Type 2'] if pd.notnull(data['Type 2']) else None
        self.total = data['Total']
        self.hp = data['HP']
        self.attack = data['Attack']
        self.defense = data['Defense']
        self.sp_atk = data['Sp. Atk']
        self.sp_def = data['Sp. Def']
        self.speed = data['Speed']
        self.generation = data['Generation']
        self.legendary = data['Legendary']

    def to_dict(self):
        return {
            '#': self.id,
            'Name': self.name,
            'Type 1': self.type1,
            'Type 2': self.type2,
            'Total': self.total,
            'HP': self.hp,
            'Attack': self.attack,
            'Defense': self.defense,
            'Sp. Atk': self.sp_atk,
            'Sp. Def': self.sp_def,
            'Speed': self.speed,
            'Generation': self.generation,
            'Legendary': self.legendary
        }

class PokemonCollection:
    def __init__(self, pokemon_list):
        self.pokemons = [Pokemon(p) for p in pokemon_list]

    def filter_pokemon(self, filters):
        filtered = self.pokemons

        for key, value in filters.items():
            if key == 'name':
                filtered = [p for p in filtered if value.lower() in p.name.lower()]
            elif key == 'type':
                filtered = [
                    p for p in filtered
                    if p.type1.lower() == value.lower() or 
                       (p.type2 and p.type2.lower() == value.lower())
                ]
            elif key == 'generation':
                filtered = [p for p in filtered if str(p.generation) == value]
            elif key == 'legendary':
                filtered = [p for p in filtered if str(p.legendary).lower() == value.lower()]
            elif key == 'stat_min':
                stat, min_val = value
                filtered = [p for p in filtered if getattr(p, stat) >= int(min_val)]

        return [p.to_dict() for p in filtered]
