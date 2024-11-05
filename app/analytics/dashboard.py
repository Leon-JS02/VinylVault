"""Script for the analytics Streamlit dashboard."""
import streamlit as st
from dotenv import load_dotenv

from analytics_utils import get_decade_counts, get_genre_counts
from graphs import decade_chart, genre_chart

if __name__ == "__main__":
    load_dotenv()
    st.set_page_config(layout="wide")
    decade_data = get_decade_counts()
    genre_data = get_genre_counts()

    cols = st.columns([1, 1])
    decade_pie_chart = decade_chart(decade_data)
    genre_bar_chart = genre_chart(genre_data)

    with cols[0]:
        st.altair_chart(decade_pie_chart, use_container_width=False)
    with cols[1]:
        st.altair_chart(genre_bar_chart, use_container_width=True)
