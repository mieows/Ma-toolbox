import os.path, urllib, re
from online.BeautifulSoup.BeautifulSoup import BeautifulSoup
from online.BeautifulSoup.BeautifulSoup import Comment

# gets url and turn into soup object
def fetch(url):
	# fetch url.
	datasource = urllib.urlopen(url)
	if(datasource == None):
		print "---- Error unable to open url"
		exit()

	# given url get the source
	page_content = removeWhiteSpace(datasource.read())
	soup = BeautifulSoup(''.join(page_content))
	
	return soup

# gets url, removes comments, scripts and style tags
def fetchClean(url):	
	# fetch url.
	datasource = urllib.urlopen(url)
	if(datasource == None):
		print "---- Error unable to open url"
		exit()

	# given url get the source
	page_content = removeWhiteSpace(datasource.read())
	soup = BeautifulSoup(''.join(page_content))
		
	# remove comments
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	[comment.extract() for comment in comments]
	
	# remove unwanted tags
	rmlist = [ 'script', 'style', 'img' ]
	for tag in soup.findAll():
		if tag.name.lower() in rmlist:
			tag.extract()

	return soup

# gets url and removes tags, where tag names are specified from args
def fetchSome(url, *args):
	# fetch url.
	datasource = urllib.urlopen(url)
	if(datasource == None):
		print "---- Error unable to open url"
		exit()

	# given url get the source
	page_content = removeWhiteSpace(datasource.read())
	soup = BeautifulSoup(''.join(page_content))
	
	# remove unwanted tags
	for tag in soup.findAll():
		if tag.name.lower() in args:
			tag.extract()
	
	if "comment" or "Comment" or "comments" or "Comments" or "COMMENT" or "COMMENTS" in args:
		# remove comments
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]

	return soup
	
def removeWhiteSpace(datasource):	
	pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
	# remove leading and trailing whitespaces
	datasource = re.sub(pat, '', datasource)   
	# convert newlines to spaces    
	datasource = re.sub('\n', ' ', datasource)
	# remove whitespaces before opening tags
	datasource = re.sub('[\s]+<', '<', datasource)
	# remove whitespaces after closing tags
	datasource = re.sub('>[\s]+', '>', datasource)
	return datasource