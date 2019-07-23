import sys
sys.path.append("..")

from helpers.indexer import Indexer

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


if __name__ == "__main__":
	main()