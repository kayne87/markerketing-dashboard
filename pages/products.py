import dash
from dash import dcc, html, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


# page 2 data

                    #------------------------|---------------------------#
                    # cursor first N ustomer | selection of segments     #
                    #                        | all                       #
                    #                        | diamond/gold/silver/bronze#
                    #------------------------|---------------------------#
                    #                        |                           #
                    # antec. vs conseq.      | table customer vs revenue #
                    #                        |                           #
                    #------------------------|---------------------------#
                    # table total revenue    |                           #
                    #------------------------|---------------------------#


dash.register_page(__name__, name='Products_revenue', order=5)
path = "/home/marcodistrutti/marketing-analytics/data/mba/"

MBA_df_DIAMOND = pd.read_csv(path + "dataframe_MBA_product_group_confidence_support_lift_threshold_1_sort_by_confidence_DIAMOND.csv")
MBA_df_GOLD = pd.read_csv(path + "dataframe_MBA_product_group_confidence_support_lift_threshold_1_sort_by_confidence_GOLD.csv")
MBA_df_SILVER = pd.read_csv(path + "dataframe_MBA_product_group_confidence_support_lift_threshold_1_sort_by_confidence_SILVER.csv")

MBA_df_revenue_DIAMOND = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_DIAMOND.csv")
MBA_df_revenue_GOLD = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_GOLD.csv")
MBA_df_revenue_SILVER = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_SILVER.csv")
MBA_df_revenue_DIAMOND.columns = ['customer','revenue']
MBA_df_revenue_GOLD.columns = ['customer','revenue']
MBA_df_revenue_SILVER.columns = ['customer','revenue']

MBA_RFM_churners_DIAMOND_prod = pd.read_csv(path + "dataframe_RFM_churners_DIAMOND_prod.csv")
MBA_RFM_churners_DIAMOND_prod = MBA_RFM_churners_DIAMOND_prod.round(2)
MBA_RFM_churners_DIAMOND_prod.columns = ['index','product', 'value', 'customer']

MBA_RFM_churners_GOLD_prod = pd.read_csv(path + "dataframe_RFM_churners_GOLD_prod.csv")
MBA_RFM_churners_GOLD_prod = MBA_RFM_churners_GOLD_prod.round(2)
MBA_RFM_churners_GOLD_prod.columns = ['index','product', 'value', 'customer']

MBA_RFM_churners_SILVER_prod = pd.read_csv(path + "dataframe_RFM_churners_SILVER_prod.csv")
MBA_RFM_churners_SILVER_prod = MBA_RFM_churners_SILVER_prod.round(2)
MBA_RFM_churners_SILVER_prod.columns = ['index','product', 'value', 'customer']

df_customer_sentiment = pd.read_csv(path + "dataframe_churners_sentiment.csv")
df_customer_sentiment_dict = df_customer_sentiment.set_index('customer_id').T.to_dict('list')


MBA_df_revenue_DIAMOND_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_DIAMOND_for_neg_sentiment.csv")
MBA_df_revenue_GOLD_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_GOLD_for_neg_sentiment.csv")
MBA_df_revenue_SILVER_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_SILVER_for_neg_sentiment.csv")
MBA_df_revenue_DIAMOND_neg_sentiment.columns = ['customer','revenue']
MBA_df_revenue_GOLD_neg_sentiment.columns = ['customer','revenue']
MBA_df_revenue_SILVER_neg_sentiment.columns = ['customer','revenue']

MBA_df_revenue_DIAMOND_non_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_DIAMOND_for_non_neg_sentiment.csv")
MBA_df_revenue_GOLD_non_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_GOLD_for_non_neg_sentiment.csv")
MBA_df_revenue_SILVER_non_neg_sentiment = pd.read_csv(path + "dataframe_MBA_revenue_RMF_CHURN_SILVER_for_non_neg_sentiment.csv")
MBA_df_revenue_DIAMOND_non_neg_sentiment.columns = ['customer','revenue']
MBA_df_revenue_GOLD_non_neg_sentiment.columns = ['customer','revenue']
MBA_df_revenue_SILVER_non_neg_sentiment.columns = ['customer','revenue']

def get_value_all_customer(MBA_df_revenue,N_first):
    N_first = min(N_first,100000000)
    get_prod_total_revenue = list()
    xyz = pd.DataFrame.from_dict(MBA_df_revenue)
    sum_ = xyz['revenue'].sum()
    sum_ = sum_.round(0)
    temp=dict()
    temp['revenue'] = sum_
    get_prod_total_revenue.append(temp)
    return get_prod_total_revenue

def get_prod_per_customer(MBA_RFM_churners__prod,customer):
    get_prod_per_customer_list = list()
    list_prod_customer = list()
    list_prod_customer = MBA_RFM_churners__prod[MBA_RFM_churners__prod['customer'] == customer]['product']


    list_prod_customer = list_prod_customer.tolist()
    rrr = str(list_prod_customer[0])
    rrr = rrr.strip('\[')
    rrr = rrr.strip('\]')
    rrr = rrr.split(',')

    for jj in rrr:
        jj = jj.strip(' ')
        jj = jj.strip('\'')
        temp=dict()
        temp['product'] = jj
        get_prod_per_customer_list.append(temp)
    return get_prod_per_customer_list

qqq = get_prod_per_customer(MBA_RFM_churners_DIAMOND_prod,742169)
rrr = get_value_all_customer(MBA_df_revenue_DIAMOND,10000)

def get_customer_sentiment(df_customer_sentiment,customer):
  df_customer_sentiment_dict = df_customer_sentiment.set_index('customer_id').T.to_dict('list')
  try:
   sentiment_value = df_customer_sentiment_dict[customer][0]
   if sentiment_value == -1:
    sentiment_temp = "NEGATIVE"
   else:
      sentiment_temp = "NONNEGATIVE"
  except:
      sentiment_temp = "NONNEGATIVE"

  return sentiment_temp

def extract_item_from_df_prd_group(_prod_group):
    temp = _prod_group.replace(',frozenset({',';({')
    temp = temp.replace('frozenset({','({')
    temp = temp.replace('({','')
    temp = temp.replace('})','')
    temp = temp.replace('.0','')
    _ant = temp.split(';')[0]
    _con = temp.split(';')[1]
    return _ant,_con


table = dash_table.DataTable(MBA_df_DIAMOND.to_dict('records'),[{"name": i, "id": i} for i in MBA_df_DIAMOND.columns], id='tbl'),

yyy = MBA_df_revenue_DIAMOND.to_dict('records')

zzz = MBA_RFM_churners_DIAMOND_prod.to_dict()


data_MBA_df_revenue=MBA_df_revenue_DIAMOND.iloc[:7].to_dict('records')

value_rules = 10

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(dcc.Markdown('# MBA ')),
            html.Hr(),
            ],
            ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            html.P("Number of customers to be contacted:"),
                            dcc.Slider(id="first_value_customer", min=1, max=11, value=7, step=1,
                                       marks={1: '1', 3: '3', 5: '5', 7: '7', 9: '9', 11: '11'})
                            ],
                        ),
                dbc.Col(
                        [
                            html.Div("RFM segments"),
                            dcc.Dropdown(
                                    options=["Diamond","Gold","Silver"],
                                    value="Diamond",
                                    multi=False,
                                    placeholder="Select a segment",
                                    id="segment",
                                    ),
                            html.Div("Sentiment"),
                            dcc.Dropdown(
                                    options=["Non Negative","Negative"],
                                    #options=["Negative"],
                                    value="Negative",
                                    multi=False,
                                    placeholder="Select a sentiment",
                                    id="sentiment",
                                    ),
                            ],
                    ),
                html.Hr(),

            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            html.H4("Revenue in $ per customer:"),
                            dash_table.DataTable(id='revenue_customer',
                                                 data=data_MBA_df_revenue,
                                                 row_selectable='single',
                                                 selected_rows=[],
                                                 #allow_duplicate=True,
                                                 page_size=10),
                            html.Div(id='datatable-row-ids-container'),
                        ],
                ),
                 dbc.Col(
                         [
                            html.H4("Suggested products per customer" ),
                            dash_table.DataTable(id='prod_customer',data=qqq, page_size=10),

                        ],
                ),
            ],
        ),
            dbc.Row(
                [
                    html.H4("Total revenue in $ per segment" ),
                    dash_table.DataTable(
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'lineHeight': '15px',
                            'width': '80px'
                        },
                        id='total_revenue',data=rrr, page_size=10),

                    ],
                ),


    ],
)

@callback( # Update list of N valuable customer
    Output('total_revenue', 'data'),
    Input('first_value_customer','value'),
    Input('revenue_customer','data'),
    )

def update_total_revenue (first_value_customer_value,revenue_customer_data):
      result_ = get_value_all_customer(revenue_customer_data,10000)
      return result_

@callback( # Update dataframe based on segment
    Output('revenue_customer','data'),
    Input('segment','value'),
    Input('first_value_customer','value'),
    Input('sentiment','value'),

    )
def update_df_value_2(segment_value,first_value_value,sentiment_value):
    if sentiment_value != 'Negative':
        if segment_value == "Silver":
            result_ = MBA_df_revenue_SILVER_non_neg_sentiment.iloc[:first_value_value].to_dict('records')
        if segment_value == "Gold":
            result_ = MBA_df_revenue_GOLD_non_neg_sentiment.iloc[:first_value_value].to_dict('records')
        if segment_value == "Diamond":
            result_ = MBA_df_revenue_DIAMOND_non_neg_sentiment.iloc[:first_value_value].to_dict('records')
    else:
        if segment_value == "Silver":
            result_ = MBA_df_revenue_SILVER_neg_sentiment.iloc[:first_value_value].to_dict('records')
        if segment_value == "Gold":
            result_ = MBA_df_revenue_GOLD_neg_sentiment.iloc[:first_value_value].to_dict('records')
        if segment_value == "Diamond":
            result_ = MBA_df_revenue_DIAMOND_neg_sentiment.iloc[:first_value_value].to_dict('records')
    return result_


@callback(
      Output('prod_customer', "data"),
      [Input('revenue_customer', 'selected_rows'),
       Input('revenue_customer','data'),
       Input('first_value_customer','value'),
       Input('segment','value')]
     )

def update_2(selected_rows,data,first_value,segment_value):
    selected_row_id_0 = 0 #selected_rows[0]
    sel_customer_0 = data[selected_row_id_0]['customer']
    if segment_value == "Diamond":
          prod_per_customer = get_prod_per_customer(MBA_RFM_churners_DIAMOND_prod,sel_customer_0)
    if segment_value == "Gold":
          prod_per_customer = get_prod_per_customer(MBA_RFM_churners_GOLD_prod,sel_customer_0)
    if segment_value == "Silver":
          prod_per_customer = get_prod_per_customer(MBA_RFM_churners_SILVER_prod,sel_customer_0)

    if selected_rows:
        selected_row_id = selected_rows[0]
        sel_customer = data[selected_row_id]['customer']
        if segment_value == "Diamond":
            prod_per_customer = get_prod_per_customer(MBA_RFM_churners_DIAMOND_prod,sel_customer)
        if segment_value == "Gold":
            prod_per_customer = get_prod_per_customer(MBA_RFM_churners_GOLD_prod,sel_customer)
        if segment_value == "Silver":
            prod_per_customer = get_prod_per_customer(MBA_RFM_churners_SILVER_prod,sel_customer)
        #selected_row_data = qqq[selected_row_id]
        return prod_per_customer


@callback(
      Output('revenue_customer', 'selected_rows'),
      [Input('first_value_customer','value')]
     )

def update_1(value):
    return [0]
