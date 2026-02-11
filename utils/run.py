import os
import pandas as pd
from utils.utils_IO import save_txt_per_cluster
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans , BisectingKMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from dotenv import load_dotenv
import matplotlib as plt
load_dotenv()


#kmeans
def kmeans_model(chosen_k):
    raw = pd.read_json(os.getenv('JSON_PATH'))
    rows = []

    for section in raw.columns: 
        block = raw[section]

        if "question" not in block:
            continue

        questions = block["question"]
        answers = block.get("answer", [None] * len(questions))

        for q, a in zip(questions, answers):
            text = q
            if section in {"qa", "completion"} and a is not None:
                text = f"{q} {a}"

            rows.append({
                "section": section,
                "question": q,
                "text": text
            })

    df = pd.DataFrame(rows)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_model.encode(
        df["text"].tolist(),
        normalize_embeddings=True,
        show_progress_bar=True
    )

    k = min(chosen_k, len(df))
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    df["cluster"] = kmeans.fit_predict(embeddings)
    print(df)
    return df, kmeans

def kmeans_run(max_clusters: int):
    os.makedirs(f"{os.getenv('RESULTS_PATH')}/K_Means", exist_ok=True)
    for i in range(5, max_clusters, 5):
            result = kmeans_model(chosen_k=i)
            df = result[0] if isinstance(result, tuple) else result

            save_txt_per_cluster(df, f"{os.getenv('RESULTS_PATH')}/K_Means/Clusters/{i}", text_col="question")
            df.to_csv(f"{os.getenv('RESULTS_PATH')}/K_Means/{i}_final_results_kmeans.csv", index=False)




#top-bottom
def hierachical_clustering_top_bottom(chosen_k,linkage="largest_cluster",json_path=os.getenv("JSON_PATH")):
    raw = pd.read_json(json_path)
    rows = []

    for section in raw.columns: 
        block = raw[section]

        if "question" not in block:
            continue

        questions = block["question"]
        answers = block.get("answer", [None] * len(questions))

        for q, a in zip(questions, answers):
            text = q
            if section in {"qa", "completion"} and a is not None:
                text = f"{q} {a}"

            rows.append({
                "section": section,
                "question": q,
                "text": text
            })

    df = pd.DataFrame(rows)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_model.encode(
        df["text"].tolist(),
        normalize_embeddings=True,
        show_progress_bar=True
    )

    hierach = BisectingKMeans(n_clusters=chosen_k, init="k-means++", n_init=1, random_state=42,
                               max_iter=300, verbose=0, tol=0.0001, 
                              copy_x=True, algorithm='lloyd', bisecting_strategy=linkage)
    df["cluster"] = hierach.fit_predict(embeddings)
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    plt.figure()
    plt.scatter(reduced[:, 0], reduced[:, 1], c=df["cluster"])
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.title("Bisecting K-Means Clustering (PCA)")
    plt.savefig(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Top-Bottom/plots/{linkage}_{chosen_k}.png", dpi=300, bbox_inches="tight")
    plt.show()


    return df , hierach


def hierarchical_top_bottom_run(max_clusters: int):
    os.makedirs(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Top-Bottom", exist_ok=True)
    for linkage in ['largest_cluster', 'largest_cluster']:
        for i in range(5, max_clusters, 5):
                df, _ = hierachical_clustering_top_bottom(chosen_k=i,linkage=linkage)
                save_txt_per_cluster(df, f"{os.getenv('RESULTS_PATH')}/Hierarchical/Top-Bottom/clusters/{linkage}/{i}", text_col="question")
                df.to_csv(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Top-Bottom/csv/{linkage}_final_results_hierarchical_{i}.csv", index=False)




#bottom-top
def hierarchical_clustering_bottom_top(chosen_k,linkage,json_path=os.getenv("JSON_PATH")):
    raw = pd.read_json(json_path)
    rows = []

    for section in raw.columns: 
        block = raw[section]

        if "question" not in block:
            continue

        questions = block["question"]
        answers = block.get("answer", [None] * len(questions))

        for q, a in zip(questions, answers):
            text = q
            if section in {"qa", "completion"} and a is not None:
                text = f"{q} {a}"

            rows.append({
                "section": section,
                "question": q,
                "text": text
            })

    df = pd.DataFrame(rows)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_model.encode(
        df["text"].tolist(),
        normalize_embeddings=True,
        show_progress_bar=True
    )

    hierach = AgglomerativeClustering(n_clusters=chosen_k,
                                       metric='euclidean' if linkage =='ward' else 'cosine',  
                                        compute_full_tree='auto', 
                                       linkage=linkage, distance_threshold=None if chosen_k != None else 2.5,
                                         compute_distances=False)
    df["cluster"] = hierach.fit_predict(embeddings)
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    plt.figure()
    plt.scatter(reduced[:, 0], reduced[:, 1], c=df["cluster"])
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.title("Hierarchical Clustering (PCA)")
    plt.savefig(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Bottom-top/plots/_{linkage}.png", dpi=300, bbox_inches="tight")
    plt.show()
    return df
    

def hierarchical_bottom_top_run(max_clusters: int):
    os.makedirs(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Bottom-top", exist_ok=True)
    for linkage in ['ward', 'complete']:
        for i in range(5, max_clusters, 5):
                df = hierarchical_clustering_bottom_top(chosen_k=i,linkage=linkage)
                save_txt_per_cluster(df, f"{os.getenv('RESULTS_PATH')}/Hierarchical/Bottom-top/clusters/{linkage}/{i}", text_col="question")
                df.to_csv(f"{os.getenv('RESULTS_PATH')}/Hierarchical/Bottom-top/csv/{linkage}_final_results_hierarchical_{i}.csv", index=False)