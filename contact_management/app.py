from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create or connect to the database
conn = sqlite3.connect('db/contacts.db')
cursor = conn.cursor()

# Execute the SQL code to create the contacts table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    work TEXT,
    address TEXT NOT NULL
);
""")

# Commit changes and close the connection
conn.commit()
conn.close()

# Create SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('db/contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database if not exists
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

# Initialize database on app startup
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        work = request.form['work']
        address = request.form['address']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO contacts (name, email, phone, work, address) VALUES (?, ?, ?, ?, ?)',
                     (name, email, phone, work, address))
        conn.commit()
        conn.close()
        
        flash('Contact added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_contact.html')


@app.route('/view_contacts')
def view_contacts():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('view_contacts.html', contacts=contacts)

@app.route('/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
