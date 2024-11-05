"""Script to form the graphs for the analytics dashboard."""

import altair as alt


def decade_chart(data: dict) -> alt.Chart:
    """Returns an Altair donut chart for the decade/release breakdowns."""

    chart = alt.Chart(alt.Data(values=data)).mark_arc(innerRadius=50, outerRadius=100).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="decade", type="nominal",
                        legend=alt.Legend(title="Decade"))).properties(
        title="Decade/Release Breakdown")

    return chart
