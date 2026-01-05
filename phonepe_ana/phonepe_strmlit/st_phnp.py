
import streamlit as st
import numpy as np
import pandas as pd
import psycopg2
import os
import plotly.express as px
from sqlalchemy import create_engine


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="phonepe_data",
        user="postgres",
        password="Greybentley@123",
        port="5432"
    )

connect = get_connection()
cursor = connect.cursor()
connect.autocommit = True



@st.cache_data
def load_data():
    agg_trans = pd.read_sql("SELECT * FROM agg_trans;", connect)
    agg_ins = pd.read_sql("SELECT * FROM agg_ins;", connect)
    agg_user = pd.read_sql("SELECT * FROM agg_user;", connect)

    map_trans = pd.read_sql("SELECT * FROM map_trans;", connect)
    map_ins = pd.read_sql("SELECT * FROM map_ins;", connect)
    map_user_list = pd.read_sql("SELECT * FROM map_user_list;", connect)

    top_trans = pd.read_sql("SELECT * FROM top_trans;", connect)
    top_ins = pd.read_sql("SELECT * FROM top_ins;", connect)
    top_user_list = pd.read_sql("SELECT * FROM top_user_list;", connect)

    return (
        agg_trans, agg_ins, agg_user,
        map_trans, map_ins, map_user_list,
        top_trans, top_ins, top_user_list
    )




st.set_page_config(page_title="PhonePe Pulse", layout="wide")

st.markdown(
    """
    <style>
        body { background-color: #ffffff; color: #212529; }
        .sidebar .sidebar-content { background-color: #f8f9fa; }
        h1 { color: #2c3e50; }
        .big-title { font-size: 2rem; font-weight: bold; }
        .highlight { color: #e74c3c; }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Business Case Study"])

#Home Page
if page == "Home":

    st.title("PhonePe Pulse Data Analysis")

    st.markdown("""
    ### 📌 Project Overview

    I built this project as an end-to-end data analysis and visualization application using **PhonePe Pulse open data**.  
    The goal of the project is to analyze large-scale digital transaction data and extract meaningful insights related to **user behavior, transaction patterns, insurance adoption, and regional growth trends across India**.

    ---

    ### 📊 What I Analyzed

    The project is structured around five real-world business scenarios:

    - **Decoding Transaction Dynamics on PhonePe**  
    I analyzed how different transaction types contribute across states, quarters, and years to understand transaction composition and trends.

    - **Insurance Penetration and Growth Potential Analysis**  
    I studied insurance transaction data to identify adoption patterns and growth opportunities across regions.

    - **User Engagement & Growth**  
    I examined transaction counts and transaction values to understand how user engagement has evolved over time.

    - **Insurance Engagement**  
    I analyzed user interaction with insurance services to measure engagement levels across states and time periods.

    - **User Registration Analysis**  
    I evaluated user registration and app usage data to identify growth patterns and regional adoption trends.

    ---

    ### 🛠️ How I Built the Project

    - I extracted raw data from the **PhonePe Pulse GitHub repository**, where the data was available in JSON format.
    - I cleaned, transformed, and structured the data using **Python (Pandas)**.
    - I stored the processed data in **PostgreSQL** to enable efficient querying and analysis.
    - I wrote all analytical queries using **SQL**.
    - I created interactive visualizations using **Plotly**.
    - I developed the complete dashboard using **Streamlit**, integrating both the UI and analytical logic in a single application.

    ---

    ### 🎯 Key Highlights

    - I implemented multiple visualization techniques, including **bar plots, stacked charts, line plots, area plots, scatter plots, and choropleth maps**.
    - The analysis is driven by **business-oriented questions**, not just descriptive statistics.
    - The dashboard is designed to be interactive, scalable, and easy to interpret.

    ---

    This project demonstrates my ability to work with real-world data, perform end-to-end data analysis, and present insights through an interactive and professional dashboard.
    """)





# Business studies page
elif page == "Business Case Study":
    st.title("Business Case Study")
    st.subheader("Select a Scenario")
    
    scenario = st.selectbox(
            "Choose a scenario",
            [
                "Decoding Transaction Dynamics on PhonePe",
                "Insurance Penetration and Growth Potential Analysis",
                "User Engagement & Growth",
                "Insurance Engagement",
                "User Registration Analysis"
            ]
        )



    # First Scenario: Decoding Transaction Dynamics on PhonePe
    if scenario == "Decoding Transaction Dynamics on PhonePe":

        st.markdown(
            "<div class='section-title'>Total Transaction Amount Analysis</div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

###########
        with col1:
            years_df = pd.read_sql(
                'SELECT DISTINCT "Year" FROM agg_trans ORDER BY "Year"',
                connect
            )

            year_selected = st.selectbox(
                "Year",
                years_df["Year"].astype(int).unique()
            )

        # ---------- QUARTER ----------
        with col2:
            quarter = st.selectbox(
                "Quarter",
                sorted(
                    pd.read_sql(
                        'SELECT DISTINCT "Quater" FROM agg_trans ORDER BY "Quater"',
                        connect
                    )["Quater"]
                )
            )

        # ---------- MAP ----------
        query = f"""
            SELECT
                "State" AS state,
                SUM("Transaction_amount") AS total_transaction_value
            FROM agg_trans
            WHERE "Year" = {year_selected}
            AND "Quater" = {quarter}
            GROUP BY "State";
        """

        df = pd.read_sql(query, connect)

        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="state",
            color="total_transaction_value",
            color_continuous_scale="Blues",
            hover_name="state",
            hover_data={"total_transaction_value": ":,.0f"}
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=520)

        st.plotly_chart(fig, use_container_width=True)

        # ---------- PAYMENT METHOD POPULARITY ----------
        st.markdown(
            "<div class='section-title'>Payment Method Popularity</div>",
            unsafe_allow_html=True
        )

        query_method = f"""
            SELECT
                "Transaction_type",
                SUM("Transaction_count") AS total_transactions,
                SUM("Transaction_amount") AS total_amount
            FROM agg_trans
            WHERE "Year" = {year_selected}
            AND "Quater" = {quarter}
            GROUP BY "Transaction_type"
            ORDER BY total_transactions DESC;
        """

        df_method = pd.read_sql(query_method, connect)

        col1, col2 = st.columns(2)

        # ---- PIE: COUNT ----
        with col1:
            fig_count = px.pie(
                df_method,
                names="Transaction_type",
                values="total_transactions",
                title="Distribution of Total Transaction Count",
                hole=0.55
            )
            fig_count.update_traces(textinfo="percent")
            st.plotly_chart(fig_count, use_container_width=True)

        # ---- PIE: AMOUNT (FILTERED) ----
        df_amount_pie = df_method[df_method["total_amount"] > 0]

        with col2:
            fig_amount = px.pie(
                df_amount_pie,
                names="Transaction_type",
                values="total_amount",
                title="Distribution of Total Transaction Amount",
                hole=0.55
            )
            st.plotly_chart(fig_amount, use_container_width=True)

        # ---------- TOP 10 STATES ----------
        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Top 10 State-wise Total Transaction Amount</h2>",
            unsafe_allow_html=True
        )

        query_top_states = f"""
            SELECT
                "State",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_trans
            WHERE "Year" = {year_selected}
            AND "Quater" = {quarter}
            GROUP BY "State"
            ORDER BY total_transaction_amount DESC
            LIMIT 10;
        """

        df_top_states = pd.read_sql(query_top_states, connect)

        fig_top_states = px.bar(
            df_top_states,
            x="State",
            y="total_transaction_amount",
            text_auto=".2s",
            color_discrete_sequence=["#0d6efd"]
        )

        fig_top_states.update_layout(height=500)
        st.plotly_chart(fig_top_states, use_container_width=True)

        # ---------- STATE-WISE CATEGORY ----------
        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Transactions by State and Payment Category</h2>",
            unsafe_allow_html=True
        )

        states = sorted(
            pd.read_sql(
                'SELECT DISTINCT "State" FROM agg_trans ORDER BY "State"',
                connect
            )["State"]
        )

        selected_state = st.selectbox("Select a State", states)

        query_state_category = f"""
            SELECT
                "Transaction_type",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_trans
            WHERE "State" = '{selected_state}'
            AND "Year" = {year_selected}
            AND "Quater" = {quarter}
            GROUP BY "Transaction_type"
            ORDER BY total_transaction_amount DESC;
        """

        df_state_category = pd.read_sql(query_state_category, connect)

        fig_state_category = px.line(
            df_state_category,
            x="Transaction_type",
            y="total_transaction_amount",
            markers=True
        )

        st.plotly_chart(fig_state_category, use_container_width=True)

        # ---------- TREND ANALYSIS ----------
        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Trend Analysis</h2>",
            unsafe_allow_html=True
        )

        trend_year = st.selectbox(
            "Select a Year",
            years_df["Year"].astype(int).unique()
        )

        query_trend = f"""
            SELECT
                "Quater" AS quarter,
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_trans
            WHERE "Year" = {trend_year}
            GROUP BY "Quater"
            ORDER BY "Quater";
        """

        df_trend = pd.read_sql(query_trend, connect)

        fig_trend = px.bar(
            df_trend,
            x="quarter",
            y="total_transaction_amount",
            text_auto=".2s",
            color_discrete_sequence=["#87CEEB"]
        )

        st.plotly_chart(fig_trend, use_container_width=True)

        # ---------- STACKED BAR & RELATIVE STACKED BAR ----------
        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Transaction Composition (Stacked Bar)</h2>",
            unsafe_allow_html=True
        )

        query_stacked = f"""
            SELECT
                "Quater",
                "Transaction_type",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_trans
            WHERE "Year" = {year_selected}
            GROUP BY "Quater", "Transaction_type"
            ORDER BY "Quater";
        """

        df_stacked = pd.read_sql(query_stacked, connect)

        fig_stacked = px.bar(
            df_stacked,
            x="Quater",
            y="total_transaction_amount",
            color="Transaction_type",
            title=f"Transaction Composition by Quarter – {year_selected}",
            barmode="stack"
        )

        fig_stacked.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Transaction Amount",
            height=500
        )

        st.plotly_chart(fig_stacked, use_container_width=True)


        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Transaction Mix (%)</h2>",
            unsafe_allow_html=True
        )

        # RELATIVE STACKED BAR BLOCK
        df_relative = (
            df_stacked
            .groupby(["Quater", "Transaction_type"], as_index=False)
            .agg({"total_transaction_amount": "sum"})
        )

        df_relative["percentage"] = (
            df_relative["total_transaction_amount"] /
            df_relative.groupby("Quater")["total_transaction_amount"].transform("sum")
        ) * 100

        fig_relative = px.bar(
            df_relative,
            x="Quater",
            y="percentage",
            color="Transaction_type",
            barmode="stack",
            title=f"Transaction Mix Percentage by Quarter – {year_selected}"
        )

        fig_relative.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Percentage (%)",
            yaxis=dict(ticksuffix="%"),
            height=500
        )

        st.plotly_chart(fig_relative, use_container_width=True)



    # Second Scenario: Insurance Penetration and Growth Potential Analysis
    elif scenario == "Insurance Penetration and Growth Potential Analysis":

        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Insurance Penetration and Growth Potential Analysis</h2>",
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)

        with col1:
            years_df = pd.read_sql(
                'SELECT DISTINCT "Year" FROM agg_ins ORDER BY "Year"',
                connect
            )

            year_selected = st.selectbox(
                "Select Year",
                years_df["Year"].astype(int)
            )

        with col2:
            quarter_selected = st.selectbox(
                "Select Quarter",
                sorted(
                    pd.read_sql(
                        'SELECT DISTINCT "Quater" FROM agg_ins ORDER BY "Quater"',
                        connect
                    )["Quater"]
                )
            )



        st.markdown(
            "<h3 style='color:#2980b9;'>Insurance Growth Trend (Year-wise)</h3>",
            unsafe_allow_html=True
        )

        query_growth = """
            SELECT
                "Year",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_ins
            GROUP BY "Year"
            ORDER BY "Year";
        """

        df_growth = pd.read_sql(query_growth, connect)

        fig_growth = px.line(
            df_growth,
            x="Year",
            y="total_transaction_amount",
            markers=True,
            title="Year-wise Insurance Transaction Growth"
        )

        fig_growth.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Transaction Amount",
            height=450
        )

        st.plotly_chart(fig_growth, use_container_width=True)


        # (YEAR + QUARTER)


        st.markdown(
            "<h3 style='color:#2980b9;'>Top 10 States by Insurance Transaction Amount</h3>",
            unsafe_allow_html=True
        )

        query_top_states = f"""
            SELECT
                "State",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_ins
            WHERE "Year" = {year_selected}
            AND "Quater" = {quarter_selected}
            GROUP BY "State"
            ORDER BY total_transaction_amount DESC
            LIMIT 10;
        """

        df_top_states = pd.read_sql(query_top_states, connect)

        fig_top_states = px.bar(
            df_top_states,
            x="State",
            y="total_transaction_amount",
            text_auto=".2s",
            title=f"Top 10 States – Insurance Transactions ({year_selected} Q{quarter_selected})",
            color_discrete_sequence=["#0d6efd"]
        )

        fig_top_states.update_layout(
            xaxis_title="State",
            yaxis_title="Transaction Amount",
            height=450
        )

        st.plotly_chart(fig_top_states, use_container_width=True)

    ################

        st.markdown(
            "<h3 style='color:#2980b9;'>Quarter-wise Insurance Trend</h3>",
            unsafe_allow_html=True
        )

        query_quarter_trend = f"""
            SELECT
                "Quater",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_ins
            WHERE "Year" = {year_selected}
            GROUP BY "Quater"
            ORDER BY "Quater";
        """

        df_quarter_trend = pd.read_sql(query_quarter_trend, connect)

        fig_quarter = px.bar(
            df_quarter_trend,
            x="Quater",
            y="total_transaction_amount",
            title=f"Quarter-wise Insurance Transactions – {year_selected}",
            text_auto=".2s",
            color_discrete_sequence=["#87CEEB"]
        )

        fig_quarter.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Transaction Amount",
            height=450
        )

        st.plotly_chart(fig_quarter, use_container_width=True)

    ##############

        st.markdown(
            "<h3 style='color:#2980b9;'>State-wise Insurance Analysis</h3>",
            unsafe_allow_html=True
        )

        states = sorted(
            pd.read_sql(
                'SELECT DISTINCT "State" FROM agg_ins ORDER BY "State"',
                connect
            )["State"]
        )

        selected_state = st.selectbox("Select a State", states)

        query_state_trend = f"""
            SELECT
                "Quater",
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_ins
            WHERE "State" = '{selected_state}'
            AND "Year" = {year_selected}
            GROUP BY "Quater"
            ORDER BY "Quater";
        """

        df_state_trend = pd.read_sql(query_state_trend, connect)

        fig_state = px.line(
            df_state_trend,
            x="Quater",
            y="total_transaction_amount",
            markers=True,
            title=f"Insurance Trend in {selected_state} – {year_selected}"
        )

        fig_state.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Transaction Amount",
            height=450
        )

        st.plotly_chart(fig_state, use_container_width=True)


    # Third Scenario: User Engagement & Growth

    elif scenario == "User Engagement & Growth":
        st.header("User Engagement & Growth")

        # ====================================================
        # FILTERS
        # ====================================================
        col_eng_1, col_eng_2 = st.columns(2)

        with col_eng_1:
            eng_year_df = pd.read_sql(
                'SELECT DISTINCT "Year" FROM agg_trans ORDER BY "Year"',
                connect
            )

            eng_year_selected = st.selectbox(
                "Select Year",
                eng_year_df["Year"].astype(int)
            )

        with col_eng_2:
            eng_quarter_selected = st.selectbox(
                "Select Quarter",
                sorted(
                    pd.read_sql(
                        'SELECT DISTINCT "Quater" FROM agg_trans ORDER BY "Quater"',
                        connect
                    )["Quater"].astype(int)
                )
            )

        # ====================================================
        # 1️⃣ LINE PLOT (COVID-STYLE TIME SERIES)
        # ====================================================
        st.subheader("Overall User Engagement Growth")

        query_eng_line = """
            SELECT
                "Year",
                SUM("Transaction_count") AS total_transactions
            FROM agg_trans
            GROUP BY "Year"
            ORDER BY "Year";
        """

        df_eng_line = pd.read_sql(query_eng_line, connect)

        fig_eng_line = px.line(
            df_eng_line,
            x="Year",
            y="total_transactions",
            markers=True,
            title="Total Transaction Count Over Years"
        )

        fig_eng_line.update_layout(
            xaxis_title="Year",
            yaxis_title="Transaction Count",
            height=450
        )

        st.plotly_chart(fig_eng_line, use_container_width=True)

        # ====================================================
        # 2️⃣ STACKED AREA PLOT (ENGAGEMENT GROWTH)
        # ====================================================
        st.subheader("Engagement Growth by Transaction Type")

        query_eng_area = """
            SELECT
                "Year",
                "Transaction_type",
                SUM("Transaction_count") AS total_transactions
            FROM agg_trans
            GROUP BY "Year", "Transaction_type"
            ORDER BY "Year";
        """

        df_eng_area = pd.read_sql(query_eng_area, connect)

        fig_eng_area = px.area(
            df_eng_area,
            x="Year",
            y="total_transactions",
            color="Transaction_type",
            title="Stacked Area: Engagement Growth by Transaction Type"
        )

        fig_eng_area.update_layout(
            xaxis_title="Year",
            yaxis_title="Transaction Count",
            height=500
        )

        st.plotly_chart(fig_eng_area, use_container_width=True)

        # ====================================================
        # 3️⃣ BAR PLOT (STATE ENGAGEMENT FOR SELECTED YEAR/Q)
        # ====================================================
        st.subheader("Top States by User Engagement")

        query_eng_state_bar = f"""
            SELECT
                "State",
                SUM("Transaction_count") AS total_transactions
            FROM agg_trans
            WHERE "Year" = {eng_year_selected}
            AND "Quater" = {eng_quarter_selected}
            GROUP BY "State"
            ORDER BY total_transactions DESC
            LIMIT 10;
        """

        df_eng_state_bar = pd.read_sql(query_eng_state_bar, connect)

        fig_eng_bar = px.bar(
            df_eng_state_bar,
            x="State",
            y="total_transactions",
            title=f"Top 10 States by Engagement ({eng_year_selected} Q{eng_quarter_selected})",
            text_auto=".2s",
            color_discrete_sequence=["#0d6efd"]
        )

        fig_eng_bar.update_layout(
            xaxis_title="State",
            yaxis_title="Transaction Count",
            height=500
        )

        st.plotly_chart(fig_eng_bar, use_container_width=True)

        # ====================================================
        # 4️⃣ SCATTER PLOT (CONTINUOUS vs CONTINUOUS)
        # ====================================================
        st.subheader("Engagement vs Transaction Value")

        query_eng_scatter = """
            SELECT
                "State",
                SUM("Transaction_count") AS total_transaction_count,
                SUM("Transaction_amount") AS total_transaction_amount
            FROM agg_trans
            GROUP BY "State";
        """

        df_eng_scatter = pd.read_sql(query_eng_scatter, connect)

        fig_eng_scatter = px.scatter(
            df_eng_scatter,
            x="total_transaction_count",
            y="total_transaction_amount",
            size="total_transaction_amount",
            hover_name="State",
            title="Scatter Plot: Engagement vs Transaction Value",
        )

        fig_eng_scatter.update_layout(
            xaxis_title="Total Transaction Count",
            yaxis_title="Total Transaction Amount",
            height=550
        )

        st.plotly_chart(fig_eng_scatter, use_container_width=True)




    # Fourth Scenario: Insurance Engagement
    elif scenario == "Insurance Engagement":

        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>Insurance Engagement Analysis</h2>",
            unsafe_allow_html=True
        )

    #########################

        col1, col2 = st.columns(2)

        with col1:
            years_df = pd.read_sql(
                'SELECT DISTINCT "Year" FROM agg_ins ORDER BY "Year"',
                connect
            )

            year_selected = st.selectbox(
                "Select Year",
                years_df["Year"].astype(int)
            )

        with col2:
            quarter_selected = st.selectbox(
                "Select Quarter",
                sorted(
                    pd.read_sql(
                        'SELECT DISTINCT "Quater" FROM agg_ins ORDER BY "Quater"',
                        connect
                    )["Quater"]
                )
            )

    ####################

        st.markdown(
            "<h3 style='color:#2980b9;'>Year-wise Insurance Engagement</h3>",
            unsafe_allow_html=True
        )

        query_year_engagement = """
            SELECT
                "Year",
                SUM("Transaction_count") AS total_transactions
            FROM agg_ins
            GROUP BY "Year"
            ORDER BY "Year";
        """

        df_year_engagement = pd.read_sql(query_year_engagement, connect)

        fig_year = px.line(
            df_year_engagement,
            x="Year",
            y="total_transactions",
            markers=True,
            title="Insurance Engagement Growth Over Years"
        )

        fig_year.update_layout(
            xaxis_title="Year",
            yaxis_title="Transaction Count",
            height=450
        )

        st.plotly_chart(fig_year, use_container_width=True)

    #######################

        st.markdown(
            "<h3 style='color:#2980b9;'>Top States by Insurance Engagement</h3>",
            unsafe_allow_html=True
        )

        query_top_states = f"""
            SELECT
                "State",
                SUM("Transaction_count") AS total_transactions
            FROM agg_ins
            WHERE "Year" = {year_selected}
            AND "Quater" = {quarter_selected}
            GROUP BY "State"
            ORDER BY total_transactions DESC
            LIMIT 10;
        """

        df_top_states = pd.read_sql(query_top_states, connect)

        fig_states = px.bar(
            df_top_states,
            x="State",
            y="total_transactions",
            text_auto=".2s",
            title=f"Top 10 States – Insurance Engagement ({year_selected} Q{quarter_selected})",
            color_discrete_sequence=["#20c997"]
        )

        fig_states.update_layout(
            xaxis_title="State",
            yaxis_title="Transaction Count",
            height=450
        )

        st.plotly_chart(fig_states, use_container_width=True)

    #######################

        st.markdown(
            "<h3 style='color:#2980b9;'>State-wise Insurance Engagement Trend</h3>",
            unsafe_allow_html=True
        )

        states = sorted(
            pd.read_sql(
                'SELECT DISTINCT "State" FROM agg_ins ORDER BY "State"',
                connect
            )["State"]
        )

        selected_state = st.selectbox("Select a State", states)

        query_state_trend = f"""
            SELECT
                "Quater",
                SUM("Transaction_count") AS total_transactions
            FROM agg_ins
            WHERE "State" = '{selected_state}'
            AND "Year" = {year_selected}
            GROUP BY "Quater"
            ORDER BY "Quater";
        """

        df_state_trend = pd.read_sql(query_state_trend, connect)

        fig_state = px.line(
            df_state_trend,
            x="Quater",
            y="total_transactions",
            markers=True,
            title=f"Insurance Engagement in {selected_state} – {year_selected}"
        )

        fig_state.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Transaction Count",
            height=450
        )

        st.plotly_chart(fig_state, use_container_width=True)



    elif scenario == "User Registration Analysis":

        st.markdown(
            "<h2 style='color:#e74c3c; text-align:center;'>User Registration Analysis</h2>",
            unsafe_allow_html=True
        )

    #####

        col_reg_1, col_reg_2 = st.columns(2)

        with col_reg_1:
            reg_year_df = pd.read_sql(
                'SELECT DISTINCT "Year" FROM map_user_list ORDER BY "Year"',
                connect
            )

            reg_year_selected = st.selectbox(
                "Select Year",
                reg_year_df["Year"].astype(int)
            )

        with col_reg_2:
            reg_quarter_selected = st.selectbox(
                "Select Quarter",
                sorted(
                    pd.read_sql(
                        'SELECT DISTINCT "Quarter" FROM map_user_list ORDER BY "Quarter"',
                        connect
                    )["Quarter"].astype(int)
                )
            )

    ##########

        st.markdown("<h3>User Registration Growth Over Time</h3>", unsafe_allow_html=True)

        query_reg_year_growth = """
            SELECT
                "Year",
                SUM("Registered_users") AS total_registered_users
            FROM map_user_list
            GROUP BY "Year"
            ORDER BY "Year";
        """

        df_reg_year_growth = pd.read_sql(query_reg_year_growth, connect)

        fig_reg_year = px.line(
            df_reg_year_growth,
            x="Year",
            y="total_registered_users",
            markers=True,
            title="Registered Users Growth Over Years"
        )

        fig_reg_year.update_layout(
            xaxis_title="Year",
            yaxis_title="Registered Users",
            height=450
        )

        st.plotly_chart(fig_reg_year, use_container_width=True)

    #############

        st.markdown("<h3>Top States by User Registration</h3>", unsafe_allow_html=True)

        query_reg_top_states = f"""
            SELECT
                "State",
                SUM("Registered_users") AS total_registered_users
            FROM map_user_list
            WHERE "Year" = {reg_year_selected}
            AND "Quarter" = {reg_quarter_selected}
            GROUP BY "State"
            ORDER BY total_registered_users DESC
            LIMIT 10;
        """

        df_reg_top_states = pd.read_sql(query_reg_top_states, connect)

        fig_reg_states = px.bar(
            df_reg_top_states,
            x="State",
            y="total_registered_users",
            text_auto=".2s",
            title=f"Top 10 States – User Registrations ({reg_year_selected} Q{reg_quarter_selected})",
            color_discrete_sequence=["#6f42c1"]
        )

        fig_reg_states.update_layout(
            xaxis_title="State",
            yaxis_title="Registered Users",
            height=500
        )

        st.plotly_chart(fig_reg_states, use_container_width=True)

    ################

        st.markdown("<h3>State-wise Registration Trend</h3>", unsafe_allow_html=True)

        reg_states_list = sorted(
            pd.read_sql(
                'SELECT DISTINCT "State" FROM map_user_list ORDER BY "State"',
                connect
            )["State"]
        )

        reg_state_selected = st.selectbox("Select a State", reg_states_list)

        query_reg_state_trend = f"""
            SELECT
                "Quarter",
                SUM("Registered_users") AS total_registered_users
            FROM map_user_list
            WHERE "State" = '{reg_state_selected}'
            AND "Year" = {reg_year_selected}
            GROUP BY "Quarter"
            ORDER BY "Quarter";
        """

        df_reg_state_trend = pd.read_sql(query_reg_state_trend, connect)

        fig_reg_state = px.line(
            df_reg_state_trend,
            x="Quarter",
            y="total_registered_users",
            markers=True,
            title=f"User Registration Trend in {reg_state_selected} – {reg_year_selected}"
        )

        fig_reg_state.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Registered Users",
            height=450
        )

        st.plotly_chart(fig_reg_state, use_container_width=True)

