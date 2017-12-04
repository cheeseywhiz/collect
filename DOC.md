<h1 id="collect.RedditSubmissionWrapper">RedditSubmissionWrapper</h1>

```python
RedditSubmissionWrapper(self, parent_path, data)
```
Wrapper for Reddit submission objects to facilitate logging and URL
    downloading.
<h2 id="collect.RedditSubmissionWrapper.download">download</h2>

```python
RedditSubmissionWrapper.download(self)
```
Save a picture to this path. Raises ValueError if the HTTP response
        indicates that we did not receive an image.
<h2 id="collect.RedditSubmissionWrapper.log">log</h2>

```python
RedditSubmissionWrapper.log(self)
```
Log the submission's title, comment URL, and link URL.
<h1 id="collect.RedditListingWrapper">RedditListingWrapper</h1>

```python
RedditListingWrapper(self, path, api_url)
```
Wrapper for Reddit listing generators to facilitate image downloading
    and handling certain behaviors.
<h2 id="collect.RedditListingWrapper.next_download">next_download</h2>

```python
RedditListingWrapper.next_download(self)
```
next(self) while downloading the submission's image.
<h2 id="collect.RedditListingWrapper.next_no_repeat">next_no_repeat</h2>

```python
RedditListingWrapper.next_no_repeat(self)
```
next(self) while skipping submissions that have already been
        collected.
<h2 id="collect.RedditListingWrapper.next_no_repeat_download">next_no_repeat_download</h2>

```python
RedditListingWrapper.next_no_repeat_download(self)
```
self.next_no_repeat() while downloading the submisson's image.
<h2 id="collect.RedditListingWrapper.flags_next_download">flags_next_download</h2>

```python
RedditListingWrapper.flags_next_download(self, flags)
```
Download the next submission's image according to the specified
        flags.
<h2 id="collect.RedditListingWrapper.flags_next_recover">flags_next_recover</h2>

```python
RedditListingWrapper.flags_next_recover(self, flags)
```
Download the next submission's image but handle collection errors
        according to the flags.
<h1 id="collect.Collect">Collect</h1>

```python
Collect(self, path=None)
```
Perform image collection operations on a path.
<h2 id="collect.Collect.reddit_listing">reddit_listing</h2>

```python
Collect.reddit_listing(self, api_url)
```
Helper for new RedditListingWrapper at this path.
<h2 id="collect.Collect.random">random</h2>

```python
Collect.random(self)
```
Return a random file within this directory. Raises FileNotFoundError
        if no suitable file was found.
<h1 id="collect.PathBase">PathBase</h1>

```python
PathBase(self, path=None)
```
Provides general functionality for all Path types.
<h2 id="collect.PathBase.parts">parts</h2>

Split the path by the OS path slash separator.
<h2 id="collect.PathBase.basename">basename</h2>

The final element in the path.
<h2 id="collect.PathBase.split">split</h2>

Split the path's basename by filename and extension.
<h2 id="collect.PathBase.url_fname">url_fname</h2>

```python
PathBase.url_fname(url)
```
Return the filename part of a url.
<h1 id="collect.PathMeta">PathMeta</h1>

```python
PathMeta(self, /, *args, **kwargs)
```
Provides the numerous class methods for all Path types.
<h2 id="collect.PathMeta.home">home</h2>

```python
PathMeta.home(self)
```
Return the user's home directory.
<h2 id="collect.PathMeta.cwd">cwd</h2>

```python
PathMeta.cwd(self)
```
Return the current working directory.
<h1 id="collect.Path">Path</h1>

```python
Path(self, path=None)
```
Provides high level and cross platform file system manipulations on
    paths.
<h2 id="collect.Path.join">join</h2>

```python
Path.join(self, *others)
```
Connect one or more file names onto this path.
<h2 id="collect.Path.realpath">realpath</h2>

```python
Path.realpath(self)
```
Return the absolute path and eliminate symbolic links.
<h2 id="collect.Path.relpath">relpath</h2>

```python
Path.relpath(self, start=None)
```
Return the abbreviated form of self relative to start. Default for
        start is the current working directory.
<h2 id="collect.Path.abspath">abspath</h2>

```python
Path.abspath(self)
```
Return the absolute path.
<h2 id="collect.Path.url_fname">url_fname</h2>

```python
Path.url_fname(self, url)
```
Join the filename part of a url to this path.
<h2 id="collect.Path.open">open</h2>

```python
Path.open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```
Open the file for changing.
<h2 id="collect.Path.exists">exists</h2>

```python
Path.exists(self)
```
Check if the path exists.
<h2 id="collect.Path.is_dir">is_dir</h2>

```python
Path.is_dir(self)
```
Check if the path is a directory.
<h2 id="collect.Path.is_file">is_file</h2>

```python
Path.is_file(self)
```
Check if the path is a file.
<h2 id="collect.Path.is_link">is_link</h2>

```python
Path.is_link(self)
```
Check if the path is a symbolic link.
<h2 id="collect.Path.is_abs">is_abs</h2>

```python
Path.is_abs(self)
```
Check if the path is absolute.
<h2 id="collect.Path.contains_toplevel">contains_toplevel</h2>

```python
Path.contains_toplevel(self, other)
```
Check if other is at the top level of self (a directory).
<h2 id="collect.Path.is_toplevel">is_toplevel</h2>

```python
Path.is_toplevel(self, other)
```
Check if self is in the top level of other (a directory).
<h2 id="collect.Path.is_in_dir">is_in_dir</h2>

```python
Path.is_in_dir(self, other)
```
return self in other
        Check if self is inside other (a directory).
<h2 id="collect.Path.rmtree">rmtree</h2>

```python
Path.rmtree(self, ignore_errors=False, onerror=None)
```
Delete every file inside a directory file.
<h2 id="collect.Path.remove">remove</h2>

```python
Path.remove(self)
```
Remove a file or a directory (if empty).
<h2 id="collect.Path.remove_contents">remove_contents</h2>

```python
Path.remove_contents(self)
```
Remove each file within a directory.
<h2 id="collect.Path.mkdir">mkdir</h2>

```python
Path.mkdir(self, mode=511, *, exist_ok=False, dir_fd=None)
```
Make a directory exist under this path.
<h2 id="collect.Path.parent">parent</h2>

Move up one directory.
<h2 id="collect.Path.type">type</h2>

Return the MIME type of this file.
<h2 id="collect.Path.tree">tree</h2>

Generate all of the paths in this directory path.
