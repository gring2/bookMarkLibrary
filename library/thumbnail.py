def create_or_update(thumbnails, bookmark_obj):
    if type(thumbnails) is list:
        thumbnails.append(bookmark_obj)
    else:
        thumbnails = [bookmark_obj]
    return thumbnails
