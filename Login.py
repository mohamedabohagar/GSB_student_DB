import streamlit as st
import plotly.graph_objects as go

page_title ="Alex_GSB"
page_icon = ":school:"
layout = "centered"

st.set_page_config(page_title=page_title ,page_icon=page_icon, layout=layout)
st.title(page_icon  + "  "+ page_title)

with st.form("Login" ,clear_on_submit=True):
    col1,col2 =st.columns(2)
    col1.text_input("Login",key="login")
    col2.text_input("Password", key = "password",type="password")

    submitted = st.form_submit_button("Submit")
    if submitted:
        username = {"username": st.session_state["login"]}
        password = {"password": st.session_state["password"]}
        st.write(f"username:{username}")
        st.write(f"password:{password}")

        st.success("Datat Saved")