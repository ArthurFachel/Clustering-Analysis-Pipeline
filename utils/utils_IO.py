import os, time, json
from utils.AWS import generate
import pandas as pd

def save_txt_per_cluster(df, out_dir, text_col):
    os.makedirs(out_dir, exist_ok=True)
    print(df)
    for cluster, g in df.groupby("cluster"):
        time.sleep(4)
        rename = generate("\n".join(g[text_col].astype(str)))
        with open(f"{out_dir}/{cluster}_{rename}_.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(g[text_col].astype(str)))

def json_to_df(path):
    with open(path) as f:
        data = json.load(f)
    return pd.DataFrame(data["testCases"])