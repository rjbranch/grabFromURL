__author__ = 'Ryan'
import urllib2
from cStringIO import StringIO
import re
import sys
import os
import errno
import csv

class File:
	#Default constructor
	def __init__(self):
		self.link = ""

	#Constructor Method
	def __init__(self, link_):
		self.link = link_

	#Set function for link
	def setLink(self, linkIn):
		self.link = linkIn

	#Get function for link
	def getLink(self):
		return self.link

class Site:
	#Default constructor
	def __init__(self):
		self.name = ""
		self.url = ""
		self.page = 0
		self.files = []
		self.success = False

	#Constructor Method
	def __init__(self, url_, page_):
		self.name = ""
		self.url = url_
		self.page = page_
		self.files = []
		self.success = False

	#Set function for name
	def setName(self, nameIn):
		self.name = nameIn

	#Get function for name
	def getName(self):
		return self.name

	#Set function for url
	def setUrl(self, urlIn):
		self.url = urlIn

	#Get function for url
	def getUrl(self):
		return self.url

	#Set function for page
	def setPage(self, numIn):
		self.page = numIn

	#Get function for page
	def getPage(self):
		return self.page

	#Function to add a file to the end of "files"
	def addFile(self, fileIn):
		self.files.append(fileIn)

	#Function to return the file at a given index of "files"
	def getFile(self, index):
		return self.files[index]

	#Function to return the entire "files" list
	def getFiles(self):
		return self.files

	#Set function for success
	def setSuccess(self, successIn):
		self.success = successIn

	#Get function for success
	def getSuccess(self):
		return self.success


class Search:
	#Default constructor
	def __init__(self):
		self.name = ""
		self.term = ""
		self.numPages = 0
		self.sites = []
		self.maxDownloads = 0

	#Constructor Method
	def __init__(self, term_, numPages_, maxDownloads_):
		self.name = ""
		self.term = term_
		self.numPages = numPages_
		self.sites = []
		self.maxDownloads = maxDownloads_

	#Set function for name
	def setName(self, nameIn):
		self.name = nameIn

	#Get function for name
	def getName(self):
		return self.name

	#Set function for term
	def setTerm(self, termIn):
		self.term = termIn

	#Get function for term
	def getTerm(self):
		return self.term

	#Set function for nunPages
	def setNumPages(self, numIn):
		self.numPages = numIn

	#Get function for numPages
	def getNumPages(self):
		return self.numPages

	#Function to add a Site to the end of "sites"
	def addSite(self, siteIn):
		self.sites.append(siteIn)

	#Function to return the Site at a given index of "sites"
	def getSite(self, index):
		return self.sites[index]

	#Function to return the entire "sites" list
	def getSites(self):
		return self.sites

	#Set function for maxDownloads
	def setMaxDownloads(self, numIn):
		self.maxDownloads = numIn

	#Get function for maxDownloads
	def getMaxDownloads(self):
		return self.maxDownloads

class Container:
	#Default constructor
	def __init__(self):
		self.inFileName = "default.txt"
		self.folderName = "default_txt"
		self.searches = []
		self.extensions = []
		self.rowNum = 0

	#Makes tree of directories to store results
	def makeFolders(self):
		for search in self.searches:
			for i in range(search.getNumPages()):
				try:
					os.makedirs(self.folderName + "/" + search.getTerm() + "/" + str(i + 1))
				except OSError as exception:
					if exception.errno != errno.EEXIST:
						raise

	#Set function for inFileName
	def setInFileName(self, nameIn):
		self.inFileName = nameIn

	#Get function for inFileName
	def getInFileName(self):
		return self.inFileName

	#Set function for folderName
	def setFolderName(self, nameIn):
		self.folderName = nameIn

	#Get function for folderName
	def getFolderName(self):
		return self.folderName

	#Function to add a Search to the end of "searches"
	def addSearch(self, searchIn):
		self.searches.append(searchIn)

	#Function to return the Search at a given index of "searches"
	def getSearch(self, index):
		return self.searches[index]

	#Function to return the entire "searches" list
	def getSearches(self):
		return self.searches

	#Function to add a string to the end of "extensions"
	def addExtension(self, extensionIn):
		self.extensions.append(extensionIn)

	#Function to return the extension at a given index of "extensions"
	def getExtension(self, index):
		return self.extensions[index]

	#Function to return the entire "extensions" list
	def getExtensions(self):
		return self.extensions

	#Set function for rowNum
	def setRowNum(self, numIn):
		self.rowNum = numIn

	#Get function for rowNum
	def getRowNum(self):
		return self.rowNum

def buildLinks(sit, exts, numDownloads):
	url = sit.getUrl()
	try:
		response = urllib2.urlopen(url)
	except:
		print('Cannot read HTML: ' + url)
		return False
	html = response.read()
	content = StringIO(html)
	numLinks = 0
	for line in content:
		for ext in exts:
			if ((ext in line) and (numLinks < numDownloads)):
				try:
					link = re.search("href=\"(.+?)" + ext + "\"", line).group(1)
					if ">" not in link:
						link = url + link + ext
						sit.addLink(link)
						numLinks += 1
					break
				except:
					#This often occurs if a link is preceded by an icon,
					#for example "sound2.gif" preceding a .mp3 file.
					pass

def checkUrl(url):
	title = ""

	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
		response = opener.open(url)
	except:
		print('Cannot parse HTML: ' + url)
		return title

	html = response.read()
	content = StringIO(html)
	for line in content:
		if "<title>Index of /" in line:
			try:
				title = re.search("<title>Index of (.+?)</title>", line).group(1)
				break
			except:
				#This can occur if the HTML of the page is formatted strangely,
				#for example if the title is spread throughout multiple lines
				pass
	return title

def fileInput(cont):
	data = open(cont.getInFileName(), 'rb')
	reader = csv.reader(data)

	for row in reader:
		#Gets extension data
		if (cont.getRowNum() == 0):
			for col in row:
				cont.addExtension(col)
			cont.setRowNum(cont.getRowNum() + 1)
		#Gets search term data
		else:
			#Creates a new Search object with the specified term and number of pages
			cont.addSearch(Search(row[0], int(row[1]), int(row[2])))

	#All objects are now read in
	data.close
	cont.makeFolders()

def parseGoogle(search, searchTerm, index):
	url = getSearchURL(searchTerm, index)

	print("CANDIDATES: " + "(Page " + str(index) + ")")
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
		response = opener.open(url)
	except:
		print('Cannot read Google Search HTML: ' + url)
		return False
	html = response.read()
	try:
		links = re.findall("href=\"http(.+?)\"", html)
	except:
		print("Could not retrieve links from search results page.")
	for link in links:
		if "google" not in link:
			link = "http" + link
			if (link[-1] != '/'):
				link = link + '/'
			print(link)
			search.addSite(Site(link, index))

def buildURLs(cont):
	for theSearch in cont.getSearches():
		for i in range(theSearch.getNumPages()):
			parseGoogle(theSearch, theSearch.getTerm(), i + 1)

def makeFilename(nameIn):
	nameOut = ""
	for char in nameIn:
		if char in "\\/:*?\"<>|":
			nameOut += "-"
		else:
			nameOut += char
	return nameOut

def getSearchURL(term, pageNum):
	tempName = ""
	for char in term:
		if (char == ' '):
			tempName += "+"
		else:
			tempName += char
	return "https://www.google.com/search?q=" + tempName + "&start=" + str((pageNum - 1) * 10)

def download(cont):
	for search in cont.getSearches():
		for site in search.getSites():
			for file in site.getFiles():
				link = file.getLink()
				path = cont.getFolderName() + "/" + search.getTerm() + "/" + str(site.getPage())
				if site.getName()[0] != "/":
					path = path + "/"
				path = path +  site.getName()
				try:
					os.makedirs(path)
				except OSError as exception:
					if exception.errno != errno.EEXIST:
						raise
				try:
					f = urllib2.urlopen(link)
					print("Downloading " + link)
					path = path + "/" + os.path.basename(link)
					with open(path, "wb") as file:
						file.write(f.read())
				except:
					print("ERROR: Could not download " + link)

def main():
	container = Container()
	container.setInFileName
	if(len(sys.argv) == 2):
		container.setInFileName(sys.argv[1])
		tempName = ""
		for char in sys.argv[1]:
			if (char == '.'):
				tempName += "_"
			else:
				tempName += char
		container.setFolderName(tempName)

	fileInput(container)
	buildURLs(container)

	for search in container.getSearches():
		for site in search.getSites():
			directoryName = checkUrl(site.getUrl())
			if(directoryName != ""):
				site.setName(directoryName)
				print("DIRECTORY NAME: " + directoryName)
				site.setSuccess(True)
			else:
				site.setSuccess(False)

	for search in container.getSearches():
		for site in search.getSites():
			if site.getSuccess():
				buildLinks(site, container.getExtensions(), search.getMaxDownloads())

	download(container)

main()