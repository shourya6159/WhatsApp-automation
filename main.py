import time
import sys
import io
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from openai import OpenAI

# Terminal Signal Integrity
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

# --- SYSTEM CONFIG ---
OPENROUTER_API_KEY = " " 
MODEL_ID = "meta-llama/llama-3.2-3b-instruct"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- BRAIN CORE ---
def generate_ai_response(user_input):
    """
    Step 2 Placeholder: Uses the pre-trained base model.
    We will replace this logic with your fine-tuned weight later.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a professional, polite, and efficient virtual assistant. Provide clear, concise, and helpful responses."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=50
        )
        # Removed .lower() to maintain professional capitalization
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"🧠 Brain Fault: {e}")
        # Replaced the uwu error message with a professional one
        return "I apologize, but I encountered a system error."

# --- ACTUATOR CORE ---
def type_humanly(driver, text):
    selector = "div[contenteditable='true'][data-tab='10']"
    try:
        textbox = driver.find_element(By.CSS_SELECTOR, selector)
        textbox.click()
        time.sleep(0.3)
        for char in text:
            driver.execute_script(
                "var el = arguments[0]; var str = arguments[1]; el.focus(); "
                "document.execCommand('insertText', false, str); "
                "el.dispatchEvent(new Event('input', { bubbles: true }));",
                textbox, char
            )
            time.sleep(random.uniform(0.02, 0.05))
        time.sleep(0.5)
        textbox.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Actuator Fault: {e}")

# --- CONTROLLER SETUP ---
brave_options = Options()
brave_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=brave_options)

# We use the raw text + timestamp as the latch signature
last_signature = None
print("🟢 Step 2 Online. AI Brain engaged.")

# --- MAIN OPERATION LOOP ---
while True:
    try:
        inbound = driver.find_elements(By.CLASS_NAME, "message-in")
        
        if inbound:
            latest_bubble = inbound[-1]
            
            # The Bubble Signature includes the text AND the time (e.g. "Lmao 19:40")
            # This guarantees we detect follow-ups perfectly without relying on HTML IDs.
            current_signature = latest_bubble.text.strip()

            # Logic Latch: Only process if the signature has changed
            if current_signature != last_signature and current_signature != "":
                
                # 1. Safely extract content using find_elements (prevents crash on stickers)
                stickers = latest_bubble.find_elements(By.CSS_SELECTOR, "img[alt*='Sticker']")
                reply_text = latest_bubble.find_elements(By.CSS_SELECTOR, "._akbu [data-testid='selectable-text']")
                normal_text = latest_bubble.find_elements(By.CSS_SELECTOR, "span.copyable-text")
                
                input_signal = None
                if stickers:
                    input_signal = "[user sent a sticker]"
                    print("📥 New Signal: Sticker")
                elif reply_text:
                    input_signal = reply_text[0].text.strip()
                    print(f"📥 New Signal: {input_signal}")
                elif normal_text:
                    # [-1] ensures we grab the newest text, not an old quote
                    input_signal = normal_text[-1].text.strip()
                    print(f"📥 New Signal: {input_signal}")
                else:
                    input_signal = "[user sent media]"
                    print("📥 New Signal: Media")

                if input_signal:
                    # Humanized processing delay
                    time.sleep(random.uniform(1.5, 3.0))
                    
                    # Let the AI think
                    ai_reply = generate_ai_response(input_signal)
                    print(f"📤 AI Output: {ai_reply}")
                    
                    # Drive output
                    type_humanly(driver, ai_reply)

                # Latch state using the signature so we wait for the NEXT message
                last_signature = current_signature
                    
    except (StaleElementReferenceException, NoSuchElementException):
        continue
    except Exception as e:
        print(f"❌ Bus Error: {e}")
    
    time.sleep(1)
