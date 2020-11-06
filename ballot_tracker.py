import requests
from bs4 import BeautifulSoup

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
urls = {
    'PA': 'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-pennsylvania-president.html',
    'AZ': 'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-arizona-president.html',
    'GA': 'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-georgia-president.html',
    'NV': 'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-nevada-president.html'
}
# new_leads = {state: 0 for state in urls.keys()} # only run this the first time
# new_totals = {state: 0 for state in urls.keys()} # only run this the first time

old_leads = new_leads.copy()
old_totals = new_totals.copy()
new_leads = {state: 0 for state in urls.keys()}
new_totals = {state: 0 for state in urls.keys()}
for state, url in urls.items():
    page = requests.get(urls[state])
    soup = BeautifulSoup(page.content, 'html.parser')
    biden_tr = soup.find('tr', class_ = 'e-joseph-r-biden')
    trump_tr = soup.find('tr', class_ = 'e-donald-j-trump')
    p_in = soup.find('span', class_="e-est-pct").text.split('%')[0]
    biden = int(biden_tr.find('span', class_ = 'e-votes-display').text.replace(',',''))
    trump = int(trump_tr.find('span', class_ = 'e-votes-display').text.replace(',',''))
    biden_lead = biden-trump
    new_leads[state] = biden_lead
    new_totals[state] = biden+trump
    diff_lead = biden_lead - old_leads[state]
    diff_total = new_totals[state] - old_totals[state]
    symbol = '+' if diff_lead >= 0 else ''
    new_B = int(diff_total/2 + diff_lead/2)
    new_T = int(diff_total/2 - diff_lead/2)
    percent_B = round(100*new_B/diff_total, 1) if diff_total !=0 else 0
    print(f'{state}: {biden_lead:,} on {p_in}% ({symbol}{diff_lead} out of {diff_total} new. B+{new_B}, T+{new_T}, {percent_B}%B)')
