# this will import all the functnality of flask we needed

from flask import Flask, render_template, request, redirect
# importing sqlite3
import sqlite3

# starter line of every flask app
app = Flask(__name__)

# define database path
db_path = 'checklist.db'


# all database crud function

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS checklist 
              (id INTEGER PRIMARY KEY AUTOINCREMENT , item TEXT)''')
    conn.commit()
    conn.close()


def get_item():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c = conn.execute("SELECT * FROM checklist")
    items = c.fetchall()
    conn.close()
    return items


def add_item(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO checklist (item) values(?)", (item,))
    conn.commit()
    conn.close()


def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE checklist SET item = ? WHERE id = ?",
              (new_item, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# this will redirect the home page
@app.route('/')
def checklist():
    create_table()
    items = get_item()
    return render_template('checklist.html', items=items)

# this will redirect to add page to add item


@app.route("/add", methods=["POST"])
def add():
    item = request.form['item']
    create_table()
    add_item(item)
    return redirect("/")  # redirect back to homepage



# to update data

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    if request.method == 'POST':
        new_item = request.form['item']
        update_item(item_id, new_item)
        return redirect("/")
    else:
        items = get_item()
        item = next((x[1] for x in items if x[0] == item_id), None)

    return render_template('edit.html', item=item, item_id=item_id)

# to delete data


@app.route('/delete/<int:item_id>')
def delete(item_id):
    delete_item(item_id)
    return redirect('/')
