from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

def migrate_data(source_db, target_db, table_name):
    try:
        # Create connections
        source_engine = create_engine(source_db)
        target_engine = create_engine(target_db)
        
        # Extract Data
        df = pd.read_sql(f'SELECT * FROM {table_name}', source_engine)
        
        # Load Data
        df.to_sql(table_name, target_engine, if_exists='replace', index=False)
        
        return "Migration Successful!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source_db = request.form['source_db']
        target_db = request.form['target_db']
        table_name = request.form['table_name']
        result = migrate_data(source_db, target_db, table_name)
        return render_template('index.html', result=result)
    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)
