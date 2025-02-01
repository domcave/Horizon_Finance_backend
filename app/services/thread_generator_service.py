from openai import OpenAI
import constants

class ThreadGenerator:
    client = OpenAI(api_key=constants.openai_secret_key)

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id
