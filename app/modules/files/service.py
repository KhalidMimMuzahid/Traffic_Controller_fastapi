
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.files.models import File
from exceptions.models import CustomError
import uuid
import base64
from fastapi.responses import Response
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



