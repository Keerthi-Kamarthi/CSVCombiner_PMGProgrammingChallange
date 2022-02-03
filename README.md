# PMG CSVCombiner Program Solution

CSV Combiner solution is a command line program, it takes several CSV files as arguments and Combine all of them to give output of new csv file. New Combined CSV file contains the rows from each of the inputs along with an additional column that has the filename from which the row came (only the file's basename).

# Command lines to run the program
To execute PMG_CombineCSV.py file:

python PMG_CombineCSV.py ./fixtures/accessories.csv ./fixtures/clothing.csv ./fixtures/household_cleaners.csv > combined.csv

and for CSVCombiner_UnitTest file:

python -m unittest test CSVCombiner_UnitTest -v
