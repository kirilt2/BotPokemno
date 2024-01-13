from random import randint
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.types = self.get_types()
        self.abilities = self.get_abilities()
        self.height = self.get_height()
        self.weight = self.get_weight()

        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(pokemon_url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_default']
        else:
            return "https://example.com/default_pokemon_image.png"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        else:
            return "Pikachu"

    def get_types(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            types = [t['type']['name'] for t in data['types']]
            return types
        else:
            return ["Normal"]

    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            abilities = [a['ability']['name'] for a in data['abilities']]
            return abilities
        else:
            return ["Run Away"]

    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['height']
        else:
            return 1.0

    def get_weight(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['weight']
        else:
            return 10.0

    def set_name(self, new_name):
        self.name = new_name

    def set_types(self, new_types):
        self.types = new_types

    def set_abilities(self, new_abilities):
        self.abilities = new_abilities

    def set_height(self, new_height):
        self.height = new_height

    def set_weight(self, new_weight):
        self.weight = new_weight

    def info(self):
        return f"Имя твоего покемона: {self.name}\nТипы: {', '.join(self.types)}\n" \
               f"Способности: {', '.join(self.abilities)}\nВысота: {self.height} дм\n" \
               f"Вес: {self.weight} г"

    def show_img(self):
        return self.img
