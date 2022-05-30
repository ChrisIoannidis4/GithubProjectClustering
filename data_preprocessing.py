from sklearn.preprocessing import StandardScaler
import pandas as pd


# Get all data
repo_data = pd.read_csv("./repo_data.csv", sep=";")
print(repo_data)

owners = repo_data.loc[:, ["User_Name"]]
repos = repo_data.loc[:, ["Repo_Name"]]
commits = repo_data.loc[:, ["Commits_On_Main"]]
open_issues = repo_data.loc[:, ["Open_Issues"]]
closed_issues = repo_data.loc[:, ["Closed_Issues"]]
contributors = repo_data.loc[:, ["Contributors"]]
total_lines = repo_data.loc[:, ["Total_Lines"]]
most_used_langs = repo_data.loc[:, ["Most_Used_Language"]]
max_lang_lines = repo_data.loc[:, ["Max_Lang_Lines"]]


# Split languages in categories and one hot encode them
lang_freq = most_used_langs.value_counts()
# print(lang_freq)

for i in range(len(lang_freq)):
    if lang_freq[i] < 20:
        most_used_langs = most_used_langs.replace(lang_freq.index[i], "Rare")
    elif lang_freq[i] < 50:
        most_used_langs = most_used_langs.replace(lang_freq.index[i], "Uncommon")

langs_encoded = pd.get_dummies(most_used_langs, prefix="Lang")
# print(langs_encoded)
# print(langs_encoded.sum())

# Get the ratio (top language lines) / (total lines)
max_lang_lines_ratio = []
for i in range(len(max_lang_lines)):
    if total_lines.loc[i, "Total_Lines"] != 0:
        max_lang_lines_ratio.append(
            max_lang_lines.loc[i, "Max_Lang_Lines"] / total_lines.loc[i, "Total_Lines"]
        )
    else:
        max_lang_lines_ratio.append(0)

max_lang_lines_ratio = pd.DataFrame(
    max_lang_lines_ratio, columns=["Max_Lang_Lines_Ratio"]
)

# print(max_lang_lines_ratio)


# Scale

# Choose the scaler
scaler = StandardScaler()

commits_scaled = pd.DataFrame(
    scaler.fit_transform(commits),
    columns=["Commits_On_Main_Scaled"],
)
open_issues_scaled = pd.DataFrame(
    scaler.fit_transform(open_issues), columns=["Open_Issues_Scaled"]
)
closed_issues_scaled = pd.DataFrame(
    scaler.fit_transform(closed_issues),
    columns=["Closed_Issues_Scaled"],
)
contributors_scaled = pd.DataFrame(
    scaler.fit_transform(contributors),
    columns=["Contributors_Scaled"],
)
total_lines_scaled = pd.DataFrame(
    scaler.fit_transform(total_lines),
    columns=["Total_Lines_Scaled"],
)

repo_data_processed = pd.concat(
    [
        commits_scaled,
        open_issues_scaled,
        closed_issues_scaled,
        contributors_scaled,
        total_lines_scaled,
        langs_encoded,
        max_lang_lines_ratio,
    ],
    axis=1,
)

print(repo_data_processed)
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from math import sqrt
from sklearn.cluster import KMeans

silhouette_coefficients=[]
inertia_values= []
for i in range(2,11):
    kmeans= KMeans(n_clusters=i)
    print("number of clusters: ", i )
    kmeans= kmeans.fit(repo_data_processed)
    print("Cluster Centers: ", kmeans.cluster_centers_)
    print(i, "\n")
    print("Inertia: ", kmeans.inertia_)
    print("Labels: ", kmeans.labels_) 
    print("Silhouette Score: ", silhouette_score(repo_data_processed, kmeans.labels_))
    silhouette_coefficients.append(silhouette_score(repo_data_processed ,kmeans.labels_))
    inertia_values.append(kmeans.inertia_)

    # separation = 0
    # repo1=pd.DataFrame({"X": repo_data_processed.loc[:, 0], "Y": repo_data_processed.loc[:, 1],"Z": repo_data_processed.loc[:, 2],"C": repo_data_processed.loc[:, 3],"B": repo_data_processed.loc[:, 4],"N": repo_data_processed.loc[:, 5],"M": repo_data_processed.loc[:, 6], "K": repo_data_processed.loc[:, 7]})
    # distance = lambda x1, x2: sqrt((x1.X - x2.X) ** 2 + (x1.Y - x2.Y) ** 2 + (x1.Z - x2.Z) ** 2 + (x1.C - x2.C) ** 2 + (x1.B - x2.B) ** 2 + (x1.N - x2.N) ** 2 + (x1.M - x2.M) ** 2 + (x1.K - x2.K) ** 2)
    # m = repo1.mean()
    # for i in list(set(kmeans.labels_)):
    #     mi = repo1.loc[kmeans.labels_ == i, :].mean()
    #     Ci = len(repo1.loc[kmeans.labels_ == i, :].index)
    #     separation += Ci * (distance(m, mi) ** 2)
    # print("Separation: ", separation)


plt.style.use("fivethirtyeight")
plt.plot(range(2, 11 ), inertia_values)
plt.xticks(range(2,11 ))
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.show()




slc = []
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
# for i in range(2,26):
    # hierarc = AgglomerativeClustering(n_clusters=i, linkage= "single").fit(repo_data_processed)
    # hierarc = AgglomerativeClustering(n_clusters=i, linkage= "complete").fit(repo_data_processed)
    # hierarc = AgglomerativeClustering(n_clusters=i, linkage= "average").fit(repo_data_processed)
    # slc.append(silhouette_score(repo_data_processed, hierarc.labels_))


#print(slc)

# plt.plot(range(2, 26), slc)
# plt.xticks(range(2, 26), range(2, 26))
# plt.show()
# hierarc = AgglomerativeClustering(n_clusters=2, linkage= "single").fit(repo_data_processed)
# print("silhuette score: ", silhouette_score(repo_data_processed, hierarc.labels_))
# print(hierarc.labels_)


