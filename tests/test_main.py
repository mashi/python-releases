import unittest

from bs4 import BeautifulSoup

import main as mn

ROW_HEADINGS = """
<div class="list-row-headings">
    <span class="release-version">Python version</span>
    <span class="release-status">Maintenance status</span>
    <span class="release-start">First released</span>
    <span class="release-end">End of support</span>
    <span class="release-pep">Release schedule</span>
</div>
"""


ROW_CONTENT = """
<ol class="list-row-container menu">
    <li>
        <span class="release-version">3.10</span>
        <span class="release-status">bugfix</span>
        <span class="release-start">2021-10-04</span>
        <span class="release-end">2026-10</span>
        <span class="release-pep"><a href="https://www.python.org/dev/peps/pep-0619">PEP 619</a></span>
    </li>
    <li>
        <span class="release-version">2.7</span>
        <span class="release-status">end-of-life</span>
        <span class="release-start">2010-07-03</span>
        <span class="release-end">2020-01-01</span>
        <span class="release-pep"><a href="https://www.python.org/dev/peps/pep-0373">PEP 373</a></span>
    </li>
</ol>
"""


class TestMain(unittest.TestCase):
    def test_true(self):
        self.assertEqual(1, 1)

    def test_header_elements(self):
        # check if the function is capable of detecting the 5 elements
        # from the # example string
        soup = BeautifulSoup(ROW_HEADINGS, "html.parser")
        columns = mn._get_header(soup)
        answer = 5
        self.assertEqual(answer, len(columns))

    def test_row_elements(self):
        # check if the function is capable of detecting the 10 elements
        # from the example string
        soup = BeautifulSoup(ROW_CONTENT, "html.parser")
        rows = mn._get_row(soup)
        answer = 10
        self.assertEqual(answer, len(rows))

    def test_df_organization_and_size(self):
        # check if the output size of the dataframe
        column_name = ["a", "b"]
        data = ["a1", "b1", "a2", "b2", "a3", "b3"]
        df = mn._create_df(column_name, data)

        row = df["a"]
        row_list = ["a1", "a2", "a3"]
        for idx, answer in enumerate(row_list):
            with self.subTest(i=idx):
                self.assertEqual(answer, row[idx])

        # check size
        answer_rows = 3
        answer_cols = 2
        self.assertEqual(answer_rows, df.shape[0])
        self.assertEqual(answer_cols, df.shape[1])


if __name__ == "__main__":
    unittest.main()
