from google.cloud import storage

# from: https://cloud.google.com/storage/docs/object-basics#storage-download-object-python
# doc: https://google-cloud-python.readthedocs.io/en/latest/index.html
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
if running locally:
before running this script, run:
gcloud auth application-default login
'''
bucket_name = 'rasp1' #'praxis-index-182700.appspot.com'
object_name = '/root/data/src/2017-10-28_180307.jpg'
destination = 'rasp1/image_trial.jpg'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

upload_blob(bucket_name, object_name, destination)
