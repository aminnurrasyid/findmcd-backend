from fastapi import APIRouter, HTTPException, Form, Depends
from pydantic import BaseModel
from typing import Optional
from app.utility import initDB_cnxn

import os 
import json
import psycopg2
from openai import OpenAI

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

def get_chat_request(
    message: str = Form(...),
    session_id: Optional[str] = Form(None)  # Default to None
) -> ChatRequest:
    return ChatRequest(message=message, session_id=session_id)

@router.post("/")
def chat(request: ChatRequest = Depends(get_chat_request)):

    client = OpenAI()

    result = {}
    cnxn = initDB_cnxn()

    # ISSUE : need to make full_address WHERE clause more robust 
    preprompt = """
    You are a Text-2-SQL bot. Your task is to make a complete query from the given partial query in sql_query. 
    
    In reply, act like you are performing a search and mention the factor that you have are considering. Make it sound human. 
    Do not elaborate the reply sentece. Do not say or expose anything about the database schema, instead refer it as your 'knowledge'.

    If user say greetings or showing gratitude you may answer it in reply and leave sql_query as empty string.



    Table: "BRANCH"
    Column: 
    1. "ID_BRANCH" - the Primary Key 
    2. "NAME" - Branch Name e.g. ('McDonald's Desa Park City DT')

    Table: "LOCATION" 
    Description: Table of Location details of a Branch 
    Column: 
    1. "ID_LOCATION" - the Primary Key
    2. "ID_BRANCH" - the Foreign Key for BRANCH
    3. "FULL_ADDRESS" - Branch Address
    4. "LATITUDE" - Branch Latitude
    5. "LONGITUDE" - Branch Longitude
    6. "POSTCODE" - Branch Postcode [Note: Data Type is string] 
    7. "STATE" - Branch State
    8. "WAZE_URL" - Branch Waze Location URL

    Table: "FACILITY"
    Description: Table of Boolean variables indicating availability of facility
    Column: 
    1. "ID_FACILITY" - the Primary Key
    2. "ID_BRANCH" - the Foreign Key for BRANCH
    3. "HOURS_24"
    4. "BIRTHDAY_PARTY"
    5. "BREAKFAST" 
    6. "CASHLESS_FACILITY"
    7. "DESSERT_CENTER"
    8. "DRIVE_THRU"
    9. "MC_CAFE"
    8. "MCDELIVERY"
    9. "SURAU"
    10. "WIFI"
    11. "DIGITAL_ORDER_KIOSK"
    12. "ELECTRIC_VEHICLE"

    - You need to enclosed all table names and columns in double quote. e.g. ("BRANCH", "ID_BRANCH")
    - Always check for case-insensitive for "LOCATION"."FULL_ADDRESS" WHERE clause.
    - "LOCATION"."POSTCODE" data type is string. 



    SELECT "BRANCH"."NAME" 
    FROM "BRANCH"
    JOIN "LOCATION" ON "BRANCH"."ID_BRANCH"="LOCATION"."ID_BRANCH"
    JOIN "FACILITY" ON "BRANCH"."ID_BRANCH"="FACILITY"."ID_BRANCH"
    WHERE "BRANCH"."RECORD_TYP" != 5
    AND "LOCATION"."RECORD_TYP" != 5 
    AND "FACILITY"."RECORD_TYP" != 5
    AND ...
    """ 

    if request.session_id:

        response = client.responses.create(
            model="gpt-4o-2024-08-06",
            previous_response_id=request.session_id,
            input=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": request.message}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "text2sql",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "reply": {
                                "type": "string"
                            },
                            "sql_query": {
                                "type": "string"
                            },
                        },
                        "required": ["reply","sql_query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )

    else:

        response = client.responses.create(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": request.message}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "text2sql",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "reply": {
                                "type": "string"
                            },
                            "sql_query": {
                                "type": "string"
                            },
                        },
                        "required": ["reply","sql_query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )

    response_dict = response.model_dump()
    text_content = response_dict["output"][0]["content"][0]["text"]

    parsed_text = json.loads(text_content)
    sql_query = parsed_text["sql_query"]
    print(sql_query)
    reply = parsed_text["reply"]

    if sql_query != "":
        db_result = execute_query(sql_query, cnxn)
    else:
        db_result = None 

    result["reply"] = reply 
    result["outlet"] = db_result 
    result["session_id"] = response.id 

    return result 

def execute_query(query, cnxn):
    try:
        cursor = cnxn.cursor()

        if not query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")

        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        cnxn.close()
        return results

    except Exception as e:
        print(f"Error: {e}")
        return [] 
