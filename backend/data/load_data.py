import csv
import os
import sys

import django

sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodgram.settings")
django.setup()


def load_all_data(func):

    from recipes.models import Ingredient

    func('ingredients.csv', Ingredient)
    print('\nИнгридиенты загружены\n')


@load_all_data
def load_table_from_csv(file_name, model):
    from recipes.models import Ingredient
    file = open(file_name, 'r', encoding='utf-8')
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        Ingredient.objects.create(
            name=row[0], measurement_unit=row[1])
        print(f'{row}')