from flask import Flask, flash, redirect, render_template, request, session, abort


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

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

@app.route("/add_recipe", methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        print("name", request.form.get('name'))
        print("amount", request.form.get('amount'))
        print("unit", request.form.get('unit'))
        # print("name", request.form['name'])
        # NewItem = Item(name=request.form['name'], description=request.form['description'], price=request.form['price'], category_id = category_id, user_id=category.user_id)
        # session.add(NewItem)
        # session.commit()
        # flash('New Menu %s Item Successfully Created' % (NewItem.name))
        return render_template('add_recipe.html')
    else:
        return render_template('add_recipe.html')

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