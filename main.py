import openai
import dotenv
from config import *
from io import BytesIO

# Load API key
api_key = dotenv.dotenv_values().get("OPEN_AI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Upload code files as .txt
uploaded_files = []
for path in files_to_upload:
    with open(path, "rb") as f:
        # converts to text file since file upload isn't supported (except PDFs for some reason)
        # workaround until OpenAI fixes their API to allow direct file upload
        base_path=path.split("/")[-1].split(".")[0]
        name=base_path+".txt"
        uploaded_files.append([f.read(), name])
# Temporarily just embedding files as text until I can upload non-PDF files to responses (rather than deprecated Assistants API)
in_msg = [
    {"role": "user",
     "content": [{"type": "text", "text": text_msg}] + [{"type": "text", "text": f"This is the content of {file[1]}: {file[0]}"} for file in uploaded_files]
}]

# gets the response
response = client.chat.completions.create(
    model="gpt-4o",
    messages=in_msg,
)

print("Response received. Writing to response.md...")
# saves response to markdown file to allow for formatting
with open("response.md", "w") as f:
    f.write(response.choices[0].message.content)

# Print the assistant’s response
# now deprecated
# print(response.choices[0].message.content)