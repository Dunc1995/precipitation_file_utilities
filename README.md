## 1.0 - Usage
> Please follow section 2.0 and 3.0 for packaging and installation.

Provided installation has been successful, the script's help information should be as follows:

```
(env)  ✘  ~/Desktop  prefileutils -h
usage: prefileutils [-h] --input_file_path INPUT_FILE_PATH
                    [--log_verbosity LOG_VERBOSITY]

Reads a .pre file such that precipitation data can be transformed and uploaded
to a SQLite database.

optional arguments:
  -h, --help            show this help message and exit
  --input_file_path INPUT_FILE_PATH, -i INPUT_FILE_PATH
                        Input file for processing.
  --log_verbosity LOG_VERBOSITY, -v LOG_VERBOSITY
                        Logging verbosity (1 to 5) - level 1 is most verbose,
                        level 5 logs critical entries only.
```

The `--input_file_path` is required and if the script parses it correctly, it should create a data directory and start uploading data rows to a locally stored SQLite database.

## 2.0 - Packaging
If making edits to the source code, it can be packaged appropriately by running the following command in the root directory of the repository:
```python
python setup.py sdist
```
Provided there are no errors, a new `./dist/<file>.tar.gz` file should have been created - we can then use this file for installation in the next section.

## 3.0 - Installation
> These instructions outline how to install the script on a Linux OS. On Windows, the same process will instead generate a `.exe` file which can be used in the same manner. However note that on Windows the the prefileutils.exe file must be in the same directory as the `prefileutils-script.py`.  

It's probably best to test this script in isolation. I would recommend creating a new directory, then extracting the archive file from section 1.0 into this directory as follows:
```python
./test_directory/extracted-package-directory
```
Within the `test_directory`, run the following commands:  
```
python -m venv env;
source env/bin/activate
```
You should now have a directory that looks like:
```
./test_directory/env
./test_directory/extracted-package-directory
```
Navigate to the `extracted-package-directory` and run the following command:
```
python setup.py install
```
The `prefileutils` application should now be installed and can be verified by entering:
```
which prefileutils
```
which should yield something similar to:
```
/home/<person>/test_directory/env/bin/prefileutils
```
Finally you can exit the virtual environment by entering `deactivate`.

## 4.0 - References
This project was for the following challenge:

> So you're curious to know whether you've got what it takes to join JBA Software. Below is our code challenge to you.
>
> At JBA we regularly receive varied datasets from our clients. To work with them efficiently, we often have to transform them into something which we can use more readily. We want to see your development skills in data manipulation.
>
>
> The example data contains precipitation (rainfall) data that we would like in a database table with the following structure:
>
> Xref	| Yref	| Date	| Value  
> 1 |	148 |	1/1/1991	| 3020  
> 1	| 148	| 2/1/1991 |	2820  
>
> The code that you write should have an option to specify the file name, read in the header data, transform the data, create the database table structure and insert the information into the database.
>
> You are free to use any programming language and database technology that you choose. For junior developers we're looking to see what you can do; for senior developers we want to see evidence of your coding standards.
>
> Once you're done - send your code (or link to a source control repository), CV and covering letter to careers@jbasoftware.com. If we need to compile your code, please let us know of any compiler flags required.
