from flask import Flask, request, jsonify, render_template, send_file,flash,redirect
from io import BytesIO
import pdfkit
from transformers import pipeline
from PyPDF2 import PdfReader, PdfWriter
import aspose.words as aw


app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Retrieve the PDF file from the request
    pdf_File = request.files['file']
    if(pdf_File=='' or pdf_File.filename.split('.')[-1]!='pdf'):
        flash('Please upload the PDF file!')
        return redirect('/')
        
    reader=PdfReader(pdf_File)
    page = reader.pages[0]

    text = page.extract_text()
    string=""
    for i in reader.pages:
     text = i.extract_text()
     string+=text


    words= string.split()
    substrings=[]
    start_index=0
    while start_index < len(words):
            end_index = min(start_index + 500, len(words))
            substring = ' '.join(words[start_index:end_index])
            substrings.append(substring)
            start_index = end_index




    summarizer= pipeline("summarization")

    final_summary=[]
    index=0
    for i in substrings:
        final_summary.append(summarizer(i,max_length=200,min_length=100,do_sample=False))
    
    
    test1=""" """
    for i in final_summary:
        test1+=i[0]['summary_text']+"\n"
    

    file_name= pdf_File.filename.split('.')[0]+'summary.txt'
    text_file=open( file_name,"w")
    n=text_file.write(test1)
    text_file.close()
    str
    # Convert the PDF file to HTML using pdfkit
   # input_html = pdfkit.from_file(input_pdf, False)
    
    # Insert your own processing logic here to modify the HTML as needed
    
    # Convert the HTML back to PDF using pdfkit


    output_pdf = file_name
    
    # Return the output PDF as a download attachment
    return send_file(output_pdf,  as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
