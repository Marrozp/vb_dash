from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import dash_daq as daq
import plotly.express as px
from datetime import date
import pandas as pd
import numpy as np
pd.options.display.multi_sparse = False

df = pd.read_csv('data_custom_fields.csv')

df['date'] = pd.to_datetime(df['cut_of_date'], utc=True)
df = df[df['display_name'] != 'Papaya Global (original investment in Azimo)']
df['program'] = df['program'].str.replace('[\[\]"]', '', regex=True)

# Replace NaN values in 'entry_round' column with 'Other'
df['entry_round'].fillna('Other', inplace=True)

# Replace NaN values in 'program' column with 'None'
df['program'].fillna('None', inplace=True)

# Add None industry to all industry-less companies
#df['industries'] = df['industries'].apply(lambda x: ['None'] if x == [] else x)
#df.loc[df['industries'] == [], 'industries'] = ['None']

print(df[df['display_name']=='Storm Ventures']['industries'])

def parse_industries(column):
    column = column.str.replace('[\[\]"]', '', regex=True)
    column = column.apply(lambda x: 'None' if x == '' else x)
    concatenated_string = column.str.cat(sep=',')
    result = set(concatenated_string.split(','))
    return result
    #filtered_result = set(filter(lambda x: x != "", result))
    #return filtered_result

def create_options_list(options):
    # This function is needed because both labels and values have to be specified in filters creation
    # in order to control their state (check all of them). Providing only strings creates the labels
    # but makes it impossible to rewrite value parameter with all the df values afterwards
    new_options_list = []
    options.sort()
    for record in options:
        new_options_list.append({
            'label': html.Div([record]),
            'value': record
        })
    return new_options_list

# def create_filter_list(vertical):
    
def create_filters():
    verticals = ['industries', 'display_name', 'fund_name', 'domicile_country', 'entry_round', 'program']
    names = {
        'industries':'Industries',
        'display_name':'Companies',
        'fund_name':'Funds',
        'domicile_country':'Countries',
        'entry_round':'Entry Rounds',
        'program':'Programs'
        }
    children = []
    headline = html.Div('Filters', className='filters-head')
    children.append(headline)
    for i in range(len(verticals)):
        button = html.Button(names[verticals[i]], n_clicks=0, id='roll-btn-' +verticals[i], className='btn-roll-in')
        checklist_all = dcc.Checklist(
                id='all-' + verticals[i],
                className='check-all-btn',
                options=[{'label':'Select All', 'value': '1'}],
                value=['1'],
                labelStyle={'display': 'flex', 'align-items': 'center'}
            )
        if verticals[i] == 'industries':
            checklist_options = dcc.Checklist(
                    id='chckl-industries',
                    className='chckl-list',
                    options=create_options_list(list(parse_industries(df.industries))),
                    value=list(parse_industries(df.industries)),
                    labelStyle={'display': 'flex', 'align-items': 'center'}
                )
        # elif verticals[i] == 'entry_round' or verticals[i] == 'program':
        #     checklist_options = dcc.Checklist(
        #             id='chckl-' + verticals[i],
        #             className='chckl-list',
        #             options=create_options_list(df[verticals[i]].dropna().unique()),
        #             value=df[verticals[i]].dropna().unique(),
        #             labelStyle={'display': 'flex', 'align-items': 'center'}
        #         )
        else:
            checklist_options = dcc.Checklist(
                    id='chckl-' + verticals[i],
                    className='chckl-list',
                    options=create_options_list(df[verticals[i]].unique()),
                    value=df[verticals[i]].unique(),
                    labelStyle={'display': 'flex', 'align-items': 'center'}
                )
        children.extend([html.Hr(), button, checklist_all, checklist_options])
    return children



app = Dash(__name__)

server = app.server

app.layout = html.Div(
    [html.Div([
        html.Div(create_filters()
        #     [
        #     html.Div('Filters', className='filters-head'),
        #     html.Hr(),
        #     html.Button('Industries', n_clicks=0, id='roll-btn-industries', className='btn-roll-in'),
        #     #html.Button('Check / Uncheck All', n_clicks=0, id='all-industries', className='check-all-btn'),
        #     dcc.Checklist(
        #         id='all-industries',
        #         className='check-all-btn',
        #         options=[{'label':'Select All', 'value': '1'}],
        #         value=['1'],
        #         labelStyle={'display': 'flex', 'align-items': 'center'}
        #     ),
        #     dcc.Checklist(
        #         id='chckl-industries',
        #         className='chckl-list',
        #         #options=[{'label': 'option 1', 'value': 'option 1'},{'label': 'option 2', 'value': 'option 2'}],
        #         options=create_options_list(list(parse_industries(df.industries))),
        #         value=list(parse_industries(df.industries)),
        #         labelStyle={'display': 'flex', 'align-items': 'center'}
        #     )
        # ]
        , className='flex-col')
    ], className='left-panel'),
    html.Div(
            [html.Div([
            html.Div([
                html.Div([
                    html.Div(className='h-bar'),
                    html.Div([
                        html.H1('Vestberry Dashboard'),
                        html.P('Quick and easy way to slice and dice data any way you need')
                    ], className='top-h-text-h')
                ], className='top-h-h'),
                html.Div([
                    html.Div([
                        html.H2('Select a metric'),
                        dcc.Dropdown(options=[
                            #{'label': 'MOIC', 'value': 'first_check_mo_ic'},
                            {'label': 'IRR', 'value': 'irr'},
                            {'label': 'Multiple', 'value': 'multiple'}#,
                            #{'label': 'TVPI', 'value': 'multiple'},
                            #{'label': 'DPI', 'value': 'multiple'},
                            #{'label': 'RVPI', 'value': 'multiple'},
                            #{'label': 'Initial investment', 'value': 'multiple'},
                            #{'label': 'Follow on investment', 'value': 'multiple'},
                            #{'label': 'Total original cost', 'value': 'multiple'},
                            #{'label': 'Current Cost', 'value': 'multiple'},
                            #{'label': 'Fair Value', 'value': 'multiple'},
                            #{'label': 'Proceeds from exits and repayment', 'value': 'multiple'}
                        ], id='dd-metric', className='picker', value='multiple')
                    ], className='flex-col'),
                    html.Div([
                        html.H2('Select a dimension'),
                        dcc.Dropdown(options=[
                            {'label': 'Industry', 'value': 'industries'},
                            {'label': 'Company', 'value': 'display_name'},
                            {'label': 'Fund', 'value': 'fund_name'},
                            {'label': 'Country', 'value': 'domicile_country'},
                            {'label': 'Entry Round', 'value': 'entry_round'},
                            {'label': 'Program', 'value': 'program'}
                            #{'label': 'Investment manager', 'value': 'entry_round'},
                            #{'label': 'Source of introduction', 'value': 'entry_round'},
                            #{'label': 'Board seats', 'value': 'entry_round'},
                            #{'label': 'Board member', 'value': 'entry_round'},
                            #{'label': 'Prominent angel investor', 'value': 'entry_round'},
                            #{'label': 'Primary commercial model', 'value': 'entry_round'},
                            #{'label': 'Fund programme', 'value': 'entry_round'}
                        ], id='dd-dimension', className='picker', value='display_name')
                    ], className='flex-col')
                ], className='filters-h'),
                html.H2('Apply filters'),
                html.Div([
                    html.Div([
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='industries-cond'),
                        dcc.Dropdown(list(parse_industries(df.industries)), id='filter-industries', className='picker', multi=True, placeholder='Select Industries')
                    ], className='flex-col'),
                    html.Div([
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='display_name-cond'),
                        dcc.Dropdown(df.display_name.unique(), id='filter-company', className='picker', multi=True, placeholder='Select Companies')
                    ], className='flex-col'),
                    html.Div([
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='fund_name-cond'),
                        dcc.Dropdown(df.fund_name.unique(), id='filter-fund', className='picker', multi=True, placeholder='Select Funds')
                    ], className='flex-col'),
                    html.Div([
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='domicile_country-cond'),
                        dcc.Dropdown(df.domicile_country.unique(), id='filter-country', className='picker', multi=True, placeholder='Select Countries')
                    ], className='flex-col'),
                    html.Div([
                        # boolslider inserted down
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='entry_round-cond'),
                        dcc.Dropdown(df['entry_round'].dropna().unique(), id='filter-entry', className='picker', multi=True, placeholder='Select Entry Round')
                    ], className='flex-col'),
                    html.Div([
                        dcc.Dropdown(options=[
                            {'label': 'Include', 'value': 'include'},
                            {'label': 'Exclude', 'value': 'exclude'},
                        ], className='picker', value='include', id='program-cond'),
                        dcc.Dropdown(df['program'].dropna().unique(), id='filter-program', className='picker', multi=True, placeholder='Select Program')
                    ], className='flex-col'),
                    
                ], className='filters-h'),
                html.H2('Select order'),
                dcc.Dropdown(options=[
                    {'label': 'Descending', 'value': False},
                    {'label': 'Ascending', 'value': True}
                ], id='dd-order', className='picker', value=False)
            ], className='picker-h'),
            html.Div([dcc.Graph(id='graph-content')], className='first-chart-div-h')
        ], className='first-chart-h'),
        html.Div([
            html.Div([
                html.H2('Select comparison period'),
                html.Div([
                    dcc.DatePickerSingle(
                    id='comp-date',
                    min_date_allowed=date(1995, 1, 1),
                    max_date_allowed=date(2030, 12, 31),
                    initial_visible_month=date(date.today().year, date.today().month, date.today().day-1),
                    date=date(date.today().year-1, date.today().month, date.today().day),
                    className='date-picker'
                    ),
                    dcc.Checklist(
                        ['Calculate difference'], id='cl-diff'
                    )
                ], className='filters-h date-filter-h')
                
            ], className='picker-h'),
            html.Div([dcc.Graph(id='graph-content-comp')], className='first-chart-div-h')
        ], className='sec-chart-h')
        ], className='right-panel'
    )], className='main'
    
)

@callback(
    Output('chckl-industries', 'value'),
    Output('chckl-display_name', 'value'),
    Output('chckl-fund_name', 'value'),
    Output('chckl-domicile_country', 'value'),
    Output('chckl-entry_round', 'value'),
    Output('chckl-program', 'value'),
    Input('all-industries', 'value'),
    Input('all-display_name', 'value'),
    Input('all-fund_name', 'value'),
    Input('all-domicile_country', 'value'),
    Input('all-entry_round', 'value'),
    Input('all-program', 'value'),
    State('chckl-industries', 'options'),
    State('chckl-display_name', 'options'),
    State('chckl-fund_name', 'options'),
    State('chckl-domicile_country', 'options'),
    State('chckl-entry_round', 'options'),
    State('chckl-program', 'options')
)
def update_filter(all_industries_value, all_companies_value, all_funds_value, all_countries_value, all_entry_rounds_value, all_programs_value,
chckl_industries_options, chckl_companies_options, chckl_funds_options, chckl_countries_options, chckl_entry_rounds_options, chckl_programs_options):
    all_buttons_value = [all_industries_value, all_companies_value, all_funds_value, all_countries_value, all_entry_rounds_value, all_programs_value]
    all_chckl_options = [chckl_industries_options, chckl_companies_options, chckl_funds_options, chckl_countries_options, chckl_entry_rounds_options, chckl_programs_options]
    result_arrays = []
    for i in range(len(all_buttons_value)):
        if len(all_buttons_value[i]) > 0:
            result_arrays.append([option["value"] for option in all_chckl_options[i]])
        else:
            result_arrays.append([])
    return result_arrays
        
    # if len(all_industries_value) > 0:
    #     return [option["value"] for option in chckl_industries_options]
    # else:
    #     return []

@callback(
    Output('roll-btn-industries', 'className'),
    Output('all-industries', 'className'),
    Output('chckl-industries', 'className'),

    Output('roll-btn-display_name', 'className'),
    Output('all-display_name', 'className'),
    Output('chckl-display_name', 'className'),

    Output('roll-btn-fund_name', 'className'),
    Output('all-fund_name', 'className'),
    Output('chckl-fund_name', 'className'),

    Output('roll-btn-domicile_country', 'className'),
    Output('all-domicile_country', 'className'),
    Output('chckl-domicile_country', 'className'),

    Output('roll-btn-entry_round', 'className'),
    Output('all-entry_round', 'className'),
    Output('chckl-entry_round', 'className'),

    Output('roll-btn-program', 'className'),
    Output('all-program', 'className'),
    Output('chckl-program', 'className'),

    Input('roll-btn-industries', 'n_clicks'),
    Input('roll-btn-display_name', 'n_clicks'),
    Input('roll-btn-fund_name', 'n_clicks'),
    Input('roll-btn-domicile_country', 'n_clicks'),
    Input('roll-btn-entry_round', 'n_clicks'),
    Input('roll-btn-program', 'n_clicks')
)
def update_roll_btn(n_click_industries, n_click_display_name, n_click_fund_name, n_click_domicile_country, n_click_entry_round, n_click_program):
    verticals = ['industries', 'display_name', 'fund_name', 'domicile_country', 'entry_round', 'program']
    n_clicks_data = [n_click_industries, n_click_display_name, n_click_fund_name, n_click_domicile_country, n_click_entry_round, n_click_program]
    output = []
    for i in range(len(verticals)):
        if n_clicks_data[i] % 2:
            output.append('btn-roll-out')
            output.append('check-all-btn')
            output.append('chckl-list')
        else:
            output.append('btn-roll-in')
            output.append('check-all-btn-hidden')
            output.append('chckl-list-hidden')
    return output

    # if roll_n_clicks % 2:
    #     roll_btn_industries_class = 'btn-roll-out'
    #     all_industries_class = 'check-all-btn'
    #     chckl_industries_class = 'chckl-list'
    # else:
    #     roll_btn_industries_class = 'btn-roll-in'
    #     all_industries_class = 'check-all-btn-hidden'
    #     chckl_industries_class = 'chckl-list-hidden'

    #print((len(chckl_industries_options) == len(chckl_industries_value) or len(chckl_industries_value) == 0))
    # if len(all_industries_value) > 0: #and (len(chckl_industries_options) == len(chckl_industries_value) or len(chckl_industries_value) == 0):
        
    #     industries_value = [option["value"] for option in chckl_industries_options]
    # else:
    #     industries_value = []
    

    # if not all_n_clicks % 2:
    #     industries_value = [option["value"] for option in chckl_industries_options]
    # else:
    #     industries_value = []

    return roll_btn_industries_class, all_industries_class, chckl_industries_class

    

@callback(
    Output('graph-content', 'figure'),
    #Output('chckl-industries', 'value'),
    Input('dd-metric', 'value'),
    Input('dd-dimension', 'value'),
    Input('chckl-industries', 'value'),
    Input('chckl-display_name', 'value'),
    Input('chckl-fund_name', 'value'),
    Input('chckl-domicile_country', 'value'),
    Input('chckl-entry_round', 'value'),
    Input('chckl-program', 'value'),

    # Input('filter-company', 'value'),
    # Input('filter-fund', 'value'),
    # Input('filter-country', 'value'),
    # Input('filter-entry', 'value'),
    # Input('filter-program', 'value'),
    Input('dd-order', 'value'),

    Input('industries-cond', 'value'),
    Input('display_name-cond', 'value'),
    Input('fund_name-cond', 'value'),
    Input('domicile_country-cond', 'value'),
    Input('entry_round-cond', 'value'),
    Input('program-cond', 'value')
)
def update_graph(metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond):

    dff = df.copy(deep=True)

    dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order, None, None,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond)
    
    #print(filter_industries)

    return formatFigure(dff, metric, dimension)


############################################### Comparison Chart ############################################

@callback(
    Output('graph-content-comp', 'figure'),
    Input('dd-metric', 'value'),
    Input('dd-dimension', 'value'),
    Input('filter-industries', 'value'),
    Input('filter-company', 'value'),
    Input('filter-fund', 'value'),
    Input('filter-country', 'value'),
    Input('filter-entry', 'value'),
    Input('filter-program', 'value'),
    Input('dd-order', 'value'),
    Input('comp-date', 'date'),
    Input('cl-diff', 'value'),

    Input('industries-cond', 'value'),
    Input('display_name-cond', 'value'),
    Input('fund_name-cond', 'value'),
    Input('domicile_country-cond', 'value'),
    Input('entry_round-cond', 'value'),
    Input('program-cond', 'value')
)
def update_comp_graph(metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order, date, difference,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond):

    dff = df.copy(deep=True)
    dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order, date, difference,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond)
    

    return formatFigure(dff, metric, dimension)

def formatFigure(dff, metric, dimension):
    fig = px.bar(dff,
        x=metric,
        y=dimension,
        title='Drilldown',
        barmode='stack',
        color=metric,
        custom_data=['industries', 'fund_name', 'domicile_country', 'entry_round', 'display_name', 'program']
    )

    for i in range(len(dff)):
        value = dff[metric].iloc[i]
        value = round(value, 2)
        shift_direction = -1 if value >= 0 else 1
        display_name = dff[dimension].iloc[i]
        fig.add_annotation(
            x=value,
            y=i,
            text=value,
            #text=f'{value} %',
            showarrow=False,
            xshift=40,
            font=dict(color='black', size=14)
        )

    height_preset = 20 if dff.shape[0]==0 else 150 if dff.shape[0]<3 else 100 if dff.shape[0]<6 else 50
    height_multiplicator = dff.shape[0] if dff.shape[0] != 0 else 1

    fig.update_layout(
        width = 950,
        #height = dff.shape[0]*(150 if dff.shape[0]<3 else 100 if dff.shape[0]<6 else 50 ),
        height = height_multiplicator * height_preset,
        showlegend=False,
        yaxis_title='',
        xaxis_title='',
        yaxis=dict(autorange='reversed'),
        xaxis_showticklabels=False,
        plot_bgcolor='white',
        hovermode='x unified'
    )

    fig.add_vline(x=0)

    fig.update_traces(
        marker=dict(
            color=[
                '#eb3464' if value < 0 else '#34a8eb' for value in dff[metric]
            ]
        ),
        width=0.4,
        hovertemplate='<br>'.join([
            "<b>Industries</b>: %{customdata[0]}",
            "<b>Fund name</b>: %{customdata[1]}",
            "<b>Country</b>: %{customdata[2]}",
            "<b>Entry Round</b>: %{customdata[3]}",
            "<b>Company</b>: %{customdata[4]}",
            "<b>Program</b>: %{customdata[5]}",
        ])
    )

    return fig


def create_groupby_object(dimension, metric):
    object_to_return = {metric: 'sum',
            #'industries': lambda x: ',<br>    '.join(x.unique()),
            'industries': lambda x: ',<br>    '.join(map(str, set([item for sublist in x for item in sublist]))),
            'display_name': lambda x: ',<br>    '.join(x.unique()),
            'fund_name': lambda x: ',<br>    '.join(x.unique()),
            'domicile_country': lambda x: ',<br>    '.join(x.unique()),
            'entry_round': lambda x: ',<br> '.join(x.dropna().unique()) if x.dropna().any() else '',
            'program': lambda x: ',<br> '.join(map(str, str(x.dropna().unique()).replace('[', '').replace(']', '').replace("'", '').split(' ')))
            #str(x.dropna().unique()).split(' ') #',<br>    '.join(str(x.dropna().unique()))
            }
    object_to_return.pop(dimension)
    return object_to_return

def prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order, date, difference,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond):
    dff = dff.copy(deep=True)
    #print(date)
    if difference:
        actual_dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, filter_program, order, None, None,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond, program_cond)

    if date:        
        dff = dff.loc[(dff['cut_of_date'] <= date)]

    dff['industries'] = dff['industries'].str.replace('[\[\]"]', '', regex=True)
    dff['industries'] = dff['industries'].str.split(',')

    if filter_companies:
        if display_name_cond == 'include':
            dff = dff[dff.display_name.isin(filter_companies)]
        else:
            dff = dff[~dff.display_name.isin(filter_companies)]
    if filter_funds:
        if fund_name_cond == 'include':
            dff = dff[dff.fund_name.isin(filter_funds)]
        else:
            dff = dff[~dff.fund_name.isin(filter_funds)]
    if filter_program:
        if program_cond == 'include':
            dff = dff[dff.program.isin(filter_program)]
        else:
            dff = dff[~dff.program.isin(filter_program)]
    if filter_countries:
        if domicile_country_cond == 'include':
            dff = dff[dff.domicile_country.isin(filter_countries)]
        else:
            dff = dff[~dff.domicile_country.isin(filter_countries)]   
    if filter_entry_round:
        if entry_round_cond == 'include':
            dff = dff[dff.entry_round.isin(filter_entry_round)]
        else:
            dff = dff[~dff.entry_round.isin(filter_entry_round)]
    if filter_industries: 
        filter_col = dff.industries.apply(lambda x: any(item in x for item in filter_industries))
       
        if industries_cond == 'include':
            dff = dff[filter_col]
        else:
            dff = dff[~filter_col]

    
        

    dff = dff.loc[dff.groupby(['display_name']).date.idxmax()]
    dff = dff.sort_values(metric, ascending=order)

    if (dimension != 'display_name'):
        if (dimension == 'industries'):
            dff = dff.explode('industries')
            dff = dff[dff['industries']!='']
            if filter_industries:
                filter_col = dff.industries.apply(lambda x: x in filter_industries)
                if industries_cond == 'include':
                    dff = dff[filter_col]
                else:
                    dff = dff[~filter_col]
    
        dff = dff.groupby(dimension, as_index=False).agg(create_groupby_object(dimension, metric))
        dff = dff.sort_values(metric, ascending=order)
        

    

    if difference:
        new_colname = metric + '_actual'
        actual_dff[new_colname] = actual_dff[metric]
        dff = pd.merge(dff, actual_dff[[dimension, new_colname]], on=dimension, how='left')
        print(dff.columns)
        dff[metric] = dff[new_colname]-dff[metric]
        dff = dff.sort_values(metric, ascending=order)


    return dff

if __name__ == '__main__':
    app.run(debug=True)

'''
html.Div([
    html.P('Include'),
    html.Div([
        daq.BooleanSwitch(
        on=True, color='#54e9dc'
        )
    ], className='updown'),
    html.P('Exclude', className='red-text')
], className='flex-row slider-h'),
'''