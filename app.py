## importing functions and modules
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
from static.graph_module import ( generate_heatmap,generate_funnel_chart,generate_bar_chart,generate_bubble_chart,generate_contour_plot,generate_line_chart,generate_pie_chart)
import ast

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}    ## function to restrict any other type of file upload 
def allowed_file(filename):             ## that is to only allow the user to upload csv or excel files
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_tuples_from_df(df, columns):
    tuples_list = []
    for _, row in df.iterrows():       ## function to create the data frame  into a list of tuple so that it can be
        tuples_list.append(tuple(row[col] for col in columns))  ## used to generate the graph 
    return tuples_list

@app.route('/')
def index():
    return render_template('upload.html')

### handling uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('select_columns', filename=filename))
    else:
        return jsonify({'message': 'Please select a valid Excel or CSV file'})

### column name selection
@app.route('/select_columns/<filename>', methods=['GET', 'POST'])
def select_columns(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path) if filename.endswith('.csv') else pd.read_excel(file_path)

    if request.method == 'POST':
        selected_columns = [request.form['column1'], request.form['column2']]
        tuples_list = create_tuples_from_df(df, selected_columns) ## creating the tuple from the records of the columns that are selected by the user 
        return redirect(url_for('select_chart_type', columns=str(tuples_list)))  ## redirecting the user to the graph generator module that is the select_chart_type function

    return render_template('select_columns.html', columns=df.columns) ## call for the column selection page 

### chart type selectionx
@app.route('/select_chart_type', methods=['GET', 'POST'])
def select_chart_type():
    if request.method == 'POST':
        chart_type = request.form['chart_type']
        columns = request.args.get('columns')
        ## print("Columns:", columns)        ## print statement used to debug the data flow between the modules 
        tuples_list = ast.literal_eval(columns) if isinstance(columns, str) else []
        ## print("Tuples List:", tuples_list)     ## print statement used to debug the data flow between the modules 

        if isinstance(tuples_list, tuple):
            tuples_list = [tuples_list]
            
        ## print("Type of tuples_list:", type(tuples_list))      ## print statement used to debug the data flow between the modules 

        tuples_list = [tpl for tpl in map(lambda tpl: tuple(filter(lambda x: x is not None, tpl)), tuples_list) if tpl]
        names = [x[0] for x in tuples_list]
        values = [x[1] for x in tuples_list]
        ## print(names)     ## print statement used to verify the data between the modules is correct 
        ## print(values)    ## print statement used to verify the data between the modules is correct
        

        ## call function for all the graph types to generate the graph using the provided input 
        if chart_type == 'bar':
            chart_html = generate_bar_chart(names, values)
        elif chart_type == 'line':
            chart_html = generate_line_chart(names, values)
        elif chart_type == 'pie':
            chart_html = generate_pie_chart(names, values)
        elif chart_type == 'bubble':
            chart_html = generate_bubble_chart(names, values)
        elif chart_type == 'contour':
            chart_html = generate_contour_plot(names, values)
        elif chart_type.lower() == 'funnel':
            data = pd.DataFrame({'labels': names, 'values': values})
            chart_html = generate_funnel_chart(data)
        elif chart_type.lower() == 'heatmap':
            chart_html = generate_heatmap(names,values)
        else:
            chart_html = "Invalid chart type. Please try again."
        ## chart_type = request.form['chart_type'] ## debug statement to verify that
        ## print("Chart type:", chart_type)        ## the correct chart type is been passed by the user or not
        if chart_html:
            with open('chart.html', 'w') as f:  
                f.write(chart_html)
            os.system('open chart.html')

            return render_template('chart.html', chart_html=chart_html)  ## call function for the rendering of the graph
        else:
            return "Failed to generate chart. Please try again."

    return render_template('select_chart_type.html')

if __name__ == '__main__':
    app.run(debug=True)