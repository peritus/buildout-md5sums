import zc.buildout.download

FALSE_VALUES = ('no', 'false', '0', 'off')

_original_methods = {}

def _replace_parameters(md5sums, args, kwargs):
    url = args[1]

    chosen = md5sums.get(url, None)

    if not chosen and '#md5' in url:
        try:
            url, chosen = url.split("#md5=")
        except ValueError, e:
            try:
                url, chosen = url.split("#md5sum=")
            except:
                pass

    if chosen:
        if 'md5sum' in kwargs:
            kwargs['md5sum'] = chosen
        elif len(args) > 2:
            args = args[:2] + (chosen,) + args[3:]

    args = args[:1] + (url,) + args[2:]

    return args, kwargs

def ext(buildout):
    global _original_methods

    md5sums = {}

    # default = true
    allow_picked_downloads = not (
      'buildout' in buildout and \
      'allow-picked-downloads' in buildout['buildout'] and \
      buildout['buildout']['allow-picked-downloads'].strip() in FALSE_VALUES
    )

    if not allow_picked_downloads:
        print "We won't allow picking downloads that have no md5sums"

    if 'md5sums' in buildout['buildout']:
        for line in buildout['buildout']['md5sums'].splitlines():
            try:
                url, md5sum = line.split("=")
            except ValueError:
                continue

            url = url.strip()
            md5sum = md5sum.strip()

            if url.startswith("#"):
                continue

            md5sums[url] = md5sum

    # I'm in your monkey patching your buildout!
    def intercept_md5sum(fun):
        def inner(*args, **kwargs):
            args, kwargs = _replace_parameters(md5sums, args, kwargs)

            if not allow_picked_downloads:
                if not (('md5sum' in kwargs and kwargs['md5sum']) or \
                        (len(args) > 2) and args[2]):
                    raise zc.buildout.UserError(
                        "Attempting to download %s without md5sum" % args[1])

            return fun(*args, **kwargs)
        inner.__doc__ = fun.__doc__
        return inner

    # save original methods
    _original_methods['__call__'] = zc.buildout.download.Download.__call__
    _original_methods['download'] = zc.buildout.download.Download.download
    _original_methods['download_cached'] = zc.buildout.download.Download.download_cached

    # patch a monkey
    zc.buildout.download.Download.__call__ = \
      intercept_md5sum(zc.buildout.download.Download.__call__)

    zc.buildout.download.Download.download = \
      intercept_md5sum(zc.buildout.download.Download.download)

    zc.buildout.download.Download.download_cached = \
      intercept_md5sum(zc.buildout.download.Download.download_cached)

def unload(buildout):
    global _original_methods

    # restore original methods
    zc.buildout.download.Download.__call__ = _original_methods['__call__']
    zc.buildout.download.Download.download = _original_methods['download']
    zc.buildout.download.Download.download_cached = _original_methods['download_cached']

