# likedTweetsDownloader

A little program to download your most recent Twitter likes, in the order you liked them

### Configuration
A config file (conf.yml) should exist, with the following required:

- **user_id**, the ID of the Twitter user to download faves from
- **bearer_token**, the Twitter application bearer token to use for access to the Twitter API

And the following optional:

- **gallery-dl_path**, the path to the gallery-dl executable, if this isn't in the PATH variable

#### Additional configuration
As gallery-dl is used for downloading, all of the gallery-dl specific configuration can be specified, in the same directory as a usual gallery-dl configuration file would be placed. This can contain configuration like renaming the downloaded files, providing cookies/OAuth to access content from locked Twitter accounts, stopping once a certain number of files have already been downloaded, etc

## Dependencies
 - [gallery-dl](https://github.com/mikf/gallery-dl), for doing the actual downloading of content
 - [pyyaml](https://pypi.org/project/PyYAML/), for parsing the configuration file

## Usage

To run the script, call it

```bash
$ python3 src/main.py
```
