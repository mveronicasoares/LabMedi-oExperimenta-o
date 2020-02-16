import requests
import json

headers = {"Authorization": "token d9eff5073950ceffc4ff93f1a49666b780fcba73"}


def run_query(query): #Função para usar request.post
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

#Query para retorno da consulta com graphQL contendo os resultados necessários para a prática      
query = """
{
  search (query:"stars:>100",
  				type: REPOSITORY, first:1) {
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
result = run_query(query)
print (result)
#parsed = json.loads(result)
#print (json.dumps(parsed, ident=4))