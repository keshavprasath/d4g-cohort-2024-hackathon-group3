# Automatically update Google Sheets data for Malaria Disease data

This data is stored inside google sheets and these google sheets are automatically updated via the who_data_collector_script.py. 

To run this script succesfully a few things need to be set up. 

## Understanding the OWID python package
The malaria disease data is all sourced using this package. There are a variety of otehr data sources available as well. Documentation for this package can be found [here](https://pypi.org/project/owid-catalog/0.2.3/).

### Credential set up for Google sheets
The steps are well explained in [this blog](https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0). 

Essentially you just need to set up a free GCP project, service account and key as explained above. One thing to note is *DO NOT* push the keyfile to your github repsoitory. Store this securely or consider using something such as [git crypt](https://dev.to/heroku/how-to-manage-your-secrets-with-git-crypt-56ih). 

### Automating running this python script via github actions
To automate the running of this script our advice would be to utilise the free credits available for use with github actions. This is likely something Ersilia may already have a blueprint for but if not, [this guide here](https://www.python-engineer.com/posts/run-python-github-actions/) has a great walkthrough!
