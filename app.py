import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.environ['OPENAI_API_KEY']


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        ond = request.form["ond"]
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=generate_prompt(ond),
                                            temperature=0,
                                            max_tokens=60,
                                            top_p=1.0,
                                            frequency_penalty=0.0,
                                            presence_penalty=0.0,
                                            stop=["\n"])
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(ond):
    return """Get airport codes from the following prompts.

Prompt: Traveling from Minneapolis to Denver
Codes: MSP, DEN
Prompt: From San Diego to San Francisco
Codes: SAN, SFO
Prompt: {}
Codes:""".format(ond).upper()


app.run(host='0.0.0.0', port=81)