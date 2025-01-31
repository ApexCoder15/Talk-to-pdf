from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from io import BytesIO
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import fitz

template = """You are expert in answering questions related to given text, give answers based on the given text only.: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="deepseek-r1:14b")

chain = prompt | model



def get_res(pdf_file, question):
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Load each page
        text += page.get_text()  # Extract text from the page
    return chain.invoke({"question": "Text:"+text+"Qustion about given text:"+question})

def index(request):
    if request.method == 'POST':
        # Get the uploaded PDF file and the string input
        if 'pdf-file' in request.FILES:
            pdf_file = request.FILES['pdf-file']
            pdf_file_in_memory = BytesIO(pdf_file.read())  # Read the file into memory
            input_string = request.POST.get('input-string', '')
            # Extract text from the PDF
            pdf_text = get_res(pdf_file_in_memory, input_string)
        else:
            pdf_text = "No PDF uploaded."
        
          # Get the string input
        
        # Return both the extracted PDF text and the entered string in the response
        return HttpResponse(f'Answer: <br>{pdf_text}<br><br>')
    
    return render(request, 'uploadPdf.html')