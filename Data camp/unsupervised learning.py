"""from sklearn.preprocessing import StandardScaler
sample = []
scaler = StandardScaler()

scaler.fit(sample)
StandardScaler(copy=True,with_std=True,with_mean=True)
samples_scaled = scaler.transform(sample)"""

## ANOTHER METHOD
samples = []

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans as km

scaler = StandardScaler()
kmeans = km(n_clusters=3)

from sklearn.pipeline import make_pipeline

pipeline = make_pipeline(scaler,kmeans)
pipeline.fit(samples)

labels = pipeline.predict(samples)

#other preprocessing methods of sklearn are MaxAbsScaler and Normalizer

