# app/routes.py
import os
from random import choice

from flask import Blueprint, jsonify, render_template, request, abort

from app import config
from app.mongodb.mongodb_connectionhandler import MongoDBConnectionHandler
from gpt4all import GPT4All
import together


# Constants
DATABASE_NAME = config.DATABASE_NAME
COLLECTION_NAME = config.COLLECTION_NAME
MODEL_NAME = config.MODEL_NAME
together.api_key = config.TOGETHER_API_KEY
CLOUD_MODEL_NAME = config.CLOUD_MODEL_NAME

# Initialization
mongo_handler = MongoDBConnectionHandler(DATABASE_NAME)
bp = Blueprint("routes", __name__)
model = GPT4All(
    model_name=MODEL_NAME,
    model_path=(os.path.join(os.getcwd(), "app/model")),
    allow_download=False
)

@bp.route("/home", methods=["GET", "POST"])
def home():
    """Render the home page."""
    message = None
    try:
        return render_template("index.html", message=message)
    except Exception as e:
        abort(500, description="Error rendering home page")

@bp.route("/info", methods=["GET", "POST"])
def info():
    """Render the info page."""
    message = None
    try:
        return render_template("info.html", message=message)
    except Exception as e:
        abort(500, description="Error rendering info page")

@bp.route("/api/fetch_sentence")
def fetch_sentence():
    """
    Fetches a random sentence based on the selected category and sentiment.

    Returns:
        - json(str): If a valid category and sentiment are provided, returns a JSON response containing a random sentence.
        - json(str): If the category or sentiment is invalid, returns a JSON response indicating the error.
    """
    selected_category = request.args.get("category")
    selected_sentiment = request.args.get("sentiment")

    # Validate Input
    if not selected_category or not selected_sentiment:
        abort(400, "Category and sentiment are required parameters.")

    document = mongo_handler.find_document_by_category(COLLECTION_NAME, selected_category)

    # Check if exists
    if document and selected_sentiment in document["sentiments"]:
        sentences_for_sentiment = document["sentiments"][selected_sentiment]
        random_sentence = choice(sentences_for_sentiment)
        return jsonify({"result": random_sentence})
    
    else:
        return jsonify({"result": "Invalid category or sentiment"})

@bp.route("/api/process_text", methods=["POST"])
def process_text():
    """
    Process the text received from the request and generate a response using a locally hosted model.

    Returns:
        - json(str): A JSON response containing the processed text.
    """
    try:
        data = request.get_json()
        text = data.get("text")

        if text:
            DESIGN_SYSTEM_TEMPLATE = f"""
            ### System: 
            You are an AI assistant that follows instruction extremely well. Help as much as you can.

            ### Instruction:
            There are 8 categories for evaluating a design-driven thesis.
            1. Project  Management
            2. Difficulty of the problem
            3. Originality
            4. Applicability
            5. Readability and Structure
            6. Requirement Analysis
            7. System Design
            8. System Implementation

            Examples: 
            1. - on time, organized -> "The student took the lead on the project, delivered everything on time, continuously identified important action points, organized meetings with the supervisors and came prepared to them."
            2. - not on time, disorganized -> "The student struggled to meet deadlines and failed to deliver key project components on time."

            Generate 1 sentence based on bullet points by the User and the context above.

            ### User:
            {text}

            ### Response:
            """

            response = model.generate(DESIGN_SYSTEM_TEMPLATE, max_tokens=50)
            processed_text = response
            return jsonify({"result": processed_text})
        else:
            return jsonify({"result": "Invalid text"})

    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

@bp.route("/api/process_text_external", methods=["POST"])
def process_text_external():
    """
    Process the text received from the request and generate a response using the Cloud model.

    Returns:
        - json(str): A JSON response containing the processed text.
    """
    try:
        data = request.get_json()
        text = data.get("text")

        if text:
            DESIGN_SYSTEM_TEMPLATE = f"""
            [INST] <<SYS>>
            You are an AI assistant that follows instruction extremely well. Generate 1 sentence evaluating a student based on bullet points by the User and the context below.

            There are 8 categories for evaluating a design-driven thesis.
            1. Project  Management
            2. Difficulty of the problem
            3. Originality
            4. Applicability
            5. Readability and Structure
            6. Requirement Analysis
            7. System Design
            8. System Implementation

            Examples: 
            1. - on time, organized -> "The student took the lead on the project, delivered everything on time, continuously identified important action points, organized meetings with the supervisors and came prepared to them."
            2. - not on time, disorganized -> "The student struggled to meet deadlines and failed to deliver key project components on time."

            Please use the format in the Examples above.
            <</SYS>>

            {text}
            [/INST]
            """
            output = together.Complete.create(
                prompt = DESIGN_SYSTEM_TEMPLATE, 
                model = CLOUD_MODEL_NAME, 
                max_tokens = 100,
            )

            processed_text = output["output"]["choices"][0]["text"]

            return jsonify({"result": processed_text})
        else:
            return jsonify({"result": "Invalid text"})

    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})