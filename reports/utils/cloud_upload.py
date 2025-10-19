import aiohttp
import asyncio
import pandas as pd
import json
from datetime import datetime

async def upload_to_cloud(student_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://jsonplaceholder.typicode.com/posts",
            json=student_data
        ) as response:
            print(await response.text())

async def push_all_to_cloud(file_path):
    # df = pd.read_csv(file_path)
    data = {"file_uploaded": file_path, "timestamp": str(datetime.now())}

    tasks = [upload_to_cloud(row._asdict()) for row in data.itertuples()]
    await asyncio.gather(*tasks)
    print("All student data uploaded to mock cloud!")

        #  2. Save locally so you can *see* what was sent!
    with open("uploaded_data_log.json", "a") as f:
        json.dump(data, f)
        f.write("\n")  # Add newline per entry

    print("Logged upload:", data)

if __name__ == "__main__":
    asyncio.run(push_all_to_cloud("processed_marks.csv"))
