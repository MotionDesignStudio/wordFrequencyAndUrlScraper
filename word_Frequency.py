#!/usr/bin/env python3.5

import sys
#
import re
#
from collections import Counter
#
import urllib.request as urllib2
#
from bs4 import BeautifulSoup
#
import random
#
import urllib.robotparser as robotparser
#
#from urllib import parse
#
import urllib.parse as urlparse
#
from html.parser import HTMLParser
#
from time import sleep
#
import os

class wordFrequency:

	def __init__ (self, url=None, file_source=None, number_to_display=200):
		self.url = url
		self.file_source = file_source
		self.number_to_display= number_to_display


	def randomize_user_agent(self):
		#randomize user agents
		u1="Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1"
		u2="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
		u3="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		u4="Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1"
		u5="Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
		u6="Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
		u7="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"

		return eval("u"+str( random.randrange (1,8) ) )
	
	def frequency_in_file(self):
		cnt = Counter()
		string_to_return= ""
		f = open(self.file_source, "r").read()
		#This catches all words with letters in them only.
		extract_all_words_to_list=re.findall('([A-Z][A-Z]+)\s', f, flags=re.IGNORECASE )
		for word in extract_all_words_to_list:
			cnt[word]+=1

		#Removing Stop Words
		with open("stopwords.txt", "r") as f:
			for line in f:
				del cnt[line.rstrip()]
				#Bellow will remove the stop word(s) if the first letter is capitalized.  This could
				#be from punctuation if starting a sentence
				del cnt[line.rstrip().title()]


		for item in cnt.most_common(self.number_to_display):
			string_to_return+= "%s , %s " % ( item[0], item[1] ) 
		return string_to_return

	def get_surrounding_words(self, word_to_search_for, left, right):
		string_to_return= ""
		#((?:\w*\W*){5})\W*wow\W*((?:\W*\w*){2})
		#search_for_word_and_words_around_it_regex = re.compile (r'((?:\w*\W*){5})\W*Christmas\W*((?:\W*\w*){2})')
		# Below will find complete sentences
		#((?:\w*\s*){4})\s*wow\s*((?:\s*\w*){3}) 
		#search_for_word_and_words_around_it_regex = re.compile (r'((\w*\s*){0,9})Christmas((\s*\w*){0,9})')
		
		search_for_word_and_words_around_it_regex = re.compile (r'((\S+\s+){0,'+str(left)+'}'+word_to_search_for+'(\s+\S+){0,'+str(right)+'})')
		f = open(self.file_source, "r").read()
	
		counter = 1
		for sentence in list(search_for_word_and_words_around_it_regex.findall(f)):
			string_to_return+= "%s: %s %s" % ( counter, sentence[0], '\r' ) 
			counter+=1
		return string_to_return

	def display_text_only(self):
		soup = BeautifulSoup( download(self.url), "html5lib" )
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
		text = soup.getText()
		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)

		return text

	def crawl_sitemap (self, retry_rate=15):
		# download site
		sitemap = download(self.url)
		# extract site map links
		links = re.findall('<loc>(.*?)</loc>', str ( sitemap ))
		# download each link

		fo = open(urlparse.urlparse(self.url).netloc + ".txt", "a")
				
		for link in links:
			print ("Downloading url %s from %s sitemap :" % (link , urlparse.urlparse(self.url).netloc) )
			# Download text from a web url
			outputme="<url :::> ", self.url, " </url>", display_text_only( link )
			outputme=str (outputme )		
			fo.write( outputme)
			sleep(retry_rate)

		fo.close

	## Web Scraping Below ##
	###		      ###


	def scrape_all_websites_text (self, link_regex, max_depth=-1, retry_rate=15, robots_file=None):
		# keep track which URL's have seen before
		seen = {}

		# Max_depth is to help avoid Spider Trap set it to set maximun number of searches

		#Crawl from the given seed URL following links matched by link_regex
		crawl_queue = [ self.url ]
		# keep track which URL's have seen before
		seen = {self.url:0}
	
		# track how many urls have been downloaded
		num_urls=0

		if robots_file == None:
			print ("No robots file has been specified I will provide a fake file. \nThis is not wise.  You might be banned for entering a restricted directory.")
			robots_file = urlparse.urljoin('file:', urllib2.pathname2url(os.path.abspath('default_robots.txt')))

		#set robots file
		rp = robotparser.RobotFileParser()
		rp.set_url(robots_file)
		rp.read()
	
		while crawl_queue:
			url = crawl_queue.pop()
			# Check url passes robots.txt restrictions
			if rp.can_fetch (randomize_user_agent(), url):
				html = download ( url )

				# Download the text for the web page
				outputme="<url :::> ", url, " </url>", display_text_only( url )
				outputme=str (outputme )
				#print ( outputme )
				fo = open(urlparse.urlparse(self.url).netloc + ".txt", "a")
				fo.write( outputme);
				fo.close			
	
				links = []
				depth = seen [url]

				if depth != max_depth:
					# can continue crawling further

					if link_regex: 
						# Filter for link(s) matching our regular expression
						links.extend(link for link in get_links(html) if re.match (link_regex, link) )
				for link in links:
					link = normalize(self.url, link)
					# check whether already crawled this link
					if link not in seen:
					#if link not in seen and not in list_of_bad_urls:
				
						seen[link]= depth+1
						# check link is within same domain
						if same_domain (self.url, link):
							# success! add this new link to queue
							crawl_queue.append (link)

				# check whether have reached downloaded maximum
				num_urls+=1
				if num_urls == max_depth:
					break	
			else:
				print ('Blocked by robots.txt', url)
			print ( seen)
			sleep(retry_rate)


	def download(self, num_retries=2):
		#print ('Downloading:', url)

		headers = { 'User-Agent': randomize_user_agent() }
	
		request = urllib2.Request(self.url, headers=headers)
		try:
			html = urllib2.urlopen(request).read()
		except urllib2.URLError as e:
			print ('Download error:', e.reason , " code :", e.code, " url: ", url)
			html = ''
			if num_retries>0:
				if hasattr(e, 'code') and 500 <= e.code < 600:
					# recursivly retry 5xx HTTP errors
					return download (url, num_retries-1)			
		return str ( html )

	def normalize(self, seed_url, link):
	    # Normalize this URL by removing hash and adding domain
	    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
	    return urlparse.urljoin(seed_url, link)

	def same_domain(self, url1, url2):
	    #Return True if both URL's belong to same domain
	    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

	def get_links(self, html):
		# Return a list of links from html
		# To add addition files to search for (?<!\.(?:jpeg|ciss)) If they are long extensions (?<!\.(?:jpegg|cisss))
		webpage_regex = re.compile (r'''(?i)<a[^>]+?href=["'](?!#)([^"']+)(?<!\.(?:jpeg|xlsx|docx))(?<!\.(?:jpg|png|pdf|gif|xls|doc))["']''', re.IGNORECASE)

		# List all links from the webpage
		# Using set to remove redundacies and convert back to list
		return list (set ( webpage_regex.findall(html) ) )






#Download a wesite using the sitemap and display its text without html
#example=wordFrequency(url="http://mo-de.net/sitemap.xml")
#print ( example.crawl_sitemap( retry_rate=15) )

#Download all the pages from a website and display its text without html
#example=wordFrequency(url="http://mustpassarobotsfile.com/")
#example.scrape_all_websites_text( link_regex='/*', max_depth=-1, retry_rate = 15, robots_file='http://mustpassarobotsfile.com/robots.txt' )

#Download a SINGLE webpage and display its text without html
#example=wordFrequency(url="http://mo-de.net/acrobaticyoga")
#print ( example.display_text_only( ) )

#Download a webpage and display its text
#example=wordFrequency(url="http://mo-de.net/acrobaticyoga")
#print ( example.download( num_retries=2 ) )


#Search for specific amount of words left or right of a specified word
#example=wordFrequency(file_source="my_text_file.txt", number_to_display = 20)
#print ( example.get_surrounding_words("Christmas", 4, 4) )

