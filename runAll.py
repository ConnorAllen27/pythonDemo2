import datetime
import os
from selenium.webdriver import DesiredCapabilities
import names
import test_functions
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from datetime import date
import pathlib
from google.cloud import storage
from datetime import datetime
from google.cloud import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import sys
import argparse




#CHOOSE WHICH ONES YOU WANT TO RUN HERE
#tests = [1,2,3,4,5,6,7,8]
tests = [1]


#Deleting the old extracts

currentDirectory = str(pathlib.Path().absolute())




blobs_to_delete = []

#Gets the old extracts
def list_blobs(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        if blob.name.endswith("extract"):
            blobs_to_delete.append(blob.name)

#Deletes the blobs that the previous function got
def delete_blob(bucket_name, blob_name):

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))

list_blobs(bucket_name)
for blob in blobs_to_delete:
    delete_blob(bucket_name,blob)


               
    
#Insert all the data
'''
importing a python file is a safer way to run it
Inserting all at once so we don't have to wait for dataflow after every test case
Have to hard code this because specific names and can't use variables in imports
'''
for test in tests:
    case = "case_" + str(test)
    #arg = "python3 "
    #os.system(arg + case + "\\" + insert_names[test-1])
    if test == 1:
        print("Running Case 1")
        from case_1 import addPatientDemographicsDetails_1
    elif test == 2:
        print("Running Case 2")
        from case_2 import addEncounter_AllergyImmuMedi_2
    elif test == 3:
        print("Running Case 3")
        from case_3 import addEncounter_DiagBillingCondObserv_3
    elif test == 4:
        print("Running Case 4")
        from case_4 import addNonEncounter_CarePlan_4
    elif test == 5:
        print("Running Case 5")
        from case_5 import updateEncounter_Allergy_5
    elif test == 6:
        print("Running Case 6")
        from case_6 import deletePatientEncounter_6
    elif test == 7:
        print("Running Case 7")
        from case_7 import addPatientAppointmentsImmunization_7
    elif test == 8:
        print("Running Case 8")
        from case_8 import addPatient_AllergyConfidential_8
        


'''
Trigger the Delta 
'''
import testDateChange

#Wait for MA->mongo delta
#Takes at most 5 mins for it to trigger and run
time.sleep(300)

#Wait for mongo-> mirth poll
#Mirth polls new data every 5 mins
time.sleep(300)

#Run all test tests
for test in tests:
    case = " case_" + str(test)
    arg = "pytest" + case + "//" + "test.py " + "--html=report_" + str(test) + ".html"
    print(str(pathlib.Path().absolute()))
    os.system(arg)



os.system("python3 getReports.py")

