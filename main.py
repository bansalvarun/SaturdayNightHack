#!/usr/bin/env python

import webapp2
from google.appengine.ext import db
from google.appengine.api import users
from Database.Votes import Votes
from datetime import datetime, timedelta
from Meal import Meal
from Template_Handler import Handler

bfast = {
            "Monday": Meal("Breakfast", "Monday", "aloo parantha, pickle, milk/tea, bread butter"),
            "Tuesday": Meal("Breakfast", "Tuesday", "suji pancake/besan chilla, milk/tea, bread butter"),
            "Wednesday": Meal("Breakfast", "Wednesday", "omelette/boiled egg, veg cutlet, mil/tea"),
            "Thursday": Meal("Breakfast", "Thursday","methi/palak/onion paratha, pickle, milk/tea, bread butter"),
            "Friday": Meal("Breakfast", "Friday","vada/idli, sambhar, milk/tea, bread butter"),
            "Saturday": Meal("Breakfast", "Saturday","poori aloo, milk/tea, bread butter"),
            "Sunday": Meal("Breakfast", "Sunday","pav bhaji/poha, milk/tea, bread butter"),
        }

lunch = {
            "Monday": Meal("Lunch", "Monday", "rajma, mix veg, rice, roti, salad, raita"),
            "Tuesday": Meal("Lunch", "Tuesday", "yellow dal, aloo soyabean, rice, roti, salad, raita"),
            "Wednesday": Meal("Lunch", "Wednesday", "yellow dal, bhindi, rice, roti, salad, raita"),
            "Thursday": Meal("Lunch", "Thursday","kadhi, aloo parwal/seasonal veg, rice, roti, salad, raita"),
            "Friday": Meal("Lunch", "Friday","black chana, aloo jeera, rice, roti, salad, raita"),
            "Saturday": Meal("Lunch", "Saturday","chole bhature, rice, salad, pickle"),
            "Sunday": Meal("Lunch", "Sunday","veg noodles, fried rice, veg manchurian"),
}


dinner = {
            "Monday": Meal("Dinner", "Monday", "arhar dal, bhindi, rice, roti, salad, gulab jamun"),
            "Tuesday": Meal("Dinner", "Tuesday", "green dal, kofta, rice, roti, salad, boondi"),
            "Wednesday": Meal("Dinner", "Wednesday", "chicken, paneer, yellow dal, rice, roti, salad, kheer/sewain"),
            "Thursday": Meal("Dinner", "Thursday","chole, lauki, rice, salad, balushahi"),
            "Friday": Meal("Dinner", "Friday","dal makhani, chilly aloo, rice, roti, salad, khaja"),
            "Saturday": Meal("Dinner", "Saturday","dal palak, mix veg, jeera rice, roti, salad, jalebi"),
            "Sunday": Meal("Dinner", "Sunday", "chicken, paneer, b masoor dal, rice, roti, salad, halwa"),
}

dinner_hours = range(15, 22 + 1)
breakfast_hours = [23, 24] + range(1, 10 + 1)

def get_current_meal():
    now = datetime.now()
    # times in appengine are in UTC
    # need to convert this to IST
    now = datetime.now() + timedelta(hours=5, minutes=30)

    hour = now.hour
    day  = now.strftime("%A")

    meal = lunch[day]
    if (now.hour in dinner_hours):
        meal = dinner[day]
    elif (now.hour in breakfast_hours):
        meal = bfast[day]

    return meal
def meal_object(meal):
    mid = meal.getMealId()
    prev = db.GqlQuery("SELECT * FROM Votes WHERE mealID = :1", mid)
    prev = prev.fetch(1)
    if len(prev) > 0:
        return prev[0]

    bt = Votes(mealID=mid)
    bt.put()

    return bt

class Homepage(Handler):
    def get(self):
        meal = get_current_meal()
        self.render("dashboard.html", meal=meal, meal_obj=meal_object(meal))

class MealVote(Handler):
    def upvote(self):
        m = get_current_meal()
        m2 = meal_object(m)
        m2.upVotes += 1
        m2.put()

    def downvote(self):
        m = get_current_meal()
        m2 = meal_object(m)
        m2.downVotes += 1
        m2.put()

    def get(self, action):
        if action == 'up':
            self.upvote()
        if action == 'down':
            self.downvote()


app = webapp2.WSGIApplication([
    ('/', Homepage),
    ('/vote/(.+)', MealVote),
], debug=True)
