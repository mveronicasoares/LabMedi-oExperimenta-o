import requests

headers = {"Authorization": "token d9eff5073950ceffc4ff93f1a49666b780fcba73"}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
{
  search (query:"stars:>100",
  				type: REPOSITORY, first:100) {
    	nodes {
        ... on Repository {
          nameWithOwner
        }
      }
  }
}"""

print (query)