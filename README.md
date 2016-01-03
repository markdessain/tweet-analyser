# tweet-analyser
Application that takes in a search query and analyses the tweets for common patterns.

Requires:
- Python3
- Redis
- Linux / Mac (Python RQ does not run under Windows - http://python-rq.org/docs/)

Install:
- pip3 freeze > requirements.txt

Run Tests:
- honcho start -f proc/TestProcfile -e environment/test
- nosetests

Run Main:
- honcho start -e environment/dev 
