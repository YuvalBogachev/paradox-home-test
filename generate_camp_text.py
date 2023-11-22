# Generate camp information (run this once and once only)
import openai
from api_key import api_key

GENERATION_PROMPT = """
Create a fictional GenAI Summer Camp including offerings, values, policies,
location, dates, pricing, and age range. The summer camp will have a focus on
data science and will targeted at children.
Since this is a summer camp the focus will be on providing the children an exciting
environment to spend their summer in while ensuring the parents that their kids
are in good hands. Generate a response in the lentgh of 1500 words.
"""

client = openai.OpenAI(api_key = api_key)


response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt=GENERATION_PROMPT,
  max_tokens = 2000,
  temperature = 0
)

print(response.choices[0].text)
