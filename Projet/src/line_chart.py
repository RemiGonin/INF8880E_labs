import plotly.graph_objects as go
import plotly.express as px

import hover_template


def add_line_trace(fig, data):
    x = data.columns.to_list()[1:]
    x = [int(value) for value in x]

    for i in range(data.shape[0]):
        list_y = data.iloc[[i]][data.columns.to_list()[1:]].reset_index(
            drop=True).values.flatten().tolist()

        fig.add_trace(go.Scatter(x=x, y=list_y, name=data.iloc[[i]].index.to_list()[0],
                                 line=dict(width=3)))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest"
    )
    fig.update_traces(
        hoverlabel={'namelength': 0},
        hovertemplate=hover_template.get_hover_template_linechart())
    fig.update_xaxes(range=[x[0], x[-1]], dtick=1, title_text="Année",
                     tickangle=45, showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(range=[0, 800], title_text="Dépenses moyennes par semaine et par personne (en Pence)",
                     showline=True, linewidth=2, linecolor='black')
    fig.add_vrect(x0=2007, x1=2008,
                  annotation_text="Crise de 2008",
                  annotation_position="top right",
                  annotation_font_size=20,
                  annotation_font_color="black",
                  annotation_textangle=90,
                  fillcolor="green",
                  opacity=0.25,
                  line_width=0
                  )
    fig.add_vrect(x0=2019, x1=2020,
                  annotation_text="Pandémie de Covid-19",
                  annotation_position="top right",
                  annotation_font_size=20,
                  annotation_font_color="black",
                  annotation_textangle=90,
                  fillcolor="green",
                  opacity=0.25,
                  line_width=0
                  )
    fig.add_vline(x=2012, line_dash="dot",
                  annotation_text="Jeux olympiques à Londre",
                  annotation_position="top right",
                  annotation_font_size=20,
                  annotation_font_color="black",
                  annotation_textangle=90
                  )
    fig.add_vline(x=2020, line_dash="dot",
                  annotation_text="Brexit",
                  annotation_position="top right",
                  annotation_font_size=20,
                  annotation_font_color="black",
                  annotation_textangle=90
                  )
    fig.add_vline(x=2014, line_dash="dot",
                  annotation_text="Indépendance de l'Écosse",
                  annotation_position="top right",
                  annotation_font_size=20,
                  annotation_font_color="black",
                  annotation_textangle=90
                  )
    return fig
