import numpy as np
from sklearn.cluster import KMeans
import csv
import os
import pickle

class ModelGenerator:
	def __init__(self, training_dataset, n_groups, n_clusters, max_iters=1000):
		self.training_dataset = training_dataset
		self.n_groups = n_groups
		self.n_clusters = n_clusters
		self.max_iters = max_iters

	def create(self):
		""" Create and save model.
		"""
		preprocessed_train_embs = self.preprocessing()

		kmeans = []
		num_data_points = self.training_dataset.shape[0]
		labels = np.zeros((num_data_points, self.n_groups))

		directory = './encode_results/encode_' + str(self.n_groups) + 'groups_' \
		                 + str(self.n_clusters) + 'clusters'
		kmeans_model_name = 'kmeans_models.pckl'
		kmeans_models_path = directory + '/' + kmeans_model_name

		if not os.path.exists(kmeans_models_path):
		    for i in range(len(preprocessed_train_embs)):
		        group_i = preprocessed_train_embs[i]
		        kmeans_i = KMeans(n_clusters=self.n_clusters, max_iter=self.max_iters, n_jobs=-1)
		        label_i = kmeans_i.fit_predict(X=group_i)
		        kmeans.append(kmeans_i)
		        labels[:, i] = label_i

		encoded_string_list = []
		for i in range(num_data_points):
		    encoded_string_i = []
		    for j in range(self.n_groups):
		        encoded_string_ij = 'position' + str(int(j + 1)) + 'cluster' + str(int(labels[i, j]))
		        encoded_string_i.append(encoded_string_ij)

		    encoded_string_list.append(encoded_string_i)

		return kmeans, encoded_string_list

	def save_results(self, kmeans, encoded_string_list):
	    csv_file_name = 'encoded_string_' + str(self.n_groups) + 'groups_' + str(self.n_clusters) + 'clusters.csv'

	    directory_name = './encode_results/encode_' + str(self.n_groups) + 'groups_' \
	                     + str(self.n_clusters) + 'clusters'

	    if not os.path.exists(directory_name):
	        os.makedirs(directory_name)

	    csv_file_name_path = directory_name + '/' + csv_file_name

	    if not os.path.exists(csv_file_name_path):
	        with open(directory_name + '/' + csv_file_name, "w",
	                  newline="") as f:
	            writer = csv.writer(f)
	            writer.writerows(encoded_string_list)

	    kmeans_model_name = 'kmeans_models.pckl'
	    kmeans_model_name_path = directory_name + '/' + kmeans_model_name

	    if not os.path.exists(kmeans_model_name_path):
	        with open(kmeans_model_name_path, "wb") as f:
	            for kmean in kmeans:
	                pickle.dump(kmean, f)


	def preprocessing(self):
		dimension = self.training_dataset.shape[1]
		group_dimension = int(dimension / self.n_groups)
		preprocessed_embs_vector = []

		for group_id in range(self.n_groups):
		    a = group_id * group_dimension
		    b = (group_id + 1) * group_dimension

		    group_i = self.training_dataset[:, a:b]
		    preprocessed_embs_vector.append(group_i)

		return preprocessed_embs_vector

	def run_encode_data(self):
		print('start to encode with {} groups and {} clusters'.format(self.n_groups, self.n_clusters))

		preprocessed_train_embs = self.preprocessing()
		kmeans, encoded_string_list = self.create()
		self.save_results(kmeans, encoded_string_list)


def main():
	training_dataset = np.load('train_embs.npy')

	num_groups = [8, 16, 32, 64]
	num_clusters = [n_clusters for n_clusters in range(8, 33)]
	max_iters = 1000

	for num_groups in num_groups:
		for num_clusters in num_clusters:
		    model_generator = ModelGenerator(
		    	training_dataset=training_dataset,
		    	n_groups=num_groups,
		    	n_clusters=num_clusters,
		    	max_iters=max_iters,
		    	)
		    model_generator.run_encode_data()

if __name__ == '__main__':
	main()







