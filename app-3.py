
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("Customer Churn.csv")

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Visualization 1: Distribution of Churn Status
churn_counts = df['Churn'].value_counts().reset_index()
churn_counts.columns = ['Churn Status', 'Count']  # Rename columns for clarity

fig1 = px.bar(
    churn_counts,
    x='Churn Status',
    y='Count',
    labels={"Churn Status": "Churn Status (0 = No, 1 = Yes)", "Count": "Count"},
    title="Distribution of Churn Status",
    color_discrete_sequence=["#636EFA"]
)

# Visualization 2: Complaints vs. Churn Status
if 'Churn' in df.columns and 'Complains' in df.columns:
    fig2 = px.box(
        df,
        x='Churn',
        y='Complains',
        color='Churn',
        title="Complaints vs. Churn Status",
        labels={
            "Complains": "Number of Complaints",
            "Churn": "Churn Status (0 = No, 1 = Yes)"
        },
        color_discrete_sequence=["#FF6361", "#58508D"]
    )
else:
    fig2 = None

# Visualization 3: Subscription Length vs. Churn
if 'Subscription  Length' in df.columns and 'Churn' in df.columns:
    fig3 = px.scatter(
        df,
        x='Subscription  Length',  # Use exact column name with double spaces
        y='Churn',
        title="Subscription Length vs. Churn",
        labels={
            "Subscription  Length": "Subscription Length (Months)",
            "Churn": "Churn Status (0 = No, 1 = Yes)"
        },
        opacity=0.6,
        color_discrete_sequence=["#00CC96"]
    )
else:
    fig3 = None

# Layout
app.layout = dbc.Container([
    html.H1("Churn Analysis Dashboard", className="text-center my-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig1), width=6),
        dbc.Col(dcc.Graph(figure=fig2), width=6) if fig2 else html.Div("Figure 2: Data missing")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig3), width=12) if fig3 else html.Div("Figure 3: Data missing")
    ]),
    dbc.Row([
        html.H4("Key Insights", className="text-center my-3"),
        html.Ul([
            html.Li("Churn distribution shows a class imbalance, which might impact model choice."),
            html.Li("Complaints positively correlate with churn; addressing complaints may reduce churn."),
            html.Li("Longer subscription lengths generally lead to lower churn rates.")
        ])
    ])
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host='0.0.0.0')
