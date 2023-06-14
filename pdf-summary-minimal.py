#----- read in PDF

from PyPDF2 import PdfReader
pdf_r = PdfReader("pdfs/paper.pdf")

text = ""
# define a word, after which parsing of PDF is terminated (useful for academic papers)
break_word = "References" # case-sensitive

for page in pdf_r.pages:
    page_text = page.extract_text()
    if break_word in page_text:
        text += page_text.split(break_word)[0]
        break
    else:
        text += page_text

#----- summarise the extracted text
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k", 
    messages=[
        {"role": "user", "content": f"Summarise: {text} in 200 words."}
        ],
    temperature=0.0,
    max_tokens=300
)

print(chat_completion.choices[0].message.content)
