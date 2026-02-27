from sqlalchemy import or_

def get_paginated_list(query, page, per_page=10):
    """
    Standardizes how we handle lists across the app.
    """
    return query.paginate(page=page, per_page=per_page, error_out=False)

def format_instrument_list(instruments):
    """
    Formats instrument data, like splitting the gallery string into a list.
    """
    formatted = []
    for item in instruments:
        # Create a dictionary or modify the object for the template
        item_data = {
            'id': item.ID,
            'name': item.Vietnamese_Name or item.Name,
            'category': item.Category,
            'region': item.Region,
            'image': item.Image_Main or 'default_instrument.jpg',
            'gallery_count': len(item.Image_Gallery.split(',')) if item.Image_Gallery else 0
        }
        formatted.append(item_data)
    return formatted