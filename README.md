python setup.py install # will install sw script into virtualenv's bin path

./run.sh sample_check_results.csv # will sort the samples and store into temp.txt then run sw script this files as argument


### Improvements

- split sorted input file by check ids then with the help of GNU Parallel process in parallel

- run with python script with pypy jit, results in significant speed improvement with more memory requirements :)

- add tests
