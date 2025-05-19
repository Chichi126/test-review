import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError



# Azure Storage connection string
storage_connection_string = 'your string here'
blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

# Define container and local directory
container_name = 'chireviews'
dataset_folder = os.path.join(os.getcwd(), 'dataset')
blob_prefix = 'raw_dataset/'  # Virtual folder name in Azure

overwrite = True

# Upload each file into the virtual folder in the container
for filename in os.listdir(dataset_folder):
    file_path = os.path.join(dataset_folder, filename)

    if os.path.isfile(file_path):
        blob_name = f"{blob_prefix}{filename}"
        try:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=overwrite)
            print(f"✅ Uploaded to {blob_name}")
        except ResourceExistsError:
            print(f"⚠️ Blob {blob_name} already exists in {container_name}.")
