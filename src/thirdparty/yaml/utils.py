# from collections.abc import MutableMapping, MutableSequence, MutableSet
from collections.abc import Sequence, Container  # , Mapping, Set
from collections import OrderedDict
import contextlib

from ruamel.yaml.constructor import ConstructorError
from ruamel.yaml.nodes import MappingNode, SequenceNode


def _is_container(value):
    # chenz: What about numbers and booleans?
    if isinstance(value, str) or isinstance(value, bytes):
        return False

    if isinstance(value, Container):
        return True

    return False


def _is_sequence(value):
    if isinstance(value, str):
        return False

    if isinstance(value, Sequence):
        return True

    return False


def _check_order(dst, src):
    dst_is_ordered = isinstance(dst, OrderedDict)
    src_is_ordered = isinstance(src, OrderedDict)
    if dst_is_ordered and not src_is_ordered:
        raise ConstructorError(
            problem="expected an ordered dictionary, but found %r" % src
        )
    if not dst_is_ordered and src_is_ordered:
        raise ConstructorError(
            problem="expected an unordered dictionary, but found %r" % src
        )


@contextlib.contextmanager
def _with_context(context_managers):
    try:
        context_manager = context_managers.pop(0)
    except IndexError:
        yield
    else:
        with context_manager:
            yield _with_context(context_managers)


def _iter_mapping_nodes(node):
    # verify node is a mapping
    if not isinstance(node, MappingNode):
        raise ConstructorError(
            problem="expected a mapping node, but found %s" % node.id,
            problem_mark=node.start_mark,
        )

    # iterate over mapping sub-nodes
    for key_node, value_node in node.value:
        yield key_node, value_node


def _iter_sequence_nodes(node):
    # verify the node is a sequence
    if not isinstance(node, SequenceNode):
        raise ConstructorError(
            problem="expected a sequence node, but found %s" % node.id,
            problem_mark=node.start_mark,
        )

    # iterate over sequence sub-nodes
    for subnode in node.value:
        yield subnode


def _iter_pairs_nodes(node):
    # iterate over sequence sub-nodes
    for seq_subnode in _iter_sequence_nodes(node):
        # get mapping sub-nodes
        map_subnodes = list(_iter_mapping_nodes(seq_subnode))

        # verify there is one mapping sub-node
        if len(map_subnodes) != 1:
            raise ConstructorError(
                problem="expected a single mapping item,"
                " but found %d items" % len(map_subnodes),
                problem_mark=seq_subnode.start_mark,
            )

        # ###### ORDERING ISSUE #####
        # extract key:value nodes
        key_node, value_node = map_subnodes[0]

        yield key_node, value_node
