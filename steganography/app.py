import streamlit as st
from cryptography.fernet import Fernet
from . import text_steganography as text_steg
from . import image_steganography as img_steg
from . import audio_steganography as audio_steg
from PIL import Image
import os

def steganography_main():
    st.title("🖼️ Steganography Tool")
    st.subheader("Securely Hide and Extract Messages from Text, Audio, and Images")

    # ✅ Manage Navigation State
    if "steg_page" not in st.session_state:
        st.session_state.steg_page = "Home"

    if st.session_state.steg_page == "Home":
        # 🔹 Welcome Section
        st.write(
            """
            **Steganography** is the practice of hiding secret messages within digital media.  
            This tool allows you to **encode** and **decode** messages in **text, audio, and images**, 
            ensuring secure communication without raising suspicion. 🔏
            """
        )

        # 🔹 Features List
        st.markdown("### 🔹 Features")
        st.write("✅ **Text Steganography** – Hide messages inside other text without detection.")  
        st.write("✅ **Audio Steganography** – Encode messages into sound waves.")  
        st.write("✅ **Image Steganography** – Conceal text inside images.")  
        st.write("✅ **Secure Encryption** – Messages are protected using cryptographic keys.")  

        # 🔹 Navigation Buttons
        st.markdown("### 🚀 Get Started")
        col1, col2 = st.columns(2)  # Align buttons in a row
        with col1:
            if st.button("📜 Use Text Steganography"):
                st.session_state.steg_page = "Text"
                st.rerun()
        with col2:
            if st.button("🎵 Use Audio Steganography"):
                st.session_state.steg_page = "Audio"
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button("🖼️ Use Image Steganography"):
                st.session_state.steg_page = "Image"
                st.rerun()
        with col4:
            if st.button("🏠 Back to Main Home"):
                st.session_state.page = "Home"
                st.rerun()

    # ✅ TEXT STEGANOGRAPHY PAGE
    elif st.session_state.steg_page == "Text":
        st.header("📜 Text Steganography")
        action = st.radio("Choose Action", ("Encode", "Decode"))

        if action == "Encode":
            message = st.text_area("Enter the message to encode", "")
            base_text = st.text_area("Enter the base text", "")
            if st.button("Encode"):
                key = Fernet.generate_key()
                encoded_text = text_steg.encode_text(base_text, message, key)
                st.success("Encoded Text:")
                st.code(encoded_text)
                st.write("Encryption Key for Decoding:")
                st.code(key.decode())
        elif action == "Decode":
            encoded_message = st.text_area("Enter the encoded text", "")
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")
            if st.button("Decode") and key_input:
                decoded_message = text_steg.decode_text(encoded_message, key_input.encode())
                st.success("Decoded Message:")
                st.code(decoded_message)

        if st.button("🏠 Back to Steganography Home"):
            st.session_state.steg_page = "Home"
            st.rerun()

    # ✅ AUDIO STEGANOGRAPHY PAGE
    elif st.session_state.steg_page == "Audio":
        st.header("🎵 Audio Steganography")
        action = st.radio("Choose Action", ("Encode", "Decode"))

        if action == "Encode":
            message = st.text_area("Enter the message to encode", "")
            audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
            if audio_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_audio = "encoded_audio.wav"
                temp_audio_path = f"temp_{audio_file.name}"
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                audio_steg.encode_audio(temp_audio_path, message, key, output_audio)
                os.remove(temp_audio_path)
                st.success("Audio successfully encoded!")
                st.write("Encryption Key for Decoding:")
                st.code(key.decode())
                with open(output_audio, "rb") as file:
                    st.download_button(label="Download Encoded Audio", data=file, file_name=output_audio, mime="audio/wav")

        elif action == "Decode":
            audio_file = st.file_uploader("Choose an encoded audio file", type=["wav"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")
            if audio_file and st.button("Decode") and key_input:
                temp_audio_path = f"temp_{audio_file.name}"
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                decoded_message = audio_steg.decode_audio(temp_audio_path, key_input.encode())
                st.success("Decoded Message:")
                st.code(decoded_message)
                os.remove(temp_audio_path)

        if st.button("🏠 Back to Steganography Home"):
            st.session_state.steg_page = "Home"
            st.rerun()

    # ✅ IMAGE STEGANOGRAPHY PAGE
    elif st.session_state.steg_page == "Image":
        st.header("🖼️ Image Steganography")
        action = st.radio("Choose Action", ("Encode", "Decode"))

        if action == "Encode":
            message = st.text_area("Enter the message to encode", "")
            image_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
            if image_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_image = "encoded_image.png"
                img = Image.open(image_file).convert("RGB")
                stego_image = img_steg.encode_image(img, message, key)
                stego_image.save(output_image)
                st.success("Image successfully encoded!")
                st.write("Encryption Key for Decoding:")
                st.code(key.decode())
                with open(output_image, "rb") as file:
                    st.download_button(label="Download Encoded Image", data=file, file_name=output_image, mime="image/png")

        elif action == "Decode":
            image_file = st.file_uploader("Choose an encoded image file", type=["png", "jpg", "jpeg"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")
            if image_file and st.button("Decode") and key_input:
                img = Image.open(image_file).convert("RGB")
                decoded_message = img_steg.decode_image(img, key_input.encode())
                st.success("Decoded Message:")
                st.code(decoded_message)

        if st.button("🏠 Back to Steganography Home"):
            st.session_state.steg_page = "Home"
            st.rerun()

if __name__ == "__main__":
    steganography_main()
