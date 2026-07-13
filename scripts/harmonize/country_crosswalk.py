"""Canonical country set for the Iran Economic Database, and per-source name/code crosswalks.

Add a country here once and every harmonize_*.py script picks it up automatically.
"""

# canonical ISO3 -> display name
COUNTRIES = {
    "IRN": "Iran",
    "KOR": "South Korea",
    "TUR": "Turkey",
    "SAU": "Saudi Arabia",
    "VEN": "Venezuela",
    "USA": "United States",
    "RUS": "Russia",
    "ARG": "Argentina",
    "ESP": "Spain",
    "PRT": "Portugal",
    "GRC": "Greece",
    "DEU": "Germany",
    "FRA": "France",
    "GBR": "United Kingdom",
    "ITA": "Italy",
    "NLD": "Netherlands",
    "SWE": "Sweden",
    "SUN": "USSR (Soviet Union)",  # pre-1991 only; post-1991 data uses RUS
}

# WDI, OWID, and IMF WEO all already key on standard ISO3 codes matching COUNTRIES exactly.

# FAOSTAT's "Area" column uses full UN names, not ISO3 -- map name -> ISO3.
FAOSTAT_AREA_TO_ISO3 = {
    "Iran (Islamic Republic of)": "IRN",
    "Republic of Korea": "KOR",
    "Türkiye": "TUR",
    "Saudi Arabia": "SAU",
    "Venezuela (Bolivarian Republic of)": "VEN",
    "United States of America": "USA",
    "Russian Federation": "RUS",
    "Argentina": "ARG",
    "Spain": "ESP",
    "Portugal": "PRT",
    "Greece": "GRC",
    "Germany": "DEU",
    "France": "FRA",
    "United Kingdom of Great Britain and Northern Ireland": "GBR",
    "Italy": "ITA",
    "Netherlands (Kingdom of the)": "NLD",
    "Sweden": "SWE",
}
