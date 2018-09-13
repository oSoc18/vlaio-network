"""
This example will insert all companies from an excel file
"""
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'vlaio_prototype.settings'
import django

# before importing any model
django.setup()

from . import insert_companies_from_file, get_dataframe

file_path = "D:\\Downloads\\companies.xlsx"

insert_companies_from_file(file_path)
