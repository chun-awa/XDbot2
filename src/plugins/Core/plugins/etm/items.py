from .item_list import ITEMS
from . import mystery_box



def json2items(items, user_id=None):
    item_list = []
    for item in items:
        item_list.append((
            ITEMS[item["id"]](item["count"], item["data"], user_id)
        ))
    return item_list

mystery_box.json2items = json2items
