from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or replace "*" with your frontend's URL like "http://localhost:5173")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Sample in-memory storage
orders = []
item_totals = {"burger": 0, "fries": 0, "drink": 0}
order_id = 1

key1 = "sk-proj-"
key2 = "TIQAlncX3SomJEx6yUVDunJmTOdNWPOiWUgPVi7bwR27A7eD93JBV1PffU2OhTOFRbkmz"
# OpenAI API Setup
openai.api_key = key1 + key2 + "RaJW0T3BlbkFJbDzkGpNx4cmoJ9XrjSfgl2I_47Jm9XlI7sxF9GXMDXdFKQ0m2eTaRaztyxefKaA8Cl-L4NeJcA"

class UserRequest(BaseModel):
    message: str

def parse_user_input(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
            "You are an assistant for a drive-thru ordering system. Interpret user inputs "
            "to extract the number of items and return the data in the following JSON format:\n\n"
            "{\n"
            "    \"data\": {\n"
            "        \"totals\": {\n"
            "            \"burger\": <number_of_burgers>,\n"
            "            \"fries\": <number_of_fries>,\n"
            "            \"drink\": <number_of_drinks>\n"
            "        },\n"
            "        \"orders\": [\n"
            "            {\n"
            "                \"order_id\": <order_number>,\n"
            "                \"items\": [\n"
            "                    {\"item\": <item_name>, \"quantity\": <quantity>}\n"
            "                ]\n"
            "            }\n"
            "        ],\n"
            "        \"cancel_order_id\": <order_id_to_cancel>\n"
            "    }\n"
            "}"
        ),
            },
            {"role": "user", "content": input_text},
        ]
    )

    # Parse the response
    result = response.choices[0].message['content']
    return result

VALID_PRODUCTS = {"burger", "fries", "drink"}  # Define valid products

@app.post("/parse_request")
async def parse_request(user_request: UserRequest):
    global order_id, orders, item_totals

    if user_request.message is None:
        raise ValueError("No message provided in the user request")
    
    # Parse user input
    res = parse_user_input(user_request.message)
    result = json.loads(res)["data"]

    # Handle order placement
    if "orders" in result and result["orders"]:
        new_order = {"id": order_id, "items": result["orders"]}

        # Validate order items
        for order in result["orders"]:
            for item in order["items"]:
                if item["item"] not in VALID_PRODUCTS:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Item '{item['item']}' not found"
                    )

        # Add order to list
        orders.append(new_order)

        # Update totals
        for order in result["orders"]:
            for item in order["items"]:
                item_totals[item["item"]] += item["quantity"]

        order_id += 1
        return {"message": "Order placed successfully.", "order_id": order_id - 1}

    # Handle cancellation
    if "cancel_order_id" in result:
        cancel_id = result["cancel_order_id"]

        # Validate cancel order ID
        if not any(order["id"] == cancel_id for order in orders):
            raise HTTPException(
                status_code=404,
                detail=f"Order {cancel_id} not found"
            )

        # Cancel the order
        canceled = False
        for order in orders:
            if order["id"] == cancel_id:
                orders.remove(order)
                canceled = True

                # Update totals
                for item in order["items"]:
                    for sub_item in item["items"]:
                        item_totals[sub_item["item"]] -= sub_item["quantity"]
                break

        if canceled:
            return {"message": f"Order {cancel_id} canceled successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Order {cancel_id} not found.")

    # Invalid request
    raise HTTPException(
        status_code=400,
        detail="Invalid request. Please provide a valid order or cancel request."
    )


@app.get("/get_summary")
async def get_summary():
    return {"totals": item_totals, "orders": orders}