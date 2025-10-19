import threading
import time
import pandas as pd
from django.conf import settings
from .grade_utils import get_grade_point
from .cloud_upload import upload_to_supabase  # add this import

start_time = time.time()

def process_student_marks(file_path):
    df = pd.read_csv(file_path)
    results = []

    def compute_row(row):
        time.sleep(1)  # simulate processing delay
        row['gpa'] = get_grade_point(row['score'])
        results.append(row)

    threads = []
    for _, row in df.iterrows():
        t = threading.Thread(target=compute_row, args=(row,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    output = pd.DataFrame(results)

    # Save locally
    output_path = "processed_marks.csv"
    output.to_csv(output_path, index=False)
    print("Concurrent processing completed.")
    
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")

    # Upload to Supabase
    try:
        with open(output_path, "rb") as f:
            file_bytes = f.read()
        cloud_file_name = f"processed_marks_{int(time.time())}.csv"
        url = upload_to_supabase(file_bytes, cloud_file_name)
        print(f"Uploaded CSV to Supabase: {url}")
    except Exception as e:
        print(f"Failed to upload CSV to Supabase: {e}")

    return output
