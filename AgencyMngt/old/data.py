import requests
from datapipes.dataio import DataContext

from dotenv import load_dotenv

load_dotenv() # https://pypi.org/project/python-dotenv/

# From Data Lasagne
# source = data_sources[key]
# self.input_objects[key] = DataContext(source)
# self.input_graph += [{'from': key, 'to': source['observers']}]

# name: document_manual
# format: csv
# path: demo
# key: demo
# observers:
#   - Run

curl -X GET -H "X-TrackerToken: $TOKEN" "https://www.pivotaltracker.com/services/v5/epics/5"
curl -X GET "https://www.pivotaltracker.com/services/v5/epics/5?token=VadersToken"

curl -X GET "https://www.pivotaltracker.com/services/v5/projects/2137779?token=41bd1e4b0d4aa3d238af94886c0150a0"

