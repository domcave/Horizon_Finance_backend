from openai import OpenAI
import constants
from app.extensions import db
from app.models.thread import Thread
import time
import json

def wait_on_run(run, thread_id, client):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


class OpenAIService:
    openai_api_key = constants.openai_secret_key
    client = OpenAI(api_key=openai_api_key)
    assistant_id = constants.openai_assistant_id
    
    def generate_summary(self, text):

        thread_id = db.session.query(Thread).filter_by(type="openai_assistant").first().thread

        message = self.client.beta.threads.messages.create(
                    thread_id=thread_id,
                    content=text,
                    role="user"
                )


        run = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=self.assistant_id)

        wait_on_run(run, thread_id, self.client)

        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id, order="asc", after=message.id
        )

        response = messages.data[0].content[0].text.value.replace('\n', '').replace('```json', '').replace('```', '')

        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            print("Error: OpenAI response was not valid JSON:", response)
            return None