import streamlit as st

def render_sidebar():
    st.sidebar.header("Graph Plotting Options")
    
    function_input = st.sidebar.text_input("Enter a function (e.g., x**2, sin(x), etc.):")
    interval_input = st.sidebar.text_input("Enter the interval (e.g., -10, 10):")
    
    if st.sidebar.button("Plot"):
        if function_input and interval_input:
            st.session_state.function = function_input
            st.session_state.interval = interval_input
        else:
            st.sidebar.warning("Please enter both a function and an interval.")