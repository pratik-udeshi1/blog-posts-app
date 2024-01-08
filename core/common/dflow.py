import json
import os

from flask import Flask, request, jsonify, Blueprint
from google.cloud import dialogflow_v2

from core.post.logic import get_posts_from_es

app = Flask(__name__)

project_id = "medium-blog-testing"
session_id = "random-session-id"

dflow_bp = Blueprint('dflow', __name__)
credential_path = "C:\wamp64\www\personal_projects\medium-blog\core\common\medium-blog-testing-3f798b5a715f.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path


@dflow_bp.route('/dflow/webhook', methods=['POST'])
def webhook():
    content = request.get_json()

    # Extract the query text from the request
    query = content['queryResult']['queryText']

    # Send the query to Dialogflow and get the response
    response = detect_intent_texts(project_id, session_id, [query], 'en')

    intent = response.intent.display_name

    posts_urls = None

    if 'Fashion' in intent or 'Technology' in intent:
        posts = get_posts_from_es(search_query=query).all()
        posts_urls = ", ".join([serialize_post_instance(post) for post in posts])
        # response = json.dumps(posts_urls, indent=2)

    res = {'fulfillmentText': f"{response.fulfillment_text} {posts_urls}"}

    # Return the fulfillment text as a JSON response
    return jsonify(res)


def serialize_post_instance(post):
    """Serialize a SQLAlchemy instance to a dictionary."""
    return f"https://b5dc-2404-bd00-3-d5d6-60ba-a504-7a0d-d99c.ngrok-free.app/post/{str(post.id)}"


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow_v2.TextInput(text=text, language_code=language_code)
        query_input = dialogflow_v2.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result


if __name__ == '__main__':
    app.run(debug=True)
