from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_daq as daq
import plotly.express as px
from datetime import date
import pandas as pd
import numpy as np
pd.options.display.multi_sparse = False

df = pd.read_csv('data_demo.csv')

df['date'] = pd.to_datetime(df['cut_of_date'], utc=True)
df = df[df['display_name'] != 'Papaya Global (original investment in Azimo)']

def parse_industries(column):
    column = column.str.replace('[\[\]"]', '', regex=True)
    concatenated_string = column.str.cat(sep=',')
    result = set(concatenated_string.split(','))
    filtered_result = set(filter(lambda x: x != "", result))
    return filtered_result

app = Dash(__name__)

server = app.server

app.layout = html.Div(
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
                        {'label': 'MOIC', 'value': 'first_check_mo_ic'},
                        {'label': 'IRR', 'value': 'irr'},
                        {'label': 'Multiple', 'value': 'multiple'},
                        {'label': 'TVPI', 'value': 'multiple'},
                        {'label': 'DPI', 'value': 'multiple'},
                        {'label': 'RVPI', 'value': 'multiple'},
                        {'label': 'Initial investment', 'value': 'multiple'},
                        {'label': 'Follow on investment', 'value': 'multiple'},
                        {'label': 'Total original cost', 'value': 'multiple'},
                        {'label': 'Current Cost', 'value': 'multiple'},
                        {'label': 'Fair Value', 'value': 'multiple'},
                        {'label': 'Proceeds from exits and repayment', 'value': 'multiple'}
                    ], id='dd-metric', className='picker', value='first_check_mo_ic')
                ], className='flex-col'),
                html.Div([
                    html.H2('Select a dimension'),
                    dcc.Dropdown(options=[
                        {'label': 'Industry', 'value': 'industries'},
                        {'label': 'Company', 'value': 'display_name'},
                        {'label': 'Fund', 'value': 'fund_name'},
                        {'label': 'Country', 'value': 'domicile_country'},
                        {'label': 'Entry Round', 'value': 'entry_round'},
                        {'label': 'Investment manager', 'value': 'entry_round'},
                        {'label': 'Source of introduction', 'value': 'entry_round'},
                        {'label': 'Board seats', 'value': 'entry_round'},
                        {'label': 'Board member', 'value': 'entry_round'},
                        {'label': 'Prominent angel investor', 'value': 'entry_round'},
                        {'label': 'Primary commercial model', 'value': 'entry_round'},
                        {'label': 'Fund programme', 'value': 'entry_round'}
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
    ]
)

@callback(
    Output('graph-content', 'figure'),
    Input('dd-metric', 'value'),
    Input('dd-dimension', 'value'),
    Input('filter-industries', 'value'),
    Input('filter-company', 'value'),
    Input('filter-fund', 'value'),
    Input('filter-country', 'value'),
    Input('filter-entry', 'value'),
    Input('dd-order', 'value'),

    Input('industries-cond', 'value'),
    Input('display_name-cond', 'value'),
    Input('fund_name-cond', 'value'),
    Input('domicile_country-cond', 'value'),
    Input('entry_round-cond', 'value')
)
def update_graph(metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond):

    dff = df.copy(deep=True)

    dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order, None, None,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond)

    '''
    fig = px.bar(dff,
        x=metric,
        y=dimension,
        title='Drilldown',
        barmode='stack',
        color=metric,
        custom_data=['industries', 'fund_name', 'domicile_country', 'entry_round', 'display_name']
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

    fig.update_layout(
        width = 950,
        height = dff.shape[0]*(150 if dff.shape[0]<3 else 100 if dff.shape[0]<6 else 50 ),
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
        ])
    )
    '''
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
    Input('dd-order', 'value'),
    Input('comp-date', 'date'),
    Input('cl-diff', 'value'),

    Input('industries-cond', 'value'),
    Input('display_name-cond', 'value'),
    Input('fund_name-cond', 'value'),
    Input('domicile_country-cond', 'value'),
    Input('entry_round-cond', 'value')
)
def update_comp_graph(metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order, date, difference,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond):

    dff = df.copy(deep=True)
    dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order, date, difference,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond)
    
    '''
    fig = px.bar(dff,
        x=metric,
        y=dimension,
        title='Drilldown',
        barmode='stack',
        color=metric,
        custom_data=['industries', 'fund_name', 'domicile_country', 'entry_round', 'display_name']
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

    fig.update_layout(
        width = 950,
        height = dff.shape[0]*(150 if dff.shape[0]<3 else 100 if dff.shape[0]<6 else 50 ),
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
        ])
    )
    '''

    return formatFigure(dff, metric, dimension)

def formatFigure(dff, metric, dimension):
    fig = px.bar(dff,
        x=metric,
        y=dimension,
        title='Drilldown',
        barmode='stack',
        color=metric,
        custom_data=['industries', 'fund_name', 'domicile_country', 'entry_round', 'display_name']
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

    fig.update_layout(
        width = 950,
        height = dff.shape[0]*(150 if dff.shape[0]<3 else 100 if dff.shape[0]<6 else 50 ),
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
            'entry_round': lambda x: ',<br> '.join(x.dropna().unique()) if x.dropna().any() else ''
            }
    object_to_return.pop(dimension)
    return object_to_return

def prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order, date, difference,
industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond):
    dff = dff.copy(deep=True)
    #print(date)
    if difference:
        actual_dff = prepare_dataframe(dff, metric, dimension, filter_industries, filter_companies, filter_funds, filter_countries, filter_entry_round, order, None, None,
    industries_cond, display_name_cond, fund_name_cond, domicile_country_cond, entry_round_cond)

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