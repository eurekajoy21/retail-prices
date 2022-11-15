from enum import unique
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go

st.set_page_config(page_title = "PH Retail")
st.header("Philippine Retail Prices (2012-2021)")

#loading data
goods_annual_df = pd.read_csv("goods_annual.csv", encoding="ISO-8859-1", index_col=0)

#selection
commodities = goods_annual_df['Commodity Type'].unique().tolist()
year = goods_annual_df['Year'].unique().tolist()

with st.sidebar:
    st.write("Filter here:")
    year_slider = st.slider('Year:',
                            min_value=min(year),
                            max_value=max(year),
                            value=(min(year),max(year)), key="year_range")
with st.sidebar:
    commodities_multi = st.multiselect('Commodity Type:',
                                       commodities,
                                       default=commodities, key="select_commodities_val")

#Filtering user selection
mask = (goods_annual_df['Year'].between(*year_slider)) & (goods_annual_df['Commodity Type'].isin(commodities_multi))
mask_year_only = goods_annual_df['Year'].between(*year_slider)
number_of_result = goods_annual_df[mask].shape[0]
st.markdown(f'*Total Results: {number_of_result}*')

#group

df_grouped = goods_annual_df[mask].groupby(by=['Year', 'Commodity Type']).mean()[['Price']].sort_values(by="Year", ascending=True)
df_grouped = df_grouped.reset_index()


#group(year only)
df_grouped_year = goods_annual_df[mask_year_only].groupby(by=['Year', 'Commodity Type']).mean()[['Price']].sort_values(by="Year", ascending=True)
df_grouped_year = df_grouped_year.reset_index()

a1, a2, a3, a4, a5, a6 = st.columns(6)
b1, b2, b3, b4, b5, b6 = st.columns(6)
for com in commodities:
    st.session_state[com] = 0



#Plotting

#col1, col2, col3 = st.columns(3)

scatter_plot = go.Figure()
for com in commodities:
    st.session_state[com+"_price_a"] = 0
    st.session_state[com+"_price_b"] = 0
for key, data in df_grouped.groupby(by='Commodity Type'):
    scatter_plot.add_trace(go.Scatter(x=data['Year'], y=data['Price'], mode='lines+markers', name=key))

for key, data in df_grouped_year.groupby(by="Commodity Type"):
    st.session_state[key] = int(goods_annual_df[(goods_annual_df["Commodity Type"]==key) & (goods_annual_df['Year'].between(int(st.session_state["year_range"][0]), int(st.session_state["year_range"][1])))]["Price"].count())
    dataset = goods_annual_df[(goods_annual_df["Commodity Type"]==key) & (goods_annual_df['Year'].between(int(st.session_state["year_range"][0]), int(st.session_state["year_range"][1])))].sort_values(by="Year")
    ds_year_a_price = dataset[dataset["Year"]==st.session_state["year_range"][0]]["Price"].mean()
    ds_year_b_price = dataset[dataset["Year"]==st.session_state["year_range"][1]]["Price"].mean()
    st.session_state[key+"_price_a"] = ds_year_a_price
    st.session_state[key+"_price_b"] = ds_year_b_price
    #st.plotly_chart(scatter_plot, use_container_width=True)

    scatter_plot.update_layout(
        width=850,
        height=550,
        margin=dict(
            l=0, r=0, t=30, b=30, pad=10
        ),
)
st.write(scatter_plot)


if int(st.session_state["year_range"][0])!=int(st.session_state["year_range"][1]):
    if int(st.session_state[commodities[0]+"_price_a"])!=0:
        a1.metric(commodities[0], "₱"+str(int(st.session_state[commodities[0]+"_price_b"])), str(int(st.session_state[commodities[0]+"_price_b"])-int(st.session_state[commodities[0]+"_price_a"])/int(st.session_state[commodities[0]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a1.metric(commodities[0], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[1]+"_price_a"])!=0:
        a2.metric(commodities[1], "₱"+str(int(st.session_state[commodities[1]+"_price_b"])), str(int(st.session_state[commodities[1]+"_price_b"])-int(st.session_state[commodities[1]+"_price_a"])/int(st.session_state[commodities[1]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a2.metric(commodities[1], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[2]+"_price_a"])!=0:
        a3.metric(commodities[2], "₱"+str(int(st.session_state[commodities[2]+"_price_b"])), str(int(st.session_state[commodities[2]+"_price_b"])-int(st.session_state[commodities[2]+"_price_a"])/int(st.session_state[commodities[2]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a3.metric(commodities[2], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[3]+"_price_a"])!=0:
        a4.metric(commodities[3], "₱"+str(int(st.session_state[commodities[3]+"_price_b"])), str(int(st.session_state[commodities[3]+"_price_b"])-int(st.session_state[commodities[3]+"_price_a"])/int(st.session_state[commodities[3]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a4.metric(commodities[3], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[4]+"_price_a"])!=0:
        a5.metric(commodities[4], "₱"+str(int(st.session_state[commodities[4]+"_price_b"])), str(int(st.session_state[commodities[4]+"_price_b"])-int(st.session_state[commodities[4]+"_price_a"])/int(st.session_state[commodities[4]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a5.metric(commodities[4], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[5]+"_price_a"])!=0:
        a6.metric(commodities[5], "₱"+str(int(st.session_state[commodities[5]+"_price_b"])), str(int(st.session_state[commodities[5]+"_price_b"])-int(st.session_state[commodities[5]+"_price_a"])/int(st.session_state[commodities[5]+"_price_a"]))+"%",delta_color="inverse")
    else:
        a6.metric(commodities[5], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[6]+"_price_a"])!=0:
        b1.metric(commodities[6], "₱"+str(int(st.session_state[commodities[6]+"_price_b"])), str(int(st.session_state[commodities[6]+"_price_b"])-int(st.session_state[commodities[6]+"_price_a"])/int(st.session_state[commodities[6]+"_price_a"]))+"%",delta_color="inverse")
    else:
        b1.metric(commodities[6], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[7]+"_price_a"])!=0:
        b2.metric(commodities[7], "₱"+str(int(st.session_state[commodities[7]+"_price_b"])), str(int(st.session_state[commodities[7]+"_price_b"])-int(st.session_state[commodities[7]+"_price_a"])/int(st.session_state[commodities[7]+"_price_a"]))+"%",delta_color="inverse")
    else:
        b2.metric(commodities[7], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[8]+"_price_a"])!=0:
        b3.metric(commodities[8], "₱"+str(int(st.session_state[commodities[8]+"_price_b"])), str(int(st.session_state[commodities[8]+"_price_b"])-int(st.session_state[commodities[8]+"_price_a"])/int(st.session_state[commodities[8]+"_price_a"]))+"%",delta_color="inverse")
    else:
        b3.metric(commodities[8], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[9]+"_price_a"])!=0:
        b4.metric(commodities[9], "₱"+str(int(st.session_state[commodities[9]+"_price_b"])), str(int(st.session_state[commodities[9]+"_price_b"])-int(st.session_state[commodities[9]+"_price_a"])/int(st.session_state[commodities[9]+"_price_a"]))+"%",delta_color="inverse")
    else:
        b4.metric(commodities[9], "₱"+str(0), str(0)+"%",delta_color="inverse")
    if int(st.session_state[commodities[10]+"_price_a"])!=0:
        b5.metric(commodities[10], "₱"+str(int(st.session_state[commodities[10]])), str(int(st.session_state[commodities[10]+"_price_b"])-int(st.session_state[commodities[10]+"_price_a"])/int(st.session_state[commodities[10]+"_price_a"]))+"%",delta_color="inverse")
    else:
        b5.metric(commodities[10], "₱"+str(0), str(0)+"%",delta_color="inverse")

if len(commodities_multi) > 0:
    df = goods_annual_df

#showing table

#col1, col2, col3 = st.columns(3)
#with col1:
#    st.dataframe(goods_annual_df)
#with col3:    
#    st.dataframe(goods_monthly_df)


                       

