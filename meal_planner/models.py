from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from meal_planner.database import Base

class Unit(Base):
    """Unit of the ingredient quantity"""
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class IngredientName(Base):
    """Ingredient name"""
    __tablename__ = 'ingredient_names'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Ingredient(Base):
    """One ingredient in a recipe"""
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('ingredient_names.id'))
    name = relationship('IngredientName')
    quantity = Column(Float)
    unit_id = Column(Integer, ForeignKey('units.id'))
    unit = relationship('Unit')
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = relationship('Ingredient')
    description = Column(String)
    nr_meals = Column(Integer, nullable=False)
    recipe_collection_id = Column(Integer, ForeignKey('recipe_collection.id'))

class RecepieCollection(Base):
    __tablename__ = 'recipe_collection'
    id = Column(Integer, primary_key=True)
    recipes = relationship('Recipe')

# class ShoppingList(Base):
#     __tablename__ = 'shopping_list'
