curl https://api.x.ai/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer xai-NbIax9xQ2WMzMQ5xTVYv47AmHLAcU5md42b10veZ7UEXySbqB9X7P5AA5HuG1rZqnc5zbjbNrOvgixIW" -d '{
  "messages": [
    {
      "role": "system",
      "content": "You are a test assistant."
    },
    {
      "role": "user",
      "content": "Testing. Just say hi and hello world and nothing else."
    }
  ],
  "model": "grok-beta",
  "stream": false,
  "temperature": 0
}'