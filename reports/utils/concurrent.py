import threading
import time
import pandas as pd
from .grade_utils import get_grade_point  # Import correct function
# import time
start_time = time.time()
# Simulate concurrent grade processing
def process_student_marks(file_path):
    df = pd.read_csv(file_path)
    results = []

    def compute_row(row):
        time.sleep(1)  # simulate processing delay
        row['gpa'] = get_grade_point(row['score'])  # use correct function
        results.append(row)

    threads = []
    for _, row in df.iterrows():
        t = threading.Thread(target=compute_row, args=(row,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    output = pd.DataFrame(results)
    output.to_csv("processed_marks.csv", index=False)
    print("Concurrent processing completed.")
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")
    return output
