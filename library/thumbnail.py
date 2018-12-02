from library.models import SnapShot


def create_or_update(thumbnails: list, bookmark_obj: SnapShot)->list:
    if type(thumbnails) is list:
        thumbnails.append(bookmark_obj)
    else:
        thumbnails = [bookmark_obj]
    return thumbnails
