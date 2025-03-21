
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.files.models import File
from exceptions.models import CustomError
import uuid
import base64
from fastapi.responses import Response
import cv2
import numpy as np
import asyncio 

latest_frames = {}
# An asyncio.Lock ensures thread-safe access to latest_frames.
latest_frames_lock = asyncio.Lock()
async def upload_file(
    db: AsyncSession,
    file: UploadFile 
):  
    read_file=await file.read()
    # Extract MIME type dynamically
    file_type = file.content_type  
    new_file = File(id=uuid.uuid4(), file=read_file, file_type= file_type)
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    base_url = "http://127.0.0.1:8000/api/v1/files/get"
    file_id = str(new_file.id)
    dynamic_url = f"{base_url}?id={file_id}"
    return {
        "url": dynamic_url
    }


async def get_file_service(
    db: AsyncSession,
    id: str
):
    result = await db.execute(select(File).where(File.id == id))
    file_record = result.scalar_one_or_none()
    file_data= base64.b64encode(file_record.file).decode('utf-8')
    file_type = file_record.file_type
    return Response(content=file_record.file, media_type=file_record.file_type)



async def upload_frame_service(
    camera_id: str,
    file:UploadFile
):
    frame_bytes = await file.read()
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Optional: Validate that the frame was decoded properly.
    if frame is None:
        raise CustomError(status_code=406, message="Invalid image frame received.")

    # Safely update the latest frame for this camera using the lock.
    async with latest_frames_lock:
        latest_frames[camera_id] = frame

    return None



async def generate_frames(camera_id: str):
    """
    Asynchronous generator that yields frames encoded in MJPEG format.
    It continuously checks for the latest frame of the specified camera.
    A short sleep is used to prevent busy waiting.
    """
    while True:
        # Safely read the latest frame for the specified camera.
        async with latest_frames_lock:
            frame = latest_frames.get(camera_id)

        # If no frame is available yet, wait a short while before checking again.
        if frame is None:
            await asyncio.sleep(0.01)  # 10ms delay to avoid high CPU usage
            continue

        # Encode the frame as JPEG.
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            # If encoding fails, wait briefly and continue.
            await asyncio.sleep(0.01)
            continue

        frame_bytes = buffer.tobytes()
        # Yield the frame in MJPEG format.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        # Delay to control frame rate (adjust the sleep for your desired FPS)
        await asyncio.sleep(0.03)  # roughly 30 FPS


async def get_video_stream_service(camera_id: str):
    """
    Returns an asynchronous generator for streaming video frames
    for the given camera_id.
    """
    return generate_frames(camera_id=camera_id)