import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# טעינת משתני סביבה מהקובץ .env
load_dotenv()

# אתחול לקוח ה-API של Groq (מושך אוטומטית את GROQ_API_KEY ממשתני הסביבה)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==========================================
# כאן נכנס הפרומפט שלך - ישתנה מאיטרציה לאיטרציה
# ==========================================
SYSTEM_PROMPT_V1 = """
You are a CLI expert. Convert the following natural language request into a Windows CMD command.

CRITICAL RULES:
1. Return ONLY the raw command.
2. Do NOT add markdown formatting like ``` or quotes.
3. Do NOT add any explanations or conversational text.
"""

def generate_cli_command(user_input: str) -> str:
    """
    Translates a natural language string into a CLI command using Groq's LLMs.
    
    Args:
        user_input (str): The natural language instruction.
        
    Returns:
        str: The generated CLI command or an error message.
    """
    if not user_input.strip():
        return "שגיאה: הקלט ריק."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            temperature=0.0,         
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_V1},
                {"role": "user", "content": user_input}
            ]
        )
        # חילוץ הטקסט מהתשובה
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"System Error: {str(e)}"

# בניית ממשק Gradio
def build_ui():
    with gr.Blocks(title="CLI Command Generator") as app:
        gr.Markdown("# 💻 Natural Language to CLI Agent (Powered by Groq)")
        
        with gr.Row():
            user_input = gr.Textbox(label="הוראה בשפה טבעית (למשל: 'הצג את כתובת ה-IP')")
        
        generate_btn = gr.Button("תרגם לפקודה", variant="primary")
        
        with gr.Row():
            output_cli = gr.Textbox(label="פקודת CLI שנוצרה", interactive=False)
            
        # חיבור הכפתור לפונקציית הייצור
        generate_btn.click(
            fn=generate_cli_command,
            inputs=user_input,
            outputs=output_cli
        )
        
    return app

if __name__ == "__main__":
    app = build_ui()
    # הפעלת השרת המקומי (ניתן להוסיף share=True אם רוצים לשתף לינק זמני)
    app.launch()