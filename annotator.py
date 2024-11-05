import base64
from openai import OpenAI
import openai
import os
client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
client = OpenAI()
template_msg =[
    {"role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "locate all the dishes and their annotated calories in pictures, please make list of all the dishes with their name, nutritions and nutrition facts, and the bbox to crop the dish",
        }]},
    {"role": "user",
        "content": [{
          "type": "image_url",
          "image_url": {
            "url":  '',"detail": "high"
          },
        },
      ],
    }
]
img = encode_image('01.jpg')
import cv2
import numpy as np

# Load a pre-trained model and set up the neural network.
('path_to_caffemodel_prototxt', 'path_to_caffemodel')
image = cv2.imread('01.jpg')

# Get the image dimensions
(h, w) = image.shape[:2]

# Create a blob from the image to forward pass through the network
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

# Set the blob as input to the network and perform a forward pass to compute the detections
net.setInput(blob)
detections = net.forward()

# Loop over the detections
for i in range(0, detections.shape[2]):
    # Extract the confidence of the prediction
    confidence = detections[0, 0, i, 2]

    # Filter out weak detections by ensuring the confidence is greater than a minimum threshold
    if confidence > 0.2:
        # Extract the index of the class label from the detections
        idx = int(detections[0, 0, i, 1])
        # Compute the (x, y)-coordinates of the bounding box for the object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # Draw the bounding box around the detected object on the image
        label = f"{confidence*100:.2f}%"
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
msg = template_msg
msg[1]['content'][0]['image_url']['url'] = f"data:image/jpeg;base64,{img}"
response = client.chat.completions.create(
    model="gpt-4o",
    messages=template_msg,
)
print(response.choices[0].message.content)
