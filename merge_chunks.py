import os
import json
import math

n = 15

for filename in os.listdir("jsons"):
    if filename.endswith(".json"):
        file_path = os.path.join("jsons", filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            new_chunks = []
            num_chunks = len(data["chunks"])  #count the number of chunks in the one video
            num_groups  = math.ceil(num_chunks / n)  # to group the chunks into groups of n  12/5 = 2.5 math.ceil = 3 groups


            for i in range(num_groups):
                start_index = i * n
                end_index = min((i + 1) * n, num_chunks)

                chunk_group  = data["chunks"][start_index:end_index]  # group the chunks into groups of 

                new_chunks.append({
                    "number": data["chunks"][0]["number"],  
                    "title": chunk_group[0]["title"],
                    "start": chunk_group[0]["start"],  # start time of the first chunk in the group
                    "end": chunk_group[-1]["end"],  # end time of the last chunk in the group
                    "text": " ".join(chunk["text"] for chunk in chunk_group)
                })

            #save the file with double .json

            os.makedirs("merged_jsons", exist_ok=True)
            with open(os.path.join("merged_jsons", f"{filename}"), "w", encoding="utf-8") as json_file:
                json.dump({"chunks": new_chunks, "text":data["text"]} , json_file, indent=4) 







