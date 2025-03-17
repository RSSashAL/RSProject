import os
import shutil
import requests
from arango import ArangoClient

# ArangoDB connection details
ARANGO_HOST = "http://localhost:8529"
ARANGO_USER = "sashi"
ARANGO_PASSWORD = "sashi!23"
ARANGO_DB_NAME = "poc"
COLLECTION_NAME = "nasa_poc"

# Directory to store images (mimicking S3-like storage)
STORAGE_DIR = "/Users/sash/docker/nasa_pics"

# Initialize ArangoDB client
client = ArangoClient(hosts=ARANGO_HOST)
sys_db = client.db("_system", username=ARANGO_USER, password=ARANGO_PASSWORD)

# Connect to the database
db = client.db(ARANGO_DB_NAME, username=ARANGO_USER, password=ARANGO_PASSWORD)

# Create collection if it doesn't exist
if not db.has_collection(COLLECTION_NAME):
    db.create_collection(COLLECTION_NAME)

# Get collection
collection = db.collection(COLLECTION_NAME)


def fetch_mission_data():
    """Fetch mission data from NASA's Mission Design API."""
    mission_design_url = "https://ssd-api.jpl.nasa.gov/mdesign.api?des=1&class=true"
    response = requests.get(mission_design_url)
    return response.json()


def insert_mission_data(data):
    """Insert mission data into ArangoDB."""
    doc = {"mission_data": data}
    result = collection.insert(doc)
    return result["_id"]


def fetch_apod_data():
    """Fetch Astronomy Picture of the Day (APOD) data from NASA API."""
    apod_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    response = requests.get(apod_url)
    return response.json()


def download_image(image_url):
    """Download an image from a given URL and save it locally."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    image_filename = image_url.split("/")[-1]
    local_path = os.path.join(STORAGE_DIR, image_filename)

    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        with open(local_path, "wb") as f:
            shutil.copyfileobj(image_response.raw, f)
        return local_path

    print("Failed to download image")
    return None


def update_document(doc_id, mission_data, image_url, local_path):
    """Update ArangoDB document with image details."""
    updated_doc = {
        "mission_data": mission_data,
        "image_url": image_url,
        "local_path": local_path,
    }
    collection.update_match({"_id": doc_id}, updated_doc)
    print(f"Document updated with ID: {doc_id}")


def main():
    """Main execution function."""
    mission_data = fetch_mission_data()
    doc_id = insert_mission_data(mission_data)

    apod_data = fetch_apod_data()
    image_url = apod_data.get("url")

    if image_url:
        local_path = download_image(image_url)
        if local_path:
            update_document(doc_id, mission_data, image_url, local_path)
    else:
        print("No image URL found in APOD response")

    print("Process completed!")


if __name__ == "__main__":
    main()
