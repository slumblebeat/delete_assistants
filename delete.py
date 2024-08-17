import os
from dotenv import load_dotenv
import time
import schedule
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

# list all of our assistants 
def list_assistants(client, limit=100):
    return client.beta.assistants.list(order='desc', limit=str(limit))

# function that deletes an assistant
def delete_assistant(client, assistant_id):
    try:
        response = client.beta.assistants.delete(assistant_id=assistant_id)
        print(f'Deleted: {assistant_id} thanks moon!')
        return response 
    except Exception as e:
        print(f'Error deleting {assistant_id}: {e}')

# what about saving some assistants
do_not_delete_ids = {
    'asst_9smBZ4UYHSS3FQZZ0iFAjVP8',
    'asst_unKu7DQ43jMdfjlZcCjNAzWK',
    'asst_55xzDmOv2VzfvdjlGO2lGvz4',
}

def bot():
    # get the list of assistants 
    my_assistants = list_assistants(client)

    # delete all of the assistants that are not in the do_not_delete_ids set
    for assistant in my_assistants.data:
        if assistant.id not in do_not_delete_ids:
            delete_assistant(client, assistant.id)
            time.sleep(.2)
        else:
            print(f'Not deleting: {assistant.id}')


schedule.every(2).seconds.do(bot)   

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print(f'+++++ maybe an internet problem.. code failed. sleeping 10: {e}')
        time.sleep(10)
