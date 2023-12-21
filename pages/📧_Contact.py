import streamlit as st
from PIL import Image


st.set_page_config(page_title="Contact", page_icon="📧", layout="centered", initial_sidebar_state="auto", menu_items=None)

image = Image.open('tek_up.png')

st.image(image)
    
def main():
    st.title("Contact Us")

    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    if st.button("Submit"):
        if name.strip() == "" or email.strip() == "" or message.strip() == "":
            st.warning("Please fill out all fields.")
        else:
            st.success("Message sent successfully!")

if __name__ == "__main__":
    main()
