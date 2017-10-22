```
install:
    make
    [sudo] make install
```

`make install` installs as `--user` if not in a virtual environment. Root access
is required for symbolically linking the `$HOME/.local/bin` script to `/usr/bin`.

```
usage: collect [-h] [--clear] [--collect] [--no-repeat] [--random] [-u URL]
               [-v]
               [PATH]

Automate downloading an image from the Reddit json API.

positional arguments:
  PATH         Set where images are downloaded to. Default
               $HOME/.cache/collect

optional arguments:
  -h, --help   show this help message and exit
  --clear      Clear the cache file and the image directory.
  --collect    Carry out the collection. Usable in conjunction with --random
               if collection failed.
  --no-repeat  Collect a new image each time.
  --random     Print out a random image path in the collection folder.
  -u URL       Set the URL for the Reddit json API. Default
               https://www.reddit.com/r/earthporn/hot/.json?limit=10
  -v           Output post information or -vv for debug information.
```
