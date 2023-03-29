# Mastering Unsupervised Anomaly Detection

20 Top Algorithms, Evaluation Metrics and Python Libraries
(adapted from LinkedIn post ~2023-03-28)

## Anomaly Detection

Unsupervised anomaly detection refres to identifying rare or abnormal instances in data without prior knowledge of what constitutes an anomaly, also called Novelty Detection

Scikit-Learn

* Density-based spatial clustering of applications with noise (DBSCAN)
* Isolation Forest
* Local Outlier Factor (LOF)
* One-Class Support Vector Machines (SVM)
* Principal Componet Analysis (PCA)
* Gaussian Mixture Model (GMM)

Keras/TensorFlow

* Autoencoder

Hmmlearn

* Hidden Markov Models (HMM)

PyOD

* Local Correlation Integral (LCI)
* Histogram-based Outlier Detection (HBOS)
* Angle-based Outlier Detection (ABOD)
* Clustering-Based Local Outlier Factor (CBLOF)
* Minimum Covariance Determinant (MCD)
* Stochastic Outlier Selection (SOS)
* Spectral Clustering for Anomaly Detection (SpectralResidual)
* Feature Bagging
* Average KNN
* Connectivity-based Outlier Factor (COF)
* Variational Autoencoder (VAE)

## Evaluation Metrics

To determine the quality of the algorithms

* Silhouette score

> A high Silhouette score (close to 1) indicates that data points within clusters are similar, and that the normal data points are well separated from the anomalous ones.

* Calinski-Harabasz index

> Calinski-Harabasz Index measures the between-cluster dispersion against within-cluster dispersion. A higher score signifies better-defined clusters.

* Davies-Bouldin index

> Davies-Bouldin Index measures the size of clusters against the average distance between clusters. A lower score signifies better-defined clusters.

* Kolmogorov-Smirnov statistic

> It measures the maximum difference between the cumulative distribution functions of the normal and anomalous data points.

* Precision at top-k

> The metric calculates the precision of the top-k anomalous data points using expert domain knowledge.
