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
    def test_add_unit(self, dbsession, data_recipes):
        i_1 = data_recipes['salty_soup']['ingredients'][0]
        if 'unit' in i_1:
            dbsession.add(Unit(name=i_1['unit']))
        res = dbsession.query(Unit)
        print(res.first().name)

    def test_add_units(self, dbsession, data_recipes):
        for name, recipe in data_recipes.items():
            for ingredient in recipe['ingredients']:
                if 'unit' in ingredient:
                    dbsession.add(Unit(name=ingredient['unit']))
        res = dbsession.query(Unit)
        for r in res:
            print(r.name)

    def test_add_ingredient(self, dbsession, data_recipes):
        i_1 = data_recipes['salty_soup']['ingredients'][0]
        dbsession.add(Ingredient(name=IngredientName(name=i_1['name']),
                                 unit=Unit(name=i_1['unit']),
                                 quantity=i_1['quantity']))
        res = dbsession.query(Ingredient)
        assert res.first().name.name == i_1['name']

    def test_add_ingredients(self, dbsession, data_recipes):
        ingredient_name_added = set()
        for name, recipe in data_recipes.items():
            for i_1 in recipe['ingredients']:
                if i_1['name'] in ingredient_name_added:
                    pass
                else:
                    unit = Unit(name=i_1['unit']) if 'unit' in i_1 else None
                    q = i_1['quantity'] if 'quantity' in i_1 else None
                    dbsession.add(Ingredient(name=IngredientName(name=i_1['name']),
                                             unit=unit,
                                             quantity=q))
                    ingredient_name_added.add(i_1['name'])
        res = dbsession.query(Ingredient)
        for r in res:
            print(r.name.name)

    def test_add_recipe(self, dbsession, data_recipes):
        r_name = 'salty_soup'
        r = data_recipes[r_name]
        recipe = Recipe(name=r_name)
        for i_1 in r['ingredients']:
            unit = Unit(name=i_1['unit']) if 'unit' in i_1 else None
            q = i_1['quantity'] if 'quantity' in i_1 else None
            recipe.ingredients.append(Ingredient(name=IngredientName(name=i_1['name']),
                                     unit=unit,
                                     quantity=q))
        recipe.nr_meals = r['nr_meals']
        recipe.description = r['description']
        dbsession.add(recipe)
        res = dbsession.query(Recipe)
        assert res.first().name == r_name

    def test_add_collection(self, dbsession, data_recipes):
        recipe_collection = RecepieCollection()
        for name, r in data_recipes.items():
            recipe = Recipe(name=name)
            for i_1 in r['ingredients']:
                n = dbsession.query(IngredientName).filter(IngredientName.name == i_1['name']).first()
                if not n:
                    n = IngredientName(name=i_1['name'])
                    dbsession.add(n)
                if 'unit' in i_1:
                    u = dbsession.query(Unit).filter(Unit.name == i_1['unit']).first()
                    if not u:
                        u = Unit(name=i_1['unit'])
                        dbsession.add(u)
                else:
                    u = None
                q = i_1['quantity'] if 'quantity' in i_1 else None
                recipe.ingredients.append(Ingredient(name=n,
                                                     unit=u,
                                                     quantity=q))
            recipe.nr_meals = r['nr_meals']
            recipe.description = r['description']
            recipe_collection.recipes.append(recipe)
        dbsession.add(recipe_collection)
        res = dbsession.query(RecepieCollection)
        assert res.first().recipes[0].name == 'salty_soup'
    # TODO: remove
    # TODO: update in database