import time
from datetime import datetime
import os
import threading

from job_handler import run_video_job
from job_logger import log_event, log_error, is_another_job_running, set_job_running, clear_job_running

def within_time_window():
    now = datetime.now().hour
    return 6 <= now <= 22  # Runs only between 6AM and 10PM

def main():
    job_id = int(time.time())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not within_time_window():
        log_event(job_id, "Skipped", "Outside allowed time window", timestamp)
        return

    if is_another_job_running():
        log_event(job_id, "Skipped", "Previous job still running", timestamp)
        return

    try:
        set_job_running(job_id)
        log_event(job_id, "Started", "Running YouTube upload job", timestamp)
        run_video_job(job_id)  # Runs full upload automation
        log_event(job_id, "Completed", "Video uploaded successfully", timestamp)
    except Exception as e:
        log_error(job_id, f"Unhandled Error: {str(e)}", timestamp)
    finally:
        clear_job_running()

if __name__ == "__main__":
    main()
