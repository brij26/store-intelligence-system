from pipeline.ingestion.video_metadata import VideoMetadata


VIDEO_PATH = "/workspaces/store-intelligence-system/data/raw/Store_1/CAM-3-entry.mp4"

metadata_reader = VideoMetadata(VIDEO_PATH)

metadata = metadata_reader.get_metadata()

print(metadata)

metadata_reader.release()