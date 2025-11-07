import requests
import time
from config import PAYSTACK_SECRET_KEY, PAYSTACK_BASE_URL

HEADERS = {
    "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    "Content-Type": "application/json"
}
          

def initialize_payment(email: str, amount:  int, product_name: str = "payment"):
    reference = f"{product_name}_{int(time.time() * 1000)}"
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    data = {"email": email, "amount": amount * 100, "reference": reference}
    
    try:
        response = requests.post(url, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()  # Raises exception for 4xx/5xx
        return response.json()
    except requests.exceptions.Timeout:
        return {"status": False, "message": "Request timed out."}
    except requests.exceptions.ConnectionError as e:
        return {"status": False, "message": f"Connection error: {e}"}
    except requests.exceptions.HTTPError as e:
        return {"status": False, "message": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": False, "message": f"An error occurred: {e}"}
    

def verify_payment(reference: str):
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    response = requests.get(url, headers=HEADERS)
    return response.json()