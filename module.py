import requests
import pandas as pd 
import numpy as np 

# Get the works from Open Alex API 

def get_work(id):
    # Get the work object from OpenAlex 
    # URL: https://docs.openalex.org/api-entities/works/work-object 
    # Input: 
    #       - id: str, OpenAlexID 
    # Output:
    #       - response: str, response from the OpenAlex API


    # Have email in header will speed up the request 
    hdr = {'mailto':'ngunamhung@gmail.com'}
    url = f"https://api.openalex.org/works/{id}"

    # Request 
    response = requests.get(url, headers=hdr)
    
    #Returns json object of the response
    return response.json()

def get_cited_url(id):
    # Get the url to request all the citations of a publication 
    # URL: https://docs.openalex.org/api-entities/works/work-object 
    # Input: 
    #       - id: str, OpenAlexID of the publication
    # Output:
    #       - response: str, response from the OpenAlex API, containing all the information of the citations

    # Have email in header will speed up the request 
    hdr = {'mailto':'ngunamhung@gmail.com'}
    url = f"https://api.openalex.org/works/{id}"

    # Request 
    response = requests.get(url, headers=hdr)

    return response.json()['cited_by_api_url']

def get_cited(url):
    # Get the url to request all the citations of a publication 
    # URL: https://docs.openalex.org/api-entities/works/work-object 
    # Input: 
    #       - url: str, the URL got from get_cited_url()
    # Output:
    #       - response: str, response from the OpenAlex API, containing all the information of the citations

     # Have email in header will speed up the request 
    hdr = {'mailto':'ngunamhung@gmail.com'}


    # Form the URL and request the citations
    new_url = f"{url}&per-page=200"
    response = requests.get(new_url, headers=hdr).json()

    # Check if the work has more than 200 citations, if so, get all
    if response['meta']['count'] > 200:
        count_page = np.ceil(response['meta']['count'] / 200.0)
        count = 2
        while count <= count_page:

            # Form new URL request for next page
            new_url = f"{url}&per-page=200&page={int(count)}"
            new_response = requests.get(new_url, headers=hdr).json()

            # Append the new results into the current results
            response['results'] = response['results'] + new_response['results']

            # Next page
            count += 1
    
    return response

def get_citation_info(response):
    # Extract the information from get_cited()
    # Input: 
    #       - response: str, the response got from get_cited()
    # Output:
    #       - infoDict: dict, information of the citations, in the form of 
    #         infoDict[CITATION NAME] = (SDG NAME, SCORE, PUBLICATION DATE, TOPIC)

    # Innitialise
    infoDict = {}

    # If response is invalid, return empty dictionary
    try:
        results = response['results']
    except:
        return infoDict
    
    # If there is no citation, return empty dictionary
    if len(results) == 0:
        return infoDict
    else:
        for citation in results:
            name = citation['display_name']
            sdg = citation["sustainable_development_goals"]
            if len(sdg) == 0:
                infoDict[name] = (None, None, citation['publication_date'], citation["primary_topic"]['display_name'])
            else:
                infoDict[name] = (sdg[0]['display_name'], sdg[0]['score'], citation['publication_date'], citation["primary_topic"]['display_name'])
        
    return infoDict


def get_author_info(response):
    # Extract the geographical information of the authors/researchers from get_cited()
    # Input: 
    #       - response: str, the response got from get_cited()
    # Output:
    #       - authorDict: dict, information of the citations, in the form of 
    #         authorDict[CITATION NAME] = (INSTUTITE NAME, AUTHOR COUNTRY CODE, AUTHOR, AUTHOR ID)

    authorDict = {}

    # Check for invalid response
    try:
        results = response['results']
    except:
        return authorDict
    
    # If there is no citation, return empty
    if len(results) == 0:
        return authorDict
    else:
        for citation in results: #Going through all citation
            # Get the name of the citation
            pub_name = citation['display_name']

            # Get the authorship object
            authors = citation['authorships']
            
            counter = 0

            # Going through ALL authors no matter of their position and get the information
            for author in authors:
                if len(author['institutions']) == 0:
                    authorDict[f"{pub_name}_{counter}"] = (None, author['countries'], author['author']['display_name'], author['author']['id'])
                else:
                    institute_name = author['institutions'][0]['display_name']
                    authorDict[f"{pub_name}_{counter}"] = (institute_name, author['institutions'][0]['country_code'], author['author']['display_name'], author['author']['id'])
                counter += 1
    
    return authorDict
