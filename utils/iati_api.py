import requests
import os

from requests.models import PreparedRequest

from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("IATI_API_KEY")

if not API_KEY:
    raise Exception("❌ IATI_API_KEY not found in environment.")


# Full static IATI country list
COUNTRY_CODES = [
    ("AF", "Afghanistan"), ("AL", "Albania"), ("DZ", "Algeria"), ("AD", "Andorra"),
    ("AO", "Angola"), ("AG", "Antigua and Barbuda"), ("AR", "Argentina"),
    ("AM", "Armenia"), ("AU", "Australia"), ("AT", "Austria"), ("AZ", "Azerbaijan"),
    ("BS", "Bahamas"), ("BH", "Bahrain"), ("BD", "Bangladesh"), ("BB", "Barbados"),
    ("BY", "Belarus"), ("BE", "Belgium"), ("BZ", "Belize"), ("BJ", "Benin"),
    ("BT", "Bhutan"), ("BO", "Bolivia"), ("BA", "Bosnia and Herzegovina"),
    ("BW", "Botswana"), ("BR", "Brazil"), ("BN", "Brunei Darussalam"), ("BG", "Bulgaria"),
    ("BF", "Burkina Faso"), ("BI", "Burundi"), ("KH", "Cambodia"), ("CM", "Cameroon"),
    ("CA", "Canada"), ("CV", "Cape Verde"), ("CF", "Central African Republic"),
    ("TD", "Chad"), ("CL", "Chile"), ("CN", "China"), ("CO", "Colombia"),
    ("KM", "Comoros"), ("CG", "Congo"), ("CD", "Congo, Democratic Republic of the"),
    ("CR", "Costa Rica"), ("CI", "Côte d'Ivoire"), ("HR", "Croatia"),
    ("CU", "Cuba"), ("CY", "Cyprus"), ("CZ", "Czech Republic"), ("DK", "Denmark"),
    ("DJ", "Djibouti"), ("DM", "Dominica"), ("DO", "Dominican Republic"),
    ("EC", "Ecuador"), ("EG", "Egypt"), ("SV", "El Salvador"), ("GQ", "Equatorial Guinea"),
    ("ER", "Eritrea"), ("EE", "Estonia"), ("ET", "Ethiopia"), ("FJ", "Fiji"),
    ("FI", "Finland"), ("FR", "France"), ("GA", "Gabon"), ("GM", "Gambia"),
    ("GE", "Georgia"), ("DE", "Germany"), ("GH", "Ghana"), ("GR", "Greece"),
    ("GD", "Grenada"), ("GT", "Guatemala"), ("GN", "Guinea"), ("GW", "Guinea-Bissau"),
    ("GY", "Guyana"), ("HT", "Haiti"), ("HN", "Honduras"), ("HU", "Hungary"),
    ("IS", "Iceland"), ("IN", "India"), ("ID", "Indonesia"), ("IR", "Iran"),
    ("IQ", "Iraq"), ("IE", "Ireland"), ("IL", "Israel"), ("IT", "Italy"),
    ("JM", "Jamaica"), ("JP", "Japan"), ("JO", "Jordan"), ("KZ", "Kazakhstan"),
    ("KE", "Kenya"), ("KI", "Kiribati"), ("KP", "Korea, Democratic People’s Republic of"),
    ("KR", "Korea, Republic of"), ("KW", "Kuwait"), ("KG", "Kyrgyzstan"),
    ("LA", "Lao People’s Democratic Republic"), ("LV", "Latvia"), ("LB", "Lebanon"),
    ("LS", "Lesotho"), ("LR", "Liberia"), ("LY", "Libya"), ("LI", "Liechtenstein"),
    ("LT", "Lithuania"), ("LU", "Luxembourg"), ("MG", "Madagascar"), ("MW", "Malawi"),
    ("MY", "Malaysia"), ("MV", "Maldives"), ("ML", "Mali"), ("MT", "Malta"),
    ("MH", "Marshall Islands"), ("MR", "Mauritania"), (("MU", "Mauritius")),
    ("MX", "Mexico"), ("FM", "Micronesia"), ("MD", "Moldova"), ("MC", "Monaco"),
    ("MN", "Mongolia"), ("ME", "Montenegro"), ("MA", "Morocco"), ("MZ", "Mozambique"),
    ("MM", "Myanmar"), ("NA", "Namibia"), ("NR", "Nauru"), ("NP", "Nepal"),
    ("NL", "Netherlands"), ("NZ", "New Zealand"), ("NI", "Nicaragua"),
    ("NE", "Niger"), ("NG", "Nigeria"), ("MK", "North Macedonia"), ("NO", "Norway"),
    ("OM", "Oman"), ("PK", "Pakistan"), ("PW", "Palau"), ("PA", "Panama"),
    ("PG", "Papua New Guinea"), ("PY", "Paraguay"), ("PE", "Peru"), ("PH", "Philippines"),
    ("PL", "Poland"), ("PT", "Portugal"), ("QA", "Qatar"), ("RO", "Romania"),
    ("RU", "Russian Federation"), ("RW", "Rwanda"), ("KN", "Saint Kitts and Nevis"),
    ("LC", "Saint Lucia"), ("VC", "Saint Vincent and the Grenadines"), ("WS", "Samoa"),
    ("SM", "San Marino"), ("ST", "Sao Tome and Principe"), ("SA", "Saudi Arabia"),
    ("SN", "Senegal"), ("RS", "Serbia"), ("SC", "Seychelles"), ("SL", "Sierra Leone"),
    ("SG", "Singapore"), ("SK", "Slovakia"), ("SI", "Slovenia"), ("SB", "Solomon Islands"),
    ("SO", "Somalia"), ("ZA", "South Africa"), ("SS", "South Sudan"), ("ES", "Spain"),
    ("LK", "Sri Lanka"), ("SD", "Sudan"), ("SR", "Suriname"), ("SE", "Sweden"),
    ("CH", "Switzerland"), ("SY", "Syrian Arab Republic"), ("TJ", "Tajikistan"),
    ("TZ", "Tanzania"), ("TH", "Thailand"), ("TL", "Timor-Leste"), ("TG", "Togo"),
    ("TO", "Tonga"), ("TT", "Trinidad and Tobago"), ("TN", "Tunisia"),
    ("TR", "Turkey"), ("TM", "Turkmenistan"), ("TV", "Tuvalu"), ("UG", "Uganda"),
    ("UA", "Ukraine"), ("AE", "United Arab Emirates"), ("GB", "United Kingdom"),
    ("US", "United States"), ("UY", "Uruguay"), ("UZ", "Uzbekistan"),
    ("VU", "Vanuatu"), ("VE", "Venezuela"), ("VN", "Viet Nam"),
    ("YE", "Yemen"), ("ZM", "Zambia"), ("ZW", "Zimbabwe")
]

SECTOR_CODES = [
    ("111", "Education, level unspecified"),
    ("112", "Basic education"),
    ("113", "Secondary education"),
    ("114", "Post-secondary education"),
    ("121", "Health, general"),
    ("122", "Basic health"),
    ("130", "Population policies / programs & reproductive health"),
    ("140", "Water supply and sanitation"),
    ("150", "Government and civil society"),
    ("160", "Other social infrastructure and services"),
    ("210", "Transport and storage"),
    ("220", "Communications"),
    ("230", "Energy generation and supply"),
    ("240", "Banking and financial services"),
    ("250", "Business and other services"),
    ("311", "Agriculture"),
    ("312", "Forestry"),
    ("313", "Fishing"),
    ("321", "Industry"),
    ("322", "Mineral resources and mining"),
    ("323", "Construction"),
    ("331", "Trade policy and regulations"),
    ("332", "Tourism"),
    ("410", "General environmental protection"),
    ("420", "Women’s equality organisations and institutions"),
    ("430", "Other multisector"),
    ("510", "General budget support"),
    ("520", "Developmental food aid/food security assistance"),
    ("530", "Other commodity assistance"),
    ("600", "Action relating to debt"),
    ("720", "Humanitarian emergency response"),
    ("730", "Reconstruction relief and rehabilitation"),
    ("740", "Disaster prevention and preparedness"),
    ("910", "Administrative costs of donors"),
    ("998", "Unallocated/unspecified"),
]

def get_country_options():
    return COUNTRY_CODES

def get_sector_options():
    return SECTOR_CODES

def extract_code(label):
    return label.split("(")[-1].strip(")") if "(" in label else label


import requests
from requests.models import PreparedRequest

def fetch_iati_activities(country_code, sector_code, year=None, limit=20):
    if not country_code or not sector_code:
        raise ValueError("Country and sector code required.")

    base_url = "https://api.iatistandard.org/datastore/activity/select"

    q_query = f"recipient_country_code:{country_code} AND sector_code:{sector_code}"

    params = [
        ("q", q_query),
        ("rows", limit),
        ("wt", "json"),
    ]

    if year:
        params.append((
            "fq",
            f"activity_date_iso_date:[{year}-01-01T00:00:00Z TO {year}-12-31T23:59:59Z]"
        ))

    headers = {"Ocp-Apim-Subscription-Key": os.getenv("IATI_API_KEY")}

    res = requests.get(base_url, params=params, headers=headers)
    print("🔗 Final URL:", res.url)
    res.raise_for_status()
    return res.json().get("response", {}).get("docs", [])
