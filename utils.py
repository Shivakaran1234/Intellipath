import os
import tempfile


def save_uploaded_file(uploaded, filename_hint=None):
    """Save a Streamlit uploaded file to a temporary path and return path."""
    if filename_hint:
        suffix = os.path.splitext(filename_hint)[1]
    else:
        suffix = ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded.read())
    tmp.flush()
    tmp.close()
    return tmp.name