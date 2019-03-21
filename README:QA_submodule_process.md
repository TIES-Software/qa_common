PROCESS FOR SUBMODULING FOLDER/FILES

Steps to add qa_common as submodule:
1) fork qa_common
2) clone qa_common locally
3) unify common folders across different projects into qa_common
4) PR and merge changes into qa_common
5) Delete corresponding folder in project
6) CD to project
7) git submodule add https://github.com/TIES-Software/qa_common common


When pulling down changes:
git submodule update --remote qa_common


Making changes to submodule:
CD into directory
git checkout <branch name>
git submodule update --remote --merge


Pushing change to submodule:
(from submodule directory)
git add
git commit -a -m "submodule message"
cd .. (back to main project folder)
git comit -a -m "commiting submodule changes from main project"
git push --recurse-submodules=check or on-demand


MORE RESCOURCES ABOUT SUBMODULES:
https://git-scm.com/book/en/v2/Git-Tools-Submodules
https://stackoverflow.com/questions/14233939/git-submodule-commit-push-pull
