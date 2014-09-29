Habitus Desktop
===============
This software is intended for the tracking of app usage in OS X.

# Code dependencies
This code uses Rumps, available on https://github.com/tito/rumps. This version is the update for OS X Mavericks of the original code available in https://github.com/jaredks/rumps

# Issues
Throughout time, two different approaches were developed for the app tracking system: Timers and threads using timers. Although threading and timers were the most effective solution, this solution is highly inefficient and therefore, new ways using events are being explored.

# Sending info
A JSON file with the following information should be created:

```
{
    "from": Sender e-mail, 
    "password": Sender e-mail password,
    "to": Receiver
}
```

I personally used the service https://sendtodropbox.com/ for the tests to send my information to my Dropbox account.
