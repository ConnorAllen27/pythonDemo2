from google.cloud import storage
from modules.STU3.bundle import Bundle
import json
import calendar
import os


def get_blob(bucket_name, source_blob_path):
    """Returns a blob from the bucket bucket_name, stored in source_blob_path."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_path)
    result = blob.download_as_text()
    return result


def verify_extract(extract):
    """Validates the extract using the fhir.resources.STU3 lib"""
    FHIR = True
    try:
        Bundle.parse_raw(extract)
    except Exception as err:
        errs = (str(err)).split("\n")
        i = 0
        for error in errs:
            if 'contained -> 0 -> component -> 0 -> code' in error:
                if 'value is not a valid list (type=type_error.list)' in errs[i + 1]:
                    errs.remove(errs[i + 1])
                    errs.remove(errs[i])
            i += 1
        print(len(errs))
        if len(errs) > 1:
            print(errs)
            FHIR = False
    if FHIR:
        print("Extract is in FHIR(STU3) format")
    return FHIR


def flatten(lst):
    """flatten(lst) consumes a list of anything and flattens it."""
    if len(lst) == 0:
        return lst
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    return lst[:1] + flatten(lst[1:])


def findField(dct, field):
    """consumes a dictionary dct and a string field and searches for field within dct.
    Returns a list, containing the values corresponding to any key named field."""
    out = []

    # findField_list(lst, field) consumes a list lst and a string field and searches for field within lst.
    # Returns a list, containing the values corresponding to any key named field.
    def findField_list(lst, field):
        result = []
        for i in lst:
            if type(i) == dict:
                res = findField(i, field)
                if res is not None:
                    result.append(res)
        return result

    for k in dct:
        if (k == field) and (type(dct[k]) != dict):
            res = dct[k]
            if res is not None:
                out.append(res)
        elif type(dct[k]) == dict:
            res = findField(dct[k], field)
            if res is not None:
                out.append(res)
        elif type(dct[k]) == list:
            res = findField_list(dct[k], field)
            if res is not None:
                out.append(res)
    return out


def checkField(JSONstring, resource, fieldName, fieldIn):
    """consumes JSONstring, the string extract
       resource, a str (the name of the resource to search), fieldName, a str (the name of the field to test), and
       fieldIn, what was entered into fieldName initially"""
    fieldIn = str(fieldIn)
    parsed = json.loads(JSONstring)
    resources = parsed['entry']
    matches = []
    found_match = 0

    for entry in resources:
        if resource in flatten(findField(entry, 'resourceType')):
            matches.append(findField(entry, fieldName))
    matches = flatten(matches)
    for item in matches:
        if str(item) == fieldIn:
            found_match = True
            print('Searched', resource, 'for', fieldName, ':', fieldIn, '",and a match '
                                                                        'was found.')
            return 1
    if not found_match:
        print('***** Searched', resource, 'for', fieldName, ':', fieldIn, '"and no match '
                                                                          'was found. *****')
        print("Found", matches, "Instead")
        return 0


def findResources(JSON, resourceType):
    parsed = json.loads(JSON)
    entries = parsed['entry']
    out = []
    for entry in entries:
        if entry['resource']['resourceType'] == resourceType:
            out.append(resourceType)
    if len(out) == 0:
        print('***** No Resource:', resourceType, "*****")
        return 0
    else:
        print("Found:", len(out), resourceType)
        return len(out)


def format_phone(areaCode, number, ext):
    """format phone to match JSON and test"""
    areaCode = str(areaCode)
    number = str(number)
    ext = str(ext)

    phone_value = str('(' + areaCode + ') ' + number[0:3] + '-' + number[3:] + ' x' + ext)
    return phone_value


def format_DOB(DOB):
    """formatting DOB string to match JSON format"""
    dateSplit = DOB.split("-")
    mon = str(list(calendar.month_abbr).index(dateSplit[1]))
    if len(mon) == 1:
        mon = "0" + mon
    newDate = dateSplit[2] + "-" + mon + "-" + dateSplit[0]
    return newDate


def format_prov(provinceValue):
    """change province name to province abbreviation"""
    provAbrv = {"Alberta": "AB", "British Columbia": "BC", "Manitoba": "MB", "New Brunswick": "NB",
                "Newfoundland and Labrador": "NL", "Northwest Territories": "NT", "Nova Scotia": "NS", "Nunavut": "NU",
                "Ontario": "ON", "Prince Edward Island": "PE", "Quebec (PQ)": "PQ", "Quebec (QC)": "QC",
                "Saskatchewan": "SK"}
    prov = provAbrv[provinceValue]
    return prov


def format_name(providerName):
    if len(providerName.split(', ')) == 2:
        nameSplit = providerName.split(', ')
        familyName = nameSplit[0]
        givenName = nameSplit[1]
        if len(givenName.split(" ")) == 2:
            givenName = givenName.split(" ")[0]
    else:
        familyName = providerName
        givenName = providerName
    return [givenName, familyName]


def formatDate(date):
    dateSplit = date.split("-")
    mon = str(list(calendar.month_abbr).index(dateSplit[1]))
    if len(mon) == 1:
        mon = "0" + mon
    newDate = dateSplit[2] + "-" + mon + "-" + dateSplit[0]
    return newDate


def format_Rxn_date(RxnDate):
    RxnDateSplit = RxnDate.split("-")
    RxnMon = str(list(calendar.month_abbr).index(RxnDateSplit[1]))
    if len(RxnMon) == 1:
        RxnMon = "0" + RxnMon
    newDateofRxn = RxnDateSplit[2] + "-" + RxnMon + "-" + RxnDateSplit[0]
    return newDateofRxn


def format_medi_text(freq, count, type, duration, durationUnit, PRNStat):
    freq = freq.split(' ')
    freq = freq[0]
    text = str(count) + " " + type + ", " + freq \
           + ", " + str(duration) + " " + durationUnit
    if PRNStat == "Yes":
        text = text + " PRN"
    return text
