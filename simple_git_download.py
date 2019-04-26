# -*- coding: utf-8 -*-
import urllib

def showHelp(err_msg=None):
	if err_msg :
		print err_msg
	print "USAGE:"
	print "python simple_git_download.py src_url target_path [down|wget]"
	print "EXAMPLE:"
	print "python simple_git_download.py https://github.com/nemon-/simple_git_download.git . down"

def outFile(s,f='./log.log'):
	print 'write file: ',f
	try:
		f= open(f,'wb')
		f.write(s)
		f.close()
	except:
		print 'ERROR !'

def creatDir(arry_path):
	import os
	work_path ='/'.join(arry_path)
	if not os.path.exists( work_path ):
		os.makedirs(  work_path )

def getUrlContent(work_url):
	print 'open url content: ',work_url
	s=''
	try:
		sf = urllib.urlopen(work_url)
		# html = sf.readlines()
		# htmls = ''.join(html)
		s =sf.read()
		sf.close()
	except:
		print 'ERROR !'
	return s

def getMinTagStart(html_str,sTag):
	i1_1 = html_str.find('<'+sTag+'>')
	i1_2 = html_str.find('<'+sTag+' ')
	if i1_1<0:
		return i1_2
	elif i1_2<0:
		return i1_1
	else:
		return min(i1_1,i1_2)

def getStrsByTag(html_str,sTag):
	a = []
	tmp_s = html_str
	i1 =getMinTagStart(tmp_s,sTag)
	while i1>=0:
		tmp_s = tmp_s[i1:]
		i2 = tmp_s.find('</'+sTag+'>')
		a.append( tmp_s[0:i2+len('</'+sTag+'>')] )
		tmp_s = tmp_s[i2+len('</'+sTag+'>'):]
		i1 =getMinTagStart(tmp_s,sTag)
	return a

def getHrefAndName(tagA):
	tmps=tagA
	i1=tmps.find('href="')
	tmps=tmps[i1+len('href="'):]
	i2=tmps.find('"')
	s_href = tmps[0:i2]
	tmps = tmps[i2:]
	i3=tmps.rfind("</a")
	tmps=tmps[0:i3]
	i4=tmps.rfind('>')
	s_name = tmps[i4+1:]
	return (s_href,s_name)


def getList(htmls):
	i1 = htmls.find('<table class="files js-navigation-container js-active-navigation-container" data-pjax>')
	h2=htmls[i1:]
	i2 = h2.find('</table>')
	h3 = h2[0:i2+len('</table>')]
	h4 = ''.join(getStrsByTag(h3,'tbody'))
	l5 = getStrsByTag(h4,'a')
	l6 = [ x for x in l5 if x.find('class="js-navigation-open"')>=0]
	i7=[getHrefAndName(x) for x in l6]
	return i7


def getFName(url):
	work_path = url if url[-1]!='/' else url[0:-1]
	i1 = work_path.rfind('/')
	name = work_path if i1<0 else work_path[i1+1:]
	return name


def findAllList(work_url,arry_tgt,str_type,s_root):
	agl = []
	url = s_root+work_url
	# print url
	htmls=getUrlContent(url)
	ipos=htmls.find('<a id="raw-url"')
	if ipos>0:
		tmps=htmls[ipos:]
		tmpa=getHrefAndName(tmps)
		agl.append( ('file',arry_tgt[::],s_root+tmpa[0]) )
		print 'find file: '+ s_root+tmpa[0]
	else:
		agl.append( ('path',arry_tgt[::],url) )
		print 'search path: '+ url
		tmpl=getList(htmls)
		for i in tmpl:
			arry_tgt.append( i[1] )
			agl.extend(  findAllList( i[0] , arry_tgt,str_type,s_root) )
			arry_tgt.pop()
	return agl

def main(setting=None):
	if setting :
		# print setting
		agl = findAllList(setting['arr_src'],setting['target_path'],setting['output_type'],setting['s_src_root'])
		if setting['output_type']=='wget':
			path = setting['target_path'][::]
			path.append('download.sh')
			f_sh = open( '/'.join(path) ,'wb')
			f_sh.writelines( '\n'.join([ 'madir '+'/'.join(item[1]) if item[0]=='path' else 'wget -P '+'/'.join(item[1])+' '+item[2] for item in agl] ) )
			f_sh.close()
		elif setting['output_type']=='down':
			for item in agl:
				if item[0]=='path':
					#print '+ path: ','/'.join(item[1]),item[2]
					creatDir( item[1] )
				elif item[0]=='file':
					#print '- file: ','/'.join(item[1]),item[2]
					outFile( getUrlContent(item[2]) , '/'.join(item[1]))
				else:
					print 'ERROR:',item[0],'/'.join(item[1]),item[2]
		else:
			print 
			for i in agl:
				print i
	else:
		return showHelp('parameter error.')

if __name__ == '__main__':
	import sys
	if len( sys.argv)<3:
		showHelp()
	else:
		"""
		tmp ={}
		for item in sys.argv:
			arr_para = item.split('=')
			tmp[ arr_para[0] ] = arr_para[1:]
		para ={}
		for item in ['src','tgt']:
			para[ item ] = tmp [ item ]
		"""
		para_src = sys.argv[1]
		para_tgt = sys.argv[2]
		if len( sys.argv)>=4:
			para_typ = sys.argv[3] if sys.argv[3] in ['wget','down'] else 'wget'
		else:
			para_typ = 'wget'
		
		arry_tgt = para_tgt.split(r'/')
		if arry_tgt[-1]=='':
			arry_tgt.pop()

		arry_src = para_src.split(r'/')
		if not( len(arry_src)>=4 ):
			showHelp('MUST WITH project name.')
		else:
			s_src_root = arry_src[0] +r'//' +arry_src[2] # 'https://github.com'
			arry_src = arry_src[3:]
			if len(arry_src)==2 and arry_src[1][-4:]=='.git':
				arry_src[1] = arry_src[1][0:-4]
			# print 'arry_src:',arry_src
			if ( len(arry_src)>1 and len(arry_src)<2 ):
				showHelp('MUST WITH tree/master .')
			elif ( len(arry_src)>2 and arry_src[2]!='tree'):
				showHelp('MUST WITH tree/master  .')
			elif ( len(arry_src)>=3 and arry_src[3]!='master'):
				showHelp('MUST WITH tree/master ..')
			else:
				if arry_src[-1]=='':
					arry_src.pop()
				if len(arry_src)==2:
					arry_src.extend(( 'tree', 'master'))
				arry_src[0]='/'+arry_src[0]
				main({'arr_src':'/'.join(arry_src),'target_path':arry_tgt,'output_type':para_typ.lower(),'s_src_root':s_src_root})


