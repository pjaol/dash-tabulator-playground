import dash_tabulator
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash_extensions.javascript import Namespace
import pandas as pd
from faker import Faker
import random

fake = Faker()

external_scripts = ['https://oss.sheetjs.com/sheetjs/xlsx.full.min.js']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']
app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

styles = {
            'pre': {
                'border': 'thin lightgrey solid',
                'overflowX': 'scroll'
            }
        }

# The asset folder there is JS methods can be declared 
# a reference can be passed using Namespace that then gets mapped client side
# see https://github.com/preftech/dash-tabulator/pull/11
# The namespace here must match the name space of the JavaScript asset.
# See https://github.com/pjaol/dash-tabulator-playground/blob/main/assets/playground.js

ns = Namespace("myNamespace", "tabulator")


columns = [
                { "title": "Name", "field": "name", "width": 150, "headerFilter":True, "editor":"input"},
                { "title": "Age", "field": "age", "hozAlign": "left", "formatter": "progress" },
                { "title": "Favourite Color", "field": "col", "headerFilter":True },
                { "title": "Date Of Birth", "field": "dob", "hozAlign": "center" },
                { "title": "Rating", "field": "rating", "hozAlign": "center", "formatter": "star" },
                { "title": "Passed?", "field": "passed", "hozAlign": "center", "formatter": "tickCross" }
              ]

# Options and Headers is where a lot of tabulator magic happens
options = { 
                # groupBy is one of the most popular tabulator functions
                # You can do it by field, JS Functions etc. http://tabulator.info/docs/4.8/group
                "groupBy": "col",

                # selectable allows you to interact with the data
                "selectable":"true", 

                # An example of passing a client side JS function using NameSpace 
                # See  https://github.com/pjaol/dash-tabulator-playground/blob/main/assets/playground.js
                #
                # These callbacks have slightly modified signiture to the tabulator callbacks
                # http://tabulator.info/docs/4.8/callbacks
                # Where the table being referenced is added as the last argument to the callback
                # eg.
                # Tabulator's cellClick => function (e, cell) {}
                # dash-tabulator cellClick => function (e, cell, table){}
                'cellClick': ns('cellLog')
        }


downloadButtonType = {"css": "btn btn-primary", "text":"Export", "type":"csv"}
clearFilterButtonType = {"css": "btn btn-outline-dark", "text":"Clear Filters"}
initialHeaderFilter = [{"field":"col", "value":"blue"}]

app.layout = html.Div([
    dash_tabulator.DashTabulator(
        id='tabulator',
        options=options,
        downloadButtonType=downloadButtonType,
        clearFilterButtonType=clearFilterButtonType,
    ),
    html.Div(id='output'),
    dcc.Interval(
                id='interval-component-iu',
                interval=1*10, # in milliseconds
                n_intervals=0,
                max_intervals=0
            )

])

@app.callback([ Output('tabulator', 'columns'),
                Output('tabulator', 'data'),
                Output('tabulator', 'initialHeaderFilter')],
                [Input('interval-component-iu', 'n_intervals')])
def initialize(val):

    # Here we're going to test what to do with Nones / nulls 
    # Nones will appear as null in excel exports, so it's easier to convert them to ""
    # Using dataframes, it's possible to do client side, but will be faster with a dataframe
    d = [[1, "Oli Bob",None,None,None,None],[2,"Mary May", 1, None, None, "foo"]]
    for i in range(3, 100):
        p = [i, fake.name(),random.randint(10, 80),fake.color_name() , fake.date_of_birth().strftime("%m/%d/%Y"), "foo" ]
        d.append(p)
        
    df = pd.DataFrame(d, columns=["id", "name", "age", "col","dob","print" ])
    df.fillna(value="", inplace=True)
    print(df.dtypes)
    print(df.to_dict('records'))

    return columns, df.to_dict('records'), initialHeaderFilter

@app.callback(Output('output', 'children'),
    [Input('tabulator', 'rowClicked'),
    Input('tabulator', 'multiRowsClicked'),
    Input('tabulator', 'cellEdited'),
    Input('tabulator', 'dataChanged'),
    Input('tabulator', 'dataFiltering'),
    Input('tabulator', 'dataFiltered')])
def display_output(row, multiRowsClicked, cell, dataChanged, filters, dataFiltered):
    print("row: {}".format(str(row)))
    print("cell: {}".format(str(cell)))
    print("data changed: {}".format(str(dataChanged)))
    print("filters: {}".format(str(filters)))
    print("data filtered: {}".format(str(dataFiltered)))
    return 'You have clicked row {} ; cell {} ; multiRowsClicked {}'.format(row, cell, multiRowsClicked)


if __name__ == '__main__':
    app.run_server(debug=True)
