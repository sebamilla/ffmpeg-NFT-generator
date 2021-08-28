#!/usr/bin/env python
# coding: utf-8


import moviepy.editor as mpe
import random
import json



# Each video is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue", "Orange", "Purple", "Red", "Yellow"] 
background_weights = [30, 44, 15, 1, 10]

body = ["Blue", "Green", "Orange", "Red", "Yellow"] 
body_weights = [34, 40, 15, 10, 1]

head = ["Blue", "Green", "Red", "Yellow"] 
head_weights = [40, 40, 19, 1]

face = ["Blue", "Green", "Orange", "Red", "Yellow"] 
face_weights = [30, 40, 15, 1, 14]

hair = ["Blue", "Green", "Orange", "Red", "Yellow"] 
hair_weights = [30, 1, 15, 45, 10]



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

TOTAL_VIDEOS = 10 # Number of random unique videos we want to generate

all_videos = [] 

# A recursive function to generate unique video combinations
def create_new_video():
    
    new_video = {} #

    # For each trait category, select a random trait based on the weightings 
    new_video ["Background"] = random.choices(background, background_weights)[0]
    new_video ["Body"] = random.choices(body, body_weights)[0]
    new_video ["Head"] = random.choices(head, head_weights)[0]
    new_video ["Face"] = random.choices(face, face_weights)[0]
    new_video ["Hair"] = random.choices(hair, hair_weights)[0]
    
    if new_video in all_videos:
        return create_new_video()
    else:
        return new_video
    
    
# Generate the unique combinations based on trait weightings
for i in range(TOTAL_VIDEOS): 
    
    new_trait_video = create_new_video()
    
    all_videos.append(new_trait_video)
    



# Returns true if all videos are unique
def all_videos_unique(all_videos):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_videos)

print("Are all videos unique?", all_videos_unique(all_videos))



# Add token Id to each video
i = 0
for item in all_videos:
    item["tokenId"] = i
    i = i + 1



print(all_videos)


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

for video in all_videos:
    background_count[video["Background"]] += 1
    body_count[video["Body"]] += 1
    head_count[video["Head"]] += 1
    face_count[video["Face"]] += 1
    hair_count[video["Hair"]] += 1
    
print(background_count)
print(body_count)
print(head_count)
print(face_count)
print(hair_count)


#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata-video/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_videos, outfile, indent=4)


#### Generate videos with ffmpeg

for item in all_videos:

    clip1 = mpe.VideoFileClip(f'./trait-layers-video/backgrounds/{background_files[item["Background"]]}.mov')
    clip2 = mpe.VideoFileClip(f'./trait-layers-video/bodies/{body_files[item["Body"]]}.mov', has_mask=True)
    clip3 = mpe.VideoFileClip(f'./trait-layers-video/heads/{head_files[item["Head"]]}.mov', has_mask=True)
    clip4 = mpe.VideoFileClip(f'./trait-layers-video/faces/{face_files[item["Face"]]}.mov', has_mask=True)
    clip5 = mpe.VideoFileClip(f'./trait-layers-video/hairs/{hair_files[item["Hair"]]}.mov', has_mask=True)
    full_clip = mpe.CompositeVideoClip([clip1, clip2, clip3, clip4, clip5])

    full_clip.write_videofile(f"./videos/{str(item['tokenId'])}.mp4", threads=286, fps=12, audio=False) 


#### Generate Metadata for each Image    

f = open('./metadata-video/all-traits.json',) 
data = json.load(f)


VIDEOS_BASE_URI = "ADD_VIDEOS_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "video": VIDEOS_BASE_URI + str(token_id) + '.mov',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Body", i["Body"]))
    token["attributes"].append(getAttribute("Head", i["Head"]))
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))

    with open('./metadata-video/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()