# [collect](#collect)

*Module*

Automate downloading an image using the Reddit API.

## [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper)

*Class*

Wrapper for Reddit submission objects to facilitate logging and URL
    downloading.

### [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper).[download](#collectredditsubmissionwrapperdownload)

*Function*

Save a picture to this path. Raises ValueError if the HTTP response
        indicates that we did not receive an image.

### [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper).[log](#collectredditsubmissionwrapperlog)

*Function*

Log the submission's title, comment URL, and link URL.

## [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper)

*Class*

Wrapper for Reddit listing generators to facilitate image downloading
    and handling certain behaviors.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_download](#collectredditlistingwrappernext_download)

*Function*

next(self) while downloading the submission's image.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_no_repeat](#collectredditlistingwrappernext_no_repeat)

*Function*

next(self) while skipping submissions that have already been
        collected.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_no_repeat_download](#collectredditlistingwrappernext_no_repeat_download)

*Function*

self.next_no_repeat() while downloading the submisson's image.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[flags_next_download](#collectredditlistingwrapperflags_next_download)

*Function*

Download the next submission's image according to the specified
        flags.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[flags_next_recover](#collectredditlistingwrapperflags_next_recover)

*Function*

Download the next submission's image but handle collection errors
        according to the flags.

## [collect](#collect).[Collect](#collectcollect)

*Class*

Perform image collection operations on a path.

### [collect](#collect).[Collect](#collectcollect).[reddit_listing](#collectcollectreddit_listing)

*Function*

Helper for new RedditListingWrapper at this path.

### [collect](#collect).[Collect](#collectcollect).[random](#collectcollectrandom)

*Function*

Return a random file within this directory. Raises FileNotFoundError
        if no suitable file was found.

## [collect](#collect).[PathBase](#collectpathbase)

*Class*

Provides general functionality for all Path types.

## [collect](#collect).[PathMeta](#collectpathmeta)

*Class*

Provides the numerous class methods for all Path types.

### [collect](#collect).[PathMeta](#collectpathmeta).[home](#collectpathmetahome)

*Function*

Return the user's home directory.

### [collect](#collect).[PathMeta](#collectpathmeta).[cwd](#collectpathmetacwd)

*Function*

Return the current working directory.

## [collect](#collect).[Path](#collectpath)

*Class*

Provides high level and cross platform file system manipulations on
    paths.

### [collect](#collect).[Path](#collectpath).[join](#collectpathjoin)

*Function*

Connect one or more file names onto this path.

### [collect](#collect).[Path](#collectpath).[realpath](#collectpathrealpath)

*Function*

Return the absolute path and eliminate symbolic links.

### [collect](#collect).[Path](#collectpath).[relpath](#collectpathrelpath)

*Function*

Return the abbreviated form of self relative to start. Default for
        start is the current working directory.

### [collect](#collect).[Path](#collectpath).[abspath](#collectpathabspath)

*Function*

Return the absolute path.

### [collect](#collect).[Path](#collectpath).[url_fname](#collectpathurl_fname)

*Function*

Join the filename part of a url to this path.

### [collect](#collect).[Path](#collectpath).[open](#collectpathopen)

*Function*

Open the file for changing.

### [collect](#collect).[Path](#collectpath).[exists](#collectpathexists)

*Function*

Check if the path exists.

### [collect](#collect).[Path](#collectpath).[is_dir](#collectpathis_dir)

*Function*

Check if the path is a directory.

### [collect](#collect).[Path](#collectpath).[is_file](#collectpathis_file)

*Function*

Check if the path is a file.

### [collect](#collect).[Path](#collectpath).[is_link](#collectpathis_link)

*Function*

Check if the path is a symbolic link.

### [collect](#collect).[Path](#collectpath).[is_abs](#collectpathis_abs)

*Function*

Check if the path is absolute.

### [collect](#collect).[Path](#collectpath).[contains_toplevel](#collectpathcontains_toplevel)

*Function*

Check if other is at the top level of self (a directory).

### [collect](#collect).[Path](#collectpath).[is_toplevel](#collectpathis_toplevel)

*Function*

Check if self is in the top level of other (a directory).

### [collect](#collect).[Path](#collectpath).[is_in_dir](#collectpathis_in_dir)

*Function*

return self in other
        Check if self is inside other (a directory).

### [collect](#collect).[Path](#collectpath).[rmtree](#collectpathrmtree)

*Function*

Delete every file inside a directory file.

### [collect](#collect).[Path](#collectpath).[remove](#collectpathremove)

*Function*

Remove a file or a directory (if empty).

### [collect](#collect).[Path](#collectpath).[remove_contents](#collectpathremove_contents)

*Function*

Remove each file within a directory.

### [collect](#collect).[Path](#collectpath).[mkdir](#collectpathmkdir)

*Function*

Make a directory exist under this path.
