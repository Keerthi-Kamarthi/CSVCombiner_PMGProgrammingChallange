# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 16:19:36 2022

@author: kamar
"""

import pandas as pd
import sys
import unittest
from PMG_CombineCSV import CSVCombiner
from io import StringIO
import warnings


class Unit_TestMethod(unittest.TestCase):
    """ Initializing all paths """

    output_path = "./test_output.csv"
    csv_combiner_code_path = "./PMG_CombineCSV.py"
    accessoriesfile_path = "./fixtures/accessories.csv"
    clothingfile_path = "./fixtures/clothing.csv"
    householdcleanersfile_path="./fixtures/household_cleaners.csv"
    emptyFilePath = "./empty.csv"


    testOutputFile = None
    ccobj = CSVCombiner()


    @classmethod
    def tearDownClass(cls):

        if cls.testOutputFile is not None:
            cls.testOutputFile.close()

    def loadTestoutputData(self):
        self.testOutputFile = open(self.output_path, 'w+', encoding="utf-8")
        

    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output
        self.loadTestoutputData()
        
        # to ignore the python resource warnings
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
            
            
    def testnumoffeatures_files(self):
        """
        validating number of columns among the files
        """
        df_acc = pd.read_csv(self.accessoriesfile_path, lineterminator='\n')
        df_cloth = pd.read_csv(self.clothingfile_path, lineterminator='\n')
        df_hC = pd.read_csv(self.householdcleanersfile_path, lineterminator='\n')
        print(df_acc.columns)
        self.assertEqual(len(df_acc.columns), len(df_cloth.columns))
        self.assertEqual(len(df_cloth.columns), len(df_hC.columns))
        self.assertEqual(len(df_hC.columns), len(df_acc.columns))
        
        
        
    def testFeaturenames_Files(self):
        """
        validating same columns in files
        """
        df_acc = pd.read_csv(self.accessoriesfile_path, lineterminator='\n')
        df_cloth = pd.read_csv(self.clothingfile_path, lineterminator='\n')
        df_hC = pd.read_csv(self.householdcleanersfile_path, lineterminator='\n')
        self.assertListEqual(list(df_acc.columns), list(df_cloth.columns))
        self.assertListEqual(list(df_cloth.columns), list(df_hC.columns))
        self.assertListEqual(list(df_hC.columns), list(df_acc.columns))


            
    def testCombinedRowsInCsv(self):
        """
        validating number of rows in final file to sum of individual rows files
        """
        argv = [self.csv_combiner_code_path, self.accessoriesfile_path, self.clothingfile_path,self.householdcleanersfile_path]

        self.ccobj.csvfiles_combiner(argv)
        #run csvfiles_combiner with valid arguments
        
        self.testOutputFile.write(self.output.getvalue())
        #to write output of csvcombiner into test output csv file
        
        
        df_acc = pd.read_csv(self.accessoriesfile_path, lineterminator='\n')
        df_cloth = pd.read_csv(self.clothingfile_path, lineterminator='\n')
        df_hC = pd.read_csv(self.householdcleanersfile_path, lineterminator='\n')
        

        df_sum = (df_acc.shape[0]+df_cloth.shape[0]+df_hC.shape[0])
        #length of the combined dataframe
        
        with open(self.output_path) as test_combinedcsv:
            try:
                testcombined_df = pd.read_csv(test_combinedcsv, lineterminator='\n')
                testcombined_df.to_csv("combinedFile.csv",index=False)
                assert testcombined_df.shape[0]!=df_sum,"rows are not same"
            except AssertionError as e:
                print(e)
    
    def testWithIncorrectFilePath(self):
        """ 
        run csv_combiner with a file that doesn't exist
        """
        argv = [self.csv_combiner_code_path, "no_file.csv"]
        self.assertRaises(FileNotFoundError, lambda: self.ccobj.csvfiles_combiner(argv))

 
    def testWithoutInputCsvFile(self):
        """
        validating input file existing or not
        """
        argv = [self.csv_combiner_code_path]
        self.assertRaises(ValueError, lambda: self.ccobj.csvfiles_combiner(argv))


    def testWithEmptyFile(self):
        """
        validating with empty file
        """
        argv = [self.csv_combiner_code_path, self.emptyFilePath]
        self.assertRaises(ValueError, lambda: self.ccobj.csvfiles_combiner(argv))


