from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, DecimalField, SelectField, FieldList, FormField, \
    SubmitField, IntegerField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

from meal_planner.database import db_session, init_db
from meal_planner.models import Recipe,Unit,IngredientName,Ingredient

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '04d8518b-110d-459c-ad3a-2c44cfb6419a'
# csrf = CSRFProtect(app)

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# TODO: I don't know how to pass a variable to a subform. That would be required for populating
# the Unit choices from the values from the database, so that the Units are queries only once
# at the beginning when the add_recipe view is initiated. Because with the current setup it would
# need to query the units for each subform entry.
# But maybe better to have a single row/form to add an ingredient, and a table below that is
# dynamically populated with the added ingredients, with the possibility to remove an ingredient.
# See: https://stackoverflow.com/questions/30668029/creating-a-form-with-a-varying-number-of-repeated-subform-in-flask-wtforms
# Maybe: https://stackoverflow.com/questions/41232105/populate-wtforms-select-field-using-value-selected-from-previous-field
# This approach would probably circumvent the need of having units selector in each subform.

class AddIngredientForm(Form):
    ingredientname = StringField()
    quantity = DecimalField()
    unit = SelectField('unit')

class AddIngredientsForm(FlaskForm):
    units = [(unit.id, unit.name) for unit in Unit.query.all()]
    app.logger.debug(units)
    ingredientlist = FieldList(FormField(AddIngredientForm), min_entries=1)
    save = SubmitField(label='Save')
    add_ingredient = SubmitField(label='Add ingredient')
    description = TextAreaField()
    recipename = StringField()
    nr_meals = IntegerField()

class SelectRecipe(FlaskForm):
    recipe_id = HiddenField()
    recipe_name = HiddenField()
    nr_meals = IntegerField()
    select = BooleanField()

class CreateShoppingList(FlaskForm):
    recipes = FieldList(FormField(SelectRecipe))
    create = SubmitField(label='Create shopping list')


def sum_recipes(form):
    for i,recipe in enumerate(form['recipes']):
        if recipe['select']:
            app.logger.debug("adding recipe to shopping list", recipe)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/recipes")
def recipes():
    recipe_list = [(recipe.id, recipe.name) for recipe in Recipe.query.all()]
    return render_template('recipe_list.html', recipes=recipe_list)

@app.route("/recipes/<string:recipe_id>/", methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
    return render_template('recipe.html', recipe=recipe)

@app.route("/add_recipe", methods=('GET', 'POST'))
def add_recipe():
    form=AddIngredientsForm()

    if form.validate_on_submit():
        app.logger.debug(form.data)

        recipe = Recipe(name=request.form['recipename'])
        for i in form.data['ingredientlist']:
            n = db_session.query(IngredientName).filter(IngredientName.name == i['ingredientname']).first()
            if not n:
                n = IngredientName(name=i['ingredientname'])
                db_session.add(n)
            if 'unit' in i:
                u = db_session.query(Unit).filter(Unit.name == i['unit']).first()
                if not u:
                    u = Unit(name=i['unit'])
                    db_session.add(u)
            else:
                u = None
            q = i['quantity'] if 'quantity' in i else None
            recipe.ingredients.append(Ingredient(name=n,
                                                 unit=u,
                                                 quantity=q))
        recipe.nr_meals = form.data['nr_meals']
        recipe.description = form.data['description']
        db_session.add(recipe)
        db_session.commit()
        return render_template('add_recipe.html', form=form, data=form.data)

    return render_template('add_recipe.html', form=form)

@app.route("/create_shopping_list", methods=('GET', 'POST'))
def create_shopping_list():
    form = CreateShoppingList()

    if form.is_submitted():
        app.logger.debug(form.data)
        sum_recipes(form.data)
        return render_template('create_shopping_list.html', form=form)

    for recipe in Recipe.query.all():
        print((recipe.id, recipe.name))
        subform = SelectRecipe()
        subform.recipe_id = recipe.id
        subform.recipe_name = recipe.name
        subform.select = False
        subform.nr_meals = 0
        form.recipes.append_entry(subform)
    return render_template('create_shopping_list.html', form=form)

@app.route("/shopping_list")
def shopping_list():
    recipe_list = [(recipe.id, recipe.name) for recipe in Recipe.query.all()]
    return render_template('shopping_list.html', recipes=recipe_list)

if __name__ == "__main__":
    app.run()