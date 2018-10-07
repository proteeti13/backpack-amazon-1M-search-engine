from selenium.webdriver.chrome.options import Options
import json
import elastic
from pprint import pprint


def search_record(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    pprint(res)



if __name__ == '__main__':
  elastic_search = elastic.connect_elasticsearch()
  
  if elastic_search is not None:
      search_object = {'query': {'match': {'title': 'cube'}}}            ####search record with  search_text = "cube"
      search_record(elastic_search, 'amazon', json.dumps(search_object))

      search_by_same_prefix = {'query': {'prefix': {'title': 'he'}}}
      search_record(elastic_search, 'amazon', json.dumps(search_by_same_prefix))     ### search record with title having same prefix = "he" ; helmet,headphone

      search_by_price = {'_source': ['title'], 'query': {'range': {'price': {'gte': 2000}}}}
      search_record(elastic_search, 'amazon', json.dumps(search_by_price))   #### search record with price >2000
