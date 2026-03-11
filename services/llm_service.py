from groq import Groq
import logging
from configs.configs import GROQ_API_KEY

logger = logging.getLogger(__name__)

def rephrase_output(prompt, ocr_output):
    client = Groq(api_key=GROQ_API_KEY)
    
    ocr_text = "\n".join(ocr_output)
    full_prompt = f"{prompt}\n{ocr_text}"
    
    logger.debug(f"Received prompt and ocr output.")
    
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}],
            response_format={"type": "json_object"}
        )
        response = chat_completion.choices[0].message.content
        
        if not response:
            logger.debug(f"Did not receive a response. Response: {response}")
        else:
            return response
    except Exception as e:
        logger.error(f"Error communicating with LLM: {e}")
        return None