__version__ = "0.2.2"


def _check_should_patch():
    try:
        import js
        return hasattr(js, "XMLHttpRequest") or hasattr(js, "fetch")
    except ImportError:
        return False


_SHOULD_PATCH = _check_should_patch()


def patch_requests(continue_on_import_error: bool = False):
    if not should_patch():
        return
    try:
        from ._requests import patch
    except ImportError:
        if continue_on_import_error:
            return
        raise
    else:
        patch()


def patch_urllib(continue_on_import_error: bool = False):
    if not should_patch():
        return

    try:
        from ._urllib import patch
    except ImportError:
        if continue_on_import_error:
            return
        raise
    else:
        patch()


def should_patch():
    return _check_should_patch()


def patch_all():
    patch_requests(continue_on_import_error=True)
    patch_urllib(continue_on_import_error=True)
