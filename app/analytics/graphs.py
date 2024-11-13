"""Script to form the graphs for the analytics dashboard."""

import altair as alt


def decade_chart(data: dict) -> alt.Chart:
    """Returns an Altair donut chart for the decade/release breakdowns."""

    data_list = [{"Decade": decade, "Count": count}
                 for decade, count in data.items()]

    chart = alt.Chart(alt.Data(values=data_list)).mark_arc(innerRadius=50, outerRadius=100).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Decade", type="nominal",
                        legend=alt.Legend(title="Decade")),
        tooltip=["Decade:N", "Count:Q"]
    ).properties(
        title="Decade Counts"
    )

    return chart


def genre_chart(data: dict) -> alt.Chart:
    """Returns an Altair bar chart for genre/release breakdowns."""
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_data[:10]

    data_list = [{"Genre": genre.title(), "Count": count}
                 for genre, count in top_10]

    chart = alt.Chart(alt.Data(values=data_list)).mark_bar().encode(
        x=alt.X("Count:Q", title="Count"),
        y=alt.Y("Genre:N", sort="-x", title="Genre"),
        tooltip=[alt.Tooltip("Genre:N"), alt.Tooltip("Count:Q")]
    ).properties(
        title="Top 10 Genres by Count"
    )

    return chart
