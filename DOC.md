# [collect](#collect)

*Module*

Automate downloading an image using the Reddit API.

## [collect](#collect).[RedditSubmissionWrapper](#collect.RedditSubmissionWrapper)

*Class*

Wrapper for Reddit submission objects to facilitate logging and URL
    downloading.

### [collect](#collect).[RedditSubmissionWrapper](#collect.RedditSubmissionWrapper).[download](#collect.RedditSubmissionWrapper.download)

*Function*

Save a picture to this path. Raises ValueError if the HTTP response
        indicates that we did not receive an image.

### [collect](#collect).[RedditSubmissionWrapper](#collect.RedditSubmissionWrapper).[log](#collect.RedditSubmissionWrapper.log)

*Function*

Log the submission's title, comment URL, and link URL.

## [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper)

*Class*

Wrapper for Reddit listing generators to facilitate image downloading
    and handling certain behaviors.

### [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper).[next_download](#collect.RedditListingWrapper.next_download)

*Function*

next(self) while downloading the submission's image.

### [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper).[next_no_repeat](#collect.RedditListingWrapper.next_no_repeat)

*Function*

next(self) while skipping submissions that have already been
        collected.

### [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper).[next_no_repeat_download](#collect.RedditListingWrapper.next_no_repeat_download)

*Function*

self.next_no_repeat() while downloading the submisson's image.

### [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper).[flags_next_download](#collect.RedditListingWrapper.flags_next_download)

*Function*

Download the next submission's image according to the specified
        flags.

### [collect](#collect).[RedditListingWrapper](#collect.RedditListingWrapper).[flags_next_recover](#collect.RedditListingWrapper.flags_next_recover)

*Function*

Download the next submission's image but handle collection errors
        according to the flags.

## [collect](#collect).[Collect](#collect.Collect)

*Class*

Perform image collection operations on a path.

### [collect](#collect).[Collect](#collect.Collect).[reddit_listing](#collect.Collect.reddit_listing)

*Function*

Helper for new RedditListingWrapper at this path.

### [collect](#collect).[Collect](#collect.Collect).[random](#collect.Collect.random)

*Function*

Return a random file within this directory. Raises FileNotFoundError
        if no suitable file was found.

## [collect](#collect).[PathBase](#collect.PathBase)

*Class*

Provides general functionality for all Path types.

## [collect](#collect).[PathMeta](#collect.PathMeta)

*Class*

Provides the numerous class methods for all Path types.

### [collect](#collect).[PathMeta](#collect.PathMeta).[home](#collect.PathMeta.home)

*Function*

Return the user's home directory.

### [collect](#collect).[PathMeta](#collect.PathMeta).[cwd](#collect.PathMeta.cwd)

*Function*

Return the current working directory.

## [collect](#collect).[Path](#collect.Path)

*Class*

Provides high level and cross platform file system manipulations on
    paths.

### [collect](#collect).[Path](#collect.Path).[join](#collect.Path.join)

*Function*

Connect one or more file names onto this path.

### [collect](#collect).[Path](#collect.Path).[realpath](#collect.Path.realpath)

*Function*

Return the absolute path and eliminate symbolic links.

### [collect](#collect).[Path](#collect.Path).[relpath](#collect.Path.relpath)

*Function*

Return the abbreviated form of self relative to start. Default for
        start is the current working directory.

### [collect](#collect).[Path](#collect.Path).[abspath](#collect.Path.abspath)

*Function*

Return the absolute path.

### [collect](#collect).[Path](#collect.Path).[url_fname](#collect.Path.url_fname)

*Function*

Join the filename part of a url to this path.

### [collect](#collect).[Path](#collect.Path).[open](#collect.Path.open)

*Function*

Open the file for changing.

### [collect](#collect).[Path](#collect.Path).[exists](#collect.Path.exists)

*Function*

Check if the path exists.

### [collect](#collect).[Path](#collect.Path).[is_dir](#collect.Path.is_dir)

*Function*

Check if the path is a directory.

### [collect](#collect).[Path](#collect.Path).[is_file](#collect.Path.is_file)

*Function*

Check if the path is a file.

### [collect](#collect).[Path](#collect.Path).[is_link](#collect.Path.is_link)

*Function*

Check if the path is a symbolic link.

### [collect](#collect).[Path](#collect.Path).[is_abs](#collect.Path.is_abs)

*Function*

Check if the path is absolute.

### [collect](#collect).[Path](#collect.Path).[contains_toplevel](#collect.Path.contains_toplevel)

*Function*

Check if other is at the top level of self (a directory).

### [collect](#collect).[Path](#collect.Path).[is_toplevel](#collect.Path.is_toplevel)

*Function*

Check if self is in the top level of other (a directory).

### [collect](#collect).[Path](#collect.Path).[is_in_dir](#collect.Path.is_in_dir)

*Function*

return self in other
        Check if self is inside other (a directory).

### [collect](#collect).[Path](#collect.Path).[rmtree](#collect.Path.rmtree)

*Function*

Delete every file inside a directory file.

### [collect](#collect).[Path](#collect.Path).[remove](#collect.Path.remove)

*Function*

Remove a file or a directory (if empty).

### [collect](#collect).[Path](#collect.Path).[remove_contents](#collect.Path.remove_contents)

*Function*

Remove each file within a directory.

### [collect](#collect).[Path](#collect.Path).[mkdir](#collect.Path.mkdir)

*Function*

Make a directory exist under this path.
