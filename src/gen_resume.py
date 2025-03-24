import io
import markdown
from xhtml2pdf import pisa
from google import genai
from google.genai import types
from src.constants import GEMINI_API_KEY
from src.prompt import RESUME_GENERATOR_PROMPT

client = genai.Client(
    api_key = GEMINI_API_KEY,
)

def md_to_pdf(md_content):

    try:
        html_content = markdown.markdown(md_content)
        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-size: 16px; /* Adjust font size as needed */
                    line-height: 1.6; /* Adjust line spacing as needed */
                    font-family: sans-serif; /* Choose a readable font */
                }}
                h1 {{
                    font-size: 24px;
                }}
                h2 {{
                    font-size: 20px;
                }}
                /* Add more styles as needed */
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        output = io.BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=output)
        if pisa_status.err:
            return None
        pdf_data = output.getvalue()
        output.close()
        return pdf_data
    except Exception as e:
        return None

def get_resume(candidate_details, job_description):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text = f"""
                            Candidate Details:
                            {candidate_details}
                            Job Descripiton:
                            {job_description}
                        """
                    ),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction= RESUME_GENERATOR_PROMPT
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config,
        )
        
        return response.text
    except Exception as e:
        return None