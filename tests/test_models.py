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

    def test_recipe(self, data_recipes):
        for name, r in data_recipes.items():
            recipe = Recipe(name=name)
            for i,e in enumerate(r['ingredients']):
                u = e['unit'] if 'unit' in e else None
                q = e['quantity'] if 'quantity' in e else None
                recipe.ingredients.append(
                    Ingredient(name=IngredientName(name=e['name']),
                               unit=Unit(name=u),
                               quantity=q)
                )
            recipe.description = r['description']
            recipe.nr_meals = r['nr_meals']
            assert len(recipe.ingredients) == (i + 1)

    def test_recipecollection(self, data_recipes):
        recipe_collection = RecepieCollection()
        for name, r in data_recipes.items():
            recipe = Recipe(name=name)
            for i,e in enumerate(r['ingredients']):
                u = e['unit'] if 'unit' in e else None
                q = e['quantity'] if 'quantity' in e else None
                recipe.ingredients.append(
                    Ingredient(name=IngredientName(name=e['name']),
                               unit=Unit(name=u),
                               quantity=q)
                )
            recipe.description = r['description']
            recipe.nr_meals = r['nr_meals']
            recipe_collection.recipes.append(recipe)
        assert len(recipe_collection.recipes) == len(data_recipes)


class TestDB:
    """Test database operations"""
    # TODO: add
    # TODO: remove
    # TODO: update in database