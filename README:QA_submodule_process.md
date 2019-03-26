##PROCESS FOR SUBMODULING FOLDER/FILES##

###Steps to add qa_common as submodule:###
1) fork qa_common
2) clone qa_common locally
3) unify common folders across different projects into qa_common
4) PR and merge changes into qa_common
5) Delete corresponding folder in project
6) CD to project repo
7) git submodule add https://github.com/TIES-Software/qa_common
8) add the following to test runner (i.e. run_tests.py or enironment.py):

import os

from os.path import abspath

import sys

sys.path.append(abspath("%s/../../%s" % (os.path.dirname(os.path.realpath(__file__)), "qa_common")))

  *may need to modify directory path in above line depending on how nested file runner is*


###When pulling down changes:###

git checkout master

git pull master


###After making changes to submodule:###

CD into submodule directory

git checkout -b <branch name>


###Pushing change to submodule:###

(from submodule directory using branch)

git status

git add

git commit -m "message"

git push


###MORE RESCOURCES ABOUT SUBMODULES:###

https://git-scm.com/book/en/v2/Git-Tools-Submodules

https://stackoverflow.com/questions/14233939/git-submodule-commit-push-pull
