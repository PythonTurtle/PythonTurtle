# flake8: noqa
# pylint: skip-file
"""
This module creates a file called almostimportstdlib.py, which "almost" imports
the entire Python stdlib. (i.e., if False: import...)
Invoke `make()` to generate that file (if it's not generated already.)

`modules` is supposed to be a list of all the modules of stdlib of Python 2.6.2.
It was created like this:

print [thing[1] for thing in pkgutil.iter_modules()]
(on a virtual machine with a clean installation of Python 2.6.2.)

Then copy-pasted into this file.
If you are interesting in import the stdlib of a different version of Python,
feel free to do the same procedure with the virtual machine and replace
`modules` in this file. (Please note this in this comment if you do.)

Submodules (i.e. email.errors) are not included in `modules`,
But it seems py2exe is careful enough to include them in the package anyway,
just because their parent module might be imported.
"""


def make():
    """
    Generates the file almostimportstdlib.py which almost imports the stdlib.
    See the documentations of the containing package and module.
    """
    modules = ['AutoComplete', 'AutoCompleteWindow', 'AutoExpand', 'BaseHTTPServer', 'Bastion', 'Bindings',
               'CGIHTTPServer', 'CallTipWindow', 'CallTips', 'Canvas', 'ClassBrowser', 'CodeContext', 'ColorDelegator',
               'ConfigParser', 'Cookie', 'Debugger', 'Delegator', 'Dialog', 'DocXMLRPCServer', 'EditorWindow',
               'FileDialog', 'FileList', 'FixTk', 'FormatParagraph', 'GrepDialog', 'HTMLParser', 'HyperParser',
               'IOBinding', 'IdleHistory', 'MimeWriter', 'MultiCall', 'MultiStatusBar', 'ObjectBrowser', 'OutputWindow',
               'ParenMatch', 'PathBrowser', 'Percolator', 'PyParse', 'PyShell', 'Queue', 'RemoteDebugger',
               'RemoteObjectBrowser', 'ReplaceDialog', 'ScriptBinding', 'ScrolledList', 'ScrolledText', 'SearchDialog',
               'SearchDialogBase', 'SearchEngine', 'SimpleDialog', 'SimpleHTTPServer', 'SimpleXMLRPCServer',
               'SocketServer', 'StackViewer', 'StringIO', 'Tix', 'Tkconstants', 'Tkdnd', 'Tkinter', 'ToolTip',
               'TreeWidget', 'UndoDelegator', 'UserDict', 'UserList', 'UserString', 'WidgetRedirector', 'WindowList',
               'ZoomHeight', '_LWPCookieJar', '_MozillaCookieJar', '__future__', '_abcoll', '_bsddb', '_ctypes',
               '_ctypes_test', '_elementtree', '_hashlib', '_msi', '_multiprocessing', '_socket', '_sqlite3', '_ssl',
               '_strptime', '_testcapi', '_threading_local', '_tkinter', 'abc', 'aboutDialog', 'aifc', 'anydbm', 'ast',
               'asynchat', 'asyncore', 'atexit', 'audiodev', 'base64', 'bdb', 'binhex', 'bisect', 'bsddb', 'bz2',
               'cProfile', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmd', 'code', 'codecs', 'codeop', 'collections',
               'colorsys', 'commands', 'compileall', 'compiler', 'configDialog', 'configHandler',
               'configHelpSourceEdit', 'configSectionNameDialog', 'contextlib', 'cookielib', 'copy', 'copy_reg', 'csv',
               'ctypes', 'curses', 'dbhash', 'decimal', 'difflib', 'dircache', 'dis', 'distutils', 'doctest', 'dumbdbm',
               'dummy_thread', 'dummy_threading', 'dynOptionMenuWidget', 'email', 'encodings', 'filecmp', 'fileinput',
               'fnmatch', 'formatter', 'fpformat', 'fractions', 'ftplib', 'functools', 'genericpath', 'getopt',
               'getpass', 'gettext', 'glob', 'gzip', 'hashlib', 'heapq', 'hmac', 'hotshot', 'htmlentitydefs', 'htmllib',
               'httplib', 'idle', 'idlelib', 'idlever', 'ihooks', 'imaplib', 'imghdr', 'imputil', 'inspect', 'io',
               'json', 'keybindingDialog', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'macosxSupport',
               'macpath', 'macurl2path', 'mailbox', 'mailcap', 'markupbase', 'md5', 'mhlib', 'mimetools', 'mimetypes',
               'mimify', 'modulefinder', 'msilib', 'multifile', 'multiprocessing', 'mutex', 'netrc', 'new', 'nntplib',
               'ntpath', 'nturl2path', 'numbers', 'opcode', 'optparse', 'os', 'os2emxpath', 'pdb', 'pickle',
               'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'popen2', 'poplib', 'posixfile', 'posixpath',
               'pprint', 'profile', 'pstats', 'pty', 'py_compile', 'pyclbr', 'pydoc', 'pydoc_topics', 'pyexpat',
               'quopri', 'random', 're', 'repr', 'rexec', 'rfc822', 'rlcompleter', 'robotparser', 'rpc', 'run', 'runpy',
               'sched', 'select', 'sets', 'sgmllib', 'sha', 'shelve', 'shlex', 'shutil', 'site', 'smtpd', 'smtplib',
               'sndhdr', 'socket', 'sqlite3', 'sre', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'stat',
               'statvfs', 'string', 'stringold', 'stringprep', 'struct', 'subprocess', 'sunau', 'sunaudio', 'symbol',
               'symtable', 'tabbedpages', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'test', 'testcode',
               'textView', 'textwrap', 'this', 'threading', 'timeit', 'tkColorChooser', 'tkCommonDialog',
               'tkFileDialog', 'tkFont', 'tkMessageBox', 'tkSimpleDialog', 'toaiff', 'token', 'tokenize', 'trace',
               'traceback', 'tty', 'turtle', 'types', 'unicodedata', 'unittest', 'urllib', 'urllib2', 'urlparse',
               'user', 'uu', 'uuid', 'warnings', 'wave', 'weakref', 'webbrowser', 'whichdb', 'winsound', 'wsgiref',
               'xdrlib', 'xml', 'xmllib', 'xmlrpclib', 'zipfile']
    import_modules = [("    import " + module) for module in modules]
    prologue = """\"\"\"
To understand this module,
please refer to the containing package's documentation.
\"\"\"

if False:
"""
    text = prologue + "\n".join(import_modules)
    f = open("almostimportstdlib.py", "w")
    f.write(text)
    f.close()


if __name__ == "__main__":
    make()
