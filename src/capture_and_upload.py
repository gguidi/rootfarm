from google.cloud import storage
import google.auth
import os
from time import sleep
from picamera import PiCamera
from datetime import datetime

# from: https://cloud.google.com/storage/docs/object-basics#storage-download-object-python
# doc: https://google-cloud-python.readthedocs.io/en/latest/index.html
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
if running locally:
before running this script, run:
gcloud auth application-default login
'''

def init_camera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    sleep(2)
    return camera

def capture_image(camera):
    #get the time - use it for the naming the image
    date_now = datetime.now() # dates in the format: 2017-10-20 13:16:03.46748345
    date = '-'.join(str(date_now).split(' ')[0].split('-'))
    time = ''.join(str(date_now).split(' ')[1].split(':')).split('.')[0]
    #capture the image
    photo_name = str('_'.join([date,time]))+'.jpg'
    camera.capture(photo_name)
    return photo_name

def delete_image(image):
    os.remove(image)

def upload_blob(client, bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    #storage_client = storage.Client()
    storage_client = client
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def download_blob(client, bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    #storage_client = storage.Client()
    storage_client = client
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def delete_blob(client, bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    #storage_client = storage.Client()
    storage_client = client
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

if __name__ == "__main__":
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "rootfarm-6e380be3a2cb.json"
    credentials, project = google.auth.default()
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
    client = storage.Client(credentials=credentials)

    #bucket parameters
    bucket_name = 'rasp1' #'praxis-index-182700.appspot.com'
    object_directory = '/root' #in container
    #object_directory = '/home/pi/rootfarm' #to test code outside of container
    #destination_directory = 'rasp1'
    
    camera = init_camera()
    img_name = capture_image(camera)
    object_name = '/'.join([object_directory,img_name])
    #destination = '/'.join([destination_directory, img_name])
    destination = img_name
    upload_blob(client, bucket_name, object_name, destination)
    delete_image(object_name)
