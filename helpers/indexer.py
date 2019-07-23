import sys
import json
from elasticsearch.helpers import bulk

sys.path.append('..')
import es_connector as ES_Connector

class Indexer:
	""" Index documents to Elasticsearch.

	Using this class for CREATING, INDEXING and UPDATING to your Elastic server.

	"""
	
	def __init__(self, doc_, host, port, index_name='face_off', op_type='index', metadata=None):
		""" Constructor

		Params:
		-------
		metadata: dict
			The argument is just used for validating hyperparam k-means.

		doc_: list[str]
			Json-format string (so-called document in Elasticsearch).
			Your data (json) is placed here.
		
		host: str
			Elastic server's host infomation to connect
		
		port: int
			Elastic server's port information to connect

		index_name: str
			Name of index for indexing.
		
		op_type: str
			Operation type for bulk api.

		"""

		self.metadata = metadata
		self.json_file = doc_
		self.op_type = op_type

		# Connect to Elastic server before any communication.
		self.es = ES_Connector.connect(host, port)


	def index(self):
		""" Index documents to Elastic server.

		"""

		# Just occur for hyperparams validation case.
		if self.metadata != None:
			bulk(self.es, self.gen_data())
		
		# When having just only document.
		else:
			self.es.index(
				index=self.index_name,
				doc_type=doc_,
				body=self.doc_[0] # Due to doc_ is list type.
				)


	def gen_data(self):
		""" Generate json-format string for indexing.

		"""

		# Open file
		with open(self.json_file) as f:
			# json_data: list of dictionaies.
			json_data = json.load(f)

		# Iterate over each element of list to
		# generate json-base documents.
		for idx, document in enumerate(json_data):
			# Convert dict to JSON-based string
			document = json.dumps(document)
			
			# generate each document for indexing
			self.index_name = 'face_off_' + str(self.metadata['n_groups']) + 'groups_' + \
						str(self.metadata['n_clusters']) + 'clusters'
			yield {
				"_index": self.index_name,
				"_type": "_doc",
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
		doc_=json_file,
		host=host,
		port=port,
		metadata=metadata
		)

	indexer.index()

if __name__ == '__main__':
	main()