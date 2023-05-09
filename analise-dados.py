import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribution(data, x_col, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x=x_col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_threatened_species(data, x_col, hue_col, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x=x_col, hue=hue_col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_top_species(data, x_col, y_col, hue_col, title, xlabel, ylabel, legend_title):
    plt.figure(figsize=(12, 8))
    sns.barplot(data=data, x=x_col, y=y_col, hue=hue_col, dodge=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title=legend_title)
    plt.show()


# Ler os dados
species_info = pd.read_csv('species_info.csv')
observations = pd.read_csv('observations.csv')

conservation_status_translation = {
    'Least Concern': 'Menor preocupação',
    'Near Threatened': 'Quase ameaçada',
    'Vulnerable': 'Vulnerável',
    'Endangered': 'Em perigo',
    'Critically Endangered': 'Criticamente em perigo',
    'Extinct': 'Extinto'
}

category_translation = {
    'Amphibian': 'Anfíbio',
    'Bird': 'Ave',
    'Fish': 'Peixe',
    'Mammal': 'Mamífero',
    'Nonvascular Plant': 'Planta não vascular',
    'Reptile': 'Réptil',
    'Vascular Plant': 'Planta vascular'
}

park_name_translation = {
    'Bryce National Park': 'Parque Nacional Bryce',
    'Great Smoky Mountains National Park': 'Parque Nacional das Montanhas Great Smoky',
    'Yosemite National Park': 'Parque Nacional Yosemite',
    'Yellowstone National Park': 'Parque Nacional Yellowstone'
}


# Aplicar traduções aos dados
species_info['conservation_status'] = species_info['conservation_status'].map(conservation_status_translation)
species_info['category'] = species_info['category'].map(category_translation)
observations['park_name'] = observations['park_name'].map(park_name_translation)

# Gráfico 1: Distribuição de conservation_status para os animais
plot_distribution(species_info, 'conservation_status', 'Distribuição de conservation_status para os animais',
                  'Status de Conservação', 'Contagem')

# Gráfico 2: Espécies Ameaçadas por Categoria
threatened_species = species_info[species_info['conservation_status'] != 'Menor preocupação']
plot_threatened_species(threatened_species, 'category', 'conservation_status', 'Espécies Ameaçadas por Categoria',
                        'Categoria', 'Contagem')

# Gráfico 3: Estado de Conservação por Categoria
plot_threatened_species(species_info, 'category', 'conservation_status', 'Estado de Conservação por Categoria',
                        'Categoria', 'Contagem')

# Gráfico 4: Top 5 Espécies Mais Vistas em Cada Parque
species_per_park = observations.groupby(['park_name', 'scientific_name'], as_index=False).sum()
sorted_species_per_park = species_per_park.sort_values(['park_name', 'observations'], ascending=[True, False])
top_species_per_park = sorted_species_per_park.groupby('park_name').head(5)
plot_top_species(top_species_per_park, 'park_name', 'observations', 'scientific_name',
                 'Top 5 Espécies Mais Vistas em Cada Parque', 'Parque', 'Observações', 'Espécie')
