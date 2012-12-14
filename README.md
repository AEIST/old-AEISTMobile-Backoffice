AEIST Mobile Contribution process
====================


The developer has it own fork of the project, on which implements new features and
bug fixes, when finished, it will be contributed to the main tree through a "Pull
request", where a gate keeper will accept the changes or request for further changes.
Once the "Pull request" is accepted, it will be merge into the main tree, which
will go into production.

Concepts
--------

+ Upstream: The main git tree of AEIST Mobile Backoffice (github.com/JoaoVasques/AEISTMobile-BackOffice)
+ Fork: A clone of upstream in github, each developer has its own fork.

Process Set-up
--------------

1. Developer forks in github AEIST Mobile Backoffice project to its own github fork.
2. Clones his/her github fork in the development computer (folder - $PROJECT).
3. Set up upstream repository as upstream to fecth and merge changes into master (http://help.github.com/fork-a-repo/)
4. Install Google App Engine for Python (https://developers.google.com/appengine/downloads)
5. Run:

    dev_appserver.py $PROJECT

Remember never to commit to master, as otherwise you will not be able to fetch and merge correctly.

Development process
-------------------
> *Note*: It is very important that the developer never commits to master branch directly.

This process is started when a new feature or bug fix need to be added.

1. Developer creates new branch in local (from master branch, usually).
2. Commits changes in local to the feature branch.
3. Pushes the new branch to the github fork after the first commit (git push origin branchname)
4. Keep committing and pushing to github fork until feature complete. Time to
time also fetch and merge from upstream, and perhaps rebase your branch
(http://learn.github.com/p/rebasing.html) or merge from master.
5. Creates "Pull request" to master branch in upstream.
6. Gatekeeper checks the change. If accepted it will be merge to uptream, otherwise continue.
7. Keep committing and pushing to fork until gatekeeper request completed. Go to 6.

Branch names
------------

In general the branch names will be:

    engname/module/changedescription

as for example:

    joaovasques/recreativa/new-event-image


Coding style
--------------------
http://www.python.org/dev/peps/pep-0008/


How to write commits
--------------------

These are two good references:

https://github.com/erlang/otp/wiki/Writing-good-commit-messages

http://lbrandy.com/blog/2009/03/writing-better-commit-messages/

Do not include many different unrelated changes in the same commit.
Try to do not make very small commits like fixing a semicolon.

Test your code before committing.

Do not include code of different modules of the software unless the
changes are completely related.

Read github.com documentation at http://help.github.com for more!!
