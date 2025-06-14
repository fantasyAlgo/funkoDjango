

# scripts/load_data.py
import os
import django
import sys
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "funkoDjango.settings")
django.setup()

from mainApp.models import FunkoPop
import random
import json
from groq import Groq

with open('/home/fantasy/Programming/pythonProjects/django/funkoDjango/funkoDjango/scripts/funko_pop.json') as json_file:
    data = json.load(json_file)

client = Groq()
def getText(m):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "Make a short description (max 3 lines) about the user funko pop, write only the description"
            },
            {
                "role" : "user",
                "content" : m
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    final_text = ""
    for chunk in completion:
        final_text += (chunk.choices[0].delta.content or "")
    return final_text

funkos = []
for i in tqdm(range(700, 1000)):
    f = data[i]
    desc = getText(f["title"])
    funkos.append(FunkoPop(name=f["title"], 
                           type=f["series"][0] if len(f["series"]) > 0 else "", 
                           description = desc,
                           link_image = f["imageName"], 
                           cost = random.randint(0, 40)
                           ))

#funkos = [
#    FunkoPop(name=f["title"], type=f["series"][0] if len(f["series"]) > 0 else "", link_image = f["imageName"], cost = random.randint(0, 40))
#    for f in data
#]
FunkoPop.objects.bulk_create(funkos)


