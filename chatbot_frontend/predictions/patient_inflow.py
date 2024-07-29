import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime, timedelta
import os


# Function to load and preprocess data
def load_and_preprocess_data(csv_url):
    df = pd.read_csv(csv_url, parse_dates=['date'])
    df.rename(columns={'date': 'ds', 'patient_inflow': 'y'}, inplace=True)
    df['ds'] = df['ds'].dt.date
    return df


# Function to fit the Prophet model
def fit_prophet_model(df):
    model = Prophet()
    model.fit(df)
    return model


# Function to create a future dataframe and make forecasts
def make_forecast(model, df, forecast_periods=60):
    future = model.make_future_dataframe(periods=forecast_periods, include_history=True)
    future['ds'] = future['ds'].dt.date
    forecast = model.predict(future)
    return forecast


# Function to determine the forecast range
def get_forecast_range(df, forecast):
    forecast_end_date = forecast['ds'].max()
    forecast_start_date = df['ds'].max() + timedelta(days=1)
    return forecast_start_date, forecast_end_date


# Function to plot forecast using Plotly with custom styling
def plot_forecast_plotly(forecast):
    fig = px.scatter(forecast, x='ds', y='yhat', title='Patient Inflow Prediction',
                     labels={'ds': 'Date', 'yhat': 'Patient Inflow'},
                     trendline="ols")

    # Customize layout
    fig.update_layout(
        title='Patient Inflow Prediction',
        xaxis_title='Date',
        yaxis_title='Patient Inflow',
        template='plotly_white',
        title_font=dict(size=24, color='darkblue', family='Arial'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        legend=dict(title='Legend', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

# Function to plot historical and forecasted data
def plot_forecast(df, forecast):
    plt.figure(figsize=(14, 7))
    sns.scatterplot(x=df['ds'], y=df['y'], color='blue', label='Historical Patient Inflow')
    sns.lineplot(x=forecast['ds'], y=forecast['yhat'], color='red', linestyle='--', label='Forecasted Patient Inflow')
    plt.title('Patient Inflow Prediction')
    plt.xlabel('Date')
    plt.ylabel('Patient Inflow')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Function to evaluate model performance
def evaluate_model(df, forecast, forecast_periods=60):
    recent_data = df.tail(forecast_periods)
    recent_forecast = forecast.tail(forecast_periods)
    mae = mean_absolute_error(recent_data['y'], recent_forecast['yhat'])
    rmse = mean_squared_error(recent_data['y'], recent_forecast['yhat'], squared=False)
    return mae, rmse

# Function to predict patient inflow for a particular date
def predict_for_date(date_str, model, df, forecast, future_periods=60):
    # Convert the input date string to a Timestamp
    date = pd.to_datetime(date_str).date()  # Convert to datetime.date

    # Convert df and forecast dates to datetime.date
    last_date = df['ds'].max()
    forecast_max_date = forecast['ds'].max().date()

    # Ensure the date is within the forecast range
    if date <= last_date or date > forecast_max_date:
        raise ValueError(f"Date {date_str} is out of the forecast range.")

    # Create future dataframe for the specific date
    future = pd.DataFrame({'ds': [pd.Timestamp(date)]})
    forecast_result = model.predict(future)
    predicted_inflow = forecast_result['yhat'].values[0]

    # Round to the nearest whole number
    return round(predicted_inflow)

# Function to calculate staff requirements
def calculate_staff_requirements(predicted_inflow, staff_ratios):
    required_staff = {
        role: round(predicted_inflow * ratio)
        for role, ratio in staff_ratios.items()
    }
    return required_staff


def load_resource_data(url):
    """Load the resource utilization data from a given URL."""
    df = pd.read_csv(url)
    return df

def get_bed_occupancy(df):
    """Calculate bed occupancy for each department."""
    bed_occupancy = {}
    departments = df['department'].unique()
    for dept in departments:
        dept_data = df[df['department'] == dept]
        total_beds = dept_data['beds_available'].sum()
        occupied_beds = dept_data['beds_occupied'].sum()
        occupancy_rate = occupied_beds / total_beds if total_beds > 0 else 0
        bed_occupancy[dept] = {
            'total_beds': total_beds,
            'occupied_beds': occupied_beds,
            'occupancy_rate': occupancy_rate
        }
    return bed_occupancy

def get_equipment_usage(df):
    """Calculate equipment usage for each type of equipment."""
    equipment_usage = {}
    equipment_types = df['equipment'].unique()
    for equip in equipment_types:
        equip_data = df[df['equipment'] == equip]
        total_units = equip_data['equipment_available'].sum()
        used_units = equip_data['equipment_used'].sum()
        usage_rate = used_units / total_units if total_units > 0 else 0
        equipment_usage[equip] = {
            'total_units': total_units,
            'used_units': used_units,
            'usage_rate': usage_rate
        }
    return equipment_usage