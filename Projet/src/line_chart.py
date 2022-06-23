import plotly.graph_objects as go
import plotly.express as px

def add_line_trace(fig, data):
    x = data.columns.to_list()[1:]
    for i in range(data.shape[0]):
        fig.add_trace(go.Scatter(x=x, y=data.iloc[[i]][data.columns.to_list()[1:]].reset_index(drop=True).values.flatten().tolist(), name=data.iloc[[i]].index.to_list()[0],
                         line=dict(width=3)))
    fig.update_layout(
        plot_bgcolor = "white",
        paper_bgcolor = "white"
        )
    return fig