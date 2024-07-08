from owid import catalog
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
folder_path = './csv'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def load_who_data():
    # mortality rate per country estimation
    results = catalog.find("malaria")
    mortality_rate = results.loc[results['table'] == "estimated_malaria_mortality_rate__per_100_000_population"].load()
    # estimated deaths per country
    results = catalog.find("malaria")
    deaths = results.loc[results['table'] == "estimated_number_of_malaria_deaths"].load()

    # estimated incidence per country
    results = catalog.find("malaria")
    incidence = results.loc[results['table'] == "estimated_number_of_malaria_cases"].load()

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

    return mortality_rate, deaths, incidence, malaria__both_sexes__1_4_years, malaria__both_sexes__lt_1_year


def import_csv_to_google_sheets():
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
    #add in file path to credentials json below
    credentials = Credentials.from_service_account_file('gdi-ersilia-hackathon-2024-92eba4d03199.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            sheet_title = os.path.splitext(filename)[0]
            print(sheet_title)
            spreadsheet = gc.open(f'who_{sheet_title}_data')
            with open(f'./csv/{filename}', 'r') as file_obj:
                content = file_obj.read()
                gc.import_csv(spreadsheet.id, data=content)

if __name__ == '__main__':   
    mortality_rate, deaths, incidence, malaria__both_sexes__1_4_years, malaria__both_sexes__lt_1_year = load_who_data()
    incidence.to_csv('to_upload/incidence.csv', sep=',', index=True, encoding='utf-8')
    df_incidence = pd.read_csv ('to_upload/incidence.csv')
    malaria__both_sexes__1_4_years.to_csv('to_upload/malaria__both_sexes__1_4_years.csv', sep=',', index=True, encoding='utf-8')
    df_malaria__both_sexes__1_4_years = pd.read_csv ('to_upload/malaria__both_sexes__1_4_years.csv')
    malaria__both_sexes__lt_1_year.to_csv('to_upload/malaria__both_sexes__lt_1_year.csv', sep=',', index=True, encoding='utf-8')
    df_malaria__both_sexes__lt_1_year = pd.read_csv ('to_upload/malaria__both_sexes__lt_1_year.csv')
    deaths.to_csv('to_upload/deaths.csv', sep=',', index=True, encoding='utf-8')
    df_deaths = pd.read_csv ('to_upload/deaths.csv')
    mortality_rate.to_csv('to_upload/mortality_rate.csv', sep=',', index=True, encoding='utf-8')
    df_mortality_rate = pd.read_csv ('to_upload/mortality_rate.csv')

    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
    #add in file path to credentials json below
    credentials = Credentials.from_service_account_file('../../.env/gdi-ersilia-hackathon-2024-92eba4d03199.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    gs = gc.open_by_key("1GiDcGDfv4tdScHQJNpadeB0ajlkQAvO2kJlGkNe6_zE")
    incidence_ws = gs.worksheet('incidence_ws')
    incidence_ws.clear()
    set_with_dataframe(worksheet=incidence_ws, dataframe=df_incidence, include_column_header=True, resize=True)

    malaria__both_sexes__1_4_years_ws = gs.worksheet('malaria__both_sexes__1_4_years_ws')
    malaria__both_sexes__1_4_years_ws.clear()
    set_with_dataframe(worksheet=malaria__both_sexes__1_4_years_ws, dataframe=df_malaria__both_sexes__1_4_years, include_column_header=True, resize=True)

    malaria__both_sexes__lt_1_year_ws = gs.worksheet('malaria__both_sexes__lt_1_year_ws')
    malaria__both_sexes__lt_1_year_ws.clear()
    set_with_dataframe(worksheet=malaria__both_sexes__lt_1_year_ws, dataframe=df_malaria__both_sexes__lt_1_year, include_column_header=True, resize=True)

    deaths_ws = gs.worksheet('deaths_ws')
    deaths_ws.clear()
    set_with_dataframe(worksheet=deaths_ws, dataframe=df_deaths, include_column_header=True, resize=True)

    mortality_rate_ws = gs.worksheet('mortality_rate_ws')
    mortality_rate_ws.clear()
    set_with_dataframe(worksheet=mortality_rate_ws, dataframe=df_mortality_rate, include_column_header=True, resize=True)
