from hchart.forms import InputForm
from flask import current_app, request, Blueprint, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import plotly
from plotly.graph_objs import Scatter, Layout, Figure, Table
import pandas as pd
import os
import tempfile



blueprint = Blueprint("chart", __name__)


@blueprint.route("/", methods=["GET", "POST"])
def chart():

    # initialize the variables we will pass to the view
    chart = None
    table = None
    numcols = 0
    filename = ""
    form = InputForm() 
    
    # did the user click one of our buttons with seed data?
    if request.method == "GET":        
        sample_files_dict = {"simple": "simple.csv", "msft": "daily_MSFT.csv"}
        sample = sample_files_dict.get( request.args.get("input"), None)
        if sample:
            application_root = os.path.join(current_app.instance_path, os.pardir)
            sample_file_path = os.path.abspath(os.path.join(application_root, "data", sample))
            chart, table, numcols = getChart(file=sample_file_path)   
            filename = sample
        
    # otherwise, user submitted data via the form
    else:
        # attempt to validate the form
        if form.validate_on_submit():
            # process the file upload field, if user uploaded a file
            if form.file.data:
                form.data.data = "" # empty data in the textarea field from previous requests
                # temporarily store the uploaded file to the file system
                with tempfile.TemporaryDirectory() as tmpdirname:
                    csv_file = form.file.data
                    filename = csv_file.filename
                    full_filename = os.path.join(tmpdirname, secure_filename(csv_file.filename)   )
                    csv_file.save(full_filename)
                    chart, table, numcols = getChart(file=full_filename)  
            # if there is no file upload data, then process data from the textarea field
            else:
                # Expect input data from the textfield area to have the same format as a csv file
                # Example:
                # a,b,c
                # 1,3,2
                # 2,6,4
                # 3,9,16
                # Below code transforms the above input data into a dict of the form:
                # {'a': [1,2,3], 'b': [3,6,9], 'c': [2,4,16]}
                try:
                    lines = form.data.data.split()
                    headers = lines[0].split(',')  # ['a','b','c']
                    data = lines[1:]  # [['1,3,2'],['2,6,4'],['3,9,16']]
                    transform = []
                    for d in data:
                        rowdata = [ int(i) for i in d.split(',') ]  # [1,3,2]
                        transform.append(rowdata)
                    zipped = list(zip(*transform))  # [(1,2,3),(3,6,9),(2,4,16)]
                    mydict = { headers[i]: list(zipped[i]) for i in range(len(headers)) }
                    chart, table, numcols = getChart(data=mydict)      
                except:
                    flash(f"There was a problem processing the input you entered.", "danger")

        else:
            # if there are validation errors in the form, include them in flash messages to display to user
            flash_errors(form)
        
        
    return render_template("index.html", chart=chart, table=table, numcols=numcols, form=form, filename=filename)



def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)

            

def getChart(file=None, data=None):
    """Process incoming data and generate a table and chart. This function can be passed a csv file of a dictionary."""
        
    if file:
        try:
            df = pd.read_csv(file)  
        except:
            flash(f"We are unable to read your file. Check that you have uploaded a valid csv file.", "danger")
            return None, None, 0
    elif data:
        try:
            df = pd.DataFrame(data)   
        except:
            flash(f"There was a problem processing the input you entered.", "danger")
            return None, None, 0
    else:
        flash(f"No data provided.", "warning")
        return None, None, 0
         
    # the first column represents our x-axis, so sort data according to the first column    
    df = df.sort_values(by=df.columns[0])
    
    # store number of columns - this gets passed to the front-end and is used to adjust the display if out data is too wide
    numcols = len(df.columns)
    
    # generate a line graph; add each column of data (besides the first col) as an additional line on the graph
    fig = Figure()
    for col in df.columns[1:]:
        fig.add_trace(Scatter(x=df[df.columns[0]], y=df[col], name=col))
    fig.update_layout(template="simple_white", margin= {'t': 5, 'l': 0, 'r': 0, 'b': 0 })

    # this is the actual html that draws the chart; pass to front-end
    chart_div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    
    # generate a table from the same data
    table = Figure(data=[Table(
                            header=dict(values=list(df.columns),align='center'),
                            cells=dict(values=[ df[col] for col in df.columns ],
                                       fill_color='white',
                                       align='center'),
                            columnwidth=50)
                    ])
    table.update_layout(margin= {'t': 5, 'l': 0, 'r': 0, 'b': 0 })
    
    # this is the actual html that draws the table; pass to front-end
    table_div = plotly.offline.plot(table, show_link=False, output_type="div", include_plotlyjs=False)

    return chart_div, table_div, numcols



