"""Script for the analytics Streamlit dashboard."""
import streamlit as st
from dotenv import load_dotenv

from analytics_utils import get_decade_counts
from graphs import decade_chart

if __name__ == "__main__":
    load_dotenv()
    st.set_page_config(layout="wide")
    decade_data = get_decade_counts()
    chart = decade_chart(decade_data)
    st.altair_chart(chart, use_container_width=True)
