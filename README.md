# AniList Liker

So did you ever go through Anilist and wondered, how the heck can I automate the process of liking my friends' activities? Well, yeah, I don't know why I did this, but here you go - this is much easier than clicking around.

## How it works

The script first logs in to the user's Anilist account, then goes to the "Following" or "Global" activity tab. It then iterates through all of the activity entries on the page, clicking the "Like" button for each entry that is not already liked. The script repeats this process until it gets stopped by the user.

It will skip already liked activity entries, and waits if there is a rate limit.

## Configuration

The script takes four parameters:

* **activity**: The type of activity to like. Valid values are "following" and "global".
* **speedometer**: The speed at which the script should run. Valid values are "fast", "medium", and "slow".
* **email**: The user's Anilist email address.
* **password**: The user's Anilist password.

These parameters can be configured in the **config.yaml** file.

## Installation

```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt.
```

**Important**: You must adjust the path of Chrome binary location and the Chrome driver in the **options.binary_location** and **chrome_driver_binary** variables to reflect the correct paths on your machine.

## How to use
1. Update the configuration with your desired settings.

2. Run the start.py script
```bash
python start.py
# or
python3 start.py
```

3. The login page will open in a Chrome window. Follow the instructions from the
terminal.

4. The script will begin liking activity entries. (Have fun) 💀

## Clarification

I'm not responsible for any damage caused by this script. Use at your own risk.

![information](/github/pictures/information.png "Information")

### Why?

Just to learn more about Selenium and web scraping.

![bored](/github/pictures/chill.gif "Bored")