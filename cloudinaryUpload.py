import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary_url = os.getenv("CLOUDINARY_URL")
cloudinary.config(
    cloud_name="dd2at7bts",
    API_key=os.getenv("CLOUDINARY_API_KEY"),
    API_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_pdf(filename):
    res = cloudinary.uploader.upload(f"reciepts/{filename}.pdf", resource_type="auto")
    print(res)
    return res['secure_url']

print(upload_pdf("UDR8E2DMRV"))
