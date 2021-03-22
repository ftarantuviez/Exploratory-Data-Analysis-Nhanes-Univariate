import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

import streamlit as st

def nhanes_univariate_analysis(df):
  st.write("The dataframe:")
  st.dataframe(df)
  # Education Level
  st.write(""" 
    ## Education Level
    Below we show the frequency distribution of the [DMDEDUC2](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.htm#DMDEDUC2) variable, which is a variable that reflects a person's level of educational attainment. 
  """)

  col1, col2 = st.beta_columns(2)
  df["DMDEDUC2x"] = df.DMDEDUC2.replace({1: "<9", 2: "9-11", 3: "HS/GED", 4: "Some college/AA", 5: "College", 
                                       7: "Refused", 9: "Don't know"})
  df["RIAGENDRx"] = df.RIAGENDR.replace({1: "Male", 2: "Female"})

  DMDEDUC_freq = pd.DataFrame(df.DMDEDUC2x.value_counts())
  col1.dataframe(DMDEDUC_freq)
  fig, ax = plt.subplots(1)
  ax.pie(labels=DMDEDUC_freq.index, x=DMDEDUC_freq.DMDEDUC2x, autopct="%.2f%%")
  plt.title("Frequency Table Education Label")
  col2.pyplot(fig)

  st.write(""" 
    We can see that most of the people have completed some college, but has not graduated with a four-year degree.
  """)

  # / Education Level

  # Body Weight

  st.write("""
  ## Body Weight
  Below we see the distribution of body weight (in Kg), shown as a histogram. It is evidently the normal distribution with right-skewed.
  """)
  fig = px.histogram(df, x="BMXWT", color="RIAGENDRx", title="Body Weight Distribution")
  st.plotly_chart(fig)
  # / Body Weight

  # Comparing distributions
  rm_na_to_numpy = lambda x: x.dropna().to_numpy()
  st.write(""" 
  ## Comparing Distributions
  To compare several distributions, we can use side-by-side boxplots.  Below we compare the distributions of the first and second systolic blood pressure measurements (BPXSY1, BPXSY2), and the first and second diastolic blood pressure measurements ([BPXDI1](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXDI1), BPXDI2). 
  
  As expected, diastolic measurements are substantially lower than systolic measurements.  Above we saw that the second blood pressure reading on a subject tended on average to be slightly lower than the first measurement.  This difference was less than 1 mm/Hg, so is not visible in the "marginal" distributions shown below.
  """)
  fig = go.Figure()
  fig.update_layout(
    title={
        'text': "Distributions Comparisons"}
    )
  fig.add_trace(go.Box(y=rm_na_to_numpy(df["BPXSY1"]), name="BPXSY1"))
  fig.add_trace(go.Box(y=rm_na_to_numpy(df["BPXSY2"]), name="BPXSY2"))
  fig.add_trace(go.Box(y=rm_na_to_numpy(df["BPXDI1"]), name="BPXDI1"))
  fig.add_trace(go.Box(y=rm_na_to_numpy(df["BPXDI2"]), name="BPXDI2"))
  st.plotly_chart(fig)
  # / Comparing distributions

  # Stratification
  st.write(""" 
  ## Stratification

  We can [partition](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html) the data into age strata, and construct side-by-side boxplots of the systolic blood pressure (SBP) distribution within each stratum.  Since age is a quantitative variable, we need to create a series of "bins" of similar SBP values in order to stratify the data.  Each box in the figure below is a summary of univariate data within a specific population stratum (here defined by age).

  """)
  df["agegrp"] = pd.cut(df.RIDAGEYR, [18, 30, 40, 50, 60, 70, 80]).astype(str)
  fig = alt.Chart(df, title="Age Stratification Blood Pressure Distribution").mark_boxplot().encode(
    x=alt.X('agegrp', axis=alt.Axis(title='Age')),
    y='BPXSY1'
  )
  st.altair_chart(fig, use_container_width=True)

  st.write(""" 
  Taking this a step further, it is also the case that blood pressure tends to differ between women and men.  While we could simply make two side-by-side boxplots to illustrate this contrast, it would be a bit odd to ignore age after already having established that it is strongly associated with blood pressure.  Therefore, we will doubly stratify the data by gender and age.

  We see from the figure below that within each gender, older people tend to have higher blood pressure than younger people.  However within an age band, the relationship between gender and systolic blood pressure is somewhat complex -- in younger people, men have substantially higher blood pressures than women of the same age.  However for people older than 50, this relationship becomes much weaker, and among people older than 70 it appears to reverse. It is also notable that the variation of these distributions, reflected in the height of each box in the boxplot, increases with age.
  """)

  fig = px.box(df, x="agegrp", y="BPXSY1", color="RIAGENDRx",
             notched=True,
             title="Blood Pressure Distribution", 
            )
  st.plotly_chart(fig, use_container_width=True)

  st.write(""" 
  When stratifying on two factors (here age and gender), we can group the boxes first by age, and within age bands by gender, as above, or we can do the opposite -- group first by gender, and then within gender group by age bands. Each approach highlights a different aspect of the data.
  """)
  df_without_agegrp_nan = df[np.logical_not(df.agegrp.isna())]
  fig = px.box(df_without_agegrp_nan, x="RIAGENDRx", y="BPXSY1", color="agegrp",
             title="Blood Pressure Distribution", 
            )
  st.plotly_chart(fig, use_container_width=True)
  # / Stratification

  # Civil Status
  st.write(""" 
  ## Civil Status
  Now we are gonna analyse the civil status of the people in the dataset. In the barplot of below, we can see there are more people of gender male which is actually married. But in comparison in the other civil status, the frequency of the males tends to be slightly less than females one.
  """)

  labels = {1: "Married", 2: "Widowed", 3: "Divorced", 4: "Separated", 5: "Never married", 6: "Living with partner", 77: "Refused"}
  df["DMDMARTL_labels"] = df["DMDMARTL"].replace(labels)
  male_table = pd.DataFrame(df[df["RIAGENDR"] == 1]["DMDMARTL_labels"].value_counts()).reset_index().rename(columns={"index": "status", "DMDMARTL_labels": "count"})
  female_table = pd.DataFrame(df[df["RIAGENDR"] == 2]["DMDMARTL_labels"].value_counts()).reset_index().rename(columns={"index": "status", "DMDMARTL_labels": "count"})
  female_table["gender"] = "Female"
  male_table["gender"] = "Male"
  df_status = pd.concat([female_table, male_table])

  fig = px.bar(df_status, x="status", y="count", color='gender', title="Civil Status Frequency Table")
  fig.update_layout(barmode='group')
  st.plotly_chart(fig)
  # / Civil Status