# This module

This moudle renames Gmail labels according to pre-defined find-and-replace patterns.

It uses Google Gmail API.

It was verified with Python 3.11.7 on 2024-01-09.

# Origin

The source code is based on a Gmail Python quickstart provided by Google. For details, visit

https://developers.google.com/gmail/api/quickstart/python?hl=en



# To run

Install python, pip. Then do this:

```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
# This opens Google OAuth sign-in page in your web browser
python <main program>.py 
```


# Test

To test,

```
python -m pytest tests
```