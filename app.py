import streamlit as st
import segno
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# Helper function to generate a QR code with optional logo
def generate_qr_code(data, logo_path=None):
    qr = segno.make(data)
    filename = "temp_qr.png"
    qr.save(filename, scale=10)
    qr_img = Image.open(filename).convert("RGB")
    
    # Overlay logo if provided
    if logo_path:
        logo = Image.open(logo_path)
        logo_size = (qr_img.size[0] // 5, qr_img.size[1] // 5)
        logo = logo.resize(logo_size)
        logo_position = (
            (qr_img.size[0] - logo_size[0]) // 2,
            (qr_img.size[1] - logo_size[1]) // 2,
        )
        qr_img.paste(logo, logo_position, mask=logo if logo.mode == 'RGBA' else None)
    
    return qr_img

# Helper function to create a 3D visualization
def render_qr_in_3d(qr_img):
    # Convert the image to a numpy array
    qr_array = np.array(qr_img.convert("L"))  # Convert to grayscale
    rows, cols = qr_array.shape
    x, y = np.meshgrid(range(cols), range(rows))

    # Normalize pixel values to height
    z = qr_array / 255.0

    # Plot 3D surface
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x, y, z, cmap="binary")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Height")
    plt.axis("off")
    return fig

# Streamlit app
st.title("QR Code Generator with 3D Visualization (Using Segno)")

# Input form
st.subheader("Generate your QR Code")
form_url = st.text_input("Enter the URL or text to encode", "")
logo_file = st.file_uploader("Upload a logo (optional)", type=["png", "jpg", "jpeg"])

if st.button("Generate QR Code"):
    if form_url:
        # Save logo if uploaded
        logo_path = None
        if logo_file:
            logo_path = os.path.join("uploaded_logo.png")
            with open(logo_path, "wb") as f:
                f.write(logo_file.read())
        
        # Generate the QR code
        qr_img = generate_qr_code(form_url, logo_path)

        # Display the QR code
        st.image(qr_img, caption="Generated QR Code", use_container_width=True)

        # Render 3D visualization
        st.subheader("3D Visualization of the QR Code")
        fig = render_qr_in_3d(qr_img)
        st.pyplot(fig)
        
        # Option to download the QR code
        qr_img_path = "generated_qr.png"
        qr_img.save(qr_img_path)
        with open(qr_img_path, "rb") as file:
            st.download_button("Download QR Code", file, file_name="qr_code.png", mime="image/png")
    else:
        st.error("Please enter a URL or text to generate the QR code.")
