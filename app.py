import numpy as np
import pandas as pd
import pickle as pk
import streamlit as st
import base64
import sklearn as sk
from streamlit.components.v1 import html

# Load trained model and scaled data (replace with your filepaths)
loaded_model = pk.load(open("trained_model_lr.sav", "rb"))
scaled_data = pk.load(open("scaled_data.sav", "rb"))

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image dynamically based on selected engine size
def set_background_image(engine_size):
    background_images = {
        0: "url('https://wallpapercave.com/wp/wp6696562.jpg')",
        1: "url('https://hips.hearstapps.com/hmg-prod/images/8cc9595364efa0fc-org-1584048843.jpg?resize=1200:*')",
        2: "url('https://global.toyota/pages/powertrain/engine/images/engine_001.png')",
        3: "url('https://blogs.gomechanic.com/wp-content/uploads/2020/01/08b88a113768de393f3d95e87c1455e8.jpg')"
    }
    background_image = background_images.get(engine_size, "url('https://wallpapercave.com/wp/wp6696562.jpg')")
    return f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: {background_image};
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
    </style>
    """

def input_converter(inp):
    vehicle = [
        "Two-seater",
        "Minicompact",
        "Compact",
        "Subcompact",
        "Mid-size",
        "Full-size",
        "SUV: Small",
        "SUV: Standard",
        "Minivan",
        "Station wagon: Small",
        "Station wagon: Mid-size",
        "Pickup truck: Small",
        "Special purpose vehicle",
        "Pickup truck: Standard",
    ]
    transmission = ["AV", "AM", "M", "AS", "A"]
    fuel = ["D", "E", "X", "Z"]
    lst = []
    for i in range(6):
        if (type(inp[i]) == str):
            if (inp[i] in vehicle):
                lst.append(vehicle.index(inp[i]))
            elif (inp[i] in transmission):
                lst.append(transmission.index(inp[i]))
            elif (inp[i] in fuel):
                if (fuel.index(inp[i]) == 0):
                    lst.extend([1, 0, 0, 0])
                    break
                elif (fuel.index(inp[i]) == 1):
                    lst.extend([0, 1, 0, 0])
                    break
                elif (fuel.index(inp[i]) == 2):
                    lst.extend([0, 0, 1, 0])
                    break
                elif (fuel.index(inp[i]) == 3):
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst)
    arr = arr.reshape(1, -1)
    arr = scaled_data.transform(arr)
    prediction = loaded_model.predict(arr)
    return (f"The Fuel Consumption km is {round(prediction[0], 2)}")

def main():
    
    
    # Title
    st.markdown("<h1 style='text-align: center; color: white;'>Fuel Consumption Prediction</h1>", unsafe_allow_html=True)

    # Input data from user
    result = 0
    vehicle = [
        "Two-seater",
        "Minicompact",
        "Compact",
        "Subcompact",
        "Mid-size",
        "Full-size",
        "SUV: Small",
        "SUV: Standard",
        "Minivan",
        "Station wagon: Small",
        "Station wagon: Mid-size",
        "Pickup truck: Small",
        "Special purpose vehicle",
        "Pickup truck: Standard",
    ]
    transmission = ["AV", "AM", "M", "AS", "A"]
    fuel = ["D", "E", "X", "Z"]

    # Vehicle class dropdown
    Vehicle_class = st.selectbox(label="Enter Vehicle class", options=vehicle)

    # Styling for the dropdown (optional)
    css = """
    <style>
        .stSelectbox [data-testid='stMarkdownContainer'] {
            color: white;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

    # Engine size dropdown
    Engine_size = st.selectbox(
        "Select Engine Size (please enter value in this range [0-3])", options=[0 , 1, 2, 3]
    )

    # Styling for the dropdown (optional)
    st.write(css, unsafe_allow_html=True)

    # Cylinder input
    Cylinders = st.number_input(
        "Enter number of Cylinders (please enter value in this range [1-16])",
        min_value=1,
        max_value=16,
    )

    # Transmission dropdown
    Transmission = st.selectbox("Select the Transmission", transmission)

    # CO2 Rating input
    Co2_Rating = st.number_input(
        "Enter CO2 Rating (please enter value in this range [1-10])",
        min_value=1,
        max_value=10,
    )

    # Fuel type dropdown
    Fuel_type = st.selectbox("Select the Fuel type", fuel)

    # Set background image based on selected engine size
    st.markdown(set_background_image(Engine_size), unsafe_allow_html=True)

    # Prediction button
    if st.button("Predict "):
        result = input_converter([Vehicle_class, Engine_size, Cylinders, Transmission, Co2_Rating, Fuel_type])
        markdown_text = f"<h2 style='color:white;'><b>{result}</b>!</h2>"
        st.markdown(markdown_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
