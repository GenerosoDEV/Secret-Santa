from flask import Flask, session, redirect, render_template, request
import random, secrets, utils, ast

app = Flask(__name__)
app.secret_key = "@M1G00CU|-70"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/raffle/<raffle_code>")
def raffle_summary(raffle_code):
    if not utils.dbQuery("SELECT * FROM raffles WHERE code=?", raffle_code):
        return redirect("/")
    
    query = utils.dbQuery("SELECT participants FROM raffles WHERE code=?", raffle_code)
    participants = ast.literal_eval(query[0][0])

    participants_links = {}

    for participant in participants:
        participants_links[participant] = utils.dbQuery("SELECT gifter_code FROM match WHERE raffle_code=? AND gifter=?", (raffle_code, participant))[0][0]

    return render_template("raffle_summary.html", raffle_code=raffle_code, participants=participants, participants_links=participants_links)

@app.route("/api/start-raffle", methods=['POST'])
def startRaffle():
    inputs = request.form
    if len(inputs) < 3:
        return redirect("/")
    
    raffle_code = secrets.token_hex(4)

    while utils.dbQuery("SELECT * FROM raffles WHERE code=?", raffle_code) is not None:
        raffle_code = secrets.token_hex(4)

    session['raffle_code'] = raffle_code

    participants = []
    for input in inputs:
        if input.startswith("input-participante-"):
            participants.append(request.form[input])

    utils.dbExec("INSERT INTO raffles(code, participants) VALUES (?, ?)", (raffle_code, str(participants)))

    match_participants = {}
    not_raffled_participants = participants.copy()

    for name in participants:
        raffled = name
        while raffled == name:
            raffled = random.choice(not_raffled_participants)

        match_participants[name] = raffled
        not_raffled_participants.remove(raffled)
        gifter_code = f"{secrets.token_hex(12)}{name}"
        while utils.dbQuery("SELECT * FROM match WHERE gifter_code=?", gifter_code) is not None:
            gifter_code = f"{secrets.token_hex(12)}{name}"

        utils.dbExec("INSERT INTO match(raffle_code, gifter_code, gifter, gifted) VALUES (?, ?, ?, ?)", (raffle_code, gifter_code, name, raffled))

    return redirect(f"/raffle/{raffle_code}")


if __name__ == "__main__":
    app.run(debug=True)