# TelegramFinder
Find channels and groups in telegram by keywords

# Installation
Download the repository. In linux you can use git:
```
git clone https://github.com/amal518/TelegramFinder.git
```

Install dependencies:
```
pip install -r requrements.txt
```

Now you can run app by writing ```python main.py```.

# Dependencies
**telethon 1.36.0** to establish connection with telegram servers, and **tqdm==4.66.5** for a more beautiful output.

# Usage
You need to edit __config.ini__ file.

Fields __api_id__ and __api_hash__ you can get from https://my.telegram.org/auth?to=apps.

The __phone__ and __username__ fields must be filled with your data.

In field __keywords__ you need to write keywords separeted by semicolons, example:
```
keywords = some;words;in;English
```

__Type__ field must be filled with one of three values: 

group - search only groups
channel - search only for channels
all - search for all types

After configuration run ```python main.py```. When the program is executed, you may see __output.txt__ file with URLs to channels/groups.
