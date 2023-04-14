#dashboard using pilot proj data
#note, this uses pandas to directly import openpyxl

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Pilot", page_icon=":bar_chart:", layout="wide")

#emojis https://www.webfx.com/tools/emoji-cheat-sheet/


df = pd.read_excel(
io = 'dash-p-projects-2017-2021.xlsx',
engine='openpyxl',
sheet_name='data',
usecols='A:P',
nrows = 119,
    )



#print(df)
#st.dataframe(df)

#sidebar w/ filters
st.sidebar.header("Filter Here:")

mechanism = st.sidebar.multiselect(
"Select Mechanism:",
options=df["Mechanism"].unique(),
default=df["Mechanism"].unique()
)

program = st.sidebar.multiselect(
"Select Program:",
options=df["Program"].unique(),
default=df["Program"].unique()
)


year = st.sidebar.multiselect(
"Select Year:",
options=df["Year"].unique(),
default=df["Year"].unique()
)


#those just create sidebar buttons.
#now to add functionality via query

df_selection = df.query("Mechanism == @mechanism & Program == @program & Year == @year")

#st.dataframe(df_selection)

#Main page
st.title(":bar_chart: KUCC Pilot Projects 2017 - 2021")
#st.markdown("##")


#top KPIs


avg_pilot_awards = int(df_selection["PilotAmount"].mean())
avg_external_awards = int(df_selection["TotalGrantAmount"].sum())
avg_roi = round(df_selection["Fold_Increase"].mean(),2)
#stars = ":star:" * ["avg_roi"]

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Avg Pilot Project Award:")
    st.subheader(f"$ {avg_pilot_awards:,}")
with middle_column:
    st.subheader("Avg External Grant Award:")
    st.subheader(f"$ {avg_external_awards:,}")
with right_column:
    st.subheader("Avg Return on Intestment:")
    st.subheader(f"{avg_roi}")


st.markdown("---")


pilot_mech = ( df_selection.groupby(by=["Mechanism"]).sum()[["PilotAmount"]].sort_values(by="PilotAmount")
)

fig_pilot_mech = px.bar(
pilot_mech, x="PilotAmount", y=pilot_mech.index,
orientation="h",
title="<b>Award Amounts by Mechanism</b>",
color_discrete_sequence=["#0083B8"] * len(pilot_mech),
template="plotly_white",
)

#test to view chart
#st.plotly_chart(fig_pilot_mech)


pilot_prog = ( df_selection.groupby(by=["Program"]).sum()[["PilotAmount"]].sort_values(by="PilotAmount")
)

fig_pilot_prog = px.bar(
pilot_prog,
x=pilot_prog.index,
y="PilotAmount",
title="<b>Award Amounts by Program</b>",
color_discrete_sequence=["#76c68f"] * len(pilot_prog),
template="plotly_white",
)

fig_pilot_prog.update_layout(
xaxis=dict(tickmode="linear"),
#plot_bgcolor="rgb(255,255,255)",
yaxis=(dict(showgrid=False)),
)

#test to view chart
#st.plotly_chart(fig_pilot_prog)

#align both charts horizontally
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pilot_mech, use_container_width=True)
right_column.plotly_chart(fig_pilot_prog, use_container_width=True)

#hide streamlit style items via CSS
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
