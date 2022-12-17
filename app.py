import os
from typing import List

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# riplit key
# openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        ond = request.form["ond"]
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
        return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    if type(result) == str:
        result = result.split(", ")

    if result is not None:
        o_url = generate_prompt_image(result[0])
        d_url = generate_prompt_image(result[1])
        return render_template("index.html", result=', '.join(result), o_url=o_url, d_url=d_url)

    return render_template("index.html", result=result)


def extract_city_names(ond):
    return """Extract city names from the following prompts.

      Prompt: Prompt: Traveling from Minneapolis to Denver
      Cities: Minneapolis, Denver
      Prompt: To San Francisco from San Diego
      Cities: San Diego, San Francisco
      Prompt: {}
      Cities:
      """.format(ond.capitalize()
                 )


def generate_prompt(ond_input):
    return """Get airport codes from the following prompts.

      Prompt: Traveling from Minneapolis to Denver
      Codes: MSP, DEN
      Prompt: To San Francisco from San Diego
      Codes: SFO, SAN
      Prompt: {}
      Codes:""".format(ond_input).upper()


def generate_prompt_image(ond_input):
    response = openai.Image.create(prompt=f"{ond_input}", n=1, size="256x256")
    image_url = response['data'][0]['url']
    return image_url


app.run(host='0.0.0.0', port=81)
