from bs4 import BeautifulSoup

def scrape(soup, id):
	highlight_words = soup.find_all(attrs={'class': re.compile(r".*\bwikitable\b.*")})
	print highlight_words
	for word in highlight_words:
		print word
	return highlight_words	

def main():
	soup = BeautifulSoup(open('test.html'))
	wordlist = soup.find_all("a" , {"class" : "ngram"})
	for word in wordlist:
		print ''.join(word.findAll(text=True))

if __name__ == '__main__':
	main()
