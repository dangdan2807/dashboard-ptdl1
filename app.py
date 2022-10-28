from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
from numpy import number
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate(
    # "./data/iuh-19529651-b4591-firebase-adminsdk-ykvzr-3be3e73702.json")
    # "./data/iuh-19529651-4462e-firebase-adminsdk-f4x21-d2ec4a7735.json")
"./data/iuh-19529651-firebase-adminsdk-3v4ij-8387769ee6.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()


# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server
app.title = "Finance Data Analysis"

# TRỰC QUAN HÓA DỮ LIỆU WEB APP

queryResults = list(dbFireStore.collection(
    "tbl-19529651").select(['PRICEEACH', 'QUANTITYORDERED', 'SALES', 'YEAR_ID', 'CATEGORY']).stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

# doanh số sale
df = pd.DataFrame(listQueryResult)
revenue = str(round(sum(df['SALES']), 2))

# doanh thu
loiNhuan = sum(df['SALES']) - sum(df['PRICEEACH'] * df['QUANTITYORDERED'])
profit = str(round(loiNhuan, 2))

# top doanh số
revenue_1 = df.groupby('CATEGORY').sum(numeric_only=True)
top_revenue = str(round(revenue_1['SALES'].max(), 2))

# top doanh thu
df['TOTAL_SALES'] = df['PRICEEACH'] * df['QUANTITYORDERED']
df['PROFIT'] = df['SALES'] - df['TOTAL_SALES']
profit_1 = df.groupby('CATEGORY').sum('PROFIT')
top_profit = str(round(profit_1['PROFIT'].max(), 2))

sp = df.groupby(['CATEGORY']).sum('SALES').sort_values(
    by="SALES", ascending=False).reset_index().head(1)['CATEGORY'][0]

# chart

# doanh số bán hàng theo năm - bar chart
figDoanhSo = px.histogram(df, y='SALES', x='YEAR_ID', color='YEAR_ID',
                          labels={'YEAR_ID': 'Năm', 'SALES': 'Doanh số'},
                          title='Doanh số bán hàng theo năm', )

# tỉ lệ đóng góp của doanh số theo từng danh mục sản phẩm trong từng năm - sunburst chart
figTiLeDoanhThu = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
                              labels={'YEAR_ID': 'Năm', 'SALES': 'Doanh số'}, color='SALES',
                              title='Tỉ lệ đóng góp của doanh số theo từng danh mục sản phẩm trong từng năm')

# lợi nhuận bán hàng theo năm - line chart
total_profit = df.groupby('YEAR_ID').sum()['PROFIT'].reset_index()
figLoiNhuan = px.line(total_profit, y='PROFIT', x='YEAR_ID',
                      labels={'YEAR_ID': 'Năm', 'PROFIT': 'Lợi nhuận'},
                      title='Lợi nhuận bán hàng theo năm')

# tỉ lệ đóng góp của lợi nhuận theo từng danh mục sản phẩm trong từng năm - sunburst chart
figTiLeLoiNhuan = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='PROFIT',
                              labels={'YEAR_ID': 'Năm', 'PROFIT': 'Lợi nhuận'}, color='PROFIT',
                              title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục sản phẩm trong từng năm')

app.layout = html.Div(
    children=[
        # header
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H5(
                                    children="Xây dựng danh mục sản phẩm tiềm năng",
                                    className="ms-5 text-white text-uppercase"),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.H5(children="ĐHCN tp.HCM - ĐHKTPM15B - 19529651 - Phạm Đăng Đan",
                                        className="text-white text-uppercase"),
                            ],
                        )
                    ],
                    className="row pt-2 row-cols-2"
                )
            ],
            className="bg-primary container-fluid",
        ),
        # wrapper
        html.Div(
            children=[
                html.Div(
                    children=[
                        # doanh số sale
                        html.Div(
                            html.Div(
                                children=[
                                    html.H6(
                                        children="Doanh số sale",
                                        className="text-uppercase fw-bold"),
                                    html.P(revenue),
                                ],
                                className="bg-white pt-3 pb-2 ps-3 card",
                            ),
                        ),

                        # lợi nhuận
                        html.Div(
                            html.Div(
                                children=[
                                    html.H6(children="Lợi nhuận",
                                            className="text-uppercase fw-bold"),
                                    html.P(profit),
                                ],
                                className="bg-white pt-3 pb-2 ps-3 card",
                            )
                        ),

                        # top doanh số
                        html.Div(
                            html.Div(
                                children=[
                                    html.H6(
                                        children="top doanh số",
                                        className="text-uppercase fw-bold"),
                                    html.P(sp + ", " + top_revenue),
                                ],
                                className="bg-white pt-3 pb-2 ps-3 card",
                            )
                        ),

                        # top lợi nhuận
                        html.Div(
                            html.Div(
                                children=[
                                    html.H6(
                                        children="Top lợi nhuận",
                                        className="text-uppercase fw-bold"),
                                    html.P(sp + ", " + top_profit),
                                ],
                                className="bg-white pt-3 pb-2 ps-3 card",
                            )
                        ),
                    ],
                    className="row mt-3 row-cols-lg-4 row-cols-md-2 row-cols-sm-1 row-cols-1",
                ),
                html.Div(
                    children=[
                        html.Div(
                            html.Div(
                                children=dcc.Graph(
                                    id='doanhso-graph',
                                    figure=figDoanhSo),
                                className="bg-white card"
                            )),
                        html.Div(
                            html.Div(
                                children=dcc.Graph(
                                    id='tiledoanhthu-graph',
                                    figure=figTiLeDoanhThu),
                                className="bg-white card"
                            )),
                    ],
                    className="row mt-1 row-cols-lg-2 row-cols-sm-1 row-cols-1"
                ),
                html.Div(
                    children=[
                        html.Div(
                            html.Div(
                                children=dcc.Graph(
                                    id='loinhuan-graph',
                                    figure=figLoiNhuan),
                                className="bg-white card"
                            )),
                        html.Div(
                            html.Div(
                                children=dcc.Graph(
                                    id='tileloinhuan-graph',
                                    figure=figTiLeLoiNhuan),
                                className="bg-white card"
                            )),
                    ],
                    className="row mt-1 row-cols-lg-2 row-cols-sm-1 row-cols-1"
                ),
            ],
            className="container pb-4",
        ),
    ],
    className="bg-light",
)


# @app.callback(Output('display-value', 'children'),
#               [Input('dropdown', 'value')])
# def display_value(value):
#     return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
