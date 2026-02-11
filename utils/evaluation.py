import pandas as pd
from utils.utils_IO import json_to_df
from utils.assign import assign_clusters
from utils.metrics import compute_score
from utils.aglomerar import aglomerar
from utils.run import hierachical_clustering_top_bottom, hierarchical_clustering_bottom_top, kmeans_model
from sentence_transformers import SentenceTransformer


def evaluate_top(models_folder, i):
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    df, model =hierachical_clustering_top_bottom(i)
    df = aglomerar(models_folder)
    df = assign_clusters(df, embed_model, model)
    df["score"] = df.apply(compute_score, axis=1)
    print(df)

    final = (
    df
    .groupby(["model", "task", "cluster",], as_index=False)
    .agg(
        num_questions=("score", "size"),

        score_mean=("score", "mean"),
        score_sum=("score", "sum"),

        answer_relevancy_mean=("answer_relevancy", "mean"),
        bert_similarity_mean=("bert_similarity", "mean"),
        correctness_geval_mean=("correctness_geval", "mean"),
        prompt_alignment_mean=("prompt_alignment", "mean"),
    )
)
    return final

def evaluate_bottom(models_folder, i):
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    df, model =hierarchical_clustering_bottom_top(i)
    df = aglomerar(models_folder)
    df = assign_clusters(df, embed_model, model)
    df["score"] = df.apply(compute_score, axis=1)
    print(df)

    final = (
    df
    .groupby(["model", "task", "cluster",], as_index=False)
    .agg(
        num_questions=("score", "size"),

        score_mean=("score", "mean"),
        score_sum=("score", "sum"),

        answer_relevancy_mean=("answer_relevancy", "mean"),
        bert_similarity_mean=("bert_similarity", "mean"),
        correctness_geval_mean=("correctness_geval", "mean"),
        prompt_alignment_mean=("prompt_alignment", "mean"),
    )
)
    return final

def evaluate_kmeans(models_folder, i):
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    df, model =kmeans_model(i)
    df = aglomerar(models_folder)
    df = assign_clusters(df, embed_model, model)
    df["score"] = df.apply(compute_score, axis=1)
    print(df)

    final = (
    df
    .groupby(["model", "task", "cluster",], as_index=False)
    .agg(
        num_questions=("score", "size"),

        score_mean=("score", "mean"),
        score_sum=("score", "sum"),

        answer_relevancy_mean=("answer_relevancy", "mean"),
        bert_similarity_mean=("bert_similarity", "mean"),
        correctness_geval_mean=("correctness_geval", "mean"),
        prompt_alignment_mean=("prompt_alignment", "mean"),
    )
)
    return final