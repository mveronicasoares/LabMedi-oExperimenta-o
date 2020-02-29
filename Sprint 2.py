import requests
from json import dump
from json import loads
import time

def run_query(json, headers):  

    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    while (request.status_code == 502):
      time.sleep(2)
      request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
      return request.json()
    else:
      raise Exception("Query failed to run by returning code of {}. {}. {}".format(request.status_code, json['query'],json['variables']))

total_pages = 1

query = """
query example{
 search (query:"stars:>100", type:REPOSITORY, first:2{AFTER}) {
    pageInfo{
        hasNextPage
        endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        pullRequests(states: MERGED){
            totalCount
        }
        releases{
          totalCount
        }
        updatedAt
        primaryLanguage{
          name
        }
        closedIssues : issues(states: CLOSED){
          totalCount
        }
        totalIssues: issues{
          totalCount
        }
      }
    }
  }
}
"""

finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

headers = {"Authorization": "Bearer c8a1f8a5de494ed29ab5743af11380a354903034"} 

result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#paginação
while (next_page and total_pages < 500):
    total_pages += 1
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#inserindo cabeçalho de identificação de dados ao csv
with open("ResultadoSprint2.csv", 'a') as the_file:
        the_file.write("nameWithOwner" + ";" + "createdAt" + ";" + "pullRequests/totalCount" + ";" 
        + "releases/totalCount" + ";" + "updatedAt" + ";" + "primaryLanguage/name" + ";" 
        + "closedIssues/totalCount" + ";" + "totalIssues/totalCount""\n")

#salvando os dados em ResultadoSprint2.csv
for node in nodes:
    if node['primaryLanguage'] is None:
            primaryLanguage = "None"
    else:
        primaryLanguage = str(node['primaryLanguage']['name'])
    with open("ResultadoSprint2.csv", 'a') as the_file:
        the_file.write(node['nameWithOwner'] + ";" + node['createdAt'] + ";" + str(node['pullRequests']['totalCount']) + ";"
        + str(node['releases']['totalCount']) + ";" + node['updatedAt'] + ";" + primaryLanguage + ";" + 
        str(node['closedIssues']['totalCount']) + ";" + str(node['totalIssues']['totalCount']) + "\n")