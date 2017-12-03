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

Automate downloading an image from the Reddit json API.

optional arguments:
  -h, --help            show this help message and exit
  --dir PATH            Set the download location. Default
                        $HOME/.cache/collect
  -v                    Set verbosity level.

Subcommands:
  {reddit,random,clear}
```

```
usage: collect reddit [-h] [--all] [--new] [--no-repeat] [--url URL]

Carry out the collection.

optional arguments:
  -h, --help         show this help message and exit
  --all, -a          Print a random file if collection failed.
  --new, -n          Print a file from the json API if collection failed.
  --no-repeat, -r    Fail if each url from the json API has been downloaded.
  --url URL, -u URL  Set the URL for the Reddit json API. Default
                     https://www.reddit.com/r/earthporn/hot/.json?limit=10
```
