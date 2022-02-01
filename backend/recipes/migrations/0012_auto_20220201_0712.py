# Generated by Django 3.1.14 on 2022-02-01 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20220131_0118'),
    ]

    operations = [
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
    ]