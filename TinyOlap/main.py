import random
from tinyolap.cell import Cell
from tinyolap.decorators import rule
from tinyolap.database import Database
from tinyolap.slice import Slice
from tinyolap.view import View
# from tinyolap.query import Query


@rule("sales", ["Delta %"])
def delta_percent(c: Cell):
    if c.Plan:  # prevent potential division by zero
        return c.Delta / c.Plan
    return None

def elons_random_numbers(low: float = 1000.0, high: float = 2000.0):
    return random.uniform(low, high)

# Purpose: Support Elon Musk on his business planning & reporting for Tesla
def play_tesla(db, console_output: bool = True):
    # 1st - define an appropriate 5-dimensional cube (the data space)
    cube = db.add_cube("sales", [
        db.add_dimension("datatypes").edit()
                       .add_many(["Actual", "Plan"])
                       .add_many("Delta", ["Actual", "Plan"], [1.0, -1.0])
                       .add_many("Delta %")
                       .commit(),
        db.add_dimension("years").edit().add_many(
            ["2021", "2022", "2023"]).commit(),
        db.add_dimension("periods").edit().add_many(
            "Year", ["Q1", "Q2", "Q3", "Q4"]).commit(),
        db.add_dimension("regions").edit().add_many(
            "Total", ["North", "South", "West", "East"]).commit(),
        db.add_dimension("products").edit().add_many(
            "Total", ["Model S", "Model 3", "Model X", "Model Y"]).commit()
    ])
    # 2nd - (if required) add custom business logic, so called 'rules'.
    #       Register the rule that has been implemented above. Take a look.
    cube.register_rule(delta_percent)

    # 3rd - (optional) some beautifying, set number formats
    db.dimensions["datatypes"].member_set_format("Delta", "{:+,.0f}")
    db.dimensions["datatypes"].member_set_format("Delta %", "{:+.2%}")

        # 4th - to write data to the cubes, just define and address and assign a value
    cube["Plan", "2021", "Q1", "North", "Model S"] = 400.0  # write a single value
    cube["Plan", "2021", "Q1", "North", "Model X"] = 200.0  # write a single value

    # 5th - TinyOlap's strength is manipulating larger areas of data
    cube["Plan"] = 500.0  # set the existing value 400.0 and 200.0 to 500.0
    cube["Plan"].set_value(500.0, True)  # 3 x 4 x 4 x 4 = set all 192 values to 500.0
    cube["Plan", "2023"] = cube["Plan", "2022"] * 1.50  # Easily data manipulation

    # Let's hand in a Python function to generate the 'Actual' data.
    cube["Actual"].set_value(elons_random_numbers, True) # 3 x 4 x 4 x 4 = set 192 values

    # 6th - some minimal reporting
    print(View(cube).refresh().to_console_output())


# main program
db = Database("tesla")
play_tesla(db)

# # sql
# sql = "SELECT * FROM tesla WHERE year = 2022"
# records = Query(db, sql).execute().records()
# print(records)