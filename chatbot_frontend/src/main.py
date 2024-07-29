import os
import requests
import streamlit as st
import pandas as pd

from predictions.patient_inflow import (
    load_and_preprocess_data,
    fit_prophet_model,
    make_forecast,
    get_forecast_range,
    plot_forecast_plotly,
    plot_forecast,
    evaluate_model,
    predict_for_date,
    calculate_staff_requirements,
    load_resource_data,
    get_bed_occupancy,
    get_equipment_usage
)

# Set page configuration at the very start of the script
st.set_page_config(page_title="Hospital Dashboard", layout="wide")

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/hospital-rag-agent")

RESOURCE_URL = 'https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/resource_utilization.csv'

def dashboard():
    st.title("Hospital Dashboard")
    st.write("Welcome to the Hospital Dashboard! Use the options below to make predictions and manage staff requirements.")

    # Go to Chatbot Button with a unique key
    if st.button("Go to Chatbot", key="go_to_chatbot"):
        st.session_state.view = "chatbot"
        st.experimental_rerun()

    # Sidebar inputs
    st.sidebar.header("Input Data")
    csv_url = st.sidebar.text_input(
        'CSV URL',
        'https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/patient_inflow.csv',
        key='csv_url_input'
    )

    specific_date = st.sidebar.text_input(
        'Date for Prediction (YYYY-MM-DD)',
        '2024-08-01',
        key='date_input'
    )

    st.sidebar.header("Current Staff Levels")
    current_physicians = st.sidebar.number_input(
        "Current Physicians",
        min_value=0,
        key='current_physicians'
    )
    current_nurses = st.sidebar.number_input(
        "Current Nurses",
        min_value=0,
        key='current_nurses'
    )
    current_technicians = st.sidebar.number_input(
        "Current Technicians",
        min_value=0,
        key='current_technicians'
    )

    if st.sidebar.button("Update", key='update_button'):
        if csv_url and specific_date:
            try:
                # Load data and fit model
                df = load_and_preprocess_data(csv_url)
                model = fit_prophet_model(df)
                forecast = make_forecast(model, df)

                # Display forecast range
                forecast_start_date, forecast_end_date = get_forecast_range(df, forecast)
                st.write(f"**Forecast range starts from:** {forecast_start_date}")
                st.write(f"**Forecast range ends on:** {forecast_end_date}")

                # Display forecast plot
                st.subheader("Forecasted Patient Inflow")
                # Assuming forecast is your forecast DataFrame
                forecast_chart = plot_forecast_plotly(forecast)
                st.plotly_chart(forecast_chart)

                # Predict for specific date
                predicted_inflow = predict_for_date(specific_date, model, df, forecast)
                # st.write(f"**Predicted patient inflow for {specific_date}: {predicted_inflow}**")
                st.subheader(
                    f"_Predicted patient inflow for_ :green[{specific_date}] is :blue[{predicted_inflow}]**"
                )

                # Staff requirements
                st.subheader("Staff Requirements")
                staff_ratios = {
                    'Physicians': 1 / 10,
                    'Nurses': 1 / 7,
                    'Technicians': 1 / 15
                }

                required_staff = calculate_staff_requirements(predicted_inflow, staff_ratios)

                # Create DataFrame for required staff
                required_staff_df = pd.DataFrame({
                    'Role': ['Physicians', 'Nurses', 'Technicians'],
                    'Required Staff': [
                        required_staff['Physicians'],
                        required_staff['Nurses'],
                        required_staff['Technicians']
                    ]
                })

                st.dataframe(
                    required_staff_df,
                    column_config={
                        "Role": "Role",
                        "Required Staff": st.column_config.NumberColumn("Required Staff"),
                    },
                    hide_index=True,
                )

                # Additional staff needed
                additional_physicians = max(0, required_staff['Physicians'] - current_physicians)
                additional_nurses = max(0, required_staff['Nurses'] - current_nurses)
                additional_technicians = max(0, required_staff['Technicians'] - current_technicians)

                additional_staff_df = pd.DataFrame({
                    'Role': ['Physicians', 'Nurses', 'Technicians'],
                    'Additional Staff Needed': [
                        additional_physicians,
                        additional_nurses,
                        additional_technicians
                    ]
                })

                st.write("**Additional Staff Needed:**")
                st.dataframe(
                    additional_staff_df,
                    column_config={
                        "Role": "Role",
                        "Additional Staff Needed": st.column_config.NumberColumn("Additional Staff Needed"),
                    },
                    hide_index=True,
                )

                # Load resource utilization data
                resource_df = load_resource_data(RESOURCE_URL)

                # Display bed occupancy
                st.subheader("Bed Occupancy")
                bed_occupancy = get_bed_occupancy(resource_df)
                bed_occupancy_df = pd.DataFrame(bed_occupancy).T.reset_index()
                bed_occupancy_df.columns = ['Department', 'Total Beds', 'Occupied Beds', 'Occupancy Rate']
                st.dataframe(
                    bed_occupancy_df,
                    column_config={
                        "Department": "Department",
                        "Total Beds": st.column_config.NumberColumn("Total Beds"),
                        "Occupied Beds": st.column_config.NumberColumn("Occupied Beds"),
                        "Occupancy Rate": st.column_config.NumberColumn("Occupancy Rate", format="%.2f%%"),
                    },
                    hide_index=True,
                )

                # Display equipment usage
                st.subheader("Equipment Usage")
                equipment_usage = get_equipment_usage(resource_df)
                equipment_usage_df = pd.DataFrame(equipment_usage).T.reset_index()
                equipment_usage_df.columns = ['Equipment', 'Total Units', 'Used Units', 'Usage Rate']
                st.dataframe(
                    equipment_usage_df,
                    column_config={
                        "Equipment": "Equipment",
                        "Total Units": st.column_config.NumberColumn("Total Units"),
                        "Used Units": st.column_config.NumberColumn("Used Units"),
                        "Usage Rate": st.column_config.NumberColumn("Usage Rate", format="%.2f%%"),
                    },
                    hide_index=True,
                )

            except ValueError as e:
                st.error(e)
        else:
            st.warning("Please provide a valid CSV URL and date for prediction.")

# if __name__ == "__main__":
#     dashboard()

def chatbot():
    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This chatbot interfaces with a
            [LangChain](https://python.langchain.com/docs/get_started/introduction)
            agent designed to answer questions about the hospitals, patients,
            visits, physicians, and insurance payers in a fake hospital system.
            The agent uses retrieval-augment generation (RAG) over both
            structured and unstructured data that has been synthetically generated.
            """
        )

        st.header("Example Questions")
        st.markdown("- Which hospitals are in the hospital system?")
        st.markdown("- What is the average duration in days for closed emergency visits?")
        st.markdown("- List a review for any visit treated by physician 16.")
        st.markdown("- What are patients saying about the nursing staff at CareWell Medical Center?")
        st.markdown("- What is the review given by patient named Henry Hays?")
        st.markdown("- What is the average billing amount for Medicaid visits?")
        st.markdown("- Which physician has the highest salary?")
        st.markdown("- How much was billed for patient 789's stay?")
        st.markdown("- What is the average billing amount per day for Aetna patients?")
        st.markdown("- How many reviews have been written from patients in Florida?")
        st.markdown("- For visits that are not missing chief complaints, what percentage have reviews?")
        st.markdown("- What is the percentage of visits that have reviews for each hospital?")
        st.markdown("- Which physician has received the most reviews for the visits they've attended?")
        st.markdown("- What is the ID for physician James Cooper?")

    st.title("Hospital System Chatbot")
    st.info(
        """Ask me questions about patients, visits, insurance payers, hospitals,
        physicians, reviews, and wait times!"""
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "output" in message.keys():
                st.markdown(message["output"])

            if "explanation" in message.keys():
                with st.expander("How was this generated?", expanded=True):
                    st.info(message["explanation"])

    if prompt := st.chat_input("What do you want to know?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "output": prompt})
        data = {"text": prompt}

        with st.spinner("Searching for an answer..."):
            response = requests.post(CHATBOT_URL, json=data)

            if response.status_code == 200:
                output_text = response.json()["output"]
                explanation = response.json()["intermediate_steps"]
            else:
                output_text = """An error occurred while processing your message.
                This usually means the chatbot failed at generating a query to
                answer your question. Please try again or rephrase your message."""
                explanation = output_text

        st.chat_message("assistant").markdown(output_text)
        with st.expander("How was this generated?", expanded=True):
            st.info(explanation)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "output": output_text,
                "explanation": explanation,
            }
        )


# Main application logic
if "view" not in st.session_state:
    st.session_state.view = "dashboard"

if st.session_state.view == "dashboard":
    dashboard()
elif st.session_state.view == "chatbot":
    chatbot()
