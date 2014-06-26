from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ['resource/*']

setup(name = 'bastis-python-toolbox',
    version = '0.1',
    description = 'Basti\'s personal python toolbox for everyday use.',
    author = 'Sebastian Tschoepel',
    author_email = 'sebastian.tschoepel@dontsendmespam.com',
    url = 'https://code.google.com/p/bastis-python-toolbox/',
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['bastisptb', 'bastisptb_scripts'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'bastisptb' : files, 'bastisptb_scripts' : files },
    #'runner' is in the root.
    scripts = ['bastisbtp_test.py'],
    long_description = '''Basti\'s personal python toolbox for everyday use.''' 
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
) 