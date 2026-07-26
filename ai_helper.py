import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an assistant for a small online seller in Pakistan who sells 
leather wallets via Cash on Delivery (COD).

You will be given order details: customer name, phone, address, product, price, and notes.

You must respond in this exact format, nothing else:

MESSAGE: <a short, polite WhatsApp confirmation message, under 4 sentences, 
confirming the order and asking the customer to keep their phone reachable for delivery>

RISK_LEVEL: <Low, Medium, or High>

RISK_REASON: <one short sentence explaining the risk level, based on things like 
incomplete address, suspicious/repeated phone number patterns, missing notes, 
or generic/placeholder-looking names>
"""

def generate_message_and_risk(customer_name, phone, address, product, price, notes):
    user_prompt = f"""
    Customer Name: {customer_name}
    Phone: {phone}
    Address: {address}
    Product: {product}
    Price: {price}
    Notes: {notes if notes else "None"}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
    )

    output = response.choices[0].message.content

    message = ""
    risk_level = "Unknown"
    risk_reason = ""

    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("MESSAGE:"):
            message = line.replace("MESSAGE:", "").strip()
        elif line.startswith("RISK_LEVEL:"):
            risk_level = line.replace("RISK_LEVEL:", "").strip()
        elif line.startswith("RISK_REASON:"):
            risk_reason = line.replace("RISK_REASON:", "").strip()

    return message, risk_level, risk_reason