####################################################################################################

ZIP FILE CONTENTS:

-constants python package folder: contains a constants file named energy_constants.py.
-energy_revenue_calculator.py: A python file containing the program to run the calculation.
-emp_salary.sql: A sql file containing the queries for the questions in the coding challenge. 
-coding_practice_python_battery_dispatch_dataset.csv: The sample dataset given for the coding challenge.


####################################################################################################

STEPS TO RUN ENERGY REVENUE CALCULATOR:

-Prerequisites:
	Python 3.8 or higher
	Pandas package installed with Python
	IDE - VsCode or Pycharm(preferrable)
	
-STEPS
	1. Extract the zip file contents onto a new python project. Note: the project should have a python environment already setup.[You can do that by typing "python -m venv <name of environment>]
	2. Open the energy_revenue_calculator.py.
	3. The program can be run in two ways
		a. Click on the play button will run the program using default values.
		b. In the terminal of the IDE of choice navigate to the location where the zip folder is extracted and type the below to execute.
			- python energy_revenue_calculator.py    #This will run the program with default values
			- python energy_revenue_calculator.py --file_path <file_path> --date <date> --chunk <chunk> #The program takes in 3 arguments, the csv file path, date and batch chunk size.
																										# Any value not specified will revert to default values provided which is 
																										# data - 2024-04-01, chunk - 100, flie_path - <path of the csv file in the zipped folder>
	4. Once the program is run, it will print an output on the terminal. 

####################################################################################################

METHODOLOGY

Chunk Processing: Processes the CSV file in smaller chunks to manage memory efficiently.

Date Filtering: Filters each chunk to include only records for the specified date.

Revenue Calculation: Calculates revenue for each interval based on initial and target MW values and energy price (RRP).

Sequential Processing: Processes each chunk and accumulates the total revenue for the specified date.

Command-Line Interface: Uses command-line arguments for file path, date, and chunk size for flexible input handling.


####################################################################################################

ASSUMPTIONS MADE

- All calculations are done irrespective of the consideration of charging and discharging.
- If the INITIALMW for the next time period is not considered then the TARGETMW is considered for calculation.
- There is no gap or stale time between the time periods.
- The calculation does not take into consideration the cost that might incur when the battery is charging. 


####################################################################################################