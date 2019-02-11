###################################################

import argparse
import subprocess
from pathlib import Path
from github import Github
import pkg_resources

###################################################

from dryfalls.utils import create_dir, read_string_from_file, write_string_to_file, read_json_from_file, rmtree

###################################################

REPOS_ROOT = "repos"

###################################################

reponame = None

###################################################

def filepath(path):
    return "{}/{}".format(REPOS_ROOT, path)

def repopath(name = None):
    global reponame
    if not name:
        name = reponame
    return filepath(name)

def repofilepath(path):
    return "{}/{}".format(repopath(), path)

def repoconfigpath(name = None):
    if not name:
        name = reponame
    return repopath("{}.json".format(name))

###################################################

def creategitconfig(gituser, gitmail, reponame):
    resfilename = pkg_resources.resource_filename('dryfalls', "config.template")
    print("config resource", resfilename)
    template = read_string_from_file(resfilename, "")
    template = template.replace("${gituser}", gituser)
    template = template.replace("${gitmail}", gitmail)
    template = template.replace("${reponame}", reponame)
    return template

def createreadme(title, description):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "README.md.template"), "")
    template = template.replace("${title}", title)
    template = template.replace("${description}", description)
    return template

def creategitignore(reponame):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "gitignore.template"), "")
    template = template.replace("${reponame}", reponame)    
    return template

def createmetayaml(gituser, reponame):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "meta.yaml.template"), "")
    template = template.replace("${gituser}", gituser)
    template = template.replace("${reponame}", reponame)
    return template

def createsetuppy(gituser, gitmail, reponame, projectShortDescription, projectDescription):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "setup.py.template"), "")
    template = template.replace("${gituser}", gituser)
    template = template.replace("${gitmail}", gitmail)
    template = template.replace("${reponame}", reponame)
    template = template.replace("${projectDescription}", projectDescription)
    template = template.replace("${projectShortDescription}", projectShortDescription)
    return template

def createinitpy():
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "__init__.py.template"), "")        
    return template

def createmainpy(reponame):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "__main__.py.template"), "")    
    template = template.replace("${reponame}", reponame)
    return template

def createtravistest(reponame):
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', "travistest.template"), "")    
    template = template.replace("${reponame}", reponame)
    return template

def createtravisyml():
    template = read_string_from_file(pkg_resources.resource_filename('dryfalls', ".travis.yml.template"), "")        
    return template

def readrepoconfigjson(name = None):    
    return read_json_from_file(repoconfigpath(name), {})

###################################################

create_dir("repos")

parser = argparse.ArgumentParser(description='Manage repos')

parser.add_argument('--create', help='create repo')
parser.add_argument('--populate', help='populate repo')
parser.add_argument('-c', "--commit", help='create commit')
parser.add_argument("--name", help='commit name')
parser.add_argument('-p', "--push", help='push')
parser.add_argument("--createvenv", help='create virtual env')
parser.add_argument("--installvenv", help='install virtual env')
parser.add_argument("--install", help='install virtual env')
parser.add_argument("--module", help='module')
parser.add_argument("--createdist", help='create dist')
parser.add_argument("--runmain", help='run main')
parser.add_argument("--twine", help='twine')
parser.add_argument("--twinever", help='twine latest version')
parser.add_argument("--setup", help='open setup')
parser.add_argument("--code", help='open with vscode')
parser.add_argument("--updatever", help='update version')
parser.add_argument("--ver", help='version')
parser.add_argument("--createrelease", help='create release')
parser.add_argument('--init', help='init')
parser.add_argument('--force', action = "store_true", help='force')
parser.add_argument('cmdargs', nargs = '*')

args = parser.parse_args()

create = args.create
setup = args.setup
populate = args.populate
commit = args.commit
commitname = args.name
push = args.push
createvenv = args.createvenv
installvenv = args.installvenv
createdist = args.createdist
twine = args.twine
twinever = args.twinever
createrelease = args.createrelease
updatever = args.updatever

if create:
    setup = args.create    

if args.init:
    populate = args.init
    commit = args.init
    commitname = "Initial commit"   
    push = args.init    
    createvenv = args.init
    installvenv = args.init
    createdist = args.init
    twine = args.init
    createrelease = args.init

###################################################

print(args)

if create:
    reponame = create
    print("creating {} as {}".format(reponame, repopath()))
    if args.force:
        rmtree(repopath())
    create_dir(repopath())
    write_string_to_file(repoconfigpath(), read_string_from_file(pkg_resources.resource_filename('dryfalls', "repotemplate.json"), "{}"), force = args.force)    

if populate:
    reponame = populate
    if args.force:
        print("removing .git")
        rmtree(repofilepath(".git"))
    subprocess.Popen(["git", "init"], cwd = str(Path(repopath()))).wait()
    configjson = readrepoconfigjson()        
    gituser = configjson["gituser"]
    gitpass = configjson["gitpass"]
    gitmail = configjson["gitmail"]
    project = configjson["project"]
    projectTitle = project["title"]
    projectDescription = project["description"]
    projectShortDescription = project["shortDescription"]
    gitconfig = creategitconfig(gituser, gitmail, reponame)
    write_string_to_file(repofilepath(".git/config"), gitconfig)
    print("written gitconfig")
    write_string_to_file(repofilepath(".gitignore"), creategitignore(reponame), force = args.force)    
    print("written .gitignore")
    write_string_to_file(repofilepath("README.md"), createreadme(projectTitle, projectDescription), force = args.force)    
    print("written README.md")
    write_string_to_file(repofilepath("LICENSE"), read_string_from_file(pkg_resources.resource_filename('dryfalls', "LICENSE.template"), ""), force = args.force)    
    print("written LICENSE")
    write_string_to_file(repofilepath("bld.bat"), read_string_from_file(pkg_resources.resource_filename('dryfalls', "bld.bat.template"), ""), force = args.force)    
    write_string_to_file(repofilepath("build.sh"), read_string_from_file(pkg_resources.resource_filename('dryfalls', "build.sh.template"), ""), force = args.force)    
    print("written PyPi build files")
    create_dir(repofilepath(reponame))
    write_string_to_file(repofilepath(reponame + "/__init__.py"), createinitpy(), "")
    write_string_to_file(repofilepath(reponame + "/__main__.py"), createmainpy(reponame), "")
    print("created package dir")
    write_string_to_file(repofilepath("Pipfile"), read_string_from_file(pkg_resources.resource_filename('dryfalls', "Pipfile.template"), ""), force = args.force)    
    write_string_to_file(repofilepath("Pipfile.lock"), read_string_from_file(pkg_resources.resource_filename('dryfalls', "Pipfile.lock.template"), ""), force = args.force)    
    print("written pipfiles")
    write_string_to_file(repofilepath("meta.yaml"), createmetayaml(gituser, reponame), force = args.force)    
    print("written meta.yaml")
    write_string_to_file(repofilepath("setup.py"), createsetuppy(gituser, gitmail, reponame, projectShortDescription, projectDescription), force = args.force)    
    print("written setup.py")
    write_string_to_file(repofilepath("travis_test.py"), createtravistest(reponame), force = args.force)    
    print("written travis test")
    write_string_to_file(repofilepath(".travis.yml"), createtravisyml(), force = args.force)    
    print("written .travis.yml")
    write_string_to_file(repofilepath("VER"), "0.0.1", force = args.force)
    print("written version")
    g = Github(gituser, gitpass)
    u = g.get_user()
    if args.force:
        try:
            u.get_repo(reponame).delete()
            print("deleted github repo")
        except:
            print("could not delete repo")
    try:
        u.create_repo(reponame, description = projectShortDescription)
        print("created github repo")
    except:
        print("could not create repo")

if updatever:
    reponame = updatever
    ver = args.ver
    if not ver:
        ver = read_string_from_file(repofilepath("VER"), "0.0.1")
        parts = ver.split(".")
        ver = "{}.{}.{}".format(parts[0], parts[1], int(parts[2]) + 1)
    print("updating {} version to {}".format(reponame, ver))
    metayaml = read_string_from_file(repofilepath("meta.yaml"), "")
    parts = metayaml.split("version:")
    parts = parts[1].split('"')
    curver = parts[1]
    print("current version", curver)
    newmetayaml = metayaml.replace('version: "{}"'.format(curver), 'version: "{}"'.format(ver))
    newmetayaml = newmetayaml.replace('git_rev: v{}'.format(curver), 'git_rev: v{}'.format(ver))    
    write_string_to_file(repofilepath("meta.yaml"), newmetayaml)
    setuppy = read_string_from_file(repofilepath("setup.py"), "")
    newsetuppy = setuppy.replace("version='{}'".format(curver), "version='{}'".format(ver))
    write_string_to_file(repofilepath("setup.py"), newsetuppy)
    write_string_to_file(repofilepath("VER"), ver)
    if commitname:
        commit = reponame
        push = reponame
        createdist = reponame
        twinever = reponame
        createrelease = reponame

if commit:
    reponame = commit    
    subprocess.Popen(["git", "add", "."], cwd = str(Path(repopath()))).wait()    
    subprocess.Popen(["git", "commit", "-m", commitname], cwd = str(Path(repopath()))).wait()    

if push:
    reponame = push        
    subprocess.Popen(["git", "push", "github", "master"], cwd = str(Path(repopath()))).wait()

if createvenv:
    reponame = createvenv
    configjson = readrepoconfigjson()
    pythonpath = configjson["pythonpath"]
    subprocess.Popen(["pipenv", "--python", str(Path(pythonpath))], cwd = str(Path(repopath()))).wait()    

if installvenv:
    reponame = installvenv    
    subprocess.Popen(["pipenv", "install"], cwd = str(Path(repopath()))).wait()    

if args.install:
    reponame = args.install    
    module = args.module
    subprocess.Popen(["pipenv", "install", module], cwd = str(Path(repopath()))).wait()    

if createdist:
    reponame = createdist    
    subprocess.Popen(["pipenv", "run", "python", "setup.py", "sdist", "bdist_wheel"], cwd = str(Path(repopath()))).wait()    

if twine:
    reponame = twine
    try:
        subprocess.Popen(["pipenv", "run", "python", "-m", "twine", "upload", "dist/*"], cwd = str(Path(repopath()))).wait()    
    except:
        print("could not twine")

if twinever:
    reponame = twinever
    curver = read_string_from_file(repofilepath("VER"), "0.0.1")
    try:
        subprocess.Popen(["pipenv", "run", "python", "-m", "twine", "upload", "dist/{}-{}*".format(reponame, curver)], cwd = str(Path(repopath()))).wait()    
    except:
        print("could not twine ver")

if setup:
    reponame = setup
    path = str(Path("repos/{}.json".format(reponame)))    
    configjson = readrepoconfigjson()
    idepath = str(Path(configjson["idepath"]))
    print("opening", path, "with", idepath)
    subprocess.Popen([idepath, path])

if args.code:
    reponame = args.code
    configjson = readrepoconfigjson()
    idepath = str(Path(configjson["idepath"]))
    subprocess.Popen([idepath, "."], cwd = str(Path(repopath())))

if createrelease:
    reponame = createrelease
    ver = read_string_from_file(repofilepath("VER"), "0.0.1")
    tag = "v" + ver
    print("creating release {} for {}".format(ver, reponame))
    configjson = readrepoconfigjson()        
    gituser = configjson["gituser"]
    gitpass = configjson["gitpass"]
    g = Github(gituser, gitpass)
    u = g.get_user()
    r = u.get_repo(reponame)
    r.create_git_release(tag, "release " + tag, "release " + tag)
    print("git release created")

if args.runmain:
    reponame = args.runmain
    subprocess.Popen(["pipenv", "run", "python", "-m", reponame] + args.cmdargs, cwd = str(Path(repopath()))).wait()    