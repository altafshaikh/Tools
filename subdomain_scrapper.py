'''
websites --> https://crt.sh/
         --> https://censys.io/
'''

import requests
from bs4 import BeautifulSoup
import sys
import os
import json
from termcolor import colored


#censys
import censys.certificates
import censys.ipv4
import censys

#shodan
import shodan


def find_subdomains_cert(domain):

    print('[*] Searching Cert for subdomains of %s' % domain)

    URL = 'https://crt.sh/?q={}'.format(domain)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.findAll("td", {"class": "outer"})
    rows = results[1].findAll('tr')

    fifth_columns = []
    for row in rows[1:]:
        fifth_columns.append(str(row.findAll('td')[4]))

    clean_data = []
    for data in fifth_columns:
        remove_td = data.replace("<td>","").replace('</td>', ',')
        add_comma_br = remove_td.replace("<br>",",").replace('<br/>', ',').replace('*.','')
        clean_data.append(add_comma_br)

    string_data = "".join(clean_data)

    list_of_subdomains = string_data.split(',')
    print('[*] DONE Searching Cert for subdomains of %s' % domain)
    return(set(list_of_subdomains))


def find_subdomains_censys(domain, api_id, api_secret):
    print('[*] Searching Censys for subdomains of %s' % domain)
    try:
        censys_certificates = censys.certificates.CensysCertificates(api_id=api_id, api_secret=api_secret)
        certificate_query = 'parsed.names: %s' % domain
        certificates_search_results = censys_certificates.search(certificate_query, fields=['parsed.names'])
        
        # Flatten the result, and remove duplicates
        subdomains = []
        for search_result in certificates_search_results:
            subdomains.extend(search_result['parsed.names'])
		
        print('[*] DONE Searching Censys for subdomains of %s' % domain)
        return set(subdomains)

    except censys.base.CensysUnauthorizedException:
        sys.stderr.write('[-] Your Censys credentials look invalid.\n')
        exit(1)
    except censys.base.CensysRateLimitExceededException:
        sys.stderr.write('[-] Looks like you exceeded your Censys account limits rate. Exiting\n')
        return set(subdomains)
    except censys.base.CensysException as e:
        # catch the Censys Base exception, example "only 1000 first results are available"
        sys.stderr.write('[-] Something bad happened, ' + repr(e))
        return set(subdomains)


def find_subdomains_shodan(domain, shodan_api):
	SD = [] 
	api = shodan.Shodan(shodan_api)

	if shodan_api == "":
		print("  \__", colored("No Shodan API key configured", "red"))
		return []

	else:
		try:
			results = api.search("hostname:.{0}".format(domain))
			print(results)
			try:
				for res in results["matches"]:
					SD.append("".join(res["hostnames"]))

			except KeyError as errk:
				print("  \__", colored(errk, "red"))
				return []

			SD = set(SD)

			print("  \__ {0}: {1}".format(colored("Unique subdomains found", "cyan"), colored(len(SD), "yellow")))
			return SD

		except shodan.exception.APIError as err:
			print("  \__", colored(err, "red"))
			return []

		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return []


## get unique subdomains
def get_unique_subdomains():
    pass


# # Writing to file 
def save_subdomains_to_file(name,domain,subdomains):
    print('\n[*] Saving %s subdomains into file' % name)

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(parent_dir, 'outputs/')
    try:
        if(not os.path.exists('outputs/')):
            os.mkdir(path)
            if(not os.path.exists('outputs/'+domain)):
                os.mkdir(path+domain)
        else:
            if(not os.path.exists('outputs/'+domain)):
                os.mkdir(path+domain)
    except:
        pass

    file_name = "{}/{}.txt".format(domain,name)
    filepath = os.path.join(path,file_name)

    with open(filepath, "w") as file1: 
        # Writing data to a file 
        for subdomain in subdomains:
            file1.write(str(subdomain)+'\n')

    print('[*] Saving %s Done' % name)

def main(domain, censys_api_id, censys_api_secret):
   
    cert_domains = find_subdomains_cert(domain)
    censys_subdomains = find_subdomains_censys(domain, censys_api_id, censys_api_secret)
    # shodan_subdoains = find_subdomains_shodan(domain, shodan_api)


    uniq_subdomains = cert_domains | censys_subdomains
   
    save_subdomains_to_file("all_subdomains",domain,uniq_subdomains)


if __name__ == "__main__":

    domain = sys.argv[1]

    censys_api_id = None
    censys_api_secret = None
    # shodan_api = None

    if 'CENSYS_API_ID' in os.environ and 'CENSYS_API_SECRET' in os.environ:
        censys_api_id = os.environ['CENSYS_API_ID']
        censys_api_secret = os.environ['CENSYS_API_SECRET']
        # shodan_api = os.environ['SHODAN_API']


    if None in [ censys_api_id, censys_api_secret ]:
        sys.stderr.write('[!] Please set your \n 1. Censys API ID and Censys Secret from your environment \n 2. Set this (CENSYS_API_ID and CENSYS_API_SECRET and SHODAN_API) variables\n using export VARIABLENAME="value" \n')
        exit(1)

    main(domain, censys_api_id, censys_api_secret)