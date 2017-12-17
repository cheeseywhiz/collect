```
install:
    make
    [sudo] make install
```

`make` installs as `--user` if not in a virtual environment. Root access is
required for installing the script in `/usr/bin` if not in a virtual
environment.

```
usage: collect [-h] [--dir PATH] [-v] {reddit,random,clear} ...

Automate downloading an image using the Reddit API.

optional arguments:
  -h, --help            show this help message and exit
  --dir PATH            Set the download location. Default
                        ~/.cache/collect
  -v                    Set verbosity level.

Subcommands:
  {reddit,random,clear}
```

```
usage: collect reddit [-h] [--all] [--new] [--no-repeat] [--url URL]
                      [--user NAME]

Carry out the collection.

optional arguments:
  -h, --help            show this help message and exit
  --all, -a             Print a random file if collection failed.
  --new, -n             Print a file from the recent listing if collection
                        failed.
  --no-repeat, -r       Fail if each URL in the listing has been downloaded.
  --url URL, -u URL     Set the URL for the Reddit API listing. Default
                        r/earthporn/hot?limit=10
  --user NAME, -s NAME  Select non-default praw.ini profile.
```
