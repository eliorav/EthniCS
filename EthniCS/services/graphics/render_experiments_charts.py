import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .constants import ETHNICS_SOLVER, supported_solvers, solver_to_color


def get_color_continuous_scale(metric_name):
    if metric_name == 'mse':
        return px.colors.sequential.Jet
    elif metric_name == 'psnr':
        return [
        (0, "rgb(128,0,0)"),
        (0.05, "rgb(250,0,0)"),
        (0.06, "rgb(255,255,0)"),
        (0.08, "rgb(135,197,95)"),
        (0.16, "rgb(5,255,255)"),
        (1, "rgb(0,0,131)"),
    ]
    else:
        return px.colors.sequential.Jet_r

def get_color_range(metric_name):
    metric_lower = metric_name.lower().strip()
    if  metric_lower == 'mse':
        return [0, 0.05]
    elif metric_lower == 'psnr':
        return [0, 350]
    else:
        return [0, 1]


def render_solver_by_pools(fig, row, col, df, metric, sparsity_ratio=None, ethnicity_num=None, showlegend=True, log_y=True):    
  assert sparsity_ratio is not None or ethnicity_num is not None, "you must use sparsity_ratio or ethnicity_num args"
  temp_df = df[(df.name.isin(list(supported_solvers.keys()))) & ((df.name == 'all zeros') | (df.original_sparsity_ratio == sparsity_ratio if sparsity_ratio is not None else df.ethnicity_num == ethnicity_num))].groupby(['name', 'num_of_pools']).mean().reset_index()
  fig1 = px.line(temp_df, x='num_of_pools', y=metric, color='name', markers=True, color_discrete_map=solver_to_color, log_y=log_y)

  fig1.update_layout(xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
  )
  traces = sorted(list(fig1.select_traces()), key=lambda x: supported_solvers.get(x.name, 1))

  for trace in traces:
      trace.showlegend = showlegend
      if trace.name == ETHNICS_SOLVER:
          # Replace ETHNICS_SOLVER line with empty square markers
          fig.add_trace(go.Scatter(
              x=trace.x,
              y=trace.y,
              mode='markers',
              marker=dict(symbol='square-open', size=12, color=solver_to_color[ETHNICS_SOLVER], line=dict(width=4, color=solver_to_color[ETHNICS_SOLVER])),
              name=f'<b>{ETHNICS_SOLVER}</b>',
              showlegend=showlegend
          ), row=row, col=col)
      else:
          fig.add_trace(trace, row=row, col=col)

  fig.update_traces(line=dict(width=6), marker=dict(size=12))
  fig.update_layout(legend_font_size=20, legend_tracegroupgap=1)
  fig.for_each_trace(lambda t: t.update(name=f'<b>{t.name}</b>'))

  return fig

def render_solver_by_sparsenees(fig, row, col, metric, num_of_pools, df, n=1024):
    temp_df = df.copy()
    temp_df['k'] = ((n-temp_df.x_sparseness)/n)*100
    temp_df = temp_df[(temp_df.name == ETHNICS_SOLVER) & (temp_df.num_of_pools == num_of_pools)].drop(columns=['name']).groupby(['k']).mean().reset_index()

    fig1 = px.scatter(
        temp_df, 
        x='k', 
        y=metric, 
        color=metric, 
        color_continuous_scale=get_color_continuous_scale(metric),
    )

    for trace in fig1.select_traces():
        fig.add_trace(trace, row=row, col=col)

    return fig

def render_heatmap(fig, row, col, coloraxis, df, metric, solver = ETHNICS_SOLVER, n=1024):
    temp_df = df[df.name == solver].copy().drop(columns=['name'])
    temp_df['k'] = ((n-temp_df.x_sparseness)/n)*100
    temp_df['m/n'] = temp_df.num_of_pools/n
    temp_df = temp_df.groupby(['k', 'm/n']).mean().reset_index()
    temp_df = temp_df[['k', 'm/n', metric]]

    temp_df2 = pd.DataFrame(
        columns=temp_df['m/n'].unique(), index=temp_df.k.unique()
    )

    zmin, zmax = get_color_range(metric)
    for item in temp_df.to_dict('records'):
        temp_df2.loc[item['k']][item['m/n']] = item.get(metric, zmin)

    temp_df2 = temp_df2.sort_index(ascending=True)
    temp_df2 = temp_df2.fillna(zmin)

    fig.add_trace(go.Heatmap(
            z=temp_df2.values,
            x=temp_df2.columns.values,
            y=temp_df2.index.values,
            hovertemplate="δ: %{x}<br>k: %{y}<br>" + solver.upper() + ": %{z}<extra></extra>",
            zmin=zmin,
            zmax=zmax,
            coloraxis=coloraxis
        ), row=row, col=col
    )
    return fig
    
def render_confidence_heatmap(fig, row, col, coloraxis, df, solver = ETHNICS_SOLVER, n=1024):
    temp_df = df[df.name == solver].copy().drop(columns=['name'])
    temp_df['k'] = ((n-temp_df.x_sparseness)/n)*100
    temp_df['m/n'] = temp_df.num_of_pools/n
    temp_df = temp_df.groupby(['k', 'm/n']).mean().reset_index()
    temp_df = temp_df[['k', 'm/n', 'confidence']]

    temp_df2 = pd.DataFrame(
        columns=temp_df['m/n'].unique(), index=temp_df.k.unique()
    )


    for item in temp_df.to_dict('records'):
        temp_df2.loc[item['k']][item['m/n']] = item.get('confidence', 1)
    temp_df2 = temp_df2.sort_index(ascending=True)
    zmin, zmax = [0, 1]
    temp_df2 = temp_df2.fillna(zmax)
    fig.add_trace(
        go.Heatmap(
            z=temp_df2.values,
            x=temp_df2.columns.values,
            y=temp_df2.index.values,
            hovertemplate="δ: %{x}<br>k: %{y}<br>" + solver.upper() + ": %{z}<extra></extra>",
            zmin=zmin,
            zmax=zmax,
            coloraxis=coloraxis
        ), row=row, col=col
    )

    return fig

def get_exp_scatter_plot(fig, row, col, x, xhat, title, color=None):
    fig.add_trace(
        go.Scatter(x=x, y=xhat, name=title, mode="markers", marker_color=color),
        row=row,
        col=col
    )

    fig.add_trace(
        go.Scatter(x=x, y=x, line_color="black", showlegend=False, line=dict(dash='dot'), name='x'),
        row=row,
        col=col
    )
    return fig

def render_subplot_layout(metric, subplot_titles, log_y1=True, log_y2=True, title_text=''):
    fig = make_subplots(
        rows=10, 
        cols=6, 
        specs=[
            [{"colspan": 3, "rowspan": 4}, None, None, {"colspan": 3, "rowspan": 4}, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [{"colspan": 3, "rowspan": 1}, None, None, {"colspan": 3, "rowspan": 1}, None, None],
            [{"colspan": 2, "rowspan": 4}, None, {"colspan": 2, "rowspan": 4}, None, {"colspan": 2, "rowspan": 4}, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
        ],
        subplot_titles=subplot_titles,
        vertical_spacing = 0.11,
        horizontal_spacing=0.15,
    )

    fig['layout']['xaxis']['title'] = '<b># pools</b>'
    fig['layout']['yaxis']['title'] = f'<b>{metric.upper()}</b>'
    fig['layout']['yaxis']['type'] = 'log' if log_y1 else fig['layout']['yaxis']['type']

    fig['layout']['xaxis2']['title'] = '<b># pools</b>'
    fig['layout']['yaxis2']['title'] = f'<b>{metric.upper()}</b>'
    fig['layout']['yaxis2']['type'] = 'log' if log_y2 else fig['layout']['yaxis2']['type']

    fig['layout']['xaxis5']['title'] = '<b>% sparsity</b>'
    fig['layout']['yaxis5']['title'] = f'<b>{metric.upper()}</b>'

    fig['layout']['xaxis6']['title'] = '<b># pools/1024</b>'
    fig['layout']['yaxis6']['title'] = '<b>% sparsity</b>'

    fig['layout']['xaxis7']['title'] = '<b># pools/1024</b>'
    fig['layout']['yaxis7']['title'] = '<b>% sparsity</b>'

    fig.update_xaxes(showline=True, linewidth=4, linecolor='black', tickfont=dict(size=22), tickprefix="<b>",ticksuffix ="</b>", title_standoff=0)
    fig.update_yaxes(showline=True, linewidth=4, linecolor='black', tickfont=dict(size=22), tickprefix="<b>",ticksuffix ="</b>", title_standoff=0)

    fig.update_layout(plot_bgcolor = "white")
    fig.update_layout(height=900, width=1500, title_text=title_text, font=dict(size=20))
    fig.update_layout(coloraxis=dict(colorbar_x=0.616, colorbar_y=0.278, colorbar_thickness=23, colorbar_len=0.365, colorscale=get_color_continuous_scale(metric)))
    fig.update_layout(coloraxis2=dict(colorbar_x=1, colorbar_y=0.278, colorbar_thickness=23, colorbar_len=0.365, colorscale=get_color_continuous_scale('probability')))
    
    
    fig.for_each_annotation(lambda a: a.update(text=f'<b>{a.text}</b>'))
    fig.update_annotations(font=dict(family="Helvetica", size=24))

    # Add subplot letters
    letters = ['a.', 'b.', 'c.', 'd.', 'e.']
    x_positions = [-0.02, 0.55, -0.02, 0.35, 0.72]
    y_positions = [1.05, 1.05, 0.48, 0.48, 0.48]
    
    for letter, x, y in zip(letters, x_positions, y_positions):
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=x,
            y=y,
            text=f"<b>{letter}</b>",
            showarrow=False,
            font=dict(size=28, color="black"),
            align="right",
            xanchor="left",
            yanchor="bottom",
        )


    return fig

def render_by_sparse_level(df, metric, sparsity_ratio1, sparsity_ratio2, num_of_pools, log_y1=True, log_y2=True, title_text='', n=1024):
    sparsity_prec1 = int(sparsity_ratio1 * 100)
    sparsity_prec2 = int(sparsity_ratio2 * 100)
    subplot_titles=(
        f"~{sparsity_prec1}% non-zero elements", 
        f"~{sparsity_prec2}% non-zero elements",
        "", 
        "" , 
        f"{num_of_pools} pools", 
        "MSE", "confidence score", 
        "", 
        "", 
        ""
    )

    fig = render_subplot_layout(metric, subplot_titles, log_y1, log_y2, title_text)

    render_solver_by_pools(fig, row=1, col=1, df=df, metric=metric, sparsity_ratio=sparsity_ratio1, log_y=True)
    render_solver_by_pools(fig, row=1, col=4, df=df, metric=metric, sparsity_ratio=sparsity_ratio2, log_y=True, showlegend=False)
    render_solver_by_sparsenees(fig, row=6, col=1, metric=metric, num_of_pools=num_of_pools, df=df, n=n)
    render_heatmap(fig, row=6, col=3, coloraxis='coloraxis', df=df, metric=metric, n=n)
    render_confidence_heatmap(fig, row=6, col=5, coloraxis='coloraxis2', df=df, n=n)

    return fig

def render_by_ethnicity_num(df, metric, ethnicity_names, ethnicities_to_full_name_mapping, ethnicity_num1, ethnicity_num2, num_of_pools, log_y1=True, log_y2=True, title_text='', n=1024):
    subplot_titles=(
        f"Ethnicity {ethnicities_to_full_name_mapping[ethnicity_names[ethnicity_num1]]}", 
        f"Ethnicity {ethnicities_to_full_name_mapping[ethnicity_names[ethnicity_num2]]}",
        "", 
        "" , 
        f"{num_of_pools} pools", 
        "MSE", "Confidence score", 
        "", 
        "", 
        ""
    )

    fig = render_subplot_layout(metric, subplot_titles, log_y1, log_y2, title_text)

    render_solver_by_pools(fig, row=1, col=1, df=df, metric=metric, ethnicity_num=ethnicity_num1, log_y=True)
    render_solver_by_pools(fig, row=1, col=4, df=df, metric=metric, ethnicity_num=ethnicity_num2, log_y=True, showlegend=False)
    render_solver_by_sparsenees(fig, row=6, col=1, metric=metric, num_of_pools=num_of_pools, df=df, n=n)
    render_heatmap(fig, row=6, col=3, coloraxis='coloraxis', df=df, metric=metric, n=n)
    render_confidence_heatmap(fig, row=6, col=5, coloraxis='coloraxis2', df=df, n=n)

    fig.show()


def render_super_pop_exp_chart(df, metric, title_text='', n=1024):
    fig = render_subplot_layout(metric, title_text)

    render_solver_by_pools(fig, row=1, col=1, metric=metric, non_zero=0.01, log_y=True)
    render_solver_by_pools(fig, row=1, col=4, metric=metric, non_zero=0.07, log_y=True, showlegend=False)
    render_solver_by_sparsenees(fig, row=6, col=1, metric=metric, num_of_pools=256, df=df, n=n)
    render_heatmap(fig, row=6, col=3, coloraxis='coloraxis', df=df, metric=metric, n=n)
    render_confidence_heatmap(fig, row=6, col=5, coloraxis='coloraxis2', df=df, n=n)

    fig.show()


def render_simulated_data_chart(df, metric, title_text='', n=1024):
    fig = render_subplot_layout(metric, title_text)

    render_solver_by_pools(fig, row=1, col=1, metric=metric, non_zero=0.01, log_y=True)
    render_solver_by_pools(fig, row=1, col=4, metric=metric, non_zero=0.08, log_y=True, showlegend=False)
    render_solver_by_sparsenees(fig, row=2, col=1, metric=metric, num_of_pools=256, df=df, n=n)
    render_heatmap(fig, row=2, col=3, coloraxis='coloraxis', df=df, metric=metric, n=n)
    render_confidence_heatmap(fig, row=2, col=5, coloraxis='coloraxis2', df=df, n=n)

    fig.show()

def render_error_bar_by_sparsity_ratio(fig, row, col, df, num_of_pools, showlegend=True):
    temp_df = df[(df.name == ETHNICS_SOLVER) & (df.num_of_pools == num_of_pools)]
    fig1 = px.box(temp_df, x='original_sparsity_ratio', y='psnr', color='original_sparsity_ratio')

    for trace in fig1.select_traces():
        trace.showlegend = showlegend
        fig.add_trace(trace, row=row, col=col)
    return fig


def render_grid_error_bar_by_non_zero(df, title_text=''):
    fig = make_subplots(
        rows=4, 
        cols=2, 
        subplot_titles=[f'm={m}' for m in range(64, 513, 64)]
    )

    for idx, m in enumerate(range(64, 513, 64)):
        row = (idx // 2) +1
        col = (idx % 2) + 1

        render_error_bar_by_sparsity_ratio(fig, row, col, df, m, showlegend=idx==0)

        axis_num = '' if idx == 0 else idx + 1
        fig['layout'][f'xaxis{axis_num}']['title'] = 'sparsity'
        fig['layout'][f'yaxis{axis_num}']['title'] = 'PSNR'

    fig.update_layout(height=1200, width=1600, title_text=title_text)
    fig.show()

def render_error_bar_by_num_of_pools(fig, row, col, df, k, showlegend=True):
    temp_df = df[(df.name == ETHNICS_SOLVER) & (df.original_sparsity_ratio == k)]
    fig1 = px.box(temp_df, x='num_of_pools', y='psnr', color='num_of_pools')

    for trace in fig1.select_traces():
        trace.showlegend = showlegend
        fig.add_trace(trace, row=row, col=col)
    return fig


def render_grid_error_bar_by_num_of_pools(df, range=np.arange(0.01, 0.11, 0.01), title_text=''):
    rows = len(range)//2 + len(range)%2

    fig = make_subplots(
        rows=rows, 
        cols=2, 
        subplot_titles=[f'k={round(k, 2)}' for k in range]
    )

    for idx, k in enumerate(range):
        row = (idx // 2) +1
        col = (idx % 2) + 1
        k = round(k, 2)

        render_error_bar_by_num_of_pools(fig, row, col, df, k, showlegend=idx==0)

        axis_num = '' if idx == 0 else idx + 1
        fig['layout'][f'xaxis{axis_num}']['title'] = '# pools'
        fig['layout'][f'yaxis{axis_num}']['title'] = 'PSNR'

    fig.update_layout(height=int(300*rows), width=1600, title_text=title_text)
    fig.show()