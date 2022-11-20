
# Steps to create a package

https://www.youtube.com/watch?v=GIF3LaRqgXo&ab_channel=CodingTech

Create `helloworld.py` and `create setup.py`

Run `py setup.py bdist_wheel`

This will run setup.py. `bdist_wheel` needs to be installed (using `pip`). This will create `build`, `dist` and `helloworld.egg-info`

Run `py -m pip install -e .`. `-e` prevents pip from copying the package to `site-packages`, and `.` means that we are installing the current directory.

To upload the package

`py -m twine upload dist/*`

To upload a new version of the package, the version number must be changed, then do:

`py setup.py bdist_wheel sdist`
`py -m twine upload --skip-existing dist/*`
