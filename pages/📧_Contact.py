import streamlit as st
from PIL import Image
import smtplib


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
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = st.secrets['email']
            smtp_password = st.secrets['password_smtp']

            from_email = st.secrets['email']
            to_email = st.secrets['email_to']
            subject = 'Data Visualiztion Facilitator'
            body = message

            full_message = f'Subject: {subject}\n\n from : {email} \n\n {body}'

            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.sendmail(from_email, to_email, full_message)
            st.success("Message sent successfully!")

if __name__ == "__main__":
    main()
