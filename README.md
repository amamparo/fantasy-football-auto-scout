# Fantasy Football Auto Scout

![Screenshot](img/screenshot.png)

## Requirements
- Python 3.7.x
- [Pipenv](https://pypi.org/project/pipenv/)
- An active Yahoo Fantasy Football team

## Setup
Just install the pip dependencies with `pipenv install`

## Environment Variables
Add these to a gitignored file called `.env` at the repository's root

| Environment&nbsp;Variable | Type | Description |
| --- | --- | --- |
| `LEAGUE_ID` | number | this can be retrieved from the URL on any league page |
| `REQUEST_COOKIE` | string | The value of the `cookie` HTTP header that gets passed around as you navigate through your Yahoo Fantasy Football league in the web browser (you'll need to use your browser's dev tools to grab this value) |

## To Run
`pipenv run scrape_pipeline`

## TODO
- deploy this as a once-daily process on AWS that emails the report to me
- add additional scouting tasks for things like finding a waiver/FA prospect, reminders to optimize my starting lineup, etc