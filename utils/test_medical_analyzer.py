from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import pdfplumber
from io import BytesIO
import json

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

client = genai.GenerativeModel("gemini-1.5-flash")  # Or 

actual_filename = "C:\\Users\\Asus\\Desktop\\GIT REPO HEALTH\\HealthSync-backend\\report analyzer\\UMR3110365.pdf"

uploaded_file = genai.upload_file(
    path=actual_filename,
    display_name="My Medical Report", # Optional: give it a friendly name
    mime_type='application/pdf'
)

print(f"Uploaded file name: {uploaded_file.name}")
print(f"Uploaded file URI: {uploaded_file.uri}")

def extract_text_from_pdf(pdf_content_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes, attempting to preserve table structure.
    """
    full_text = []
    try:
        with pdfplumber.open(BytesIO(pdf_content_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                full_text.append(f"\n--- PAGE {page_num + 1} ---\n")
                
                # Extract text
                text = page.extract_text()
                if text:
                    full_text.append(text)
                
                # Attempt to extract tables and format them clearly
                tables = page.extract_tables()
                for table in tables:
                    if table: # Ensure table is not empty
                        full_text.append("\n--- TABLE START ---\n")
                        for row in table:
                            cleaned_row = [cell if cell is not None else "" for cell in row]
                            full_text.append("\t".join(cleaned_row))
                        full_text.append("\n--- TABLE END ---\n")
            
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error extracting text from PDF with pdfplumber: {e}")
        return f"Error: Could not extract text from PDF: {e}"


def analyze_pdf_report(pdf_content_bytes: bytes, filename: str) -> dict:
    """
    Analyzes a PDF medical report by first extracting text and then using Gemini
    to extract key parameters in JSON format.
    """
    if not filename.lower().endswith('.pdf'):
        return {"error": "Unsupported file type. Only PDF files are supported for this analysis."}

    extracted_text = extract_text_from_pdf(pdf_content_bytes)
    
    if extracted_text.startswith("Error:"):
        return {"error": extracted_text}

    try:
        # --- MODIFIED PROMPT FOR BETTER JSON ADHERENCE ---
        prompt = f"""
        You are an intelligent medical report parser.
        Analyze the following text extracted from a patient's diagnostic test report.
        The text includes content from different pages, marked by "--- PAGE X ---".
        Tables are indicated by "--- TABLE START ---" and "--- TABLE END ---", with cells often separated by tabs.
        
        Extract ALL information meticulously and present it in a comprehensive, **STRICTLY VALID JSON** format.
        **DO NOT include any text or commentary outside the JSON object.**
        **Ensure all commas, brackets, and quotes are correctly placed according to JSON syntax rules.**
        Pay close attention to all text, including data that might have come from tables,
        to accurately associate 'Investigation', 'Observed Value', and 'Biological Reference Interval'.

        Ensure the JSON output includes:
        - `patient_details`: (Object)
            - `name`: Candidate's full name.
            - `age_gender`: Age and gender (e.g., "50 Years / Female").
            - `registered_by`: The referring clinic/hospital.
            - `reg_no`: Registration number.
            - `tid_sid`: TID/SID.
            - `registered_on`: Date and time of registration.
            - `collected_on`: Date and time of sample collection.
            - `reported_on`: Date and time the report was issued.
            - `reference`: Reference lab/clinic.
        - `test_sections`: (Array of Objects) Each object represents a distinct test section/department.
            Each object should contain:
            - `department`: The name of the department (e.g., "DEPARTMENT OF CLINICAL CHEMISTRY II").
            - `test_name`: The main test name for that section (e.g., "Thyroid Profile (T3, T4, TSH)").
            - `investigations`: (Array of Objects) Each detailing an individual investigation within that test.
                Each investigation object should include:
                - `name`: The name of the investigation (e.g., "25 Hydroxy Vitamin D").
                - `observed_value`: The value observed for the investigation.
                - `biological_reference_interval`: The normal/reference range for the investigation.
                - `method`: The method used for the investigation, if explicitly mentioned next to it.
            - `interpretation`: A concise summary of the interpretation for that test section.
            - `doctor_name`: The name of the doctor who signed off on this section of the report.
            - `doctor_designation`: The designation of the doctor.
            - `page_number`: The page number of this section within the PDF.

        If a field is not found, use `null` or an empty string, but do not omit the key.
        
        --- START OF EXTRACTED PDF TEXT ---
        {extracted_text}
        --- END OF EXTRACTED PDF TEXT ---
        """

        response = client.generate_content(contents=[uploaded_file, prompt], request_options={"timeout": 600})
        if response:
            print(response.text)
        else:
            return {"error": "No response text from LLM."}

        if response and response.text:
            try:
                # IMPORTANT: Strip leading/trailing whitespace to help with JSON parsing
                llm_response_text = response.text.strip() 
                
                # Check if the response already starts and ends with JSON markers
                if llm_response_text.startswith('{') and llm_response_text.endswith('}'):
                    json_string = llm_response_text
                else:
                    # Fallback for cases where LLM might add preamble/postamble text
                    json_start = llm_response_text.find('{')
                    json_end = llm_response_text.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_string = llm_response_text[json_start:json_end]
                    else:
                        return {"error": "Could not find a complete JSON object in the model's response.", "raw_response": llm_response_text}
                        
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                return {"error": f"Failed to parse JSON from LLM response: {e}", "raw_response": llm_response_text}
        else:
            return {"error": "No response text from LLM."}

    except Exception as e:
        return {"error": f"An error occurred during LLM analysis: {e}"}

if __name__ == "__main__":
    #actual_filename = "C:\\Users\\Asus\\Desktop\\GIT REPO HEALTH\\HealthSync-backend\\report analyzer\\UMR3110365.pdf"
    try:
        with open(actual_filename, "rb") as f:
            pdf_content_bytes_from_file = f.read()
        
        print(f"Analyzing {actual_filename} using text extraction approach...")
        result_json = analyze_pdf_report(pdf_content_bytes_from_file, actual_filename)
        
        if "error" in result_json:
            print("Error during analysis:")
            print(json.dumps(result_json, indent=2))
        else:
            print("Analysis successful! Extracted JSON:")
            print(json.dumps(result_json, indent=2))
            
    except FileNotFoundError:
        print(f"Error: The file '{actual_filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
