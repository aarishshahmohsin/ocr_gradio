import gradio as gr
from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor
import re
from transformers import AutoModel, AutoTokenizer
import torch
import tempfile
import os

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
got_model_name = "stepfun-ai/GOT-OCR2_0" if device == 'cuda' else "aarishshahmohsin/got_ocr_2"

det_processor, det_model = load_det_processor(), load_det_model()
det_model.to(device)
rec_model, rec_processor = load_rec_model(), load_rec_processor()
rec_model.to(device)

tokenizer = AutoTokenizer.from_pretrained(got_model_name, trust_remote_code=True, device_map=device)
got_model = AutoModel.from_pretrained(got_model_name, trust_remote_code=True, low_cpu_mem_usage=True, device_map=device, use_safetensors=True)
got_model = got_model.eval().to(device)

def extract_hindi(text):
    hindi_pattern = re.compile(r'[\u0900-\u097F]+')  # Unicode range for Devanagari script
    hindi_words = hindi_pattern.findall(text)
    return ' '.join(hindi_words)

def process_image(image):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name)
        temp_file_path = temp_file.name

    image = Image.open(temp_file_path)
    image = image.convert("RGB")  

    langs = ["hi"]  
    surya_predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)
    
    surya_text_list = re.findall(r"text='(.*?)'", str(surya_predictions[0]))
    surya_text = '\n'.join(surya_text_list)  
    surya_text = extract_hindi(surya_text)
    
    got_res = got_model.chat(tokenizer, temp_file_path, ocr_type='ocr')

    combined_text = f"<h2> Hindi Text (Surya OCR) </h2> <br>{surya_text}<br> <br> <h2> English Text (GOT OCR) </h2> <br> {got_res}"

    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return combined_text

def highlight_search(text, query):
    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        highlighted_text = pattern.sub(lambda m: f"<span style='background-color: limegreen;'>{m.group(0)}</span>", text)
        return highlighted_text
    return text

with gr.Blocks() as ocr_interface:
    gr.Markdown("# OCR Application (IIT Roorkee Assignment)")
    gr.Markdown("Upload an image for OCR processing. This uses Surya OCR (for Hindi) and GOT-OCR (for English). The results from both models will be concatenated. (Takes 2-3 minutes for inference due to running on CPU)")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload an Image")
            run_ocr_button = gr.Button("Run OCR")

        with gr.Column():
            output_text = gr.HTML(label="Extracted Text")
            query_input = gr.Textbox(label="Search in extracted text", placeholder="Type to search...")
            search_button = gr.Button("Search")
    
    def process_and_display(image):
        combined_text = process_image(image)
        return combined_text

    def search_text(combined_text, query):
        highlighted = highlight_search(combined_text, query)
        return highlighted

    run_ocr_button.click(fn=process_and_display, inputs=image_input, outputs=output_text)

    search_button.click(fn=search_text, inputs=[output_text, query_input], outputs=output_text)

ocr_interface.launch()
