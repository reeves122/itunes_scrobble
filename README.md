# itunes_scrobble

This python script scans your iTunes library for new plays and scrobbles them to LastFM. 
The tracks which have been previously scrobbled are saved to a text file locally so they will not be scrobbled again
on the next run. 

Note: don't delete `previous_scrobbles.txt` or you will see lots of duplicate scrobbles for the time period configured.

## Requirements

- Python 3.6 or greater
- `pylast` python module
- A LastFM account and API Key + Secret
- iTunes configured to save the library as XML

## How to Run

Export environment variables for the configuration parameters needed:

- `DAYS_BACK` - How many days back to look for new plays. The default is 14. The script needs to run at least once during
this time to detect new plays.

- `ITUNES_XML` - The full system path to your iTunes library file. 

- `LASTFM_APIKEY`, `LASTFM_APISECRET`, `LASTFM_USERNAME`, `LASTFM_PASSWORD` - LastFM credentials


Run the script with `python3 itunes_scrobble.py`

