# Programming vacancies compare.
A service for collecting statistics on programmers' salaries among the most popular programming languages based on HeadHunter and SuperJob  sites.
## Prerequisites:
To run the script successfully you will need to get API token.
+ Sign up here: [SuperJob](https://api.superjob.ru)
  > API token looks like this (example): **v1.r.12645444.ae08567rfgfgdgd466fdgd2345gbc0ced562e9375b47.bbecdfsdfs32454yggfdf989348b6**   
## Installing:
Install Python3 latest version. Install PyCharm IDE, if you need it.
> To isolate the project, I'd recommend to use a virtual environment model. [vertualenv/venv](https://docs.python.org/3/library/venv.html).
 ## Preparing to run the script.
+ Create a virtualenv and activate it.
+ Then use pip (or pip3, there is a conflict with Python2) to install the dependencies (use the requirements.txt file):
```bash
% pip install -r requirements.txt
```
> For permanent set, create .env file inside project folder and add variable like this:
```python
SJ_TOKEN = "YOUR_TOKEN"
```
> If you don't want to create .env file, then for a quick test run, export your private "SJ_TOKEN" by this command:
``` bash
% export SJ_TOKEN="YOUR_TOKEN"
```
## Run the script.
Use command:
``` bash
% python3 main.py  
```
Output:
image.png
## Project goals.
*The program was designed by a student from online web development courses for educational purposes [Devman](https://dvmn.org).*