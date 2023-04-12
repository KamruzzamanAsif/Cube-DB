import random
# from tinyolap.query import Query
from tinyolap.cell import Cell
from tinyolap.decorators import rule
from tinyolap.database import Database
from tinyolap.slice import Slice
from tinyolap.view import View



@rule("sales", ["Deviation"])
def deviation(c: Cell):
    return c["Actual"] - c["Plan"]


@rule("sales", ["Deviation %"])
def deviation_percent(c: Cell):
    if c["Plan"]:  # prevent potential division by zero
        return c["Deviation"] / c["Plan"]
    return None


def elons_random_number(low: float = 1000.0, high: float = 2000.0):
    return random.uniform(low, high)



def analysis_tesla(console_output: bool = True):
    ################# define the data space ###################
    db = Database("tesla")
    cube = db.add_cube("sales", [
        db.add_dimension("tesla_datatypes").edit().add_many(
            ["Actual", "Plan", "Deviation", "Deviation %"]).commit(),

        db.add_dimension("years").edit().add_many(
            ["2021", "2022", "2023"]).commit(),

        db.add_dimension("periods").edit().add_many(
            ["Q1", "Q2", "Q3", "Q4"],
            [("Jan", "Feb", "Mar"), 
            ("Apr", "Mai", "Jun"),
            ("Jul", "Aug", "Sep"), 
            ("Oct", "Nov", "Dec")]).commit(),
           
        db.add_dimension("regions").edit().add_many(
            "Total_Regions", ["North", "South", "West", "East"]).commit(),

        db.add_dimension("products").edit().add_many(
            "Total_Products", ["Model S", "Model 3", "Model X", "Model Y"]).commit()
    ])


    ############## adding Business Logics ##################### 
    cube.register_rule(deviation)
    cube.register_rule(deviation_percent)


    ############## ADD DATA #################
    
    # Add some 'Plan' data
    cube["Plan", "2021", "Jan", "North", "Model S"] = 400.0  # write to a single cell
    cube["Plan", "2021", "Feb", "North", "Model X"] = 200.0  # write to a single cell


    cube["Plan"] = 500.0   # assigning all plan cells to 500
    if cube["Plan", "2021", "Q1", "North", "Model S"] != 500.00:
        raise ValueError("TinyOlap is cheating...")  # cheking that if assigned
    
        # giving the true we assure that the value will surely assigned
    cube["Plan"].set_value(500.0, True)  # this will write 3 x 12 x 4 x 4 = 576 values to the cube


    cube["Plan", "2023"] = cube["Plan", "2022"] * 1.50  # Elon is skyrocketing, 50% more for 2023



    # Add some 'Actual' data
    cube["Actual"].set_value(elons_random_number)  # really? Elon is going for a shortcut here.


    ################ CHECKING Performance #################################
    print("Prformance Checking for year 2023 first 3 months: ")
    dev_percent = cube["Deviation %", "2023", "Q1", "Total_Regions",  "Total_Products"]
    if console_output:
        print(f"\t>>>>>>Elon's performance in 2023 is {dev_percent:.2%}. Congrats!")


    print("=====================Showing Minimal Reporting Statistics ===================")
    print(View(cube).refresh().to_console_output())


    # sql = "SELECT * FROM sales WHERE '2022'"
    # records = Query(db, sql).execute().records()


if __name__ == '__main__':
    analysis_tesla()
