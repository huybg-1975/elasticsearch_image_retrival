import numpy as np
import argparse
import csv
import json
import math
import logging

import sys
sys.path.append("..")

import es_connector as ES_Connector
from data_encoder import DataEncoder as Encoder

class Searcher():
	def __init__(self, es_client, embed_vector, n_groups, n_clusters, num_searches=20, top_K=5):
		self.embed_vector = embed_vector
		self.n_groups = n_groups
		self.n_clusters = n_clusters
		self.num_searches = num_searches
		self.top_K = top_K
		self.es_client = es_client


	def search(self, top_K=None):
		if top_K != None:
			self.top_K = top_K

		if self.top_K > self.num_searches:
			raise Exception("`top_K` argument need to less than or equal ")

		########### ENCODE ##########
		encoder = Encoder()
		string_tokens = encoder.encode(self.embed_vector)

		string_tokens_chunks = list()
		for i in range(encoder.num_groups):
			sub_field = {
				"filter": {
					"term": {
						"string_token": string_tokens[i]
					}
				},
				"weight": 1
			}

			string_tokens_chunks.append(sub_field);

		# RETRIEVE ONLY
		request_body = {
			"size": self.num_searches,
			"query": {
				"function_score": {
					"functions": string_tokens_chunks,
					"score_mode": "sum",
					"boost_mode": "replace"
				}
			}
		}

		############ QUERY #############
		index_name = "face_off_" + str(self.num_groups) + "groups" + str()
		res = ES_client.search(index="face_off", body=request_body)
		
		# Print some results in console for debugging.
		logging.debug(json.dumps(res, indent=2))

		############ RE-RANK ############
		vectors = []
		for i in range(s):
			embed_vector = res['hits']['hits'][i]['_source']['embedding_vector']
			id_ = res['hits']['hits'][i]['_id']

			# Convert to numpy array for reranking.
			embed_vector = np.array(embed_vector).reshape((1, -1))
			vectors.append(dict({
					'vector': embed_vector,
					'id': id_,
					'dist': 0
				}))
		
		self.rerank(vectors, anchor_vector=query_vector)
		top_id = [vector['id'] for vector in vectors]

		ret = []
		objs = res['hits']['hits']
		for id_ in top_id:
			for obj in objs:
				if obj['_id'] == id_:
					ret.append(obj)
					break

		return ret[:self.top_K]


	def rerank(self, vectors, anchor_vector):
		s = len(vectors)
		for i in range(s):
			# Compare distance between two vector
			# using *Euclided distance* by default.
			dist = get_distance(vectors[i]['vector'], anchor_vector)
			vectors[i]['dist'] = dist
		
		# Ascending sort.
		vectors.sort(key=lambda x: x['dist'])


	def get_distance(self, vector1, vector2, metric='Euclidean'):
		if metric == 'Euclidean':
			return math.sqrt(np.sum((vector2 - vector1)**2))


def logger_config(level):

	es_logger = logging.getLogger('elasticsearch')
	urllib_logger = logging.getLogger('urllib3')
	
	es_logger.setLevel(logging.WARNING)
	urllib_logger.setLevel(logging.WARNING)

	logging.basicConfig(level=level)


def main():

	logger_config(level=logging.WARNING)

	# Elasticsearch client.
	host = "localhost"
	port = 9200
	es = ES_Connector.connect(host, port)

	# Query vector for testing purpose.
	model_folder_path = "../hyperparams_training_data/"
	embedding_vectors = np.load(model_folder_path + "train_embs.npy")

	# Get i-th Embedding vector for searching.
	i = 1
	query_vector = np.expand_dims(embedding_vectors[i], axis=0)

	# Search
	searcher = Searcher(es, query_vector, n_groups=16, n_clusters=20)
	objs = searcher.search()


if __name__ == "__main__":
	main()













