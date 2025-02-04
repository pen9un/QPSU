#coding=utf-8
import sys,pathlib
# 要修改路径，框选两行，一起删除 *.py /qgb   /[gsqp]  
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
# 上个版本问题： print(dir(py),py) #['__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__'] <module 'py' (namespace)>
U,T,N,F=py.importUTNF()

import os,sys
import shutil

import dulwich
from dulwich import client,index,repo,porcelain
from dulwich.client import get_transport_and_path_from_url #	return (<dulwich.client.SSHGitClient at 0x23218db7f88>, '/qgb/xxnet.git')

try:
	import paramiko
except Exception as e:
	print('pip install dulwich paramiko',e)



# from six.moves import urllib
# opener = urllib.request.build_opener()
# headers={'Authorization':F.read('Authorization')}
# opener.addheaders = py.list(headers.items())
# urllib.request.install_opener(opener)
grepo=U.get('git.repo')

def clone(url,path=None):
	client, target = dulwich.client.get_transport_and_path(url) #c , 'user/repo'
	if not path:
		if target.endswith('.git'):
			target=target[:-4]
		path=target
	path=F.mkdir(path)
	ls=F.ls(path)
	if len(ls)>1: #skip .git
		return py.No('Not empty dir:'+path,ls)
	if len(ls)==1:
		r = dulwich.repo.Repo(path)
	else:	
		r = dulwich.repo.Repo.init(path)
	print(U.stime(),'fetching url...')
	remote_refs = client.fetch(url, r)
	r[b"HEAD"] = remote_refs[b"HEAD"]

	print(U.stime(),'build_index_from_tree ...')
	index.build_index_from_tree(r.path, r.index_path(), r.object_store, r[b'HEAD'].tree)
	
	r.close()
	return path,r

def up(url,path=None,commit_msg=None,username=None,password=None,branch='master',**ka):
	'''
porcelain.push(repo.path,"https://wrong_name@e.coding.net/...",'master',username='correct_name',password=_) ## 也会GitProtocolError: unexpected http resp 401 for

porcelain.push(repo.path,"https://http://e.coding.net/...",'master',username='correct_name',password=_)  #  OK!	
	'''
	global grepo
	if ':' not in url:
		url='https://'+url
	if 'git@' not in url:
		domain=T.netloc(url)
		if not username:
			username=U.get_or_input(domain+'_git.username')
		ka['username']=username
		if not password:
			password=U.get_or_input(domain+'_git.password')
		ka['password']=password
	if not 'refspecs' in ka:
		ka['refspecs']=branch
	if not path and '/qpsu' in url.lower():
		path=U.get_qpsu_dir()
	if not path:	
		_client, target = dulwich.client.get_transport_and_path(url) 
		if target.endswith('.git'):
			target=target[:-4]
		path=target
		
	path=F.auto_path(path)
	ls=[i[len(path):] for i in F.ls(path,d=0,f=1,r=1)]
	if len(ls) < 1:
		return py.No('Not contains .git dir:'+path,ls)

	repo=dulwich.repo.Repo(path)
	U.pln(path,'adding ...',U.stime())
	repo.stage(['git.py'],)
	dulwich.porcelain.add(repo.path)  #TODO  pwd 必须在当前repo目录下 ，否则
# 1-> 212     treepath = os.path.relpath(path, repopath)
    # 213     if treepath.startswith(b'..'):
    # 214         raise ValueError('Path not in repo')
# ipdb> !(path, repopath)
# (b'C:\\test\\www\\png\\0010005960.png', b'C:/QGB/babun/cygwin/bin/qgb/')		
	
	U.pln('commit ...',U.stime())

	bhash,commit_msg=commit(repo,commit_msg)					
	r= bhash,commit_msg, ka
	repo.close()
	U.pln('push ...',U.stime())
	try:
		#repo.path == 'C:/QGB/babun/cygwin/bin/qgb/'
		if 'git@' in url:
			push_with_key(repo.path,url,**ka)
		else:
			dulwich.porcelain.push(repo.path, url , **ka )
		
	except Exception as e:
		U.print_tb()
		U.v.dulwich.porcelain.push(repo.path, url , **ka )
		r=py.No(e,r)
	return r
	# porcelain.push(repo.repo.path, result.url, branch_name, errstream=outstream)					
	
def commit(repo,commit_msg):
	if not commit_msg:
		commit_msg='dulwich_'+U.stime()
	if not py.isbytes(commit_msg):
		commit_msg=commit_msg.encode('utf-8')
			
	index = repo.open_index()
	new_tree = index.commit(repo.object_store)
	if new_tree != repo[repo.head()].tree:
		bhash=repo.do_commit(commit_msg, tree=new_tree)
		return bhash,commit_msg
	else:
		return b'',py.No("Empty commit!")

def log(max_entries=11,repo=None):
	
	return dulwich.porcelain.log(max_entries=max_entries) 
	
	
def open_private_key(f,):
	''' 
paramiko.RSAKey.from_private_key(open_private_key(f),)  == <paramiko.rsakey.RSAKey at 0x23218fda648> '''
	if py.isfile(f):
		file=f
	elif not py.istr(f):
		raise py.ArgumentError('key f type must file or str',f)
	elif F.exist(f):
		file=py.open(f)
	elif py.len(f)<256 and 'PRIVATE KEY' not in f.upper():
		raise py.ArgumentError('private_key f str format Error ! Or [%s] not exist'%f)
	else:
		from io import StringIO
		file=StringIO(f)
	return file	
	
def push_with_key(repo_path,remote="ssh://git@github.com:22/QGB/QPSU.git",private_key='',refspecs='master',errstream=getattr(sys.stderr, 'buffer', None),private_key_password=None,):
	r''' #important#	三引号string中不能出现 \util 这种字符（常见于路径）
# 会导致 SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 1-2: truncated \uXXXX escape 错误
# 最好 引号前加r 强制用 raw-string
	
push ... 2021-04-15__06.26.44__.288
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 106, in up
    push_with_key(repo.path,url,**ka)
  File "C:/QGB/babun/cygwin/bin\qgb\git.py", line 205, in push_with_key
    progress=errstream.write)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 789, in send_pack
    proto, unused_can_read, stderr = self._connect(b'receive-pack', path)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\client.py", line 1410, in _connect
    **kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\dulwich\contrib\paramiko_vendor.py", line 103, in run_command
    client.connect(**connection_kwargs)
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in connect
    retry_on_signal(lambda: sock.connect(addr))
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\util.py", line 283, in retry_on_signal
    return function()
  File "C:\QGB\Anaconda3\lib\site-packages\paramiko\client.py", line 349, in <lambda>
    retry_on_signal(lambda: sock.connect(addr))
Out[26]: 'C:/QGB/babun/cygwin/bin/qgb/'
 '''
	from dulwich.contrib.paramiko_vendor import ParamikoSSHVendor
	import dulwich.porcelain
	from dulwich.protocol import (
		Protocol,
		ZERO_SHA,
	)
	from dulwich.objectspec import (
		parse_commit,
		parse_object,
		parse_ref,
		parse_reftuples,
		parse_tree,
		)
	from dulwich.errors import (
		GitProtocolError,
		NotGitRepository,
		SendPackError,
		UpdateRefsError,
    )	
	DEFAULT_ENCODING = 'utf-8'	
	selected_refs = []
	
	if not private_key:
		private_key=U.get_or_set('id_rsa',U.gst+'id_rsa')
	
	
	with open_private_key(private_key) as fpkey, dulwich.porcelain.open_repo_closing(repo_path) as r:
		def update_refs(refs):
			selected_refs.extend(parse_reftuples(r.refs, refs, refspecs))
			new_refs = {}
			# TODO: Handle selected_refs == {None: None}
			for (lh, rh, force) in selected_refs:
				if lh is None:
					new_refs[rh] = ZERO_SHA
				else:
					new_refs[rh] = r.refs[lh]
			return new_refs
		
		import paramiko
		pkey=paramiko.RSAKey.from_private_key(fpkey, password=private_key_password)

		if 'git@' not in repo_path:
			# raise py.NotImplementedError("'git@' not in repo_path")
			repo_path
		
		client, path=dulwich.client.get_transport_and_path( remote, vendor=ParamikoSSHVendor(pkey=pkey))
		
		err_encoding = getattr(errstream, 'encoding', None) or DEFAULT_ENCODING
		remote_location_bytes = client.get_url(path).encode(err_encoding)
		#b'ssh://git@github.com:22/QGB/QPSU.git'
		try:
			client.send_pack(
				path, update_refs,
				generate_pack_data=r.object_store.generate_pack_data,
				progress=errstream.write)
			# print(remote_location_bytes)
			errstream.write(
				b"Push to " + remote_location_bytes + b" successful.\n")
			errstream.flush()	# 与 stdout 混合打印时 ，顺序可能不同
		except (UpdateRefsError, SendPackError) as e:
			errstream.write(b"Push to " + remote_location_bytes +
							b" failed -> " + e.message.encode(err_encoding) +
							b"\n")
			return py.No(e)
		finally:
			errstream.flush()
		return client
		# return r.path,remote_location_bytes
		
