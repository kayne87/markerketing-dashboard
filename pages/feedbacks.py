import dash
from dash import dcc, html, callback, Output, Input, clientside_callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objs as go
import matplotlib.pyplot as plt

from datetime import date
from datetime import datetime
import pandas as pd
import numpy as np
import os

from collections import Counter
from wordcloud import WordCloud
import base64
import io
from PIL import Image

dash.register_page(__name__, name='Feedbacks', order=4)
cherrypicked_seed = 42

path = "/home/marcodistrutti/marketing-analytics/data/" #".//data//"
df_sentiments = pd.read_csv(path + "customers_sentiments.csv")
df_rfm = pd.read_csv(path + "customers_rfm_jenks.csv").round(2)
df_churners_sentiments = pd.read_csv(path + "churners_sentiments.csv")
df_orders = pd.read_csv(path + "orders.csv")

df_orders["purchase_datetime"] = pd.to_datetime(df_orders["purchase_datetime"])
print(len(df_orders))

df_orders_active = df_orders[df_orders["purchase_datetime"] >= '2023-01-01']

df_sentiments["sentiment_description"] = ["" for i in range(0, len(df_sentiments))]
df_sentiments.loc[df_sentiments["sentiment"] == 1, "sentiment_description"] = "Positive"
df_sentiments.loc[df_sentiments["sentiment"] == 0, "sentiment_description"] = "Neutral"
df_sentiments.loc[df_sentiments["sentiment"] == -1, "sentiment_description"] = "Negative"

sentiments_color = {"positive": "#C1FF72", "neutral": "#D9D9D9", "negative": "#FFBD59"}

df_sentiments_pie = df_sentiments.groupby(by=["sentiment_description"]).count().reset_index()[["sentiment_description", "sentiment"]]

total = df_sentiments_pie["sentiment"].sum()
positive = df_sentiments_pie[df_sentiments_pie["sentiment_description"] == "Positive"]["sentiment"].values[0]
negative = df_sentiments_pie[df_sentiments_pie["sentiment_description"] == "Negative"]["sentiment"].values[0]

brs = (positive/total) - (negative/total)
brs = round(brs*100, 2)

df_sentiments_active = pd.merge(
    df_sentiments,
    df_orders_active,
    on="customer_id",
    how='inner'
)
active_users_sentiments = df_sentiments_active["customer_id"].unique()
df_sentiments_active = df_sentiments[df_sentiments["customer_id"].isin(active_users_sentiments)]

df_sentiments_active_pie = df_sentiments_active.groupby(by=["sentiment_description"]).count().reset_index()[["sentiment_description", "sentiment"]]

df_churners_sentiments_aggregation = df_churners_sentiments[df_churners_sentiments["CHURN"] == 1].groupby(by=["CLASS", "sentiment"]).count().reset_index()
df_churners_sentiments_aggregation = df_churners_sentiments_aggregation[df_churners_sentiments_aggregation["sentiment"] != 0]
setiment_mapped = df_churners_sentiments_aggregation["sentiment"].apply(lambda sent: "Ambassadors" if sent == 1 else "Detractors")
df_churners_sentiments_aggregation["sentiment"] = setiment_mapped
df_churners_sentiments_aggregation["customers"] = df_churners_sentiments_aggregation["customer_id"]
df_churners_sentiments_classes = df_churners_sentiments_aggregation[["CLASS", "sentiment", "customers"]]

layout = html.Div(
    [
        dcc.Markdown('# Customer base satisfaction'),
        html.H4('What do customers talk about?', style={'margin': '30px 0', 'color': 'gray'}),
        html.Div(children=
            [
                html.Div(children=
                    [
                        html.Img(
                            style={'maxWidth': '511px', 'marginLeft': '-15px'},
                            src="/assets/customers_reviews_words.png",
                            alt="Studied reviews"
                        )#,
                        #html.P('.', style={'color': 'transparent'}),
                        #html.P('Machine learning training reviews (top 100 reviews)', style={'font-weight': 'bold', 'color': 'gray'}),
                        #html.Img(
                        #    src="/assets/training_reviews.png",
                        #    alt="Studied reviews",
                        #    width=400
                        #),
                    ], style={'padding': 0, 'flex-grow': 0, 'flex-shrink': 0}
                ),

                html.Div(children=
                    [
                        #html.P('Predicted BRS (Brand Reccomandation Score): %' + str(brs) + '%', style={'font-weight': 'bold'}),
                        dcc.Graph(
                            id='sentiment_pie',
                            style={'padding': 0, 'margin': 0},
                            figure = px.pie(
                                df_sentiments_pie,
                                values='sentiment',
                                names='sentiment_description',
                                color='sentiment_description',
                                color_discrete_map={ 'Positive': sentiments_color["positive"], 'Neutral': sentiments_color["neutral"], 'Negative': sentiments_color["negative"]},
                                hole=0.5
                            ).update_layout(
                                margin={"t": 0, "r": 0, "b": 0, "l": 0},
                                height=250,
                                autosize=True
                            ),
                            config = {'displayModeBar': False}
                        )
                    ], style={'padding': 0, 'paddingLeft': 10, 'margin': 0, 'flex': 1}
                ),

                html.Div(children= [ ],style={'flex': 1})
            ],
            style={'display': 'flex', 'flex-direction': 'row', 'height': '210px'}
        ),
        html.Div(style={'margin-top': '140px'}),
        html.H4('Churners\' sentiments', style={'margin': '30px 0', 'color': 'gray'}),
        html.Div(children=[
            dcc.Graph(
                id='diamonds-sentiments',
                figure=px.bar(
                    df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "DIAMOND"],
                    x='sentiment',
                    y='customers',
                    text=df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "DIAMOND"]['customers']
                ).update_traces(marker_color=['#FFBD59', '#C1FF72'],showlegend=False,textfont=dict(size=14, family='Arial')).update_layout(
                    margin={"t": 0, "r": 0, "b": 0, "l": 0},
                    height=200,
                    autosize=True,
                    yaxis=dict(title='Churners'),
                    xaxis=dict(title='DIAMOND', title_font=dict(size=16, family='Arial')),
                    plot_bgcolor='rgba(99, 197, 218, 0.5)'
                ),
                config = {'displayModeBar': False},
                style = {'flex': 1}
            ),
            dcc.Graph(
                id='diamonds-sentiments',
                figure=px.bar(
                    df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "GOLD"],
                    x='sentiment',
                    y='customers',
                    text=df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "GOLD"]['customers']
                ).update_traces(marker_color=['#FFBD59', '#C1FF72'],showlegend=False,textfont=dict(size=14, family='Arial')).update_layout(
                    margin={"t": 0, "r": 0, "b": 0, "l": 0},
                    height=200,
                    autosize=True,
                    yaxis=dict(title=None),
                    xaxis=dict(title='GOLD', title_font=dict(size=16, family='Arial')),
                    plot_bgcolor='rgba(255, 215, 0, 0.5)'
                ),
                config = {'displayModeBar': False},
                style = {'flex': 1}
            ),
            dcc.Graph(
                id='diamonds-sentiments',
                figure=px.bar(
                    df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "SILVER"],
                    x='sentiment',
                    y='customers',
                    text=df_churners_sentiments_classes[df_churners_sentiments_classes["CLASS"] == "SILVER"]['customers']
                ).update_traces(marker_color=['#FFBD59', '#C1FF72'],showlegend=False,textfont=dict(size=14, family='Arial')).update_layout(
                    margin={"t": 0, "r": 0, "b": 0, "l": 0},
                    height=200,
                    autosize=True,
                    yaxis=dict(title=None),
                    xaxis=dict(title='SILVER', title_font=dict(size=16, family='Arial')),
                    plot_bgcolor='rgba(192, 192, 192, 0.5)'
                ),
                config = {'displayModeBar': False},
                style = {'flex': 1}
            )
        ],
        style={'display': 'flex', 'flex-direction': 'row'})
    ]
)