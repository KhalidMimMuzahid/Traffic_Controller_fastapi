
from fastapi import APIRouter, Depends, File, UploadFile, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
# from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreateRequest
from database import get_db 
# from modules.intersections.service import create_intersection, get_intersections, delete_intersection_service
# from responses.handler import create_response
# from responses.models import Response
from modules.files.service import get_file_service, upload_frame_service, get_video_stream_service
from responses.handler import create_response
from modules.files.schemas import streamUpdateRequest

file_router = APIRouter()



@file_router.get("/get"
# , response_model=Response[list[IntersectionListResponse]]
)
async def get_file( id:str,db: AsyncSession = Depends(get_db)):
    result= await get_file_service(db, id=id)
    return result
    # return create_response(result=result["data"], pydantic_model=IntersectionListResponse, message="intersections have retrieved successfully", meta_data=result["meta_data"])


@file_router.post("/send-video-stream")
async def upload_frame(
    camera_id: str = Form(...), 
    file: UploadFile = File(...)
):
    """
    Endpoint to receive a video frame from the camera server and update the stored frame for the specified camera_id.
    """
    result = await upload_frame_service(camera_id=camera_id, file=file)
    return create_response(result=result, pydantic_model=streamUpdateRequest, message="Stream updated successfully")



@file_router.get("/get-video-stream/{camera_id}")
async def get_video_stream(camera_id: str):
    """
    Endpoint to stream the MJPEG video feed for a specific camera.
    It uses an asynchronous generator to continuously send the latest frame.
    """
    # Retrieve the frame generator for the specified camera.
    frame_generator = await get_video_stream_service(camera_id=camera_id)
    # Return the streaming response with the appropriate media type.
    return Response(frame_generator, media_type="multipart/x-mixed-replace; boundary=frame")








# for server 1
# from fastapi import FastAPI
# import cv2
# import requests
# import threading

# app = FastAPI()

# # Configure your cameras in a dictionary.
# # Keys are unique camera IDs and values are video sources.
# # Replace 0 and 1 with your actual camera sources or RTSP URLs if needed.
# CAMERAS = {
#     "camera1": 0,  # Example: local webcam
#     "camera2": 1,  # Example: second webcam or another source
# }

# # Server 2 endpoint URL that handles incoming frames.
# # Make sure to update this with the correct IP and port of your main server.
# SERVER_2_URL = "http://your_main_server_ip:8001/send-video-stream"

# def stream_video(camera_id: str, video_source):
#     """
#     Captures video frames from the specified camera and sends them
#     to Server 2 along with the camera ID.

#     Args:
#         camera_id (str): Unique identifier for the camera.
#         video_source (int or str): OpenCV video capture source.
#     """
#     # Open the video capture source using OpenCV.
#     cap = cv2.VideoCapture(video_source)
    
#     while True:
#         # Capture a frame from the camera.
#         success, frame = cap.read()
#         if not success:
#             print(f"[{camera_id}] Unable to capture frame.")
#             break  # Exit if no frame is captured.

#         # Encode the captured frame as JPEG.
#         success, buffer = cv2.imencode('.jpg', frame)
#         if not success:
#             print(f"[{camera_id}] Frame encoding failed.")
#             continue  # Skip sending this frame if encoding fails.
        
#         frame_bytes = buffer.tobytes()

#         # Send the frame to Server 2 using an HTTP POST request.
#         # We send the image as a file and include the camera_id as form data.
#         try:
#             response = requests.post(
#                 SERVER_2_URL,
#                 files={"file": frame_bytes},
#                 data={"camera_id": camera_id}
#             )
#             if response.status_code != 200:
#                 print(f"[{camera_id}] Failed to send frame. Status code: {response.status_code}")
#         except Exception as e:
#             print(f"[{camera_id}] Exception occurred while sending frame: {e}")

#         # Optional: Sleep to control the frame rate.
#         # cv2.waitKey waits in milliseconds.
#         cv2.waitKey(30)  # approximately 30ms delay (~33 FPS maximum)

# @app.on_event("startup")
# def start_stream():
#     """
#     Starts streaming for each camera on server startup using separate threads.
#     Each thread runs the stream_video function for a given camera.
#     """
#     for cam_id, source in CAMERAS.items():
#         thread = threading.Thread(target=stream_video, args=(cam_id, source), daemon=True)
#         thread.start()
#         print(f"[{cam_id}] Stream started.")

# @app.get("/")
# def read_root():
#     """
#     Basic endpoint to verify that the Camera Server is running.
#     """
#     return {"message": "Camera Server Running"}