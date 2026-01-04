# main.py

import db
import import_csv
import os
import pandas as pd

# Task 2 (12 points)
# Context of this taks is the energy monitoring system of TU Wien's (Plus-)Plus-Energy Office High-Rise Building
# - The data is from the electric energy meters that were recorded in 2018.
# !!The data may only be used to carry out the exercise!!
# There are time series about:
# Energy (counter values) in MWh
# Power (instantaneous values) in W
# The zip-File "Assignment3.zip" consists of the following parts:
#
# Folder PythonCode (Code for the connection via python)
# EnergyMeter.db (sqlite database file for your task - it is completely empty)
# EnergyMeter2018.csv (time series data from the year 2018)
# Metainformation_ElectricEnergyMeter.csv (Metainformation to the time series data)
# requirements.txt (Python information for your python project)
# In the python code you can see that the first create statement for the metainformation,
# the import for the Metainformation_ElectricEnergyMeter.csv and the return of all entries is already coded as an example for you.
# Just run the main.py file with PyCharm to fill in the first data to your database.
# You can always have a look on your database with the DB Browser as it was shown in the lecture.
#
# Requirements
# You can use PyCharm like in Assignment 2
# You need Python again
# Additional Information
# The Python code has been intentionally kept simple to make it easy for you to customize.
# No attention has been paid to SQL security, hard coded stuff, speedup or complex programming.
# You can keep your programming just as simple if you want.
#
# Your tasks
# Create the table for the data of "EnergyMeter2018.csv"
# - it should be names "EnergyMeterValues" and consists of the following attributes:
# TagID - Integer; Primary Key
# Timestamp - DateTime; Primary Key
# Value - Real
# Insert the data of "EnergyMeter2018.csv" into the new created table
# In the csv the structure is as follows:
# First row - header (TagID from the different data points)
# First column - Timestamp
# All other cells - Values
#
# Query 1: Get all data where the TagID belongs to the EnergyMeters where the "Description_German" Field consists of "2P1_Gesamt_OG" and the "Unit" is "MWh"
# (this will provide the energy counter values of all floors of the building)
#
# Query 2: Get the average of the day for each floor
# (You will need the rows where the "Description_German" Field consists of "2P1_Gesamt_OG" and the "Unit" is "W")
# In the provided python code classes you will see parts  "#Your code here"
# - there you have to adapt the things to get everything to work (you will find this comment only in the db.py)
#
# In the main.py change the directory to your working directory and when you finally implemented the stuff delete # in front of import_energy_data(db_name) to try it out
#
# You do not have to adapt the csv import since it is already implemented but you can have a look on it in the import_csv.py
#
# Since the import of your csv file will then take about 3 up to 4 minutes (more than 22million entries)
# - I would suggest run this code only once and then comment it out (your database file will grow up to ~1.6GB)
#
# There are some additional comments regarding the queries directly in the code.
#
# Execution of the queries will take around 30 seconds (and finally it is only a simple print out
# - of course once again you can also store the information in a data frame and work with it regarding analysis, visualization, .... - but it is out of scope of this assignment)


def main():
    # Define your database - !CHANGE the name to the directory at your OS!
    cwd = os.getcwd()
    db_name = cwd + '/EnergyMeter.db'
    import_energy_metadata(db_name)

    #When you finally have implemented your code, delete the comment sign in front of the following method to execute it
    # import_energy_data(db_name)



def import_energy_metadata(db_name):
    # Connection to SQLite-Database
    conn = db.connect_db(db_name)

    # table name
    table_name = 'EnergyMeter'

    # Create table (if it does not exist)
    db.create_table(conn, table_name)

    # CSV import for the database !CHANGE the name to the directory at your OS!
    cwd = os.getcwd()

    # Reading UTF-8 CSV
    # df = pd.read_csv(cwd + '/Metainformation_ElectricEnergyMeter.csv', encoding='utf-8')
    #
    # # Writing UTF-8 CSV
    # df.to_csv('output.csv', encoding='utf-8', index=False)
    csv_data = import_csv.read_csv(cwd + '/Metainformation_ElectricEnergyMeter.csv')
    db.insert_data_from_csv(conn, table_name, csv_data)

    # Get data from the database
    rows = db.fetch_all_data(conn, table_name)

    # Show results
    for row in rows:
        print(row)

    # Close database connection
    db.close_db(conn)

def import_energy_data(db_name):
    # Connection to SQLite-Database
    conn = db.connect_db(db_name)

    # table name
    table_name = 'EnergyMeterValues'

    # Create table (if it does not exist) for Energy Values
    db.create_table_energy_values(conn, table_name)

    # CSV import for the database !CHANGE the name to the directory at your OS!
    cwd = os.getcwd()
    csv_data = import_csv.read_csv_specific_format(cwd + '/EnergyMeter2018.csv')
    db.insert_data_from_energy_values_csv(conn, table_name, csv_data)

    # Get data from the database for Query 1
    rows = db.fetch_all_data_floor_counter_values(conn)

    # Show results
    for row in rows:
        print(row)

    # Get data from the database for Query 2
    rows = db.fetch_average_day_power_floors(conn)

    # Show results
    for row in rows:
        print(row)

    # Close database connection
    db.close_db(conn)



if __name__ == "__main__":
    main()
