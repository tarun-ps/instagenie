import boto3
from settings import S3_BUCKET

s3_client = boto3.resource("s3")

def upload_file_to_s3(s3_path: str, file_path: str, mime_type: str):
    s3_client.Bucket(S3_BUCKET).put_object(Key=f"{s3_path}", Body=open(file_path, "rb"), ContentType=mime_type)
