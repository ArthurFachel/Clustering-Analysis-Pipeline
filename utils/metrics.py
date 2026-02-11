import numpy as np

def split_metrics(metrics):
    out = {
        "answer_relevancy": None,
        "bert_similarity": None,
        "correctness_geval": None,
        "prompt_alignment": None,
    }
    for m in metrics:
        if m["name"] == "Answer Relevancy":
            out["answer_relevancy"] = m.get("score")
        elif m["name"] == "Bert Similarity Metric":
            out["bert_similarity"] = m.get("score")
        elif m["name"] == "Correctness (GEval)":
            out["correctness_geval"] = m.get("score")
        elif m["name"] == "Prompt Alignment":
            out["prompt_alignment"] = m.get("score")

    return out 

def compute_score(row):
    if row["task"].lower() in {"tf", "choice"}:
        return float(row["success"] in {True, "true", 1})
    




    scores = [
        row["answer_relevancy"],
        row["bert_similarity"],
        row["correctness_geval"],
        row["prompt_alignment"],
    ]
    scores = [s for s in scores if s is not None]
    return float(np.mean(scores)) if scores else None