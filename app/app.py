import plotly.express as px
import numpy as np
from math import sqrt
from numpy.random import seed
from numpy.random import randint
from random import sample
import pandas as pd
import streamlit as st
import warnings
import os
warnings.filterwarnings("ignore")



st.set_page_config(page_title="Validation", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

def build_graph(value):
    # seed random number generator
    seed(1)
    # generate some integers
    values = list(randint(0, 100000, 50000))
    # Declare empty lists to store Variance of the Sample and Correction Factor
    var = [0] * 51
    corr = [0] * 51
    n = 0
    x = 0.1

    # 300 is the number of times a sample of size 'value' is drawn from the population
    while n < 300:
        subset = sample(values, int(value))
        sample_mean = np.mean(subset)
        squared_sum = 0
        for i in range(int(value)):
            squared_sum = squared_sum + (subset[i] - sample_mean) ** 2
        j = 0
        x = -3  # Initialize Correction factor as -3
        
        # Iteratively loop through a number of Correction Factors from -3 to 2
        while x < 2.1:  
            var[j] += squared_sum / (value + x)
            corr[j] = x
            x += 0.1
            j += 1
        n += 1
    var_calc = list(map(lambda y: sqrt(y / 300), var))

    # Calculate Population Mean
    pop_mean = np.mean(values)
    squared = 0
    for i in range(50000):
        squared = squared + (values[i] - pop_mean) ** 2
    # Calculate Population Standard Deviation
    sd = sqrt(squared / 50000)

    # Store results in a dataframest.slider('SoH threshold', 0.60,0.90,0.80)
    info = pd.DataFrame(columns=['Correction_Factor', 'Variance', 'SD'])
    info['Correction_Factor'] = corr
    info['Variance'] = var
    info['SD'] = var_calc

    table_output = pd.DataFrame(columns=['Sample_Size', 'Dev@0', 'Dev@-1'])
    table_output.loc[0] = [int(value), abs(sd - info.loc[31, 'SD']) * 100 / sd, 
                                  abs(sd - info.loc[21, 'SD']) * 100 / sd]

    data = [dict(table_output.loc[0, ])]
    columns = [
        {'name': k.capitalize(), 'id': k}
        for k in list(table_output.columns)
    ]

    fig = px.line(info, x="Correction_Factor", y="SD")

    fig.update_layout(yaxis={'title': 'Mean Standard Deviation'},
                      title={'text': 'Bessel Correction'}, shapes=[dict(
            type='line',
            yref='y', y0=sd, y1=sd,
            xref='x', x0=-3, x1=2
        )])
    return(fig, data, columns)


value = st.slider('SoH threshold', 100,1000,300)
fig, data, columns = build_graph(value)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(data, 1200)