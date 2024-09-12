import logging
import mimetypes
import time

from azure.core.exceptions import AzureError, ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from fastapi import HTTPException

from app.core import LOGGER
from app.core.config import AZURE_CONNECTION_STRING, CONTAINER_NAME


def get_blob_service_client_sas():

    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )

    return blob_service_client


def upload_image(image, name_image, retries=3):
    blob_service_client = get_blob_service_client_sas()

    mime_type, _ = mimetypes.guess_type(name_image)
    if not mime_type or not mime_type.startswith("image/"):
        LOGGER.error(f"The file {name_image} is not a valid image.")
        raise HTTPException(
            status_code=503,
            detail=f"The file {name_image} is not a valid image.",
        )

    try:
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, blob=name_image
        )

        blob_client.upload_blob(image, overwrite=False)
        image_url = blob_client.url

        return image_url

    except ResourceExistsError as e:
        LOGGER.error(f"Image {name_image} already exists: {e.response}")
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Image {name_image} already exists",
        )

    except AzureError as e:
        LOGGER.error(f"Error trying to upload image {name_image}: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Error trying to upload image{name_image}: {e}",
        )
