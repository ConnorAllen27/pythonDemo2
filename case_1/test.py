
import os
from google.cloud import storage
import pathlib
import sys
import argparse
import inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from test_functions import *


currentDirectory = str(pathlib.Path().absolute())

f = open('case_1//pInfo.txt','r')
lines = f.readlines()
values = {}
for line in lines:
    line = line.strip()
    info = line.split(":")
    values[info[0]] = info[1]

fileName = values['id'] + "_extract"
#fileName = "17748_extract"
print(fileName)
extract = get_blob('', 'extracts/'+ fileName)  # getting extract



def test_FHIR():
    fhirSTD = verify_extract(extract)
    assert fhirSTD == True


# Testing Resources
def test_patient_exists():
    Patients = findResources(extract, 'Patient')
    assert Patients == 1


def test_pract_exists():
    Practitioners = findResources(extract, 'Practitioner')
    assert Practitioners != 0


def test_CareTeam_exists():
    CareTeams = findResources(extract, 'CareTeam')
    assert CareTeams == 1


def test_practRole_exists():
    PractitionerRoles = findResources(extract, 'PractitionerRole')
    assert PractitionerRoles != 0


# Patient Tests
def test_id():
    id_exists = checkField(extract, 'Patient', 'id', values['id'])
    assert id_exists == 1


def test_line():
    line_exists = checkField(extract, 'Patient', 'line', values['addressValue'])
    assert line_exists == 1


def test_postal():
    postal_exists = checkField(extract, 'Patient', 'postalCode', values['postalCodeValue'])
    assert postal_exists == 1


def test_state():
    prov = format_prov(values['provinceValue'])
    prov_exists = checkField(extract, 'Patient', 'state', prov)
    assert prov_exists == 1


def test_city():
    city_exists = checkField(extract, 'Patient', 'city', values['cityValue'])
    assert city_exists == 1


def test_birth():
    newDate = format_DOB(values['DOB'])
    birth_exists = checkField(extract, 'Patient', 'birthDate', newDate)
    assert birth_exists == 1


def test_phone():
    newPhone = format_phone(values['areaCode'], values['number'], values['ext'])
    phone_exists = checkField(extract, 'Patient', 'value', newPhone)
    assert phone_exists == 1


def test_Pract_pri_name():
    names = format_name(values['primaryProviderValue'])
    names_pri_exists = 0
    names_pri_exists += checkField(extract, 'Practitioner', 'given', names[0])
    names_pri_exists += checkField(extract, 'Practitioner', 'family', names[1])
    assert names_pri_exists == 2


def test_Pract_sec_name():
    names = format_name(values['secondaryProviderValue'])
    names_sec_exists = 0
    names_sec_exists += checkField(extract, 'Practitioner', 'given', names[0])
    names_sec_exists += checkField(extract, 'Practitioner', 'family', names[1])
    assert names_sec_exists == 2


def test_Pract_fam_name():
    names = format_name(values['familyProviderValue'])
    names_fam_exists = 0
    names_fam_exists += checkField(extract, 'Practitioner', 'given', names[0])
    names_fam_exists += checkField(extract, 'Practitioner', 'family', names[1])
    assert names_fam_exists == 2
