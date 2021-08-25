#!/usr/bin/python
"""
This script can be run as :
    $ python main.py
If the user would like to add a zipcode parameter then use something like:
    $ python main.py xxxxx
where xxxxx is a 5 digit zipcode.

This script has been written in Python 3.8 using PyCharm IDE on a Windows 10 machine.
"""

import sys
import csv

"""Path to all 3 csv files"""
path_to_slcsp = "slcsp.csv"
path_to_zips = "zips.csv"
path_to_plans = "plans.csv"

"""List of error messages"""
err_msg_bad_zipcode = f"""Please check to make sure zipcode is of 5 digits.
This zipcode is invalid:"""
err_msg_file_path_error = "Check file path for zips.csv or plans.csv or slcsp.csv are valid"
err_msg_file_error = "Check if file is accessible:"


def read_data(data_path_to_zips):
    """Read data from zips.csv file."""
    try:
        with open(data_path_to_zips) as data_zips_csv:
            data = list(csv.reader(data_zips_csv))[1:]
    except OSError as e:
        print(err_msg_file_path_error)
        print(e)
        sys.exit(1)
    return data


def dedup_zips(zips):
    """
    De-duplicate all the zipcodes.
	If there are multiple zipcodes then create a seperate list for them since we need to leave those from the calculations.
    Disregard columns 2 and 3 from the zips.csv file because we do not need county_code or name at this time.
	"""

    zips = set([(zipcode[0], zipcode[1], zipcode[4]) for zipcode in zips])
    included_zips = set()
    unique_zips = dict()
    duplicate_zips = set()
    for zipcode in zips:
        if zipcode[0] in included_zips:
            duplicate_zips.add(zipcode[0])
        else:
            included_zips.add(zipcode[0])
            #           zipcode        state        rate_area
            unique_zips[zipcode[0]] = [zipcode[1], zipcode[2]]
    return unique_zips, duplicate_zips


def sort_all_plans(all_plans):
    """
    Find unique rates for only Silver metal plan type. Return only the state, rate and rate_area combination values.
    """
    return set([(plans_col[1], plans_col[3], plans_col[4])
                for plans_col in all_plans
                if plans_col[2] == "Silver"])

def get_slcsp(zipcode, unique_zips, duplicate_zips, all_plans):
    """Based on the 2 lists that have been created, find the 2nd lowest rate for the given zipcode."""
    rate = ""
    if zipcode not in duplicate_zips:
        zipcode_info = unique_zips[zipcode]
        rates = [float(plan[1]) for plan in all_plans  # rate
                 if plan[0] == zipcode_info[0]  # state
                 and plan[2] == zipcode_info[1]]  # rate_area
        if len(rates) > 1:
            rate = format(round(sorted(rates)[1], 2), ".2f")
    return [zipcode, rate]


def find_print_slcsp(arguments):
    zips = read_data(path_to_zips)
    list_of_zips = set([zipcode[0] for zipcode in zips])
    unique_zips, duplicate_zips = dedup_zips(zips)
    plans = read_data(path_to_plans)
    plans = sort_all_plans(plans)
    if len(arguments) > 1:
        slcsp = [[arguments[1], ""]]
    else:
        slcsp = read_data(path_to_slcsp)
    slcsp_rates = []
    print("zipcode,rate")

    for zip_rate in slcsp:
        """Make sure zipcode is 5 digits"""
        if len(zip_rate[0]) != 5 or not zip_rate[0].isdigit():
            print(err_msg_bad_zipcode, zip_rate[0])
            sys.exit(2)
        if zip_rate[0] in list_of_zips:
            output = get_slcsp(zip_rate[0], unique_zips, duplicate_zips,
                               plans)
        else:
            output = [zip_rate[0], ""]
        slcsp_rates.append(output)
    for row in slcsp_rates:
        print(f"{row[0]},{row[1]}")

if __name__ == "__main__":
    find_print_slcsp(sys.argv)