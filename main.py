# Import necessary libraries
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Set page Configuration
st.set_page_config(page_title="DataVision Pro", layout="centered", page_icon="📊")

# Title
st.title("📊 DataVision Pro App")

# Get the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the "data" folder
folder_path = f"{working_dir}/data"

# List the files present in the "data" folder
files_list = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Dropdown for all the files
selected_file = st.selectbox("Select a file", files_list, index=None)

# Initialize selected_plot variable
selected_plot = None

# Check if a file is selected
if selected_file:
    # Get the complete path of the selected file
    file_path = os.path.join(folder_path, selected_file)

    # Reading the CSV file as a pandas dataframe
    df = pd.read_csv(file_path)

    # Create two columns in the Streamlit layout
    col1, col2 = st.columns(2)

    with col1:
        # Display the first few rows of the dataframe
        st.write("Preview of the Dataframe:")
        st.write(df.head())

    with col2:
        # User selection of dataframe columns for X and Y axes
        x_axis = st.selectbox("Select the X-axis", options=df.columns.tolist(), index=None)
        y_axis = st.selectbox("Select the Y-axis", options=df.columns.tolist(), index=None)

        # List of available plot types
        plot_list = ["Line Plot", "Scatter Plot", "Bar Chart", "Histogram", "Boxplot", "Pie Chart",
                     "Area Plot", "Contour Plot", "Heatmap", "Violin Plot"]

        # User selection of plot type
        selected_plot = st.selectbox("Select the plot", options=plot_list, index=None)

# Button to generate plots
if st.button("Generate Plot"):
    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Check if selected_plot is not None before using it
    if selected_file is None:
        st.warning("Please select a file")

    elif x_axis is None or y_axis is None:
        st.warning("Please select both X-axis and Y-axis")

    elif selected_plot is not None:
        # Generate selected plot based on user's choice
        if selected_plot == "Line Plot":
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            plt.title(f"Line Plot of {y_axis} vs {x_axis}")

        elif selected_plot == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            plt.title(f"Scatter Plot of {y_axis} vs {x_axis}")

        elif selected_plot == "Bar Chart":
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            plt.title(f"Bar Chart of {y_axis} vs {x_axis}")

        elif selected_plot == "Histogram":
            sns.histplot(data=df, x=x_axis, y=y_axis, ax=ax, kde=True)
            plt.title(f"Histogram of {y_axis} vs {x_axis}")

        elif selected_plot == "Boxplot":
            sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)
            plt.title(f"Boxplot of {y_axis} vs {x_axis}")

        elif selected_plot == "Pie Chart":
            plt.pie(df[y_axis], labels=df[x_axis], autopct='%1.1f%%', startangle=140)
            plt.title(f"Pie Chart of {y_axis} vs {x_axis}")

        elif selected_plot == "Area Plot":
            df.plot.area(x=x_axis, y=y_axis, ax=ax)
            plt.title(f"Area Plot of {y_axis} vs {x_axis}")

        elif selected_plot == "Contour Plot":
            plt.contour(df.pivot_table(index=y_axis, columns=x_axis, values=df.columns[2]))
            plt.title(f"Contour Plot of {y_axis} vs {x_axis}")

        elif selected_plot == "Heatmap":
            sns.heatmap(df.pivot_table(index=y_axis, columns=x_axis, values=df.columns[2]), cmap="YlGnBu")
            plt.title(f"Heatmap of {y_axis} vs {x_axis}")

        elif selected_plot == "Violin Plot":
            sns.violinplot(x=df[x_axis], y=df[y_axis], ax=ax)
            plt.title(f"Violin Plot of {y_axis} vs {x_axis}")

        # Set labels for the plot
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        # Display the plot in Streamlit
        st.pyplot(fig)

# Show data summary
if st.button("Show Data Summary"):
    st.subheader("Data Summary:")
    st.write(df.describe())

# Allow data filtering
if st.checkbox("Enable Data Filtering"):
    # Example: Add sliders for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    min_value = st.slider("Minimum Value", float(df[numeric_columns].min().min()),
                          float(df[numeric_columns].max().max()))
    max_value = st.slider("Maximum Value", float(df[numeric_columns].min().min()),
                          float(df[numeric_columns].max().max()))

    # Apply filter to the dataframe
    filtered_df = df[(df[numeric_columns] >= min_value) & (df[numeric_columns] <= max_value)]

    # Display filtered dataframe
    st.subheader("Filtered Data:")
    st.write(filtered_df)
