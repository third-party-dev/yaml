def _delete_set_item(self, dst, key):
    dst.remove(key)


def _delete_mapping_item(self, dst, key):
    del dst[key]


# def register_operation_delete(cls):
#     delete_handlers = {
#         "set": _delete_set_item,
#         "omap": _delete_mapping_item,
#         "map": _delete_mapping_item,
#     }

#     cls.overlay_add_operation("delete", delete_handlers, "!delete")

def register_operation_delete(ops_handler):
    delete_handlers = {
        "set": _delete_set_item,
        "omap": _delete_mapping_item,
        "map": _delete_mapping_item,
    }

    ops_handler.register_operation("delete", delete_handlers, "!delete")