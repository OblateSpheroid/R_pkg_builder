# R Package Builder: for storing specific versions of R packages

## Ad-hoc method of adding packages
#### Adding a package to the repo
To add a new package to this repo (e.g., `tweenr`, version `0.1.5`):

1. Add it's zip file (e.g., `tweenr_0.1.5.zip`) to `bin/windows/contrib/3.4`
2. From the local directory where the zip files are (`setwd(bin/windows/contrib/3.4)`), run this is R to generate the PACKAGES index file:
	```
	require(tools)
	tools::write_PACKAGES('.', type='win.binary')
	```
3. Upload these files to `bin/windows/contrib/3.4`:
	```
	git add .
	git commit -m "adding new packages"
	git push origin master
	```

#### Installing a package from this repo
The package can then be installed using the `repos=https://oblatespheroid.github.io/R_pkg_builder` argument. E.g.:

    install.packages('tweenr', repos='repos=https://oblatespheroid.github.io/R_pkg_builder', type='win.binary')


## Scripted method of adding multiple packages

#### Requirements:
 - Python 3
 - packages in `requirements.txt`.
   - Within a virtual env, run: `pip install requirements-pip.txt`
   - Or, within a conda environment, run: `conda install -f requirements-conda.txt`

#### Run:
In Windows, from the main directory in your local repo (`RPackages`), something like:

    python R_pkg_builder.py LIBFOLDER=%RHOME%/library OUTFOLDER=%cd%/bin/windows/contrib/3.4

If your packages are in another folder, change LIBFOLDER to that directory.