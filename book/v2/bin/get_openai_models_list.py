#!/bin/env python3
from openai import OpenAI
import os
from datetime import datetime

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)
models = client.models.list()

dlist = []
for model in models:
    timestamp = model.created

    # Convert to datetime object
    date_obj = datetime.utcfromtimestamp(timestamp)  # Use datetime.fromtimestamp() for local time

    # Format as a readable string
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')

    dlist.append((formatted_date, model.id))

# Sort the list by the first element (date)
dlist.sort(key=lambda x: x[0])

for item in dlist:
    print(item)
