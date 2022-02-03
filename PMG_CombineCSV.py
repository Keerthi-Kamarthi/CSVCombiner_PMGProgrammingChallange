# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 08:59:55 2022

@author: kamar
"""

import sys
import pandas as pd
import os
from pathlib import Path

class CSVCombiner:
    
    def validate_arguments(self, argv):
        """
        To validate the given arguments like filepaths and extensions
        """
        
        files = argv[1:]        
        #in arguments provided, 1st is python file name and followed by csv files to process
        #atleast 2 arguments should be provided, so it contains minimum of one csv file to process
        if (len(argv)) < 2:
            raise ValueError("No files provided in command line arguments")

        for filepath in files:
            #path validation
            get_filepath = Path(filepath)
           
            if not get_filepath.exists():
                raise FileNotFoundError("File is not found in the given path")

            filePathWithoutExtension, filepathExtension = os.path.splitext(filepath)
            #file extension validation- to check if they are csv files
            if filepathExtension!= ".csv":
                raise Exception("File"+ str(filePathWithoutExtension)+ " is not in csv format")
                
            #File should not be empty
            csv_data = pd.read_csv(get_filepath)                  
            if csv_data.empty :
                raise ValueError("csv file is empty")
                
    
    def filememory_usage(self, files):  
        """
        provides the memory usage for the input files
        """
        for filepath in files:
            file_name =  filepath.split("/")[-1]
            #split('/')[-1] gives filename present in the filepath
            
            files_data = pd.read_csv(filepath)
            memory_usage = sys.getsizeof(files_data)
            print("Memory usage of file",file_name,"is", memory_usage,"Bytes.")
          
                               
    def csvfiles_combiner(self, argv: list):
        """
        combines the rows of csv file as per the requirements store it in csv
        """
        files = argv[1:]
        # validate the arguments passed from command line
        self.validate_arguments(argv)
        
        #As per given task,CSV files of any size can be used for this program
        #So, Commented the below method calling
        #self.filememory_usage(files)
        
        #Taken default chunk size as 10*5, change according to data 
        chunksize = 10*5
        #chunksize is used to avoid memory related issues
        
        df_flsconcat = []
        #list of dataframes where all input files will be combined 
        
        for filepath in files:
            chunk_list = []  #to append each chunk
            files_data = pd.read_csv(filepath, chunksize = chunksize)
            #files data is read in form of list of chunks

            for chunk in files_data:
                # chuck will have list of rows of files data according to chunksize
                
                chunk['filename'] = filepath.split('/')[-1]
                #to create a new column as filename and split('/')[-1] gives filename present in the filepath
                chunk_list.append(chunk)
            
            df_flsconcat.append(pd.concat(chunk_list))
            #to convert the chunk list to dataframe for each file and append to list of df_flsconcat
            
        output_file = pd.concat(df_flsconcat, ignore_index = True)
        
        #to write all combined data frame into output csv file 
        output_file.to_csv(sys.stdout,index=False,line_terminator='\n')
                
def main():
    ccobj = CSVCombiner() 
    
    #calling method to combine all csv files
    ccobj.csvfiles_combiner(sys.argv)
    
    
if __name__ == '__main__':
    main() 
    #calling main method to run the program
    
    
