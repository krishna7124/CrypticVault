import streamlit as st  

# Set page configuration (MUST be the first Streamlit command)
st.set_page_config(page_title="CrypticVault", page_icon="🔐", layout="wide")

from secret_keeper.app import secret_keeper_main
from steganography.app import steganography_main

# ✅ Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ✅ Sidebar Navigation (Updates session state)
sidebar_selection = st.sidebar.radio("Choose Feature", ["Home", "Secret Keeper", "Steganography"], index=["Home", "Secret Keeper", "Steganography"].index(st.session_state.page))

# ✅ Sync Sidebar Selection with Session State
if sidebar_selection != st.session_state.page:
    st.session_state.page = sidebar_selection
    st.rerun()

# ✅ Page Routing Based on Selection
if st.session_state.page == "Secret Keeper":
    secret_keeper_main()
elif st.session_state.page == "Steganography":
    steganography_main()
else:
    # ✅ Home Page Content (Text-Only)
    st.title("🔐 Welcome to CrypticVault")
    st.subheader("Secure Your Secrets with CrypticVault")

    st.write(
        """
        CrypticVault is your **one-stop solution** for securing sensitive information. 
        With advanced encryption and steganography techniques, you can **store secrets safely 
        and hide messages inside images, audio, and text**.  
        Whether you're protecting passwords, confidential notes, or hidden messages, 
        CrypticVault keeps your data **safe and accessible**. 🔒
        """
    )

    st.markdown("### 🔹 Features")
    st.write("✅ **Secret Keeper** – Store passwords & confidential data securely")  
    st.write("✅ **Steganography** – Hide messages in images, text, and audio")  
    st.write("✅ **Biometric Support** – Enhanced authentication for better security")  
    st.write("✅ **User-Friendly UI** – Easy navigation & seamless experience")  

    # ✅ Call-to-Action with Fully Working Buttons
    st.markdown("### 🚀 Get Started")
    col1, col2 = st.columns(2)  # Align buttons in a row
    with col1:
        if st.button("🔑 Explore Secret Keeper"):
            st.session_state.page = "Secret Keeper"
            st.rerun()
    with col2:
        if st.button("🖼️ Try Steganography"):
            st.session_state.page = "Steganography"
            st.rerun()

    st.write("👈 **Use the sidebar to switch between features!**")
