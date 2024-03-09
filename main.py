from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup


def _get_header(soup):
    """Extract the column names from the "list-row-headings" class.

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        The html web page.

    Returns
    -------
    list
        Each element is a string with a column name.
    """
    column_heading_class = "list-row-headings"
    columns = soup.find(class_=column_heading_class).get_text()
    column_list = [
        column_name for column_name in columns.split("\n") if column_name != ""
    ]
    return column_list


def _get_row(soup):
    """Extract the row information from the "list-row-container menu" class.

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        The html web page.

    Returns
    -------
    list
        Each element is a string of information.

    Example
    -------
    Note the orientation of the information:
    ['3.10', 'bugfix', '2021-10-04', '2026-10', 'PEP 619',
        '2.7', 'end-of-life', '2010-07-03', '2020-01-01', 'PEP 373']
    """
    row_content_class = "list-row-container menu"
    rows = soup.find(class_=row_content_class).get_text()
    row_list = [row_text for row_text in rows.split("\n") if row_text != ""]
    return row_list


def _create_df(column_header, row_list):
    """Create a dataframe using the column header and the row elements.

    Parameters
    ----------
    column_header: list
        The column names.
    row_list: list
        The information strings.

    Returns
    -------
    pandas.DataFrame
        A dataframe of data to be plotted.

    Example
    -------
    Create a dataframe like:
      Python version Maintenance status First released End of support Release schedule
    0            3.9             bugfix     2020-10-05        2025-10          PEP 596
    1            3.8             bugfix     2019-10-14        2024-10          PEP 569
    """
    number_of_columns = len(column_header)
    number_of_rows = len(row_list) // number_of_columns
    matrix = np.array(row_list).reshape(number_of_rows, number_of_columns)
    df = pd.DataFrame(columns=column_header, data=matrix)
    return df


def get_information():
    """Web scraping: get python releases from html page and returns a
    dataframe.

    Returns
    -------
    pandas.DataFrame
        Dataframe with the collected data.
    """
    site = "https://www.python.org/downloads/"
    page = requests.get(site, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    column_header = _get_header(soup)
    row_list = _get_row(soup)
    df = _create_df(column_header, row_list)
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
    df["First released"] = df["First released"].str.replace("(planned)", "").str.strip()
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
