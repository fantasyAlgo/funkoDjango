
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "funkoDjango.settings")
django.setup()

from mainApp.models import FunkoPop
from groq import Groq
from tqdm import tqdm

client = Groq()
def getText(m):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "Identify if the given funko pop is [Marvel, DC, Disney, Anime, Video games, Other], write only that"
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

for funko in tqdm(FunkoPop.objects.all()):
    funko.category = getText(funko.name)
    funko.cost += 15
    funko.save()

