from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "oompaloompa"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show board."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("base.html", board=board,
                           highscore=highscore,
                           nplays=nplays)

@app.route("/check-word", methods=["POST"])
def check_word():
    """Check if word is in dictionary."""
    word = request.json.get("word")  # Use .get() to avoid KeyError
    board = session.get("board")

    if not board:
        return jsonify({'result': 'error', 'message': 'Board not found in session'}), 500

    response = boggle_game.check_valid_word(board, word)

    # Debugging print
    print(f"Checking word: {word}, Response: {response}")

    # Ensure response is not None and return the result correctly
    if response is None:
        return jsonify({'result': 'error', 'message': 'Invalid word check response'}), 500

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json.get("score", 0)
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

if __name__ == "__main__":
    app.run(debug=True)
