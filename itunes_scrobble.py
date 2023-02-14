from datetime import datetime, timedelta
import os
import plistlib
import time

import pylast

DAYS_BACK = int(os.environ.get('DAYS_BACK', 14))
PREVIOUS_SCROBBLES = os.environ.get('PREVIOUS_SCROBBLES', '/iTunes/previous_scrobbles.txt')
ITUNES_XML = os.environ.get('ITUNES_XML', '/iTunes/iTunes Music Library.xml')

LASTFM = pylast.LastFMNetwork(api_key=os.environ.get('LASTFM_APIKEY'),
                              api_secret=os.environ.get('LASTFM_APISECRET'),
                              username=os.environ.get('LASTFM_USERNAME'),
                              password_hash=pylast.md5(os.environ.get('LASTFM_PASSWORD')))


def load_previous_scrobbles():
    """
    Load the list of tracks that we scrobbled in previous runs
    :return: List of track timestamps
    """
    try:
        with open(PREVIOUS_SCROBBLES) as handle:
            previous_scrobbles = handle.read().splitlines()
            print(f'Previous scrobbles: {len(previous_scrobbles)}')
        return previous_scrobbles
    except FileNotFoundError:
        return []


def save_scrobble(track_datetime):
    """
    Save a track play datetime to the list of previous scrobbles
    :param track_datetime: datetime object of track play
    """
    with open(PREVIOUS_SCROBBLES, 'a+') as handle:
        handle.write(f'{track_datetime}\n')


def load_library():
    """
    Load the iTunes XML library file
    :return: dictionary of itunes library
    """
    print(f'Loading iTunes XML file: {ITUNES_XML}')
    with open(ITUNES_XML, 'rb') as handle:
        return plistlib.load(handle)


def scrobble_track(track):
    """
    Call the LastFM API to scrobble a track play
    :param track: dictionary of a track
    """
    LASTFM.scrobble(artist=track['Artist'], title=track['Name'], timestamp=track['Play Date UTC'])
    print('Track was scrobbled successfully')
    time.sleep(1)  # Throttle API calls


if __name__ == '__main__':

    # Generate a datetime to use as the starting point when looking for new track plays
    start_time = datetime.utcnow() - timedelta(days=DAYS_BACK)

    previous_scrobbles = load_previous_scrobbles()
    library = load_library()

    for _, track in library['Tracks'].items():

        if 'Artist' not in track.keys():
            continue
        if 'Album' not in track.keys():
            continue
        if 'Play Date UTC' not in track.keys():
            continue
        if track['Play Date UTC'] < start_time:
            continue
        if str(track['Play Date UTC']) in previous_scrobbles:
            continue

        print(f"Found a new play: {track['Play Date UTC']} - {track['Name']} - {track['Album']}")
        scrobble_track(track)
        save_scrobble(track['Play Date UTC'])
