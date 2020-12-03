from ruamel.yaml.constructor import ConstructorError


def _add_set_item(self, dst, item):
    key, value = item

    if value is not None:
        raise ConstructorError(
            problem="expected a null value, but found: %r" % value
        )

    dst.add(key)


def _add_sequence_item(self, dst, item):
    dst.append(item)


def _add_mapping_item(self, dst, item):
    key, value = item

    dst[key] = value

# def register_operation_add(cls):
#     add_handlers = {
#         "seq": _add_sequence_item,
#         "pairs": _add_sequence_item,
#         "set": _add_set_item,
#         "omap": _add_mapping_item,
#         "map": _add_mapping_item,
#     }

#     cls.overlay_add_operation("add", add_handlers)


def register_operation_add(ops_handler):
    add_handlers = {
        "seq": _add_sequence_item,
        "pairs": _add_sequence_item,
        "set": _add_set_item,
        "omap": _add_mapping_item,
        "map": _add_mapping_item,
    }

    ops_handler.register_operation("add", add_handlers)
