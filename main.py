import requests, json, sys, os
import urllib.parse


clr = lambda: os.system('cls' if os.name == 'nt' else 'clear')
url = "http://eprints.polbeng.ac.id/cgi/search/archive/advanced?dataset=archive&screen=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&contributors_name_merge=ALL&contributors_name=&abstract_merge=ALL&abstract=&date=&keywords_merge=ALL&keywords=&subjects_merge=ANY&type=thesis&department=KODEPRODI58301%23RekayasaPerangkatLunak&editors_name_merge=ALL&editors_name=&refereed=EITHER&publication_merge=ALL&publication=&satisfyall=ALL&order=-date%2Fcreators_name%2Ftitle&_action_search=Cari+"


class Scraper:
	def __init__(self, timeout=10) -> None:
		self.timeout = timeout
		self.url = url
		self.base_url = self.url.split("/cgi")[0]
		self.headers = {
			"connection": "keep-alive", 
			"host": "eprints.polbeng.ac.id", 
			"referer": "http://eprints.polbeng.ac.id", 
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
		}

	def network_err(self):
		print(" [!] Please check your internet connection")
		sys.exit()

	def get_json_url(self):
		try: resp = str(requests.get(self.url, headers=self.headers, timeout=self.timeout).text).split('<form method="get" accept-charset="utf-8" action="')[-1].split("</form>")[0]
		except: self.network_err()
		url = "http://eprints.polbeng.ac.id/cgi/search/archive/advanced/export_eprints_JSON.js?dataset=archive&screen=Search&_action_export=1&output=JSON&exp="
		exp = urllib.parse.quote_plus(str(resp.split('id="exp" value="')[-1].split('"')[0]))
		url+=exp
		return url

	def run(self, saveto:str, amount:int):
		try: data = requests.get(self.get_json_url(), headers=self.headers, timeout=self.timeout).json()
		except Exception as e: self.network_err()
		json.dump([{"title": i["title"], "url": i["uri"], "abstract": i["abstract"]} for i in data][:amount], open(saveto, "w"), indent=4)


def preperate():
	while True:
		try:
			amount = int(input(" [*] Enter max abstract amount : "))
			break
		except:
			print(" [!] Invalid input")

	while True:
		saveto = str(input(" [*] Save result to : "))
		if saveto.split(".")[-1] != "json": saveto+=".json"
		if os.path.exists(saveto):
			print(f" [!] File {saveto} already exists, please use other name")
			continue
		break

	return amount, saveto


def main():
	clr()
	amount, saveto = preperate()
	Scraper().run(saveto, amount)
	print(f" [+] {amount} data was scrapped")

if __name__ == "__main__":
	main()
