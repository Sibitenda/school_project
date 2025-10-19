# import aiohttp
# import asyncio
# import pandas as pd
# import json
# from datetime import datetime

# async def upload_to_cloud(student_data):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(
#             "https://jsonplaceholder.typicode.com/posts",
#             json=student_data
#         ) as response:
#             print(await response.text())

# async def push_all_to_cloud(file_path):
#     # df = pd.read_csv(file_path)
#     data = {"file_uploaded": file_path, "timestamp": str(datetime.now())}

#     tasks = [upload_to_cloud(row._asdict()) for row in data.itertuples()]
#     await asyncio.gather(*tasks)
#     print("All student data uploaded to mock cloud!")

#         #  2. Save locally so you can *see* what was sent!
#     with open("uploaded_data_log.json", "a") as f:
#         json.dump(data, f)
#         f.write("\n")  # Add newline per entry

#     print("Logged upload:", data)

# if __name__ == "__main__":
#     asyncio.run(push_all_to_cloud("processed_marks.csv"))

from supabase import create_client
from django.conf import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_to_supabase(file_bytes, cloud_file_name):
    """
    Uploads a file to Supabase Storage.
    :param file_bytes: Binary data (PDF or ZIP)
    :param cloud_file_name: e.g. 'student_reports_2025.zip'
    :return: Public URL of uploaded file
    """
    bucket_name = "reports"  # Supabase bucket
    supabase.storage.from_(bucket_name).upload(
        path=cloud_file_name,
        file=file_bytes,
        file_options={"content-type": "application/zip"}
    )

    # Generate public URL
    public_url = supabase.storage.from_(bucket_name).get_public_url(cloud_file_name)
    return public_url
