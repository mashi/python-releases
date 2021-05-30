from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup


def get_information():
    """Web scraping: get python releases from html page and returns a
    dataframe.

    Returns
    -------
    pandas.DataFrame
        Dataframe with the collected data.
    """
    site = "https://www.python.org/downloads/"
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")

    # desired information are inside two classes: column names and table content
    # example of the data:
    # </div>
    #     <span class="release-version">Python version</span>
    #     <span class="release-status">Maintenance status</span>
    #     ...
    # </div>
    column_heading_class = "list-row-headings"
    columns = soup.find(class_=column_heading_class).get_text()
    column_list = [
        column_name for column_name in columns.split("\n") if column_name != ""
    ]

    # <ol class="list-row-container menu">
    #     <li>
    #         <span class="release-version">3.9</span>
    #         <span class="release-status">bugfix</span>
    #         ...
    #     </li>
    #     <li>
    #     ...
    #     </li>
    #     ...
    # </ol>
    row_content_class = "list-row-container menu"
    rows = soup.find(class_=row_content_class).get_text()
    row_list = [row_text for row_text in rows.split("\n") if row_text != ""]

    # create dataframe like:
    #   Python version Maintenance status First released End of support Release schedule
    # 0            3.9             bugfix     2020-10-05        2025-10          PEP 596
    # 1            3.8             bugfix     2019-10-14        2024-10          PEP 569
    # ...
    matrix = np.array(row_list).reshape(5, 5)
    df = pd.DataFrame(columns=column_list, data=matrix)
    return df


def visualization(df):
    """Gantt charts for the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with information about the python releases.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Plotly graph of the dataframe.
    """
    # bar plot of the dates
    fig = px.timeline(
        df,
        x_start="First released",
        x_end="End of support",
        y="Python version",
        color="Maintenance status",
        color_discrete_sequence=["#1CBE4F", "#FEAF16", "#EF553B"],
    )

    today = datetime.today().strftime("%Y-%m-%d")
    fig.add_vline(x=today)
    return fig


if __name__ == "__main__":
    df = get_information()
    fig = visualization(df)
    fig.show()
