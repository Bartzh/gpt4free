from fastapi import FastAPI, Request
import uvicorn, json, datetime

import g4f

from g4f.Provider import Bing

g4f.debug.logging = True  # Enable logging
g4f.debug.check_version = False  # Disable automatic version checking
print(g4f.Provider.Ails.params)  # Supported args

app = FastAPI()

@app.get("/")
def read_root():
    print('onget')
    return 'onget'

@app.post("/imitate/v1/chat/completions")
async def create_item(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    history = json_post_list.get('history')
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        provider=g4f.Provider.Bing,
        messages=history,
        timeout=120
    )
    history.append({"role": "assistant", "content": response})
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    return answer


if __name__ == '__main__':
    aihistory = []
    uvicorn.run(app, host='0.0.0.0', port=36262, workers=1)
