import pytest

from scrapers.wiki import WikiScraper

# oldid=1215058959
MOCK_HTML = """
<html>
    <table class="wikitable">
        <tbody>
            <tr>
                <th>Location</th>
                <th>Population<br/>(1 July 2022)</th>
                <th>Population<br/>(1 July 2023)</th>
                <th>Change</th>
                <th>UN Continental Region<sup class="reference">[1]</sup></th>
                <th>UN Statistical Subregion<sup class="reference">[1]</sup></th>
            </tr>
            <tr class="static-row-numbers-norank">
                <td><b><span class="flagicon"> </span><a href="#">World</a></b></td>
                <td>7,975,105,156</td>
                <td>8,045,311,448</td>
                <td><span>+0.88%</span></td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td><span class="flagicon"> </span><a href="#">India</a></td>
                <td>1,417,173,173</td>
                <td>1,428,627,663</td>
                <td><span>+0.81%</span></td>
                <td><a href="#">Asia</a></td>
                <td><a href="#">Southern Asia</a></td>
            </tr>
            <tr>
                <td><span class="flagicon"> </span><a href="#">China</a><sup class="reference">[a]</sup></td>
                <td>1,425,887,337</td>
                <td>1,425,671,352</td>
                <td><span>−0.02%</span></td>
                <td><a href="#">Asia</a></td>
                <td><a href="#">Eastern Asia</a></td>
            </tr>
            <tr>
                <td><span class="flagicon"> </span><a href="#">Invalid Country</a></td>
                <td>N/A</td>
                <td>N/A</td>
                <td><span>N/A</span></td>
                <td><a href="#">Unknown Region</a></td>
                <td><a href="#">Unknown</a></td>
            </tr>
        </tbody>
    </table>
</html>
"""

@pytest.mark.asyncio
async def test_wiki_scraper_parse():
    scraper = WikiScraper()
    results = await scraper.parse(MOCK_HTML)
    
    assert len(results) == 2 
    
    assert results[0]["country_name"] == "India"
    assert results[0]["population"] == 1428627663
    assert results[0]["region_name"] == "Asia"
    assert results[0]["source"] == "wiki"

    assert results[1]["country_name"] == "China"
    assert results[1]["population"] == 1425671352
    assert results[1]["region_name"] == "Asia"
    assert results[1]["source"] == "wiki"