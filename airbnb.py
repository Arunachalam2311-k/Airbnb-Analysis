import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image



st.title("AirBnb-Analysis")


select = option_menu(
    menu_title=None,
    options=['Home','analysis','contact'],
    icons=['house','bar-chart','at'],
    default_index=2,
    orientation='horizontal',

)

#----------------------------/ Home \-----------------------

if select == "Home":

    st.header('Airbnb Analysis')
    st.subheader('Airbnb is a platform that allows people to rent out their homes, apartments, or other accommodations to guests. It also provides a way for travelers to find and book lodging. Users can list their properties, communicate with guests, and manage bookings through the platform. Airbnb operates worldwide and offers a range of accommodations, from single rooms to entire homes.')
    st.subheader('Skills take away from this project :')
    st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
    st.subheader('Domain :')
    st.subheader('Travel Industry, Property management and Tourism')


# ---------------------/ Explore Data \-----------------------

if select == "analysis":
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx","json"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding="ISO-8859-1")
    else:
        st.write("Please Choose A File Above For Visualization")

    st.sidebar.header("Choose your filter: ")



    try:


        # Assuming df is your DataFrame containing Airbnb data

        # Country selection in the sidebar
        country = st.sidebar.selectbox("Pick your country", ["All"] + list(df["country"].unique()))

        # Filter DataFrame based on selected country
        if country == "All":
            df_filtered = df.copy()
        else:
            df_filtered = df[df["country"] == country]

        # City selection in the sidebar based on the filtered DataFrame
        city = st.sidebar.selectbox("Pick the city", ["All"] + list(df_filtered["city"].unique()))

        # Filter DataFrame based on selected city
        if city != "All":
            df_filtered = df_filtered[df_filtered["city"] == city]

        # Property type selection in the sidebar
        property_types = st.sidebar.multiselect("Pick property types", df_filtered["property_type"].unique(), default=df_filtered["property_type"].unique())

        # Filter DataFrame based on selected property types
        if property_types:
            df_filtered = df_filtered[df_filtered["property_type"].isin(property_types)]

        # Price range selection in the sidebar
        price_range = st.sidebar.slider("Price range", min_value=int(df_filtered["price in $"].min()), 
                                        max_value=int(df_filtered["price in $"].max()),
                                        value=(int(df_filtered["price in $"].min()), int(df_filtered["price in $"].max())))

        # Filter DataFrame based on selected price range
        df_filtered = df_filtered[(df_filtered["price in $"] >= price_range[0]) & (df_filtered["price in $"] <= price_range[1])]

        # Display filtered data
        st.write("Filtered Data")
        st.dataframe(df_filtered)

        # Create a scatter plot
        scatter_plot = px.scatter(df_filtered, x="property_type", y="price in $", color="room_type")

        # Update the layout
        scatter_plot.update_layout(
            title="Room Type in Property Type and Price-wise Data Using Scatter Plot",
            titlefont=dict(size=20),
            xaxis=dict(title="Property Type", titlefont=dict(size=20)),
            yaxis=dict(title="Price in $", titlefont=dict(size=20))
        )

        # Display the plot
        st.plotly_chart(scatter_plot, use_container_width=True)

        # Calculate the number of reviews per property type
        df_reviews = df_filtered.groupby('property_type')['review_scores'].sum().reset_index()

        # Display Airbnb Property Reviews Pie Chart
        st.title('Airbnb Property Reviews Pie Chart')

        # Create a Pie chart
        fig = px.pie(df_reviews, values='review_scores', names='property_type', title='Reviews by Property Type')
        fig.update_layout(width=400, height=400)
        # Display the Pie chart in Streamlit
        st.plotly_chart(fig)

        # Define the data for the funnel chart
        funnel_data = dict(
            number=[df_filtered['availability_30'].sum(), df_filtered['availability_60'].sum(),
                    df_filtered['availability_90'].sum(), df_filtered['availability_365'].sum()],
            stage=['availability_30', 'availability_60', 'availability_90', 'availability_365']
        )

        # Create the funnel chart
        fig_funnel = px.funnel(funnel_data, x='number', y='stage', title="Property Availability Funnel Chart")

        # Display the funnel chart
        st.plotly_chart(fig_funnel, use_container_width=True)



    except:
        pass

# ---------------------------------/ contact \------------------


if select == "contact":


    # Load an image from a file
    image = Image.open("D:\project3\download.png")

    # Display the image
    st.image(image, caption="Sample Image", use_column_width=True)


    st.write("For more details, visit [Airbnb](https://www.airbnb.co.in/)")


    st.write("Thanks for visiting.....")

