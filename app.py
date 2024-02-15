#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/message')
def get_message_db():
    # write some helpful comments here
    try:
        return g.message_db
    except AttributeError:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cursor = g.message_db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                          (id INTEGER PRIMARY KEY, handle TEXT, message TEXT)''')
        g.message_db.commit()
#         g.message_db.close()
        return g.message_db

def insert_message(request):
    handle = request.form['handle']
    message = request.form['message']

    con = get_message_db()
    cur = con.cursor()
    cur.execute('''INSERT INTO messages (handle, message) VALUES (?, ?)''', (handle, message))
    
    con.commit()
    con.close()

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template("submit.html")
    else:
        insert_message(request)
        thanks = "Thank you for your submission!"
        return render_template("submit.html", thanks = thanks)
    
def random_messages(n):
    con = get_message_db()
    cur = con.cursor()
    cur.execute('''SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT ?''', (n,))
    messages = cur.fetchall()
    cur.close()
    return messages

@app.route('/view')
def view():
    messages = random_messages(5)
    return render_template("view.html", messages=messages)
        
if __name__ == '__main__':
    app.run(debug=True)
