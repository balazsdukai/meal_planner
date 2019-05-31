import pytest
from meal_planner.models import Unit, IngredientName, Ingredient, Recipe, RecepieCollection


class TestModels:
    def test_units(self):
        tbsp = Unit(name='tbsp')
        assert tbsp.name == 'tbsp'

    def test_ingredient_name(self):
        salt = IngredientName(name='salt')
        assert salt.name == 'salt'

    def test_ingredient(self):
        salt_tbsp = Ingredient(name=IngredientName(name='salt'),
                              unit=Unit(name='tbsp'),
                              quantity=1.0)
        assert salt_tbsp.quantity == 1.0
        assert salt_tbsp.name.name == 'salt'
        assert salt_tbsp.unit.name == 'tbsp'

    def test_recipe(self, dbsession):
        recipe = Recipe(name='salty soup')