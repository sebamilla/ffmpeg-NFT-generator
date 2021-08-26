#!/usr/bin/env python
# coding: utf-8

# In[49]:


from PIL import Image 
from IPython.display import display 
import random
import json


# In[50]:


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


# In[51]:


## Generate Traits

TOTAL_IMAGES = 300 # Number of random unique images we want to generate

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
    


# In[52]:


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))


# In[53]:


# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1


# In[54]:


print(all_images)


# In[55]:


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


# In[56]:


#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


# In[57]:



  
#### Generate Images    
for item in all_images:

  im1 = Image.open(f'./trait-layers/backgrounds/{background_files[item["Background"]]}.png').convert('RGBA')
  im2 = Image.open(f'./trait-layers/bodies/{body_files[item["Body"]]}.png').convert('RGBA')
  im3 = Image.open(f'./trait-layers/heads/{head_files[item["Head"]]}.png').convert('RGBA')
  im4 = Image.open(f'./trait-layers/faces/{face_files[item["Face"]]}.png').convert('RGBA')
  im5 = Image.open(f'./trait-layers/hairs/{hair_files[item["Hair"]]}.png').convert('RGBA')

  
  #Create each composite
  com1 = Image.alpha_composite(im1, im2)
  com2 = Image.alpha_composite(com1, im3)
  com3 = Image.alpha_composite(com2, im4)
  com4 = Image.alpha_composite(com3, im5)

  #Convert to RGB
  rgb_im = com4.convert('RGB')
  file_name = str(item["tokenId"]) + ".png"
  rgb_im.save("./images/" + file_name)
  
  
  


# In[58]:


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
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
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


# In[ ]:




