#!/usr/bin/env python
# coding: utf-8


import moviepy.editor as mpe
from IPython.display import display 
import random
import json



# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue", "Orange", "Purple", "Red", "Yellow"] 
background_weights = [30, 40, 15, 5, 10]

body = ["Blue", "Green", "Orange", "Red", "Yellow"] 
body_weights = [30, 40, 15, 5, 10]

head = ["Blue", "Green", "Red", "Yellow"] 
head_weights = [30, 40, 20, 10]

face = ["Blue", "Green", "Orange", "Red", "Yellow"] 
face_weights = [30, 40, 15, 5, 10]

hair = ["Blue", "Green", "Orange", "Red", "Yellow"] 
hair_weights = [30, 40, 15, 5, 10]



# Dictionary variable for each trait. 
# Eech trait corresponds to its file name

background_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
}

body_files = {
    "Blue": "blue-body",
    "Green": "green-body",
    "Orange": "orange-body",
    "Red": "red-body",
    "Yellow": "yellow-body"   
}

head_files = {
    "Blue": "blue-head",
    "Green": "green-head",
    "Red": "red-head",
    "Yellow": "yellow-head"  
          
}
face_files = {
    "Blue": "blue-face",
    "Green": "green-face",
    "Orange": "orange-face",
    "Red": "red-face",
    "Yellow": "yellow-face"  
          
}
hair_files = {
    "Blue": "blue-hair",
    "Green": "green-hair",
    "Orange": "orange-hair",
    "Red": "red-hair",
    "Yellow": "yellow-hair"  
          
}


## Generate Traits

TOTAL_IMAGES = 2 # Number of random unique images we want to generate

all_images = [] 

# A recursive function to generate unique image combinations
def create_new_image():
    
    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image ["Background"] = random.choices(background, background_weights)[0]
    new_image ["Body"] = random.choices(body, body_weights)[0]
    new_image ["Head"] = random.choices(head, head_weights)[0]
    new_image ["Face"] = random.choices(face, face_weights)[0]
    new_image ["Hair"] = random.choices(hair, hair_weights)[0]
    
    if new_image in all_images:
        return create_new_image()
    else:
        return new_image
    
    
# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    
    new_trait_image = create_new_image()
    
    all_images.append(new_trait_image)
    



# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))



# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1



print(all_images)


# Get Trait Counts

background_count = {}
for item in background:
    background_count[item] = 0
    
body_count = {}
for item in body:
    body_count[item] = 0

head_count = {}
for item in head:
    head_count[item] = 0
    
face_count = {}
for item in face:
    face_count[item] = 0
    
hair_count = {}
for item in hair:
    hair_count[item] = 0

for image in all_images:
    background_count[image["Background"]] += 1
    body_count[image["Body"]] += 1
    head_count[image["Head"]] += 1
    face_count[image["Face"]] += 1
    hair_count[image["Hair"]] += 1
    
print(background_count)
print(body_count)
print(head_count)
print(face_count)
print(hair_count)


#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


#### Generate videos with ffmpeg

for item in all_images:

    clip1 = mpe.VideoFileClip(f'./trait-layers-video/backgrounds/{background_files[item["Background"]]}.mov')
    clip2 = mpe.VideoFileClip(f'./trait-layers-video/bodies/{body_files[item["Body"]]}.mov', has_mask=True)
    clip3 = mpe.VideoFileClip(f'./trait-layers-video/heads/{head_files[item["Head"]]}.mov', has_mask=True)
    clip4 = mpe.VideoFileClip(f'./trait-layers-video/faces/{face_files[item["Face"]]}.mov', has_mask=True)
    clip5 = mpe.VideoFileClip(f'./trait-layers-video/hairs/{hair_files[item["Hair"]]}.mov', has_mask=True)
    full_clip = mpe.CompositeVideoClip([clip1, clip2, clip3, clip4, clip5])

    full_clip.write_videofile(f"./videos/{str(item['tokenId'])}.mp4") 


#### Generate Metadata for each Image    

f = open('./metadata/all-traits.json',) 
data = json.load(f)


IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.mov',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Body", i["Body"]))
    token["attributes"].append(getAttribute("Head", i["Head"]))
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()