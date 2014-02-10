Send a Sickbeard post processing email notification.

This is designed to be called by Sickbeard as an additional post-processing script (see
[Sick Beard advanced settings](https://code.google.com/p/sickbeard/wiki/AdvancedSettings)).

It takes 6 parameters (although it only uses 3-5):

 1. Final full path to the episode file
 2. Original name of the episode file
 3. Series TVDB id
 4. Season number
 5. Episode number
 6. Episode air date

You will need to set the following values in `config.ini`:

 1. `[TVDB]`
    1. `[tvdb_api_key]` - A TVDB API key
 2. `[Mail]`
    1. `[mail_server]` - An SMTP mail server (currently set for GMail)
    2. `[mail_port]` - SMTP mail server port (currently set for GMail)
    3. `[mail_account]` - SMTP mail account name
    4. `[mail_password]` - SMTP mail account password
 3. `[Notification]`
    1. `[mail_to]` - Email recepient
    2. `[mail_from]` - Email from address