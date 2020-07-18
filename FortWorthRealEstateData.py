import csv
import pickle
import pandas as pd 
import xgboost as xgb
from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import math
import numpy as np
import os
from sklearn import preprocessing

# I originally did everything with this Property class (crucial to the loadProperties function) but later realized I should have used pandas to read in the file at the beginning.
# I may later decide it's worth it to redo it using pandas dataframe from the get-go instead of converting objects later.

class Property:
    def __init__(self,RP,Appraisal_Year,Account_Num,Record_Type,Sequence_No,PIDN,Owner_Name,Owner_Address,Owner_CityState,Owner_Zip,Owner_Zip4,Owner_CRRT,Situs_Address,Property_Class,TAD_Map,MAPSCO,Exemption_Code,State_Use_Code,LegalDescription,Notice_Date,County,City,School,Num_Special_Dist,Spec1,Spec2,Spec3,Spec4,Spec5,Deed_Date,Deed_Book,Deed_Page,Land_Value,Improvement_Value,Total_Value,Garage_Capacity,Num_Bedrooms,Num_Bathrooms,Year_Built,Living_Area,Swimming_Pool_Ind,ARB_Indicator,Ag_Code,Land_Acres,Land_SqFt,Ag_Acres,Ag_Value,Central_Heat_Ind,Central_Air_Ind,Structure_Count,From_Accts,Appraisal_Date,Appraised_Value,GIS_Link,Instrument_No,Overlap_Flag):
        self.RP = RP
        self.Appraisal_Year = Appraisal_Year
        self.Account_Num = Account_Num
        self.Record_Type = Record_Type
        self.Sequence_No = Sequence_No
        self.PIDN = PIDN
        self.Owner_Name = Owner_Name
        self.Owner_Address = Owner_Address
        self.Owner_CityState = Owner_CityState
        self.Owner_Zip = Owner_Zip
        self.Owner_Zip4 = Owner_Zip4
        self.Owner_CRRT = Owner_CRRT
        self.Situs_Address = Situs_Address
        self.Property_Class = Property_Class
        self.TAD_Map = TAD_Map
        self.MAPSCO = MAPSCO
        self.Exemption_Code = Exemption_Code
        self.State_Use_Code = State_Use_Code
        self.LegalDescription = LegalDescription
        self.Notice_Date = Notice_Date
        self.County = County
        self.City = City
        self.School = School
        self.Num_Special_Dist = Num_Special_Dist
        self.Spec1 = Spec1
        self.Spec2 = Spec2
        self.Spec3 = Spec3
        self.Spec4 = Spec4
        self.Spec5 = Spec5
        self.Deed_Date = Deed_Date
        self.Deed_Book = Deed_Book
        self.Deed_Page = Deed_Page
        self.Land_Value = Land_Value
        self.Improvement_Value = Improvement_Value
        self.Total_Value = Total_Value
        self.Garage_Capacity = Garage_Capacity
        self.Num_Bedrooms = Num_Bedrooms
        self.Num_Bathrooms = Num_Bathrooms
        self.Year_Built = Year_Built
        self.Living_Area = Living_Area
        self.Swimming_Pool_Ind = Swimming_Pool_Ind
        self.ARB_Indicator = ARB_Indicator
        self.Ag_Code = Ag_Code
        self.Land_Acres = Land_Acres
        self.Land_SqFt = Land_SqFt
        self.Ag_Acres = Ag_Acres
        self.Ag_Value = Ag_Value
        self.Central_Heat_Ind = Central_Heat_Ind
        self.Central_Air_Ind = Central_Air_Ind
        self.Structure_Count = Structure_Count
        self.From_Accts = From_Accts
        self.Appraisal_Date = Appraisal_Date
        self.Appraised_Value = Appraised_Value
        self.GIS_Link = GIS_Link
        self.Instrument_No = Instrument_No
        self.Overlap_Flag = Overlap_Flag
    redfinSoldPrice = "N/A"
    redfinSoldDate = "N/A"
    redfinSqft = "N/A"

    def to_dict(self):
        return {
            'RP': self.RP ,
            'Appraisal_Year': self.Appraisal_Year,
            'Account_Num': self.Account_Num,
            'Record_Type': self.Record_Type,
            'Sequence_No': self.Sequence_No,
            'PIDN': self.PIDN,
            'Owner_Name': self.Owner_Name,
            'Owner_Address': self.Owner_Address,
            'Owner_CityState': self.Owner_CityState,
            'Owner_Zip': self.Owner_Zip,
            'Owner_Zip4': self.Owner_Zip4,
            'Owner_CRRT': self.Owner_CRRT,
            'Situs_Address': self.Situs_Address,
            'Property_Class': self.Property_Class,
            'TAD_Map': self.TAD_Map,
            'MAPSCO': self.MAPSCO,
            'Exemption_Code': self.Exemption_Code,
            'State_Use_Code': self.State_Use_Code,
            'LegalDescription': self.LegalDescription,
            'Notice_Date': self.Notice_Date,
            'County': self.County,
            'City': self.City,
            'School': self.School,
            'Num_Special_Dist': self.Num_Special_Dist,
            'Spec1': self.Spec1,
            'Spec2': self.Spec2,
            'Spec3': self.Spec3,
            'Spec4': self.Spec4,
            'Spec5': self.Spec5,
            'Deed_Date': self.Deed_Date,
            'Deed_Book': self.Deed_Book,
            'Deed_Page': self.Deed_Page,
            'Land_Value': self.Land_Value,
            'Improvement_Value': self.Improvement_Value,
            'Total_Value': self.Total_Value,
            'Garage_Capacity': self.Garage_Capacity,
            'Num_Bedrooms': self.Num_Bedrooms,
            'Num_Bathrooms': self.Num_Bathrooms,
            'Year_Built': self.Year_Built,
            'Living_Area': self.Living_Area,
            'Swimming_Pool_Ind': self.Swimming_Pool_Ind,
            'ARB_Indicator': self.ARB_Indicator,
            'Ag_Code': self.Ag_Code,
            'Land_Acres': self.Land_Acres,
            'Land_SqFt': self.Land_SqFt,
            'Ag_Acres': self.Ag_Acres,
            'Ag_Value': self.Ag_Value,
            'Central_Heat_Ind': self.Central_Heat_Ind,
            'Central_Air_Ind': self.Central_Air_Ind,
            'Structure_Count': self.Structure_Count,
            'From_Accts': self.From_Accts,
            'Appraisal_Date': self.Appraisal_Date,
            'Appraised_Value': self.Appraised_Value,
            'GIS_Link': self.GIS_Link,
            'Instrument_No': self.Instrument_No,
            'Overlap_Flag': self.Overlap_Flag,
            'redfinSoldPrice': self.redfinSoldPrice,
            'redfinSoldDate': self.redfinSoldDate,
            'redfinSqft': self.redfinSqft
        }

class redfinProperty:
    def __init__(self,address,price,date,sqft):
        self.address = address
        self.price = price
        self.date = date
        self.sqft = sqft

# Global Variables
properties = []
redfinProperties = []
property_count = 0
userChoice=99

# GENERAL FUNCTIONS

# Loads properties from data downloaded from http://www.tad.org/Data_files/Download_files/PropertyData_R_2019(Certified).ZIP
def loadProperties():
    global properties
    global property_count
    with open ('PropertyData_R_2019.txt') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter='|')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                #print ("\n")
                line_count += 1
            else:
                properties.append(Property(row[0].strip(),row[1].strip(),row[2].strip(),row[3].strip(),row[4].strip(),row[5].strip(),row[6].strip(),row[7].strip(),row[8].strip(),row[9].strip(),row[10].strip(),row[11].strip(),row[12].strip(),row[13].strip(),row[14].strip(),row[15].strip(),row[16].strip(),row[17].strip(),row[18].strip(),row[19].strip(),row[20].strip(),row[21].strip(),row[22].strip(),row[23].strip(),row[24].strip(),row[25].strip(),row[26].strip(),row[27].strip(),row[28].strip(),row[29].strip(),row[30].strip(),row[31].strip(),row[32].strip(),row[33].strip(),row[34].strip(),row[35].strip(),row[36].strip(),row[37].strip(),row[38].strip(),row[39].strip(),row[40].strip(),row[41].strip(),row[42].strip(),row[43].strip(),row[44].strip(),row[45].strip(),row[46].strip(),row[47].strip(),row[48].strip(),row[49].strip(),row[50].strip(),row[51].strip(),row[52].strip(),row[53].strip(),row[54].strip(),row[55].strip()))
                #print(str(properties[property_count].Situs_Address) + "\nTotal Value: " + str(properties[property_count].Total_Value + "\n"))
                property_count += 1
                line_count += 1
                if (property_count%100000==0):
                    print (str(property_count)+ " properties loaded.\n")
        makePropertyFrame()
        print("\nDone!\n")

# Exports properties loaded from CSV (and any data merged from Redfin or other sources) to pickle
def exportPickle():
    with open('property.pickle', 'wb') as f:
        pickle.dump(properties,f)
    print("\nDone!\n")

# Imports properties from pickle
def importPickle():
    global properties
    with open ('property.pickle', 'rb') as f:
        properties=pickle.load(f)
    makePropertyFrame()
    print("\nDone!\n")

# Prints every address and market value (from TAD)
def printAllValues():
    property_count=0
    for item in properties:
        print(str(properties[property_count].Situs_Address) + "\nTotal Value: " + str(properties[property_count].Total_Value + "\n"))
        property_count += 1
    print("\nDone!\n")

# Prints all data on given address
def printAddressData(address):
    try:
        property_row = propertyFrame.loc[address.upper(),:]
        print (property_row)
    except:
        print ("Property not found")

def printAddressSummary(address):
    try:
        property_row = propertyFrame.loc[address.upper(),['Total_Value', 'Appraisal_Year','Owner_Name','Owner_Address','Owner_Zip','Property_Class','Deed_Date','Land_Acres','redfinSqft','redfinSoldPrice','redfinSoldDate']]
        print (property_row)
    except:
        print ("Property not found")
        
# Adds the prices of the homes sold in the last year to the corresponding property object. Data from Redfin.
def redfinImport():
    global properties
    global redfinProperties
    global propertyFrame 
    propertyFrame = propertyFrame[~propertyFrame.index.duplicated()]
    for filename in os.listdir('Redfin'):
        with open (os.path.join('Redfin/',filename)) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count=0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    redfinProperties.append(redfinProperty(row[3],row[7],row[1],row[11]))
                    line_count += 1
    i=0
    for lot in redfinProperties:
        print ("Getting Redfin for: "+str(lot.address.upper()))
        i=i+1
        propertyFrame.loc[str(lot.address.upper()),"redfinSoldPrice"]=lot.price
        propertyFrame.loc[str(lot.address.upper()),"redfinSoldDate"]=lot.date
        propertyFrame.loc[str(lot.address.upper()),"redfinSqft"]=lot.sqft
    print("\nDone! " + str(i) + " properties added.\n")

# Converts the property objects to a pandas dataframe
def makePropertyFrame():
    global propertyFrame
    propertyFrame = pd.DataFrame(p.to_dict() for p in properties)
    propertyFrame = propertyFrame.set_index('Situs_Address')
    propertyFrame.index.names = [None]

# ML FUNCTIONS

# Regression model to predict Redfin sale price based on all other data

def letsBoost():
    #Remove properties that don't have redfin
    print ("Let's boost!")
    print ("Running...")
    pfLocal = propertyFrame
    pfLocal= pfLocal.replace("N/A",np.NaN)
    nullRemoved = pfLocal[pfLocal.redfinSoldPrice.notnull()]
    print (nullRemoved.head(5))
    train_x = nullRemoved.drop(columns=['Account_Num','Deed_Book','Deed_Page','Instrument_No','Owner_Zip','Owner_Name','Owner_Address','Owner_CityState','Owner_Zip4','Owner_CRRT','GIS_Link', 'LegalDescription', 'Deed_Date','PIDN', 'redfinSoldDate'],axis=1)
    ohe_rest = pd.get_dummies(train_x,drop_first=True, columns=['RP', 'Record_Type', 'Property_Class', 'TAD_Map', 'MAPSCO', 'Exemption_Code', 'State_Use_Code', 'Notice_Date', 'Num_Special_Dist', 'Spec1', 'Spec2', 'Spec3', 'Spec4', 'Spec5', 'Swimming_Pool_Ind', 'ARB_Indicator', 'Ag_Code', 'Central_Heat_Ind', 'Central_Air_Ind', 'From_Accts', 'Appraisal_Date', 'Overlap_Flag','County','City','School'])
    #maybe later convert date to numeric
    print ("Finished one hot encoding")


    #Combine OHE
    #train_x_final = pd.concat([train_x,ohe_rest], axis=1)
    train_x_final = ohe_rest
    print ("Now converting to numeric.")
    cols = ["Appraisal_Year","Sequence_No","Land_Value", "Improvement_Value", "Total_Value", "Garage_Capacity","Num_Bedrooms", "Num_Bathrooms", "Year_Built", "Living_Area","Land_Acres", "Land_SqFt", "Ag_Acres", "Ag_Value","Structure_Count","Appraised_Value","redfinSoldPrice", "redfinSqft"]
    train_x_final[cols] = train_x[cols].apply(pd.to_numeric,errors='coerce')
    print ("Finished converting to numeric.")
    #Output head of data
    print (str(len(train_x_final.index)) + " properties in model.")
    #Split into test and train
    train_x_final.to_csv(r'train_x_final.csv')
    train, test = train_test_split(train_x_final,test_size=0.2,random_state=42, shuffle=True)
    train_x_final = train.drop(columns=['redfinSoldPrice'],axis=1)
    train_y_final = train['redfinSoldPrice']
    test_x_final = test.drop(columns=['redfinSoldPrice'],axis=1)
    test_y_final = test['redfinSoldPrice']

    xgbooster = xgb.XGBRegressor()
    xgbooster.fit(train_x_final,train_y_final)
    predictions = xgbooster.predict(test_x_final)
    predictionSeries = pd.Series(predictions)
    predictionSeries.to_csv(r'predictions.csv')
    test_y_final.to_csv(r'test_y_final.csv')
    print("Explained variance score: " + str(explained_variance_score(test_y_final,predictions)))
    print("Mean absolute error: " + str(mean_absolute_error(test_y_final,predictions)))
    print("R2 score: " + str(r2_score(test_y_final,predictions)))
    print("Mean squared error: " + str(mean_squared_error(test_y_final,predictions)))

def testing():
    pfLocal = propertyFrame
    pfLocal= pfLocal.replace("N/A",np.NaN)
    print (pfLocal.redfinSoldPrice.notnull())
    print (pfLocal.head(5))
    print (pfLocal.redfinSoldPrice)
    print (pfLocal.redfinSoldPrice.dtypes)

# Model to determine factors that cause large gap between Redfin sale and appraised value

# Menus
# SET WORKING DIRECTORY HERE
os.chdir('C:/Users/Thomas/Desktop/FortWorthRealEstateData')
print ("Working directory is: " + os.getcwd())

# First menu
while (userChoice!='0'):
    print ("\nSelect your choice from the menu (e.g. '2'):\n1: Load properties into program from previously saved pickle\n2: Load properties into program from TAD CSV\n3: Merge Redfin file with TAD data\n4: Export properties to pickle\n0: Done manipulating data, move on to next menu.\n")
    userChoice=input()
    if (userChoice=='1'):
        print ("\nLoading properties from pickle...\n")
        importPickle()
    elif (userChoice=='2'):
        print ("\nLoading properties from CSV...\n")
        loadProperties()
    elif (userChoice=='3'):
        print ("Merging Redfin data with TAD data...")
        redfinImport()
    elif (userChoice=='4'):
        print ("\nExporting properties to pickle...\n")
        exportPickle()

    elif (userChoice=='0'):
        print ("\n")
    else:
        print("You entered: " + userChoice + ". That was not a valid option, please try again.\n")
userChoice = 1

# Second menu
while (userChoice!='0'):
    print("\nSelect your choice from the menu (e.g. '2'):\n1: Print all data on a property.\n2: Print summary of a property.\n3: Print first five rows of property data.\n4: Run XGBoost on data to predict Redfin sale price based on all other\n0: Quit program.\n")
    userChoice=input()
    if (userChoice=='1'):
        print("\nPlease enter address to search: \n")
        searchTerm=input()
        printAddressData(searchTerm)
    elif (userChoice=='2'):
        print ("\nPlease enter an address to search: \n")
        searchTerm=input()
        printAddressSummary(searchTerm)
    elif (userChoice=='3'):
        print (propertyFrame.head(5))
    elif (userChoice=='4'):
        letsBoost()
    elif (userChoice=='42'):
        testing()
    elif (userChoice=='0'):
        print ("Goodbye!\n")
    else:
        print("You entered: " + userChoice + ". That was not a valid option, please try again.\n")

        