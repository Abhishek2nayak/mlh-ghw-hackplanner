#this will import all the functnality of flask we needed

from flask import Flask,render_template ,request,redirect

#starter line of every flask app
app = Flask(__name__)
items =[]

#this will redirect the home page
@app.route('/')
def checklist():
    return render_template('checklist.html',items = items)

#this will redirect to add page to add item
@app.route("/add",methods=["POST"])
def add_item():
    item = request.form['item']
    items.append(item) #append item of form into items list
    return redirect("/") #redirect back to homepage

#to update data 
@app.route('/edit/<int:item_id>',methods=['GET','POST'])
def edit_item(item_id):
    item = items[item_id-1] #retrieve item

    if request.method == 'POST':
        new_item = request.form('item')
        items[item_id-1] = new_item
        return redirect('/')
    return render_template('edit.html',item = item,item_id = item_id)

#to delete data
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    del items[item_id-1]
    return redirect('/')


