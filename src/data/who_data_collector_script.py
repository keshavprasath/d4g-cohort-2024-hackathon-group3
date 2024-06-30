from owid import catalog
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# mortality rate per country estimation
results = catalog.find("malaria")
df_mortality_rate = results.loc[results['table'] == "estimated_malaria_mortality_rate__per_100_000_population"].load()
df_mortality_rate.head()

# estimated deaths per country
results = catalog.find("malaria")
df_deaths = results.loc[results['table'] == "estimated_number_of_malaria_deaths"].load()
df_deaths.head()

# estimated incidence per country
results = catalog.find("malaria")
df_incidence = results.loc[results['table'] == "estimated_number_of_malaria_cases"].load()
df_incidence.head()
df_incidence.columns

# child mortality <1
results = catalog.find("malaria")
malaria__both_sexes__lt_1_year = results.loc[(results['table'] == "malaria__both_sexes__lt_1_year" ) & (results["dataset"] == "gbd_child_mortality")].load()
malaria__both_sexes__lt_1_year.head()
malaria__both_sexes__lt_1_year.columns = malaria__both_sexes__lt_1_year.columns.str.rstrip('_aged__lt_1_year')
malaria__both_sexes__lt_1_year["age_range"] = '<1 year'

# child mortality 1 to 4 years
results = catalog.find("malaria")
malaria__both_sexes__1_4_years = results.loc[(results['table'] == "malaria__both_sexes__1_4_years" ) & (results["dataset"] == "gbd_child_mortality")].load()
malaria__both_sexes__1_4_years.head()
malaria__both_sexes__1_4_years.columns = malaria__both_sexes__1_4_years.columns.str.rstrip('_aged_1_4_years')
malaria__both_sexes__1_4_years["age_range"] = '1_4 years'

# setting up auth for google sheets 
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

#add in file path to credentials json below
credentials = Credentials.from_service_account_file('', scopes=scopes)

gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# open a google sheet, add in google sheet key below
gs = gc.open_by_key("")
# select a work sheet from its name
ws_child_mortality = gs.worksheet('child_mortality')
ws_child_mortality.clear()
set_with_dataframe(worksheet=ws_child_mortality, dataframe=malaria__both_sexes__lt_1_year, include_index=True,
include_column_header=True, resize=True)

df_values = malaria__both_sexes__lt_1_year.values.tolist()
gs.values_append('child_mortality', {'valueInputOption': 'RAW'}, {'values': df_values})
# saving to google sheets 
df_values = malaria__both_sexes__1_4_years.values.tolist()
gs.values_append('child_mortality', {'valueInputOption': 'RAW'}, {'values': df_values})

##### incidience
ws_incidence = gs.worksheet('incidence')
ws_incidence.clear()
set_with_dataframe(worksheet=ws_incidence, dataframe=df_incidence, include_index=True,
include_column_header=True, resize=True)

df_values = df_incidence.values.tolist()
gs.values_append('incidence', {'valueInputOption': 'RAW'}, {'values': df_values})

##### Deaths
ws_deaths = gs.worksheet('estimated_deaths')
ws_deaths.clear()
set_with_dataframe(worksheet=ws_deaths, dataframe=df_deaths, include_index=True,
include_column_header=True, resize=True)

df_values = df_deaths.values.tolist()
gs.values_append('estimated_deaths', {'valueInputOption': 'RAW'}, {'values': df_values})

##### mortality rate
ws_mortality_rate = gs.worksheet('overall_mortality')
ws_mortality_rate.clear()
set_with_dataframe(worksheet=ws_mortality_rate, dataframe=df_mortality_rate, include_index=True,
include_column_header=True, resize=True)

df_values = df_mortality_rate.values.tolist()
gs.values_append('overall_mortality', {'valueInputOption': 'RAW'}, {'values': df_values})