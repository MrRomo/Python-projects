
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans

X, Y = make_blobs(n_samples=700,centers=8,random_state=1)
plt.scatter(X[:, 0], X[:, 1], s=50)
kMeans = KMeans(n_clusters=4)
kMeans.fit(X)
y_kMeans = kMeans.predict(X)
centers = kMeans.cluster_centers_
print(centers)
plt.scatter(X[:, 0], X[:, 1], c=y_kMeans,cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black',s=200,alpha=0.5)
plt.show()