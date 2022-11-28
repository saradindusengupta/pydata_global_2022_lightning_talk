import plotly.express as px
import numpy as np
from math import sqrt
from numpy.random import seed
from numpy.random import randint
from random import sample
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings("ignore")




st.set_page_config(page_title="Bessel's Correction", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

def bessel_correction(sample_size, pop_size):
    # Generate population within a range of 0<x<=100000
    seed(1)
    values = list(randint(0, 100000, pop_size))

    var = [0] * 51
    corr = [0] * 51
    n = 0

    # epoch is 300
    while n < 300:
        subset = sample(values, int(sample_size))
        sample_mean = np.mean(subset)
        squared_sum = 0
        for i in range(int(sample_size)):
            squared_sum = squared_sum + (subset[i] - sample_mean) ** 2
        j = 0
        # Initialize Correction factor as -3
        x = -3  
        
        # Iteratively loop through a number of Correction Factors from -3 to 3
        while x < 2.1:  
            var[j] += squared_sum / (sample_size + x)
            corr[j] = x
            x += 0.1
            j += 1
        n += 1
    var_calc = list(map(lambda y: sqrt(y / 300), var))

    # Calculate Population Mean
    pop_mean = np.mean(values)
    squared = 0
    for i in range(pop_size):
        squared = squared + (values[i] - pop_mean) ** 2
    # Calculate Population Standard Deviation
    sd = sqrt(squared / pop_size)

    
    info = pd.DataFrame(columns=['Correction_Factor', 'Variance', 'STD'])
    info['Correction_Factor'] = corr
    info['Variance'] = var
    info['STD'] = var_calc

    table_output = pd.DataFrame(columns=['Sample_Size', 'True_Population_vs_Uncorrected_Standard_deviation', 'True_Population_vs_Unbiased_Standard_deviation'])
    table_output.loc[0] = [int(sample_size), abs(sd - info.loc[31, 'STD']) * 100 / sd, 
                                  abs(sd - info.loc[21, 'STD']) * 100 / sd]

    data = [dict(table_output.loc[0, ])]
    columns = [
        {'name': k.capitalize(), 'id': k}
        for k in list(table_output.columns)
    ]

    fig = px.line(info, x="Correction_Factor", y="STD")

    fig.update_layout(yaxis={'title': "Mean Standard Deviation"},
                      xaxis={'title': "Correction Factor"},
                      shapes=[dict(
            type='line',
            yref='y', y0=sd, y1=sd,
            xref='x', x0=-3, x1=3)],
            margin=dict(l=20, r=20, t=20, b=60),
            paper_bgcolor="LightSteelBlue"
                      )

    # add annotation
    fig.add_annotation(dict(font=dict(color='black',size=13),
                                            x=0,
                                            y=-0.17,
                                            showarrow=False,
                                            text="As the sample size increases, the unbiased standard deviation is closer to uncorrected standard deviation. There is no rule of thumb though to determine when both of them will be same.",
                                            textangle=0,
                                            xanchor='left',
                                            xref="paper",
                                            yref="paper"))
    return(fig, data, columns)

st.title("Bessel's Correction - Lightning Talk at PyData Global 2022")
st.header("Sample Size")
sample_size = st.slider('Sample Size', 100,1000,300)
st.header("Population Size")
pop_size = st.slider('Population Size', 40000,80000,50000)
fig, data, columns = bessel_correction(sample_size, pop_size)
st.subheader("How Uncorrected vs Unbiased Standard Deviation varies with Sample and Population size")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(data, 1200)