import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


#heat map functions
def generate_heatmap(excel_file):
    df = pd.read_excel(excel_file)
    fig = px.imshow(df)
    return fig.to_html(full_html=False)


# funnel chart functions
def generate_funnel_chart(data):
    fig = go.Figure(go.Funnel(
        y=data['labels'],
        x=data['values'],
        textinfo="value+percent initial"
    ))
    fig.update_layout(title="Funnel Chart")
    return fig.to_html(full_html=False)


# bar chart function
def generate_bar_chart(names, values):
    fig = px.bar(x=names, y=values)
    return fig.to_html(full_html=False)

# line chart function
def generate_line_chart(names, values):
    fig = px.line(x=names, y=values)
    return fig.to_html(full_html=False)

# pie chart function
def generate_pie_chart(names, values):
    fig = px.pie(values=values, names=names)
    return fig.to_html(full_html=False)


# bubble chart function
def generate_bubble_chart(names, values):
    fig = px.scatter(x=names, y=values, size=values, color=names, hover_name=names)
    return fig.to_html(full_html=False)

# countour plot function
def generate_contour_plot(names,values):
    fig = px.density_contour( x=names, y=values, marginal_x='histogram', marginal_y='histogram')
    return fig.to_html(full_html=False)

