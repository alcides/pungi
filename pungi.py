#!/usr/bin/python

"""
Pungi Framework v0.1

Module Dependicies:
	sys
	os
	re
	cgi
	MySQLdb ( http://sourceforge.net/projects/mysql-python )
	
General Variables:
	server
		server['name'] - Server's name
		server['query'] - Everything in the URL after the ?
		server['client_ip'] - Visitor's IP
		server['client'] - Visitor's browser information
		server['script'] - Filename

	get
		get['foo'] - returns 'bar' if the url ends in ....?foo=bar
	post
		post['foo'] - returns all the fields in the form submited in a dictionary

		
Notes:
	1) If you want to use the autoTable, you MUST have a auto_increment primary key with the name 'id'
	2) If you want to set a field as a password one, you'll have to add a comment saying 'pass' to the field.
	3) This Framework is always being updated, your suggestions will be useful, so drop us a post ;)
		
To Do:
	1) Support relations between the tables
	2) Maybe add TinyMCE and some javascript library.
	3) AJAX or something
		
		
		
© 2007 - Alcides Fonseca. All Rights Reserved.
"""

# Built-in Imports
import sys
import os

# Check if it's not running from the console.
#if 'SCRIPT_NAME' not in os.environ:
#	print 'This is a web script.\n Visit http://pungi.sourceforge.net for more details. '
#	raw_input()
#	sys.exit()

# General Imports
import re
import cgi
from Cookie import SimpleCookie

# General Variables
if 'SCRIPT_NAME' in os.environ:
	server={}
	server.update({'name':os.environ['SERVER_NAME']})
	server.update({'query':os.environ['QUERY_STRING']})
	server.update({'client_ip':os.environ['REMOTE_ADDR']})
	server.update({'client':os.environ['HTTP_USER_AGENT']})
	server.update({'script':os.environ['SCRIPT_NAME']})

	# Parse query string
	parts=server['query'].split("&")
	get={}
	for part in parts:
		segment=part.split("=")
		try:
			segment[1]=int(segment[1])
		except:
			try:
				segment[1]=float(segment[1])
			except:
				pass
		if len(segment) > 1:
			get.update({segment[0]:segment[1]})

	# Post variables
	dict=cgi.FieldStorage()
	post={}
	post_files={}
	for part in dict:
		if dict[part].filename != None:
			post.update({part:dict[part].filename})
			post_files.update({part:dict[part]})
		else:
			post.update({part:dict[part].value})
	# Cookies
	if os.environ.has_key('HTTP_COOKIE'):
		cookies = SimpleCookie(os.environ['HTTP_COOKIE'])
	else:
		cookies = SimpleCookie()
else:
	get={}
	post={}
	server={}
	cookies={}
		
def writeget(dict):
	"""Writes the URL from of the get dictionary"""
	url='?'
	for item in dict:
		url += str(item) + '=' + str(dict[item]) + '&'
	if len(dict):
		return url[:-1]	
	else:
		return url
		
def upload(data,dir):
	"""Uploads the data into the given dir. Usually data, is the post_files."""
	uploaded=[]
	if not os.path.exists(dir):
		os.mkdir(dir,0777)
	for elem in data:
		if data[elem].filename != None:
		
			# Binary mode in Windows
			try:
				import msvcrt       
			except ImportError:
				pass
			else:
				for fd in(0,1):
					msvcrt.setmode(fd, os.O_BINARY)
					
			#Write the file in the dir.
			file=dir+os.sep+data[elem].filename
			o = open(file,"wb")
			o.write(data[elem].value)
			o.close()
			uploaded.append(file)
	return uploaded		
	
	
def start_output():
	"""Prints the first line so it's a HTML file. You should use this function before the first print"""
	global cookies
	if len(cookies.keys()) > 0:
		return str(cookies) + """\nContent-type: text/html\n"""
	else:
		return """Content-type: text/html\n"""
	
def escape(s, quote=None):
    """Replace special characters '&', '<' and '>' by SGML entities."""
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s
	
def dbescape(s):
	""" Escapes string for MySQL insertion """
	if s:
		import MySQLdb
		return MySQLdb.escape_string(s)
		#return s.replace("\"","\\\"").replace("'","\'")
	else:
		return "NULL"

def link(desc,url):
	""" Links the text 'desc' to the 'url'. In fact, it's only a helper for the HTML <a> tag. """
	return "<a href='" + url + "'>" + desc + "</a>"
	
def img(src,alt='',url=''):
	""" Just a helper for HTML <img> tag. You can set it's source, alternative text and if you want, the url it's linked to. """
	if url:
		return link('<img src=' + src + ' border=0 alt="' + alt + '">',url)
	else:
		return '<img src=' + src + ' border=0 alt="' + alt + '">'

def css_link(src):
	""" Includes the source as a CSS in the header."""
	return "<link rel=\"stylesheet\" type=\"text/css\" href=\"" + src + "\" />"
	
def js_link(src):
	""" Includes the source as a CSS in the header."""
	return "<script language=\"JavaScript\" type=\"text/javascript\" src=\"" + src + "\" /></script>"

def rss_link(src,title=''):
	""" Includes the source as a RSS file. """
	return "<link rel=\"alternate\" type=\"application/rss+xml\" title=\"" + title + "\" href=\"" + src + "\" />"
	
def keywords(keys):
	""" Includes the meta header for the search engine keywords. """
	return "<meta name=\"keywords\" content=\"" + keys +"\" />"

def redirect(url):
	"""Redirects to the url given. You cannot send any HTML header before."""
	print "Location: " + url
	print
	
def debug():
	"""Just a debug window. Add it at the end of output"""
	rt='<div id=debug style="font-family: verdana; font-size: 10; padding: 5px; color: black; background-color: white; border: solid black 1px; position: absolute; top: 50px; left: 50px; 	filter: alpha(opacity=80); -moz-opacity: 0.8; opacity: 0.8;">'
	rt += '<b>Server Information:</b><br/>'
	for item in server:
		rt += str(item) + ': ' + str(server[item]) + '<br>'
	rt += '<br><b>GET Information:</b><br/>'
	for item in get:
		rt += str(item) + ': ' + str(get[item]) + '<br>'
	rt += '<br /><b>POST Information:</b><br/>'
	for item in post:
		rt += str(item) + ': ' + str(post[item]) + '<br>'
	rt +='</div>'
	return rt
	
def log(str,file='log.txt'):
	""" Adds to the log file that information. Used for debugging"""
	f = open(file,'a')
	f.write(str + "\n")
	
def nl2br(str):
	"""Converts the new lines (\n) in the string to <br /> tags"""
	return str.replace("\n","<br />")
	
def wordwrap(L,margin=80):
	""" Word Wrap the string to a certains number of chars per line. Defaul is 80"""
	b=""
	for a in L:
		if len(str(a)+b)+3 >= margin :
			print b
			b = "'"+str(a)+"'"
		else:
			if b: b+=","
			b += "'"+str(a)+"'"
	if b: print b
	b=""
	
def timef(t,format="%d of %B of %Y - (%H:%M)"):
	""" Function to convert the unix time in a readable format"""
	import time
	return time.strftime(format,time.localtime(float(t)))

_url_encre = re.compile(r"[^A-Za-z0-9_.!~*()-]") # RFC 2396 section 2.3
_url_decre = re.compile(r"%([0-9A-Fa-f]{2})")
_html_encre = re.compile("[&<>\"'+]")
# '+' is encoded because it is special in UTF-7, which the browser may select
# automatically if the content-type header does not specify the character
# encoding. This is paranoia and is not bulletproof, but it does no harm. See
# section 4 of www.microsoft.com/technet/security/news/csoverv.mspx
_html_encodes = { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;",
                  "'": "&#39;", "+": "&#43;" }

def html_encode(raw):
	"""Return the string parameter HTML-encoded."""
	"""
	Specifically, the following characters are encoded as entities:
	 & < > " ' +
	"""
	if not isinstance(raw, unicode):
		raw = str(raw)
	return re.sub(_html_encre, lambda m: _html_encodes[m.group(0)], raw)

def url_encode(raw):
	"""Return the string parameter URL-encoded."""
	if not isinstance(raw, unicode):
		raw = str(raw)
	return re.sub(_url_encre, lambda m: "%%%02X" % ord(m.group(0)), raw)

def url_decode(enc):
	"""Return the string parameter URL-decoded (including '+' -> ' ')."""
	s = enc.replace("+", " ")
	return re.sub(_url_decre, lambda m: chr(int(m.group(1), 16)), s)
	
	
#--------------------------------------------------------------------------------------------------------------------------------------------------
	
class Page:
	"""This class represents the final page"""
	def __init__(self,template=""):
		"Sets the template and add default tags."
		self.file=template
		self.tags={'pungi':"<a href='http://pungi.sourceforge.net' target='_blank'><img src='http://pungi.sourceforge.net/pungi.png' border=0></a>"}
		
	def add_tag(self,tag,text):
		"Adds a tag to be parsed in the template"
		self.tags.update({tag:text})
		
	def output(self):
		"Returns the final HTML from the template"
		r=''
		if self.file != "":
			f=open(self.file,'r')
			for line in f:
				r+=line
			f.close()
			for tag in self.tags.iterkeys():
				r=r.replace('<%' + str(tag) + '%>',str(self.tags[tag]))
		return r

#--------------------------------------------------------------------------------------------------------------------------------------------------
		
class DB:
	"""MySQL Handler"""
	def __init__(self,server,username,password,database):
		import MySQLdb
		try:
			self.conn = MySQLdb.connect(host = server, user = username, passwd = password , db = database)
			self.username = username
			self.database = database
			self.cur = self.conn.cursor()
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)
	
	def close(self):
		"""Closes the connection"""
		self.conn.close()
	
	def query(self,str,single = 0):
		"""Executs the query and returns the most likely wanted values"""
		log("MySQL Query: " + str)
		self.cur.execute(str.decode('ISO-8859-1'))
		if 'select' in str.lower():
			if single:
				if cursor.rowcount > 0:
					return self.cur.fetchone()
				else:
					return ""
			else:
				return self.cur.fetchall()
		elif 'show' in str.lower():
			if single:
				if cursor.rowcount > 0:
					return self.cur.fetchone()[0]
				else:
					return ""
			else:
				return [ i[0] for i in self.cur.fetchall()]
		elif 'update' in str.lower():
			return self.cur.rowcount
		elif 'insert' in str.lower():
			try:
				return self.cur.lastrowid
			except:
				return self.cur.rowcount
		else:
			return 0
			
	def version(self):
		"""Returns the MySQL version"""
		return self.query('SELECT VERSION()',1)[0]

		
class autoDB(DB):
	"""Converts the database in a workable class"""
	def __init__(self,*arg):
		DB.__init__(self,*arg)
		self.tables={}
		self.update()
	
	def __str__(self):
		return self.database
		
	def __getattr__(self, name):
		return self.tables[name]
	
	def __getitem__(self, name):
		return self.tables[name]
		
	def update(self):
		"""Gets all the information from the database"""
		self.tables={}
		for i in self.query('SHOW TABLES;'):
			self.tables.update({i:autoTable(i,self)})
			
	def listtables(self,relative=1):
		"""Lists all the tables in HTML format"""
		if len(get) and relative:
			if 'table' in get:
				nget=get.copy()
				nget.pop('table')
				if len(nget):
					bef= writeget(nget) + '&'
				else:
					bef='?'
			else:
				if len(get):
					bef= writeget(get) + '&'
				else:
					bef='?'
		else:
			bef= '?'
		ret='<ul>'
		for table in self.tables:
			ret+='<li><a href='+bef+'table=' + str(table) + '>' + str(table) + '</a></li>'
		ret+='</ul>'
		return ret
			

		
class autoTable:
	"""Object representation of a database table"""
	def __init__(self,name,db,update=1):
		self.name=name
		self.db=db
		self.content={}
		self.columns=self.db.query('SHOW COLUMNS FROM ' + self.name)
		self.rows=[]
		self.index=0
		if update:
			self.update()
		
	def __str__(self):
		return self.name
		
	def __add__(self, other):
		return str(self.name) + str(other)
		
	def __getitem__(self, key):
		"""Returns the row with the specified id."""
		result=self.where("id ='" + str(key) +"'")
		if len(result) == 0:
			return None
		else:
			return autoRow(result[0].content,self)
			
	def __setitem__(self, key, value):
		if key in self.content:
			if type(value) == type({}):
				self.edit(key,value)
			else:
				return 0
		else:
			if type(value) == type({}):
				self.insert(value)
			else:
				return 0

	def __contains__(self, item):
		return item in self.content
	
	def __iter__(self):
		return self
		
	def next(self):
		if self.index == len(self.content):
			self.index=0
			raise StopIteration
		row=self.content[self.index]
		self.index += 1
		return autoRow(row,self)

	def __len__(self):
		return len(self.content)
	
	def first(self):
		"""Returns the first row"""
		return autoRow(self.content[0],self)
		
	def last(self):
		"""Returns the last row"""
		return autoRow(self.content[-1],self)
		
	
	def update(self,order='id ASC'):
		"""Updates the class structure from the database."""
		self.columns=self.db.query('SHOW COLUMNS FROM ' + self.name)
		self.rows=self.db.query('SELECT * FROM ' + self.name + ' ORDER BY ' + order)
		self.content=[]
		for row in self.rows:
			dict={}
			for field in range(len(row)):
				dict.update({self.columns[field]:row[field]})
			self.content.append(dict)
			
	def where(self,wh,order='id ASC'):
		"""Returns the result of the query using the where and order arguments. Default is ordered by id ascendent"""
		self.rows=self.db.query('SELECT * FROM ' + self.name + ' WHERE ' + wh + ' ORDER BY ' + order)
		results=[]
		for row in self.rows:
			dict={}
			for field in range(len(row)):
				dict.update({self.columns[field]:row[field]})
			results.append(autoRow(dict,self))
		return results
	
	def row(self,id):
		"""Returns the row with the specified id."""
		result=self.where('id =' + str(id))
		if len(result) == 0:
			return None
		else:
			return autoRow(result[0].content,self)
	
	def clear(self):
		"""Deletes all the rows from the table."""
		self.db.query('DELETE FROM ' + self.name + ' WHERE id > 0')
		self.content=[]
		return 'Cleared.'
	
	def delete(self,id):
		"""Deletes a specified row from the table."""
		self.db.query('DELETE FROM ' + self.name + ' WHERE id = ' + str(id))
		for row in self.content:
			if row['id'] == key:
				self.content.remove(row)
		return 'Deleted.'
	
	def showtable(self,columns='',edit=1,delete=1,new=1):
		"""Builds a table for showing the table with the defined settings"""
		if columns=='':
			columns=self.columns
		if server['query'] !='':
			bef= '?' + server['query'] + '&'
		else:
			bef= '?'
		
		body=''
		if  'insert' in get:
			body = self.insert(post)
		elif 'edit' in get:
			if 'action' in get and get['action'] == 'do':
				body=self.edit(get['edit'],post)
			else:
				body = self.editForm(get['edit'])
		elif 'delete' in get:
			body=self.delete(get['delete'])
		else:
			body+='<table><tr>'
			for col in self.columns:
				body+='<td><b>' + str(col) + '</b></td>'
			body+='<td colspan=2></td></tr>'
			tables=[ i for i in self.db.query('SHOW TABLES;') ]
			for row in self.content:
				body+='<tr>'
				for col in columns:
					if col[-3:] == '_id' and col[:-3] in tables:
						# Relations N - 1
						ocolumns = self.db.query('SHOW COLUMNS FROM ' + col[:-3])
						orows=self.db.query('SELECT ' + ocolumns[0] + ', ' + ocolumns[1] + ' FROM ' + col[:-3] + ' WHERE id=' + str(row[col]))
						dict={}
						body += '<td>'
						for orow in orows:
							body += str(orow[1]) +' (' + str(orow[0]) + ')<br>'
						body += '</td>'
					else:
						body += '<td>' + str(row[col]) + '</td>'
				body+='<td><a href='+bef+'edit=' + str(row['id'])  + '>Edit</a></td><td><a href='+bef+'delete=' + str(row['id'])  + '>Delete</a></td></tr>'
			body += '</table><br><hr><br>'
			body += self.insertForm()
		return body
	
	def edit(self,id,dict):
		"""Edits the values of a record from a dictionary."""
		q='UPDATE ' + self.name + ' SET '
		c=0
		for item in dict:
			if item != 'id':
				if item in self.columns:
					q += dbescape(str(item)) + "='" + dbescape(str(dict[item])) + "', "
					c+=1
		if c > 0:
			q = q[:-2] + " WHERE id = " + str(id)
			k=self.db.query(q)
			self.update()
			return 'Edited ' + str(k) + ' rows.'
		else:
			return 'Error.'
	
	def editForm(self,id,table=1):
		"""Creates the Form to edit a row in this table with that exact id"""	
		if table:
			form=tableForm(server['query'] + '&action=do')
		else:
			form=Form(server['query'] + '&action=do')
		tables=[ i for i in self.db.query('SHOW TABLES;') ]
		for row in self.content:
			if str(row['id']) == str(id):
				self.db.cur.execute('SHOW FULL COLUMNS FROM ' + self.name)
				tb = self.db.cur.fetchall()
				for field in tb:
					fname = field[0]
					ftype = field[1]
					fdefault = field[5]
					fcomment = field[8]
					fdesc = fname[0].upper() + fname[1:].lower() + ':'
					if fname == 'id':
						form.hidden(fname,row[fname])
					elif fname[-3:] == '_id' and fname[:-3] in tables:
						# Relations N - 1
						ocolumns = self.db.query('SHOW COLUMNS FROM ' + fname[:-3])
						orows=self.db.query('SELECT ' + ocolumns[0] + ', ' + ocolumns[1] + ' FROM ' + fname[:-3])
						dict={}
						for orow in orows:
							dict.update({orow[1]:orow[0]})
						if table:
							form.select(fdesc,fname,dict,row[fname])
						else:
							form.select(fname,dict,row[fname])						
					elif ftype == 'text':
						if table:
							form.text(fdesc,fname,row[fname])
						else:
							form.text(fname,row[fname])
					elif fcomment == 'pass':
						if table:
							form.pwd(fdesc,fname,row[fname])
						else:
							form.pwd(fname,row[fname])
					else:
						if table:
							form.input(fdesc,fname,row[fname])
						else:
							form.input(fname,row[fname])
		form.submit('Edit')
		return form.end()

	def insert(self,dict):
		"""Edits the values of a record from a dictionary."""
		q='INSERT INTO ' + self.name + ' ('
		for item in dict:
			q += str(item) + ','
		q = q[:-1] + ') VALUES('
		for item in dict:
			if item == 'id':
				q += "'',"
			else:
				q += "'" + dbescape(str(dict[item])) + "',"	
		q = q[:-1] + ');'
		id = self.db.query(q)
		self.update()
		return id
		
	def insertForm(self,table=1,filled={}):
		"""Creates the Form to insert a new row in this table"""
		if table:
			form=tableForm(server['query'] + '&insert=true&action=do')
		else:
			form=Form(server['query'] + '&insert=true&action=do')
			
		self.db.cur.execute('SHOW FULL COLUMNS FROM ' + self.name)
		tb = self.db.cur.fetchall()
		
		tables=[ i for i in self.db.query('SHOW TABLES;') ]
		for field in tb:
			fname = field[0]
			ftype = field[1]
			fdefault = field[5]
			fcomment = field[8]
			fdesc = fname[0].upper() + fname[1:].lower() + ':'
			if fname in filled:
				form.hidden(fname,filled[fname])
			elif fname == 'id':
				form.hidden(fname,fdefault)
			elif fname[-3:] == '_id' and fname[:-3] in tables:
				# Relations N - 1
				ocolumns = self.db.query('SHOW COLUMNS FROM ' + fname[:-3])
				orows=self.db.query('SELECT ' + ocolumns[0] + ', ' + ocolumns[1] + ' FROM ' + fname[:-3])
				dict={}
				for row in orows:
					dict.update({row[1]:row[0]})
				if table:
					form.select(fdesc,fname,dict,fdefault)
				else:
					form.select(fname,dict,fdefault)	
			elif ftype == 'text':
				if table:
					form.text(fdesc,fname,fdefault)
				else:
					form.text(fname,fdefault)
			elif fcomment == 'pass':
				if table:
					form.pwd(fdesc,fname,fdefault)
				else:
					form.pwd(fname,fdefault)
			elif fcomment == 'time':
				from time import time
				form.hidden(fname,time())
			else:
				if table:
					form.input(fdesc,fname,fdefault)
				else:
					form.input(fname,fdefault)
		form.submit('Insert')
		return form.end()		

class autoRow:
	"""Object representation of a table row"""
	def __init__(self,content,table):
		self.content=content
		self.table=table

	def __str__(self):
		return str(self.content)
		
	def __getattr__(self, name):
		if name in self.content:
			# Direct call of the item
			return self.content[name]
		else:
			# Relations
			tables=[ i for i in self.table.db.query('SHOW TABLES;') ]
			if name in tables:
				#Relation N - 1
				if name + '_id' in self.content:
					oid = self.content[name+'_id']
					otable = autoTable(name,self.table.db,update=0)
					orows = otable.where("id = "+str(oid))
					return orows[0]
				else:
					#Relations 1 - N
					columns = self.table.db.query('SHOW COLUMNS FROM ' + name)
					if self.table.name + "_id" in columns:
						otable = autoTable(name,self.table.db,update=0)
						otable.content = otable.where( self.table.name + "_id = " + str(self.content['id']))
						return otable
					else:
						#relations N - N
						pnames=[self.table.name + '_' + name,name + '_' + self.table.name]
						for pname in pnames:
							if pname in tables:
								rsource=self.content['id']
								rtable = autoTable(pname,self.table.db,update=0)
								rrows = rtable.where( self.table.name + "_id = " + str(self.content['id']))
								otable = autoTable(name,self.table.db,update=0)
								orows=[]
								for row in rrows:
									results = otable.where('id = ' + str(row.content[name+'_id']))
									for result in results:
										orows.append(result)
								return orows
			return None

				
		
	def __getitem__(self, name):
		return self.content[name]
		
	#def __setattr__(self,name,value):
	#	self.__table.edit(self.__content['id'],{name:value})
		
	def __setitem__(self,name,value):
		self.table.edit(self.content['id'],{name:value})
	def __iter__(self):
		return self.content.iterkeys()
		
	def edit(self,dict):
		self.table.edit(self.content['id'],dict)
	
#--------------------------------------------------------------------------------------------------------------------------------------------------
		
		
class Form:
	"""Helps creating forms without HTML."""
	def __init__(self,extra=''):
		self.output = '<form method="post" action="' + server['script'] + '?' + str(extra) + '" enctype="multipart/form-data">'
		
	def input(self,name,value=''):
		"""Creates a simple input field"""
		self.output += '<input name=' + str(name) + ' value="' + str(value) + '" />'
		
	def pwd(self,name,value=''):
		"""Creates a simple password field"""
		self.output += '<input name=' + str(name) + ' value="' + str(value) + '" type="password" />'
		
	def hidden(self,name,value=''):
		"""Creates a simple hidden field"""
		self.output += '<input name=' + str(name) + ' value="' + str(value) + '" type="hidden" />'
		
	def file(self,name):
		"""Creates a simple file field"""
		self.output += '<input name=' + str(name) + '  type="file" />'
		
	def select(self,name,dict,selected=''):
		"""Creates a select field where the dictionary keys are the description."""
		self.output += '<select name=' + str(name) + '>'
		for key in dict:
			if str(dict[key]) == str(selected):
				self.output += '<option value=' + str(dict[key]) + ' selected>' + str(key) + '</option>'
			else:
				self.output += '<option value=' + str(dict[key]) + '>' + str(key) + '</option>'
		self.output += '</select>'
		
	def text(self,name,value='',rows=6,cols=35):
		"""Creates a textarea field"""
		self.output += '<textarea name=' + str(name) + ' cols="' + str(cols) + '" rows="'+str(rows)+'">' + str(value) + '</textarea>'
		
	def submit(self,name):
		"""Creates a submit button"""
		self.output += '<input value=' + str(name) + ' type="submit" />'
		
	def end(self):
		"""Finishes the form and returns it all"""
		self.output += '</form>'
		return self.output

		
class tableForm:
	"""Helps creating forms without HTML in tables."""
	def __init__(self,extra=''):
		self.output = '<table><form method="post" action="' + server['script'] + '?' + str(extra) + '">'
		
	def input(self,desc,name,value=''):
		"""Creates a simple input field"""
		self.output += '<tr><td align=right><b>' + str(desc) + '</b></td><td><input name=' + str(name) + ' value="' + str(value) + '" /></td></tr>'
		
	def pwd(self,desc,name,value=''):
		"""Creates a simple password field"""
		self.output += '<tr><td align=right><b>' + str(desc) + '</b></td><td><input name=' + str(name) + ' value="' + str(value) + '" type="password" /></td></tr>'
		
	def hidden(self,name,value=''):
		"""Creates a simple hidden field"""
		self.output += '<input name=' + str(name) + ' value="' + str(value) + '" type="hidden" />'
		
	def select(self,desc,name,dict,selected=''):
		"""Creates a select field where the dictionary keys are the description."""
		self.output += '<tr><td align=right><b>' + str(desc) + '</b></td><td><select name=' + str(name) + '>'
		for key in dict:
			if str(dict[key]) == str(selected):
				self.output += '<option value=' + str(dict[key]) + ' selected>' + str(key) + '</option>'
			else:
				self.output += '<option value=' + str(dict[key]) + '>' + str(key) + '</option>'
		self.output += '</select></td></tr>'
		
	def text(self,desc,name,value='',rows=6,cols=35):
		"""Creates a textarea field"""
		self.output += '<tr><td align=right><b>' + str(desc) + '</b></td><td><textarea name="' + str(name) + '" cols="' + str(cols) + '" rows="'+str(rows)+'">' + str(value) + '</textarea></td></tr>'
		
	def submit(self,name):
		"""Creates a submit button"""
		self.output += '<tr><td colspan="2" align="center"><input value="' + str(name) + '" type="submit" /></td></tr>'
		
	def end(self):
		"""Finishes the form and returns it all"""
		self.output += '</form></table>'
		return self.output
		
# ------------------------------------------------------------------------------------------------------------------------------

class Paging:
	"""Helps to page lists"""
	def __init__(self,ppp,total,post):
		self.ppp = ppp
		self.total = total
		
		if 'pg' in post:
			self.page = int(post['pg'])
		else:
			self.page = 0
		
		self.start = self.page * ppp
		self.end = (self.page + 1) * ppp
		
		from math import ceil
		self.lastpage = int(ceil(float(self.total)/ppp))-1
		
	def menu(self,first='[First Page]',previous='[Previous Page]',current='[Current Page]',next='[Next Page]',last='[Last Page]'):
		"""Generates a paging menu"""
		f=''
		if self.page > 0:
			if self.page > 1:
				f+=link(first, self.__url() + '&amp;pg=0' )
				f+=' '
			f+=link(previous, self.__url() + '&amp;pg=' + str(self.page-1) )
			f+=' '
		f+=current + ' '
		if self.page < self.lastpage:
			f+=link(next, self.__url() + '&amp;pg=' + str(self.page+1) )
			f+=' '
			if self.page < (self.lastpage -1):
				f+=link(last, self.__url() + '&amp;pg=' + str(self.lastpage) )
		return f
		
	def __url(self):
		end=''
		for w in get:
			if w != 'pg':
				end += '&amp;' + str(w) + '=' +  str(get[w])
		end = server['script'] + '?' + end[5:]
		return end
		
		
class table:
	""" Helper for table creation """
	def __init__(self):
		self.output="<table align=center>"
		
	def row(*arguments):
		"""Adds a new row with the following rows"""
		self.output+="<tr>"
		for arg in arguments:
			self.output+="<td>" + str(arg) + "</td>"
		self.output+="</tr>"
		
	def end():
		""" Returns table's HTML """
		return self.output + "</table>"

import datetime
class RSSgenerator:
	"""Creates a RSS feed from a table with certain fields.
	After you create it, you'll have to set the fields used as title, desc and the link base.
	To link base, a id will be added in the end.
	"""
	def __init__(self,table,g_title='',g_link='',g_desc='',time=''):
		self.table=table
		self.g_title=g_title
		self.g_link=g_link
		self.g_desc=g_desc
		self.col_title=''
		self.col_desc=''
		self.link_base=''
		self.field='id'
		self.output=''
		self.time = time
			
	def format_date(self,dt):
		dt = datetime.datetime(2000,1,1).fromtimestamp(float(float(dt) + ( 9 * 3600 ) ))
		return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
				["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
				dt.day,
				["Jan", "Feb", "Mar", "Apr", "May", "Jun",
				 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month-1],
				dt.year, dt.hour, dt.minute, dt.second)		
		
		
		
	def out(self):
		"""Outputs all of the feed, including the header."""
		self.output += "Content-type:text/xml\n\n"
		self.output += """<rss version="2.0"><channel>"""
		if self.g_title:
			self.output += """<title>""" + cgi.escape(self.g_title) + """</title>"""
		if self.g_link:
			self.output += """<link>""" + cgi.escape(self.g_link) + """</link>"""
		if self.g_desc:
			self.output += """<description>""" + cgi.escape(self.g_desc) + """</description>"""

		
		
		for row in self.table.content:
			self.output += """
			<item>
				<title>"""+cgi.escape(str(row[self.col_title]))+"""</title>
				<link>"""+cgi.escape(str(self.link_base) + str(row[self.field]))+"""</link>
				<pubDate>"""+self.format_date(row[self.time])+"""</pubDate>
			<description>"""+cgi.escape(str(row[self.col_desc]))+"""			
			
			&lt;br/&gt;
			&lt;script type=&quot;text/javascript&quot;&gt;&lt;!--
				google_ad_client = &quot;pub-1411256716541452&quot;;
				google_ad_width = 468;
				google_ad_height = 15;
				google_ad_format = &quot;468x15_0ads_al&quot;;
				google_ad_channel = &quot;&quot;;
				google_color_border = &quot;FFFFFF&quot;;
				google_color_bg = &quot;FFFFFF&quot;;
				google_color_link = &quot;2D8930&quot;;
				google_color_text = &quot;000000&quot;;
				google_color_url = &quot;008000&quot;;
				//--&gt;
			&lt;/script&gt;
			&lt;script type=&quot;text/javascript&quot;
				src=&quot;http://pagead2.googlesyndication.com/pagead/show_ads.js&quot;&gt;
			&lt;/script&gt;
			""" + """</description></item>"""
			
		self.output += """</channel></rss>"""
		
		return self.output