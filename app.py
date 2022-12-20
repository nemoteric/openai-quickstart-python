import os
from typing import List

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# using replit method for getting API key
# openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/", methods=("GET", "POST"))
def index():
    # response to form submission
    if request.method == "POST":
        # input box value = "ond"
        ond = request.form["ond"]
        # get Completion response using the text from "prompt"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=extract_city_names(ond),
            temperature=0,
            # max_tokens=60,
            # top_p=1.0,
            # frequency_penalty=0.0,
            # presence_penalty=0.0,
            # stop=["\n"],
        )
        # append the choices to the end of the index url
        # e.g. /?result=+San+Diego%2C+San+Francisco
        return redirect(url_for("index", result=response.choices[0].text))

    # response to GET request (initial page load) or form submission redirect (GET)
    # get the "result" query parameter from the url
    result = request.args.get("result")
    # get the "ond" query parameter from the url (if it exists)
    if type(result) == str:
        result = result.split(", ")

    if result is not None:
        # get the image urls
        o_url = generate_prompt_image("Beautiful photo of " + result[0])
        d_url = generate_prompt_image("Beautiful photo of " + result[1])
        return render_template("index.html", result=', '.join(result), o_url=o_url, d_url=d_url)
    # if no result, return the index page without any result
    return render_template("index.html", result=result)


def generate_prompt_image(ond_input):
    """Returns a url for an image generated from the given prompt. Note urls expire after 1 hour."""
    response = openai.Image.create(prompt=f"{ond_input}", n=1, size="256x256")
    image_url = response['data'][0]['url']
    return image_url


# ====================Prompts for GPT-3====================
def extract_city_names(ond):
    """Prompt that GPT3 will use to return the city names from the form input."""
    return """Extract city names from the following prompts.

      Prompt: Prompt: Traveling from Minneapolis to Denver
      Cities: Minneapolis, Denver
      Prompt: To San Francisco from San Diego
      Cities: San Diego, San Francisco
      Prompt: {}
      Cities:
      """.format(ond.capitalize()
                 )


def extract_codes(ond_input):
    """Prompt that GPT3 will use to find the code for the given city."""
    return """Get airport codes from the following prompts.

      Prompt: Traveling from Minneapolis to Denver
      Codes: MSP, DEN
      Prompt: To San Francisco from San Diego
      Codes: SFO, SAN
      Prompt: {}
      Codes:""".format(ond_input).upper()


# =========================================================

# for replit, use port 81
app.run(host='127.0.0.1', port=8080)
