# [collect](#collect)

*Module*

Automate downloading an image using the Reddit API.

## [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper)

*Class*

Wrapper for Reddit submission objects to facilitate logging and URL
    downloading.

### [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper).[download](#collectredditsubmissionwrapperdownload)

*Method of class [collect.RedditSubmissionWrapper](#collectredditsubmissionwrapper)*

Save a picture to this path. Raises `ValueError` if the HTTP
        response indicates that we did not receive an image.

### [collect](#collect).[RedditSubmissionWrapper](#collectredditsubmissionwrapper).[log](#collectredditsubmissionwrapperlog)

*Method of class [collect.RedditSubmissionWrapper](#collectredditsubmissionwrapper)*

Log the submission's title, comment URL, and link URL.

## [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper)

*Class*

Wrapper for Reddit listing generators to facilitate image downloading
    and handling certain behaviors.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_download](#collectredditlistingwrappernext_download)

*Method of class [collect.RedditListingWrapper](#collectredditlistingwrapper)*

`next([self](#collectredditlistingwrapper))` while downloading the submission's image.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_no_repeat](#collectredditlistingwrappernext_no_repeat)

*Method of class [collect.RedditListingWrapper](#collectredditlistingwrapper)*

`next([self](#collectredditlistingwrapper))` while skipping submissions that have already been
        collected.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[next_no_repeat_download](#collectredditlistingwrappernext_no_repeat_download)

*Method of class [collect.RedditListingWrapper](#collectredditlistingwrapper)*

`[self](#collectredditlistingwrapper).next_no_repeat()` while downloading the submisson's
        image.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[flags_next_download](#collectredditlistingwrapperflags_next_download)

*Method of class [collect.RedditListingWrapper](#collectredditlistingwrapper)*

Download the next submission's image according to the specified
        flags.

### [collect](#collect).[RedditListingWrapper](#collectredditlistingwrapper).[flags_next_recover](#collectredditlistingwrapperflags_next_recover)

*Method of class [collect.RedditListingWrapper](#collectredditlistingwrapper)*

Download the next submission's image but handle collection errors
        according to the flags.

## [collect](#collect).[Collect](#collectcollect)

*Class*

Perform image collection operations on a path.

### [collect](#collect).[Collect](#collectcollect).[reddit_listing](#collectcollectreddit_listing)

*Method of class [collect.Collect](#collectcollect)*

Helper for new `RedditListingWrapper` at this path.

### [collect](#collect).[Collect](#collectcollect).[random](#collectcollectrandom)

*Method of class [collect.Collect](#collectcollect)*

Return a random file within this directory. Raises
        `FileNotFoundError` if no suitable file was found.

## [collect](#collect).[PathBase](#collectpathbase)

*Class*

Provides general functionality for all Path types.

### [collect](#collect).[PathBase](#collectpathbase).[url_fname](#collectpathbaseurl_fname)

*Static Method of class [collect.PathBase](#collectpathbase)*

Return the filename part of a url.

## [collect](#collect).[PathMeta](#collectpathmeta)

*Class*

Provides the numerous class methods for all Path types.

### [collect](#collect).[PathMeta](#collectpathmeta).[home](#collectpathmetahome)

*Method of class [collect.PathMeta](#collectpathmeta)*

Return the user's home directory.

### [collect](#collect).[PathMeta](#collectpathmeta).[cwd](#collectpathmetacwd)

*Method of class [collect.PathMeta](#collectpathmeta)*

Return the current working directory.

## [collect](#collect).[Path](#collectpath)

*Class*

Provides high level and cross platform file system manipulations on
    paths.

### [collect](#collect).[Path](#collectpath).[join](#collectpathjoin)

*Method of class [collect.Path](#collectpath)*

Connect one or more file names onto this path.

### [collect](#collect).[Path](#collectpath).[realpath](#collectpathrealpath)

*Method of class [collect.Path](#collectpath)*

Return the absolute path and eliminate symbolic links.

### [collect](#collect).[Path](#collectpath).[relpath](#collectpathrelpath)

*Method of class [collect.Path](#collectpath)*

Return the abbreviated form of self relative to start. Default for
        `start` is the current working directory.

### [collect](#collect).[Path](#collectpath).[abspath](#collectpathabspath)

*Method of class [collect.Path](#collectpath)*

Return the absolute path.

### [collect](#collect).[Path](#collectpath).[url_fname](#collectpathurl_fname)

*Method of class [collect.Path](#collectpath)*

Join the filename part of a url to `[self](#collectpath)`.

### [collect](#collect).[Path](#collectpath).[open](#collectpathopen)

*Method of class [collect.Path](#collectpath)*

Open the file for changing.

### [collect](#collect).[Path](#collectpath).[exists](#collectpathexists)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` exists on the filesystem.

### [collect](#collect).[Path](#collectpath).[is_dir](#collectpathis_dir)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` is a directory.

### [collect](#collect).[Path](#collectpath).[is_file](#collectpathis_file)

*Method of class [collect.Path](#collectpath)*

Check `[self](#collectpath)` is a file on the filesystem.

### [collect](#collect).[Path](#collectpath).[is_link](#collectpathis_link)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` is a symbolic link.

### [collect](#collect).[Path](#collectpath).[is_abs](#collectpathis_abs)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` is an absolute path.

### [collect](#collect).[Path](#collectpath).[contains_toplevel](#collectpathcontains_toplevel)

*Method of class [collect.Path](#collectpath)*

Check if `other` is at the top level of `[self](#collectpath)` (a directory).

### [collect](#collect).[Path](#collectpath).[is_toplevel](#collectpathis_toplevel)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` is in the top level of `other` (a directory).

### [collect](#collect).[Path](#collectpath).[is_in_dir](#collectpathis_in_dir)

*Method of class [collect.Path](#collectpath)*

Check if `[self](#collectpath)` is inside `other` (a directory).

### [collect](#collect).[Path](#collectpath).[rmtree](#collectpathrmtree)

*Method of class [collect.Path](#collectpath)*

Delete every file inside `[self](#collectpath)` (a directory).

### [collect](#collect).[Path](#collectpath).[remove](#collectpathremove)

*Method of class [collect.Path](#collectpath)*

Remove a file or a directory (if empty).

### [collect](#collect).[Path](#collectpath).[remove_contents](#collectpathremove_contents)

*Method of class [collect.Path](#collectpath)*

Remove each file within `[self](#collectpath)` (a directory).

### [collect](#collect).[Path](#collectpath).[mkdir](#collectpathmkdir)

*Method of class [collect.Path](#collectpath)*

Make a directory exist under `[self](#collectpath)`.
