import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import whisper
import json

model = whisper.load_model("small")

result = model.transcribe(audio = "audios/9_Id & Classes in HTML.mp3",
                          language = "hi",
                          task = "translate",
                          word_timestamps = False   )


print(result["segments"])
chunks = []
for segment in result["segments"]:
    chunks.append({"start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                    })                        

print(chunks)


with open("output.json" ,"w") as f:
    json.dump(chunks,f)
