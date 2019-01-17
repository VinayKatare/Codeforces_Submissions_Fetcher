# Codeforces Submissions Fetcher

A Python Script for downloading Codeforces ACCEPTED submissions.
```
Requirement : Python3
```
## Instructions
Install the dependency `bs4`
```
pip install bs4
```
Download and Run fetch.py
```
python fetch.py
```
Then Enter your Codeforces handle, It will create folder "Code_\<handle\>" and saves the submissions there.
Each file name contains ContestID, Problem_type, Problem_name.
```
NOTE : # Each solutions file will have the Problem link as comment line.
       # In case of multiple submission to same problem, Only one solution file will be created for each Problem having the latest accepted solution.
