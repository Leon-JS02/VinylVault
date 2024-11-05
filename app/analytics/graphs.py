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
