import sys
import json
from elasticsearch.helpers import bulk

sys.path.append('..')
import es_connector as ES_Connector

class Indexer:
	def __init__(self, metadata: dict, json_file: str, host: str, port: int):
		self.metadata = metadata
		self.json_file = json_file

		self.es = ES_Connector.connect(host, port)


	def index(self):
		bulk(self.es, self.gen_data())


	def gen_data(self):
		# Open file
		with open(self.json_file) as f:
			# json_data: list of dictionaies.
			json_data = json.load(f)

		for idx, document in enumerate(json_data):
			# Convert dict to JSON-based string
			document = json.dumps(document)
			
			# generate each document for indexing
			index_name = 'face_off_' + str(self.metadata['n_groups']) + 'groups_' + \
						str(self.metadata['n_clusters']) + 'clusters'
			yield {
				"op_type": "index",
				"_index": index_name,
				"_type": "_doc",
				# "_id": str(idx),
				"_source": document
			}

def main():
	# Elasticsearch's info
	host = 'localhost'
	port = 9200

	n_groups = 8
	n_clusters = 8
	metadata = dict({
			'n_groups': n_groups,
			'n_clusters': n_clusters
		})
	json_file = 'encode_results/' + \
				'encode_8groups_8clusters/' + \
				'encode_8groups_8clusters.json'
	indexer = Indexer(
		metadata=metadata,
		json_file=json_file,
		host=host,
		port=port,
		)

	indexer.index()

if __name__ == '__main__':
	main()