import unittest
import datetime
from bs4 import BeautifulSoup
from crawler import get_single_post


class TestGetSinglePost(unittest.TestCase):
    def setUp(self):
        html_content = """
<tr class="athing" id="1">
  <td align="right" valign="top" class="title">
    <span class="rank">1.</span>
  </td>
  <td valign="top" class="votelinks">
    <center>
      <a id="up_1" href="vote?id=1&amp;how=up&amp;goto=front%3Fday%3D2006-10-09">
        <div class="votearrow" title="upvote"></div>
      </a>
    </center>
  </td>
  <td class="title">
    <span class="titleline">
      <a href="http://ycombinator.com">Y Combinator</a>
      <span class="sitebit comhead"> ( <a href="from?site=ycombinator.com">
          <span class="sitestr">ycombinator.com</span>
        </a>) </span>
    </span>
  </td>
</tr>
<tr>
  <td colspan="2"></td>
  <td class="subtext">
    <span class="subline">
      <span class="score" id="score_1">57 points</span> by <a href="user?id=pg" class="hnuser">pg</a>
      <span class="age" title="2006-10-09T18:21:51">
        <a href="item?id=1">on Oct 9, 2006</a>
      </span>
      <span id="unv_1"></span> | <a href="item?id=1">15&nbsp;comments</a>
    </span>
  </td>
</tr>
"""
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.mock_item = self.soup.find("tr")

    def test_get_single_post(self):
        result = get_single_post(self.mock_item)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["title"], "Y Combinator")
        self.assertEqual(result["link"], "http://ycombinator.com")
        self.assertEqual(result["scores"], 57)
        self.assertEqual(result["user"], "pg")
        self.assertEqual(result["date"], datetime.datetime(2006, 10, 9, 18, 21, 51))


if __name__ == "__main__":
    unittest.main()
