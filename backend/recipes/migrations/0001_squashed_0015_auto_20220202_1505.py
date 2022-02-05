# Generated by Django 3.1.14 on 2022-02-05 05:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('recipes', '0001_initial'), ('recipes', '0002_auto_20220114_0843'), ('recipes', '0003_auto_20220124_2123'), ('recipes', '0004_auto_20220127_1432'), ('recipes', '0005_auto_20220127_1434'), ('recipes', '0006_auto_20220127_1435'), ('recipes', '0007_auto_20220127_1437'), ('recipes', '0008_auto_20220127_1439'), ('recipes', '0009_auto_20220129_1249'), ('recipes', '0010_auto_20220131_0117'), ('recipes', '0011_auto_20220131_0118'), ('recipes', '0012_auto_20220201_0712'), ('recipes', '0013_auto_20220201_0715'), ('recipes', '0014_remove_recipe_ingredients'), ('recipes', '0015_auto_20220202_1505')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название продукта')),
                ('measurement_unit', models.CharField(max_length=10, verbose_name='единица измерения')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='название блюда')),
                ('image', models.ImageField(upload_to='recipes', verbose_name='изображение')),
                ('text', models.TextField(verbose_name='описание приготовления')),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Круглый ноль такой хорошенький, Но не значит ничегошеньки!')], verbose_name='время приготовления (мин)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='тег')),
                ('color', models.CharField(default='#ffffff', max_length=7, unique=True, verbose_name='цвет тега')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Из ноля каши не сваришь!')], verbose_name='количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.ingredient', verbose_name='рецепт')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепт')),
            ],
            options={
                'ordering': ['recipe'],
                'unique_together': {('ingredient', 'recipe')},
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='теги'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'unique_together': {('user', 'recipe')},
            },
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('author', 'name'), name='unique_recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'recipe')},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe',
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.ingredient', verbose_name='ингредиент'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, verbose_name='цвет тега'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user and favorite recipe not unique'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('author', 'name'), name='author and recipe name not unique'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipe and ingredient not unique'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user and recipe in shopping cart not unique'),
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'рецепт', 'verbose_name_plural': 'рецепты'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['user'], 'verbose_name': 'избранное', 'verbose_name_plural': 'избранное'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['user'], 'verbose_name': 'список покупок', 'verbose_name_plural': 'список покупок'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(verbose_name='время приготовления (мин)'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1, message='Круглый ноль такой хорошенький, Но не значит ничегошеньки!')], verbose_name='время приготовления (мин)'),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='рецепт'),
        ),
    ]
