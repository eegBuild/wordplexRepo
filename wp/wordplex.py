from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, session
from wordGuessControl import *
from xmlParse import xmlTojson
from threading import Thread


app = Flask(__name__)


@app.route('/')
def display_index():

    return render_template("index.html",
                            the_title= "Index Page",
                            the_save_url=url_for("savename"),)

@app.route('/saveform', methods=["POST"])
def savename():
    #t = Thread(target=savePlayerName(user_fname,user_sname))
    #t.start()
    user_fname = request.form['user_fname']
    user_sname = request.form['user_sname']
    t = Thread(target=savePlayerName(user_fname,user_sname))
    t.start()
    #savePlayerName(user_fname,user_sname)
    full_name = user_fname+' '+user_sname                          
    #session['last_visitor'] = full_name
    return render_template("game.html",
                           the_person = "Welcome "+user_fname,
                           the_title="Game Page")
	    
							
@app.route('/game')
def display_game():
    return render_template("game.html",
                            the_title="Game Page",
                            sevenword_url=url_for("sevenword"),)
    
@app.route('/check_the_word', methods=["GET"])
def checktheword():
    get_input = request.args.get('echoValue')
    word = str(get_input)
    check = checkInputWord(word, "static\\Files\\testWords.txt")
    ret_data = {"value": check}
    return jsonify(ret_data)

@app.route('/test')
def display_test():
    return render_template("test.html",
                            the_title="test Page",)

@app.route('/start_game', methods = ['POST'])
def start_game():
    random_word = begin_game()
    return random_word

@app.route('/winner', methods = ['POST'])
def record_winner():
    winner = saveGame()
    return jsonify(winner)

@app.route('/score',  methods = ['POST'])
def replay_game():
    return render_template("game.html",
                            the_title="Game Page",)
    
@app.route('/getxmldata', methods = ['POST'])
def getmyxml():
    return xmlTojson()

app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'
if __name__ == '__main__':
    app.run(port=5001, debug=True)


    

