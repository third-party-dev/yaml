from ruamel.yaml.constructor import ConstructorError
from collections.abc import MutableMapping, MutableSequence, MutableSet
from collections.abc import Mapping, Set  # , Sequence, Container

# TODO: Clean this up
# import thirdparty.yaml.overlay as xyaml
from thirdparty.yaml.utils import _is_sequence, _check_order, _is_container
from future.utils import iteritems


def _merge_sequence(self, dst, src):
    # verify source is a sequence
    if not _is_sequence(src):
        raise ConstructorError(
            problem="expected a sequence, but found %r" % src
        )

    dst.extend(src)


def _merge_set(self, dst, src):
    # verify source is a set
    if not isinstance(src, Set):
        raise ConstructorError(problem="expected a set, but found %r" % src)

    dst.update(src)


def _merge_mapping(self, dst, src, recursive=False):
    # verify source is a mapping
    if not isinstance(src, Mapping):
        raise ConstructorError(
            problem="expected a mapping, but found %r" % src
        )

    # verify destination and source ordering matches
    # Note: don't case about ordering if source has a length of 1
    if len(src) != 1:
        _check_order(dst, src)

    for key, src_value in iteritems(src):
        if recursive and key in dst:
            dst_value = dst[key]

            # is destination a sequence?
            if isinstance(dst_value, MutableSequence):
                _merge_sequence(self, dst_value, src_value)

            # is destination a set?
            elif isinstance(dst_value, MutableSet):
                _merge_set(self, dst_value, src_value)

            # if destination a mapping
            elif isinstance(dst_value, MutableMapping):
                _merge_mapping(self, dst_value, src_value, True)

            # its a scalar, so just replace key:value pair
            else:
                # verify the types are identical
                if _is_container(src_value):
                    raise ConstructorError(
                        problem="expected scalar, but found %r" % src_value
                    )

                dst[key] = src_value

        else:
            # recursive merge not required, so just add key_value pair
            dst[key] = src_value


def _recursive_merge_mapping(self, dst, src):
    _merge_mapping(self, dst, src, recursive=True)


# def register_operation_merge(cls):
#     merge_handlers = {
#         "seq": _merge_sequence,
#         "pairs": _merge_sequence,
#         "set": _merge_set,
#         "omap": _merge_mapping,
#         "map": _merge_mapping,
#     }

#     cls.overlay_add_operation("merge", merge_handlers, "!merge")


# def register_operation_recursive_merge(cls):
#     recursive_merge_handlers = {
#         "seq": _merge_sequence,
#         "pairs": _merge_sequence,
#         "set": _merge_set,
#         "omap": _recursive_merge_mapping,
#         "map": _recursive_merge_mapping,
#     }

#     cls.overlay_add_operation(
#         "recursive_merge", recursive_merge_handlers, "!recursive_merge"
#     )

def register_operation_merge(ops_handler):
    merge_handlers = {
        "seq": _merge_sequence,
        "pairs": _merge_sequence,
        "set": _merge_set,
        "omap": _merge_mapping,
        "map": _merge_mapping,
    }

    ops_handler.register_operation("merge", merge_handlers, "!merge")


def register_operation_recursive_merge(ops_handler):
    recursive_merge_handlers = {
        "seq": _merge_sequence,
        "pairs": _merge_sequence,
        "set": _merge_set,
        "omap": _recursive_merge_mapping,
        "map": _recursive_merge_mapping,
    }

    ops_handler.register_operation(
        "recursive_merge", recursive_merge_handlers, "!recursive_merge"
    )