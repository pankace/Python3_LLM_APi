import streamlit as st
from components.plotting import plot_function
from utils.parser import parse_user_input
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_session():
    if 'history' not in st.session_state:
        st.session_state.history = []

def main():
    st.title("Function Plotter")
    initialize_session()
    
    with st.sidebar:
        st.header("Plot Controls")
        user_input = st.text_area(
            "What would you like to plot?",
            placeholder="e.g., 'Plot sine function from -5 to 5'"
        )
        
        if st.button("Plot"):
            if user_input:
                try:
                    result = parse_user_input(user_input)
                    
                    if result == "exit":
                        st.success("Goodbye! Thanks for using the function plotter.")
                        return
                        
                    if result:
                        func_type, params = result
                        fig = plot_function(func_type, params)
                        st.session_state.history.append({
                            'input': user_input,
                            'type': func_type,
                            'params': params
                        })
                        st.pyplot(fig)
                    else:
                        st.error("I couldn't understand that. Please try again.")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        if st.session_state.history:
            st.header("History")
            for idx, item in enumerate(st.session_state.history):
                with st.expander(f"Plot {idx + 1}: {item['type']}"):
                    st.write(f"Input: {item['input']}")
                    st.write(f"Parameters: {item['params']}")
        
        if st.button("Clear History"):
            st.session_state.history = []


if __name__ == "__main__":
    main()