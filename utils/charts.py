import plotly.graph_objects as go
import numpy as np

COLORWAY = ['#6C63FF', '#00B4D8', '#2A9D8F', '#F77F00', '#E63946']

def apply_common_layout(fig):
    fig.update_layout(
        colorway=COLORWAY,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        font=dict(family="Inter, sans-serif")
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=False)
    return fig

def draw_clock(h, m):
    angle_h = np.pi/2 - np.radians(0.5 * (60 * h + m))
    angle_m = np.pi/2 - np.radians(6 * m)

    fig = go.Figure()
    
    # Draw clock face with neutral grey outline
    fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1, line_color="#888888")
    
    # Draw hour ticks
    for i in range(12):
        angle = np.pi/2 - i * np.pi/6
        fig.add_shape(type="line", x0=0.85*np.cos(angle), y0=0.85*np.sin(angle), 
                      x1=1*np.cos(angle), y1=1*np.sin(angle), line=dict(color="#888888", width=3))
                      
    # Hour hand
    fig.add_shape(type="line", x0=0, y0=0, x1=0.5*np.cos(angle_h), y1=0.5*np.sin(angle_h),
                  line=dict(color="#6C63FF", width=6))
    
    # Minute hand
    fig.add_shape(type="line", x0=0, y0=0, x1=0.8*np.cos(angle_m), y1=0.8*np.sin(angle_m),
                  line=dict(color="#00B4D8", width=4))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.2, 1.2]),
        yaxis=dict(visible=False, range=[-1.2, 1.2]),
        width=380, height=380, margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_bar_chart(df, x_col, y_cols, barmode='group'):
    fig = go.Figure()
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Bar(x=df[x_col], y=df[y_col], name=y_col, marker_color=COLORWAY[i % len(COLORWAY)]))
    fig.update_layout(barmode=barmode, title=dict(text=f"{', '.join(y_cols)} by {x_col}", font=dict(size=14)))
    return apply_common_layout(fig)

def create_pie_chart(df, labels_col, values_col, is_donut=False):
    hole = 0.4 if is_donut else 0
    fig = go.Figure(data=[go.Pie(labels=df[labels_col], values=df[values_col], hole=hole, marker=dict(colors=COLORWAY))])
    fig.update_layout(title=dict(text=f"{values_col} distribution", font=dict(size=14)))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=40, b=40), height=380, font=dict(family="Inter, sans-serif"), legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    return fig
    
def create_line_chart(df, x_col, y_cols):
    fig = go.Figure()
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers', name=y_col, line=dict(color=COLORWAY[i % len(COLORWAY)])))
    fig.update_layout(title=dict(text=f"Trend of {', '.join(y_cols)}", font=dict(size=14)))
    return apply_common_layout(fig)

def create_scatter_plot(df, x_col, y_col):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='markers', name='Data Points', marker=dict(color=COLORWAY[0])))
    
    # Trendline
    m, c = np.polyfit(df[x_col], df[y_col], 1)
    fig.add_trace(go.Scatter(x=df[x_col], y=m*df[x_col] + c, mode='lines', name='Trendline', line=dict(color=COLORWAY[1], dash='dash')))
    
    fig.update_layout(title=dict(text=f"{y_col} vs {x_col}", font=dict(size=14)))
    return apply_common_layout(fig)
