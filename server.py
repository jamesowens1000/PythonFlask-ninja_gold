from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)
import random, datetime
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def root():
    if not 'gold' in session:
        session['gold'] = 0
        session['messages'] = []
    return render_template('index.html', gold=session['gold'], messages=session['messages'])

@app.route('/process_money', methods=['POST'])
def process_money():
    directory = {'farm': [10,20],'cave': [5,10],'house': [2,5],'casino': [-50,50]}
    now = datetime.datetime.now()

    for key in directory:
        if key == request.form['location']:
            temp = random.randint(directory[key][0], directory[key][1])
            session['gold'] += temp
            if temp >= 0:
                session['messages'].insert(0,'Earned '+ str(temp) + ' golds from the ' + key + '! ('+now.strftime("%Y/%m/%d %I:%M %p")+')')
            else:
                session['messages'].insert(0,'Entered a ' + key + ' and lost '+ str(temp*-1) + ' golds... Ouch.. ('+now.strftime("%Y/%m/%d %I:%M %p")+')')
    return redirect("/")

@app.route('/destroy', methods=['POST'])
def destroy():
    session.clear()
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry! No response. Try again.'

if __name__=="__main__":
    app.run(debug=True)