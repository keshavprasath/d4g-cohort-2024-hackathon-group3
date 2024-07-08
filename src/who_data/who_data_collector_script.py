from owid import catalog
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
folder_path = './csv'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
KEY_FILE_PATH = 'REPLACE WITH FILE PATH TO LOCATION OF KEY'
GOOGLE_SPREADSHEET_ID = 'PLEACE WITH ID OF GSPREAD'

def load_who_data(data_source_string, dataset_filter):
    # mortality rate per country estimation
    results = catalog.find("malaria")
    if dataset_filter is None:
        df = results.loc[results['table'] == data_source_string].load()
    else:
        df = results.loc[(results['table'] == data_source_string) & (results["dataset"] == dataset_filter)].load()
    return df

def export_to_csv_and_read_to_df(df, filename):
    df.to_csv(f'to_upload/{filename}.csv', sep=',', index=True, encoding='utf-8')
    pd_df = pd.read_csv (f'to_upload/{filename}.csv')
    return pd_df

def add_data_to_google_sheet(df, filename):
    credentials = Credentials.from_service_account_file(KEY_FILE_PATH, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    gs = gc.open_by_key(GOOGLE_SPREADSHEET_ID)
    ws = gs.worksheet(f'{filename}')
    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=df, include_column_header=True,include_index=True, resize=True)

if __name__ == '__main__':   
    data_sources = [
        {"name" :"estimated_malaria_mortality_rate__per_100_000_population", "dataset": None},
        {"name": "estimated_number_of_malaria_deaths", "dataset": None},
        {"name":"estimated_number_of_malaria_cases", "dataset": None},
        {"name": "malaria__both_sexes__1_4_years","dataset": "gbd_child_mortality"},
        {"name":"malaria__both_sexes__lt_1_year", "dataset": "gbd_child_mortality"},
    ]
    for source in data_sources:
        df = load_who_data(data_source_string=source["name"],dataset_filter=source["dataset"] )
        print(df.head())
        pd_df = export_to_csv_and_read_to_df(df = df, filename=source["name"])
        add_data_to_google_sheet(df=df, filename=source["name"])
