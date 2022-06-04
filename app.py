import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

bd = 'your db'

class BuldDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def spell_accounts(self):
        result = self.cursor.execute("SELECT * FROM `accounts`")
        res = result.fetchall()
        arr = []
        for each in res:
            arr.append({'block': ('id: '+
                                  str(each[0])+' number: '+ str(each[1]) + ' date: ' + str(each[2]) + ' client: ' + str(each[3]))})
        return arr


    def insert_account(self, id_add, nomber_add, client_add, date=datetime.datetime.now()):
        self.cursor.execute("INSERT INTO `accounts` (`id`, `nomber`, `Date`, `Client`) "
                            "VALUES (?,?,?,?) ", (id_add, nomber_add, date, client_add))
        return self.conn.commit()

    def delete_account(self, id_ac):
        self.cursor.execute("DELETE FROM `accounts` WHERE `id` = ?", [id_ac])
        self.cursor.execute("DELETE FROM `punts` WHERE `I_id` = ?", [id_ac])
        return self.conn.commit()

app = Flask(__name__)

BuldDB = BuldDB(bd)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        id = request.form['id_input']
        number = request.form['number_input']
        client = request.form['client_input']

        BuldDB.insert_account(id, number, client)
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/checking', methods=['GET'])
def check():
    results = BuldDB.spell_accounts()
    return render_template('index.html', results=results)

@app.route('/deleting', methods=['POST'])
def delete():
    dellete = request.form['del_input']
    BuldDB.delete_account(dellete)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
