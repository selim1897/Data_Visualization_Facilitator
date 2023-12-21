import streamlit as st


st.set_page_config(page_title="Results", page_icon="😎", layout="centered", initial_sidebar_state="auto", menu_items=None)

if 'title' in st.session_state:
    st.title(':blue[{}] :sunglasses:'.format(st.session_state['title']))

if 'charts' in st.session_state:
    charts = st.session_state['charts']

    for fig in charts:
        st.plotly_chart(fig, use_container_width=True)