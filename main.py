from langchain.prompts import PromptTemplate
from prompts import *
from genai_info import *
from api_key import api_key
import openai

client = openai.OpenAI(api_key = api_key)

# Template to extract camp info
extraction_template = PromptTemplate.from_template("""
You are an information extraction bot. Your purpose is to extract the required
information from the given piece of camp description.
CAMP INFORMATION:
{CAMP_INFORMATION}
------------------------------------------------------
Specifically note the offerings, values, policies, location, dates, pricing, and age range.
Make sure you understand exactly what they are - write them down specifically in a JSON
format.
""")

extraction_prompt = extraction_template.format(CAMP_INFORMATION=CAMP_INFORMATION)

# Use LLMs to extract camp info
response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt=extraction_prompt,
  max_tokens = 2000
)

EXTRACTED_CAMP_INFO = response.choices[0].text


# A template combining all other templates
mega_template = PromptTemplate.from_template("""
{ROUTER_PROMPT}
------------------------------------------------------
Once you have determined what the parent wants you may utitlize the following information
given to you in JSON form. CAMP INFORMATION:
{EXTRACTED_CAMP_INFO}
------------------------------------------------------
Do not assume anything not inside CAMP INFORMATION about the camp - everything you
can tell them is in there. Specifically don't assume regular summer camp activities,
only tell about the offerings provided in CAMP INFORMATION.
------------------------------------------------------
{QUESTION_PROMPT}
------------------------------------------------------
{APPLICATION_PROMPT}
-----------------------------------------------------
When the parent has no further questions, politely end the conversation while making
clear to them that you are available for further questions.
""")

mega_prompt = mega_template.format(ROUTER_PROMPT=ROUTER_PROMPT, EXTRACTED_CAMP_INFO=EXTRACTED_CAMP_INFO,
                   QUESTION_PROMPT=QUESTION_PROMPT, APPLICATION_PROMPT=APPLICATION_PROMPT)


# Setup message queue
messages=[
    {"role": "system", "content": mega_prompt},
    {"role": "user", "content": "Hello."},
]

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages,
  temperature=0
)

# Intial response
resp_str = response.choices[0].message.content
messages.append({"role": "assistant", "content": resp_str})
print(f"Assistant: {resp_str}")

inp = input("You: ")
messages.append({"role": "user", "content": inp})

# Main Loop
while True:
  # Get response
  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages,
  temperature=0
  )
  resp_str = response.choices[0].message.content
  # Add to message queue
  messages.append({"role": "assistant", "content": resp_str})
  print(f"Assistant: {resp_str}")

  # Get user input
  inp = input("You: ")
  messages.append({"role": "user", "content": inp})

