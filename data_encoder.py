import numpy as np
from sklearn.cluster import KMeans
import csv
import os
import pickle

class DataEncoder:

    def __init__(self, num_groups=16, num_clusters=20):
        self.num_groups = num_groups
        self.num_clusters = num_clusters


    def preprocess(self):
        """ subdivide embedding vector into groups for clustering
        """

        dimension = self.embs_vector.shape[1]
        group_dimension = int(dimension / self.num_groups)
        preprocessed_embs_vector = []
       
        for group_id in range(self.num_groups):
            a = group_id * group_dimension
            b = (group_id + 1) * group_dimension

            group_i = self.embs_vector[0, a:b]
            preprocessed_embs_vector.append(group_i)

        return preprocessed_embs_vector


    def encode(self, embs_vector):
        """ Genterate encoded string tokens
        """

        self.embs_vector = embs_vector

        preprocessed_embs_vector = self.preprocess()

        # Load kmeans model for encoding.
        kmeans = []
        kmeans_model_path = "models/kmeans_" + str(self.num_groups) + "groups_" + \
                            str(self.num_clusters) + "clusters_" + "model/subvector"
        for group in range(self.num_groups):
            with open(kmeans_model_path + str(group + 1) + '.pckl', "rb") as f:
                kmeans.append(pickle.load(f))

        ############## Clustering ##############
        # Predict cluster for each subvector
        subvector_clusters = []
        for i in range(self.num_groups):
            group = preprocessed_embs_vector[i]
            label = kmeans[i].predict(X=group.reshape((1, -1)))
            subvector_clusters.append(label)

        ############# Tokenize ################
        string_tokens = []
        for idx in range(self.num_groups):
            string_tokens.append( "position" + str(idx + 1) + "cluster" + str(subvector_clusters[idx][0]) )

        return string_tokens
