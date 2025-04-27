from flask import Flask,render_template, request, url_for, flash,Response, redirect
import json
import csv


app = Flask(__name__)
app.secret_key = '0808'



@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data = data)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        data = load_data()
        new_id = request.form['id']

        if any(record['id'] == new_id for record in data):
            flash(f"Error: ID {new_id} already exists", 'danger')
            return render_template('create.html', data=data)

        new_record = {
            'id': new_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone']
        }

        data.append(new_record)
        save_data(data)
        flash('Record created successfully', 'success')
        return redirect(url_for('home'))

    return render_template('create.html')





@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = load_data()
    record = next((record for record in data if record['id'] == id), None)

    if record is None:
        flash(f'Record with ID {id} not found.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        record['name'] = request.form['name']
        record['email'] = request.form['email']
        record['phone'] = request.form['phone']
        save_data(data)
        flash(f'Record with ID {id} updated successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('edit.html', record=record)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    data = load_data()
    data = [record for record in data if record['id'] != id]
    save_data(data)
    flash(f'Record with ID {id} has been deleted.', 'success')
    return redirect(url_for('home'))





def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=1)



@app.route('/download')
def download():
    data = load_data()

    
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'name', 'email', 'phone'])
    writer.writeheader()
    for record in data:
        writer.writerow(record)
    csv_data = output.getvalue()
    output.close()
    return Response(csv_data, mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=records.csv"})




if __name__ == '__main__':
    app.run(debug=True)