import requests
import time


def get_llm_response(prompt: str):
    # time.sleep(10)
    response = requests.post(f"http://localhost:5000/ai", json={"Question": prompt})
    answer = response.json()
    return answer["answer"]


while True:
    print("Worker beep...")

    response = requests.put("http://vps:8080/prompt", json={"Auth": "secret"})

    print(response.status_code)
    message = response.json()
    print(message)

    if "QueueId" in message:
        print(f"Getting answer from LLM with prompt {message['Prompt']}...")
        answer = get_llm_response(message["Prompt"])

        print(f"Answer is {answer}")
        response = requests.post(
            f"http://vps:8080/prompt/{message['QueueId']}",
            json={"Auth": "secret", "Response": answer},
        )
        print(response.status_code)

    time.sleep(3)
