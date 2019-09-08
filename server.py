from flask import Flask, render_template, request, redirect, session # added request
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def index():
    if 'from_click' not in session:  # 增加一个变量，判断是刷新进页面还是按button进页面， 等于0是刷新，等于1是按button
        session['from_click'] = 0
    if 'message' not in session:
        session['message'] =  []
    if 'gold' not in session:
        session['gold'] = 0 
    if 'moves' not in session:
        session['moves'] = 0
    else:
        if session['from_click'] == 1:    # 判断为按button后，move才能加1， 加1后再把变量设为0
            session['moves'] += 1          
            session['from_click'] = 0

    return render_template('index.html', gold_on_template = session['gold'], message_on_template = session['message'],
    moves_on_template = session['moves'])


@app.route('/process_money', methods=['POST'])
def process_money():
    if request.form['building'] == 'farm':
        farm_earned = random.randint(10, 50)
        session['gold'] += farm_earned
        session['message'].insert(0, ( "<p class='win'>Earned " + str(farm_earned) + " golds from the farm!</p>")) 

    elif request.form['building'] == 'cave':
        cave_earned = random.randint(5, 10)
        session['gold'] += cave_earned
        session['message'].insert(0, ( "<p class='win'>Earned " + str(cave_earned) + " golds from the cave!</p>"))

    elif request.form['building'] == 'house':
        house_earned = random.randint(2, 5)
        session['gold'] += house_earned
        session['message'].insert(0, ( "<p class='win'>Earned " + str(house_earned) + " golds from the house!</p>"))

    elif request.form['building'] == 'casino':
        casino_earned = random.randint(-100, 100)
        session['gold'] += casino_earned
        if casino_earned >= 0:
            session['message'].insert(0, ( "<p class='win'>Earned " + str(casino_earned) + " golds from the casino!</p>"))
        elif casino_earned < 0:
            casino_earned = -casino_earned
            session['message'].insert(0, ( "<p class='lost'>Entered a casino and lost " + str(casino_earned) + " golds... Ouch...</p>"))

    session['from_click'] = 1
    return redirect('/')
 
@app.route('/1', methods = ['POST'])   
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)