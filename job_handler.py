import os
from job_logger import log_event, log_error
from modules.topic_research import get_trending_topic
from modules.script_generator import generate_and_rank_scripts
from modules.image_generator import create_video_from_images
from modules.voiceover_generator import generate_voiceover_video
from modules.seo_optimizer import generate_metadata
from modules.shadow_tester import simulate_ctr_check
from modules.uploader import upload_to_youtube

def run_video_job(job_id):
    try:
        # 1. Topic Research
        log_event(job_id, "Topic", "Researching trending topic...")
        topic = get_trending_topic()
        log_event(job_id, "Topic", f"Selected topic: {topic}")

        # 2. Script Generation
        log_event(job_id, "Script", "Generating 10 script versions...")
        script = generate_and_rank_scripts(topic)
        log_event(job_id, "Script", f"Selected best script for topic.")

        # 3. Image/Video Montage
        log_event(job_id, "Images", "Generating AI images and video...")
        visual_path = create_video_from_images(script, topic)
        log_event(job_id, "Images", f"Video draft created at {visual_path}")

        # 4. Voiceover
        log_event(job_id, "Voiceover", "Adding voiceover and music...")
        final_video = generate_voiceover_video(visual_path, script)
        log_event(job_id, "Voiceover", f"Voice + BGM done: {final_video}")

        # 5. SEO Metadata
        log_event(job_id, "SEO", "Generating title, desc, and tags...")
        metadata = generate_metadata(script, topic)
        log_event(job_id, "SEO", f"Title: {metadata['title']}")

        # 6. Shadow Ban Test
        log_event(job_id, "Test", "Testing CTR simulation...")
        passed = simulate_ctr_check(final_video, metadata['title'])
        if not passed:
            log_event(job_id, "Test", "CTR test failed. Aborting upload.")
            return

        # 7. Upload to YouTube
        log_event(job_id, "Upload", "Uploading video...")
        upload_to_youtube(final_video, metadata)
        log_event(job_id, "Upload", "Video uploaded successfully!")

    except Exception as e:
        log_error(job_id, f"Pipeline error: {str(e)}")
