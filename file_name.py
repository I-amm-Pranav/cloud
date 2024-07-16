# Import necessary modules
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time

# Subscription key and endpoint from Azure Cognitive Services
subscription_key = "720436171a4a46c1a228c59cc04c766e"
endpoint = "https://pranav-nandha.cognitiveservices.azure.com/"

# Initialize Computer Vision client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

print("===== Read File - remote =====")

# URL of the image to perform text recognition
read_image_url = "https://i.stack.imgur.com/0Jl54.png"

# Perform read operation on the remote image
read_response = computervision_client.read(read_image_url, raw=True)

# Get the operation location to track the status
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

# Wait for the operation to complete
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text and bounding boxes line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)

print()
print("End of Text Recognition..")
