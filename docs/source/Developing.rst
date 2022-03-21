Developers' Instructions
========================

The `tempest_helper` code contains a comprehensive set of unit tests to check that
it works as intended; the tests are run automatically on pull
requests using GitHub Actions. Details of the tests that are run and instructions
on how to run them locally are included here. A suggested Git workflow has also
been included for users who are new to Git.

Tests run
#########

The following tests are configured (in the ``.github/workflows/*.yml`` files in the
repository) to run on pull requests and branches in GitHub:

* the unit tests in the ``test_tempest_helper`` directory. The tests use the
  unittest framework but pytest provides a convenient way to run them;
* the `Black <https://black.readthedocs.io/en/stable/>`_ Python code formatter
  to ensure that code is written in a consistent style;
* `pycodestyle <https://pycodestyle.pycqa.org/en/latest/>`_ (known previously as
  `pep8`) to check that code follows the `Python PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
  style conventions.

Running the tests locally
#########################

#. Load a Python environment in the usual way for your location.

#. Run the tests::

      pytest -vv

   the warnings reported come from modules imported by `tempest_helper` and can be
   ignored but all of the tests must pass.

#. The version of Black run should match the version run by GitHub actions to prevent
   the automated tests from failing. The version of Black in scientific Python
   environments may lag behind the version used by GitHub Actions (the latest
   version installed using pip). Please contact your local Python expert if you need
   assistance installing the latest version.

   Black will modify your code so that it complies with its format. You may want to commit
   your changes using Git before running Black. Black can be run with::

    black .

#. pycodestyle can be run with::

    pycodestyle --max-line-length=88 .

   and a return value of 0 or no output to the termninal indicates success.

Building the documentation
##########################

In the checked out repository, make sure that your Python environment includes
Sphinx (standard scientific ones often do)::

   export PYTHONPATH=/path/to/tempest_helper
   cd docs
   make clean && make html

The build documentation can then be viewed in your browser (replace Firefox
with the name of your browser if required)::

   firefox build/html/index.html

Git workflow
############

This is just a suggested workflow for users who are new to Git.

#. Setup your SSH keys (https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh)
#. Obtain a local copy of the suite::

      git clone git@github.com:MetOffice/tempest_helper.git

#. Change directory into the repository::

      cd tempest_helper

#. If you have previously cloned the repository then update your local copy to
   the latest version::

      git checkout main
      git pull origin main

#. Create a branch for your changes and change to this branch::

      git fetch origin
      git branch <branch-name> origin/main
      git checkout <branch-name>

#. When you're happy with your changes, check the changes that you've made::

      git status
      git diff

#. You can then commit these changes and push them back up to GitHub::

      git commit -am '<commit message>'
      git push origin <branch-name>

#. You can make as many commits and pushes as you want.
#. Create a pull request at https://github.com/MetOffice/tempest_helper/compare
   by in the compare box selecting your branch and clicking on "Create pull request".

#. Once the code has been reviewed then the pull request can be merged using the
   GitHub web page for that pull request.

#. After merging, change your local copy of the code back to the main branch, delete
   your local copy of the development branch and pull in the changes from GitHub's
   main branch to your local copy::

      git checkout main
      git branch -D  <branch-name>
      git pull origin main

To examine complex changes, you might also want to consider using graphical diff
rather than just the command line, in which case you should add the following lines
to your ``~/.gitconfig`` file::

   [diff]
        tool = tkdiff
   [difftool]
        prompt = False

and then, rather than just ``git diff``, you can use::

   git difftool



