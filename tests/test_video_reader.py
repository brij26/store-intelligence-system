from pipeline.ingestion.video_reader import VideoReader


VIDEO_PATH = "/workspaces/store-intelligence-system/data/raw/Store_1/CAM-3-entry.mp4"

reader = VideoReader(
    VIDEO_PATH,
    frame_skip=10
)

for item in reader.read_frames():

    print(
        item["frame_id"],
        item["timestamp"],
        item["frame"].shape
    )

    break

reader.release()