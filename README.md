# PTS Data Processing
There are a few scripts. This is my attempt at briefly explaining what each script does.

## Usage
### `clean.py`
```bash
python clean.py my_test_folder
```
Just run `python clean.py [folder_name]` where the `[folder_name]` is the name of the folder containing the run folders (containing the pub/sub data). It will crash if it doesn't select the folder with the following structure:

```
- my_test_folder
    - run_1
        - pub_0.csv
        - ...
        - pub_n.csv
        - sub_0.csv
        - ...
        - sub_n.csv
    - ...
    - run_n
```
### `analyse.py`
```bash
python analyse.py my_tests
```
Just run `python analyse.py [folder_containing_all_tests]` where `[folder_containing_all_tests]` is the folder containing all the tests in the following example structure:
```
- my_tests
    - my_test_one_folder
        - run_1
            - pub_0.csv
            - ...
            - pub_n.csv
            - sub_0.csv
            - ...
            - sub_n.csv
        - ...
        - run_n
    - ...
    - my_test_n_folder
```
---
The two main scripts are:

1. `clean.py`
2. `analyse.py`

## 1. `clean.py`
This script will basically organise the pub and sub data. 

For the pubs/latency, it will take the pub_0.csv file from each run and extract only the latency values and place it in a another central file with the corresponding `run_n_latency` heading. So the final central file produced will be labelled `average_latencies.csv` and will contain the following structure:

|     | run_1_latency | ... | run_n_latency | avg_non_mal_run_latency | avg_mal_run_latency | avg_run_latency |
|-----|---------------|-----|---------------|-------------------------|---------------------|-----------------|
| 0   | ...           | ... | ...           | ...                     | ...                 | ...             |
| ... | ...           | ... | ...           | ...                     | ...                 | ...             |
| n   | ...           | ..  | ...           | ...                     | ...                 | ...             |

It will basically also do this for each sub_n.csv file as well. So after everything is generated you will files of the following fashion:

```
- average_latencies.csv
- sub_0_output_average_throughputs.csv
- ...
- sub_n_output_average_throughputs.csv
```
---
## 2. `analyse.py`
This script will analyse all of the results and do checks for errors such as config file not being found, no run_n folders being found, etc. Below is a snippet from the commments explaining the checks:
```
Errors:
    1. Config not found.
        - Can't read any config data.
    2. 0 runs.
        - No restarts recorded in the config file.
        - Normally happens when test is interrupted before first restart.
    3. Config run and run_n folder amount mismatch.
        3.1. run_n < run
            - Hasn't completed all runs.
        3.2. run_n > run
            - HUH?!
    4. Can't read run amount from config.
        - Config file is corrupted/incomplete/something is wrong with it.
    5. Participant amount == 0 from config.
        - Either error with analysis.py or for some reason there are no participants in the config file.
    6. Config participants and test result participant amount mismatch.
        - Test results haven't been downloaded properly.
        6.1. Config participants > test result participants
            - Missing test data
        6.2. Config participants < test result participants
            - HUH?!
    7. Test duration hasn't been calculated in the config file.
        - Test has probably been interrupted and there is no test end
        7.1. Test Start exists but Test End doesn't
            - Test has been interrupted and didn't complete properly
        7.2. Test End exists but Test Start doesn't
            - HUH?!
    8. Test duration doesn't match duration set in config
        - Very weird...
```

The script will then output a table in the console listing all of the tests and the issues that were found. Here is an overview of the table output:
| Test   | Has Config | Config Runs | Data Runs | Config Participants | Data Participants | Test Duration | Comments                                                                                                         |
|--------|------------|-------------|-----------|---------------------|-------------------|---------------|------------------------------------------------------------------------------------------------------------------|
| test_n | Yes        | 1           | 1         | ...                 | ...               | 1:10:15       | Config duration and actual test duration do NOT match:     Config Duration: 6:00:00     Actual Duration: 1:10:15 |
| ...    | ...        | ...         | ...       | ...                 | ...               | ...           | ...                                                                                                              |