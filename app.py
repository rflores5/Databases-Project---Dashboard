# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, dash_table, State, callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from bf_mongodb import MongodbClass
from bf_neo4j import Neo4jClass
from bf_mysql import MySqlClass

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

#app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
mongo = MongodbClass()
neo4j = Neo4jClass()
neo4j2 = Neo4jClass()
mysql = MySqlClass()
mysql2 = MySqlClass()


years_ = list(range(1990,2022))
faculty_ = mysql.findRandomFaculty()
top_publications = pd.DataFrame(neo4j.publications_citations()).to_dict('records')
universities_ = dict(mysql.getUniveristyList())
university_names = list(universities_.values())
university_names.append(None)

header = html.H2(children="Observing Research Interest Over Time")

label_1 = html.Label('Keyword: ')
title_1 = html.H4(children="Number of Publications Mentioning Keyword Each Year")
input_1 = dcc.Input(id="input-1", value='keyword', type='text', debounce=True)
values1 = mongo.keyword_mentions('keyword')
df1 = pd.DataFrame(values1)
fig1 = px.line(df1, x="_id", y="count")
fig1.update_layout(xaxis_title='Year', yaxis_title='Count')
graph_1 = dcc.Graph(id='graph-1', figure=fig1)
one_div = html.Div(children=[title_1, label_1,input_1,graph_1], className="six columns")

label_2 = html.Label('Year: ')
input_2 = dcc.Dropdown(options=years_,value='2021',id='input-2')
title_2 = html.H4(children="Top 10 Keywords For a Given Year")
values2 = mongo.top_keywords(2021)
df2 = pd.DataFrame(values2).to_dict('records')
table_2 = dash_table.DataTable(data=df2, id='table-2')
two_div = html.Div(children=[title_2,label_2,input_2,table_2], className="four columns")

title_3 = html.H4(children="Top 5 Professors by Number of Citations/Publications")
label_3 = html.Label('Year: ')
input_3a = dcc.Dropdown(options=years_,value='2021',id='input-3a')
input_3b = dcc.RadioItems(['Publications','Citations'],value='Publications',id='input-3b')
data3 = neo4j.top_professors_publications(2021)
df3 = pd.DataFrame(data3).to_dict('records')
table_3 = dash_table.DataTable(data=df3, id='table-3')
three_div = html.Div(children=[title_3,label_3,input_3a,input_3b,table_3], className="six columns")

title_4 = html.H4(children="Top 5 Universities by Number of Citations/Publications")
label_4 = html.Label('Year: ')
input_4a = dcc.Dropdown(options=years_,value='2021',id='input-4a')
input_4b = dcc.RadioItems(['Publications','Citations'],value='Publications',id='input-4b')
data4 = neo4j2.top_university_publications(2021)
df4 = pd.DataFrame(data4)
fig4 = px.bar(df4,x="Name",y="Publications")
graph_4 = dcc.Graph(id='graph-4', figure=fig4)
four_div = html.Div(children=[title_4,label_4, input_4a,input_4b,graph_4], className="six columns")

title_5 = html.H4(children="Featured Faculty")

new_name_5 = dcc.Input(id='state-name-5', type='text', placeholder='Name')
new_position_5 = dcc.Input(id='state-position-5', type='text', placeholder='Position')
new_research_5 = dcc.Input(id='state-research-5', type='text', placeholder='Research Interest')
new_email_5 = dcc.Input(id='state-email-5', type='text', placeholder='Email')
new_phone_5 = dcc.Input(id='state-phone-5', type='text', placeholder='Phone')
new_photo_5 = dcc.Input(id='state-photo-5', type='text', placeholder='Photo Url')
new_uni_5 = dcc.Dropdown(options=university_names,value=None,id='state-uni-5', placeholder="University")
new_button_5 = html.Button(id='submit-button-state',n_clicks=0,children='Submit')
result = html.Div(id='faculty-added',children="")
new_faculty_5 = html.Div(children=[new_name_5, new_position_5, new_research_5, new_email_5, new_phone_5, new_photo_5, new_uni_5, new_button_5,result])
subtitle_6 = html.H6(children="Add New Faculty")
pop_up = html.Div(children=[subtitle_6,new_faculty_5])

faculty = mysql.findRandomFaculty()
img = faculty[0][6]
name = faculty[0][1]
uni_id = faculty[0][7]
uni = universities_[uni_id]
input_5 = dcc.Input(id='state-faculty-search-5', type='text', placeholder='Faculty Search')
search_button_5 = html.Button('Search',id='submit-faculty-search', n_clicks=0)
button_5 = html.Button('Random Faculty',id='input-5', n_clicks=0)
image_ = html.A(children=[html.Img(id='image-5',src=img, height=300, width=200)])
name_ = html.Div(id='name-5',children=name)
uni_ = html.Div(id='uni-5',children=uni)
top = html.Div(id='top-5',children=[input_5,search_button_5,button_5])
five_faculty = html.Div(children=[title_5,top,image_,name_,uni_])
five_div = html.Div(children=[five_faculty,pop_up], className="five columns")

title_6 = html.H4(children="Top Publication Each Year by Number of Citations")
table_6 = dash_table.DataTable(data=top_publications,id='table-6',style_table={'height':'600px', 'overflowY': 'auto'})
alert_6 = dbc.Alert(id='alert-6')
input_6 = dcc.Input(id='input-6',type='text', placeholder='New Title')
new_button_6 = html.Button(id='submit-button-6',n_clicks=0,children='Edit')
six_div = html.Div(children=[title_6,input_6,new_button_6,table_6,alert_6], className="seven columns")

row1 = html.Div(children=[one_div,two_div], className="twelve columns")
row2 = html.Div(children=[three_div,four_div], className="twelve columns")
row3 = html.Div(children=[five_div,six_div], className="twelve columns")

app.layout = html.Div(children=[header, row1, row2, row3], style={"text-align": "center", "justifyContent":"center"})

@app.callback(
Output('graph-1','figure'),
Input('input-1','value')
)
def update_graph1(selected_keyword):
	values = mongo.keyword_mentions(selected_keyword)
	df = pd.DataFrame(values)
	fig = px.line(df, x=df["_id"], y=df["count"])
	fig.update_layout(xaxis_title='Year', yaxis_title='Count')
	return fig
	

@app.callback(
Output('table-2','data'),
Input('input-2','value')
)
def update_table2(selected_year):
	values = mongo.top_keywords(int(selected_year))
	df = pd.DataFrame(values)
	return df.to_dict('records')

	
@app.callback(
Output('table-3','data'),
Input('input-3a','value'),
Input('input-3b','value')
)
def update_graph3(year, type):
	if (type == 'Citations'):
		data = neo4j2.top_professors_citations(int(year))
		df = pd.DataFrame(data)
	else:
		data = neo4j2.top_professors_publications(int(year))
		df = pd.DataFrame(data)
	
	return df.to_dict('records')
	
@app.callback(
Output('graph-4','figure'),
Input('input-4a','value'),
Input('input-4b','value')
)
def update_graph4(year, type):
	if (type == 'Citations'):
		data = neo4j.top_university_citations(int(year))
		df = pd.DataFrame(data)
		fig = px.bar(df,x="Name",y="Citations")
	else:
		data = neo4j.top_university_publications(int(year))
		df = pd.DataFrame(data)
		fig = px.bar(df,x="Name",y="Publications")
	return fig

	
@app.callback(
Output('image-5','src'),
Output('name-5','children'),
Output('uni-5','children'),
Input('input-5','n_clicks'),
Input('submit-faculty-search','n_clicks'),
State('state-faculty-search-5','value')
)
def update_faculty(random_button,search_button,faculty_name):
	change_id = [p['prop_id'] for p in callback_context.triggered][0]
	if 'submit-faculty-search'in change_id:
		print(faculty_name)
		result = mysql.findFaculty_name(faculty_name)
		print(result)
		faculty = result[0]
		img = faculty[6]
		name = faculty[1]
		uni_id = faculty[7]
		uni = universities_[uni_id]
		return img, name, uni
	else:
		faculty = mysql.findRandomFaculty()[0]
		img = faculty[6]
		name = faculty[1]
		uni_id = faculty[7]
		uni = universities_[uni_id]
		return img, name, uni
	
@app.callback(
Output('faculty-added','children'),
Input('submit-button-state','n_clicks'),
State('state-name-5','value'),
State('state-position-5','value'),
State('state-research-5','value'),
State('state-email-5','value'),
State('state-phone-5','value'),
State('state-photo-5','value'),
State('state-uni-5','value')
)
def add_faculty(n_clicks, name, position, research, email, phone, photo, uni):

	id = None
	for id_, uni_ in universities_.items(): 
		if uni == uni_:
			id = id_
	
	if name != None:
		mysql2.addFaculty(name,position,research,email,phone,photo,id)
		result = "%s added to faculty" % name
		mysql.commit()
		return result
	else:
		return ""
	
	
@app.callback(
Output('input-6','placeholder'),
Output('submit-button-6','n_clicks'),
Output('table-6','data'),
Input('table-6','data'),
Input('table-6','active_cell'),
Input('submit-button-6','n_clicks'),
State('input-6','value')
)
def update_pub_name(data, cell, n_clicks, value):
	if cell and value and n_clicks:
		row = cell['row']
		title = top_publications[row]['title']
		mongo.update_publication_name(title,value)
		neo4j.update_publication_name(title,value)
		new_top_publications = pd.DataFrame(neo4j.publications_citations()).to_dict('records')
		return title,0,new_top_publications
	elif cell:
		row = cell['row']
		title = data[row]['title']
		return title,0,data
	else: 
		return "Edit Selected Title",0,data
	
	
	
if __name__ == '__main__':
        app.run_server(debug=True)
