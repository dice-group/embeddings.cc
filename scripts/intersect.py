import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("input1")
parser.add_argument("input2")
parser.add_argument("output")

args = parser.parse_args()

df1 = pd.read_csv(args.input1)
df2 = pd.read_csv(args.input2)

result = df1.merge(
    df2,
    on="domain",
    how="inner",
    suffixes=("_1", "_2")
)

result["embedding_count"] = result[
    ["embedding_count_1", "embedding_count_2"]
].min(axis=1)

result[["domain", "embedding_count"]].to_csv(args.output, index=False)