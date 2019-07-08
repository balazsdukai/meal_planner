from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, DecimalField, SelectField, FieldList, FormField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

from meal_planner.database import db_session, init_db
from meal_planner.models import Recipe,Unit,IngredientName,Ingredient

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '04d8518b-110d-459c-ad3a-2c44cfb6419a'
csrf = CSRFProtect(app)

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

class AddIngredientForm(Form):
    units = [('',''),('tbsp', 'tbsp'), ('l', 'l'), ('kg', 'kg'), ('cup', 'cup')]
    ingredientname = StringField()
    quantity = DecimalField()
    unit = SelectField('unit', choices=units)

class AddIngredientsForm(FlaskForm):
    units = [('',''),('tbsp', 'tbsp'), ('l', 'l'), ('kg', 'kg'), ('cup', 'cup')]
    ingredientlist = FieldList(FormField(AddIngredientForm), min_entries=1)
    save = SubmitField(label='Save')
    add_ingredient = SubmitField(label='Add ingredient')
    description = TextAreaField()
    recipename = StringField()
    nr_meals = IntegerField()

def get_recipes():
    recipes = [(1,'salty soup'), (2,'hummus with hummus sauce'), (3,'tasty pie'),
    (4,'this is very long names recepie with many ingredients'), (5,'blaa bla blaa')]
    return recipes
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/recipes")
def recipes():
    recipe_list = get_recipes()
    return render_template('recipe_list.html', recipes=recipe_list)

@app.route("/recipes/<string:recipe_name>/", methods=['GET'])
def recipe(recipe_name):
    return render_template('recipe.html', recipe_name=recipe_name)

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

    #     # NewItem = Item(name=request.form['name'], description=request.form['description'], price=request.form['price'], category_id = category_id, user_id=category.user_id)
    #     # session.add(NewItem)
    #     # session.commit()
    #     # flash('New Menu %s Item Successfully Created' % (NewItem.name))
    #     return render_template('add_recipe.html', form=form)

    return render_template('add_recipe.html', form=form)

@app.route("/create_shopping_list")
def create_shopping_list():
    recipe_list = get_recipes()
    return render_template('create_shopping_list.html', recipes=recipe_list)

@app.route("/shopping_list")
def shopping_list():
    recipe_list = get_recipes()
    return render_template('shopping_list.html', recipes=recipe_list)

if __name__ == "__main__":
    app.run()