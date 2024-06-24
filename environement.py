import os
prod = False

if(prod):
    file_path = 'Euro_2020_Data_Visualization/EURO_2020_DATA.xlsx'
    file_path = os.path.abspath(file_path)
else:
    file_path = "./EURO_2020_DATA.xlsx"


