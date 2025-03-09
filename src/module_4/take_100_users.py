import json
import pandas as pd
from pathlib import Path

def take_20_users(folder_path):
    feature_frame = pd.read_csv(folder_path)
    size_of_order = feature_frame.groupby("order_id").outcome.sum()
    size_of_order = size_of_order[size_of_order>=5]
    feature_frame = feature_frame[feature_frame["order_id"].isin(size_of_order.index)]
    df = feature_frame[feature_frame["outcome"]==1][["user_id", "ordered_before", "global_popularity", "abandoned_before"]].sample(20)
    result = df.set_index("user_id").to_dict(orient="index")
    print(json.dumps(result, indent=2))


    OUTPUT_PATH = Path("D:\Users\maick\Desktop\Codigos\zrive-ds\src\module_4\models")


    output_path = OUTPUT_PATH / "filtered_users.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Archivo guardado en: {output_path}")

def main():
    FOLDER_PATH = Path("D:/Users/maick/Desktop/Codigos/zrive-ds/data/box_builder_dataset/feature_frame.csv")
    take_20_users(FOLDER_PATH)  

if __name__ == "__main__":
    main()
