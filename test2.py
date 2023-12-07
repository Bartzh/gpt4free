from fastapi import FastAPI, Request
import uvicorn, json, datetime

import g4f

from g4f.Provider import Bing

g4f.debug.logging = True  # Enable logging
g4f.debug.check_version = False  # Disable automatic version checking
print(g4f.Provider.Ails.params)  # Supported args

app = FastAPI()
@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('topp')
    temperature = json_post_list.get('temp')
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": prompt}],
        timeout=120
    )
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": "history",
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    return answer


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=36262, workers=1)
