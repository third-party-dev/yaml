import thirdparty.yaml.operation.add
import thirdparty.yaml.operation.merge
import thirdparty.yaml.operation.delete

from ruamel.yaml.nodes import MappingNode, Node
from thirdparty.yaml.utils import _with_context, _iter_mapping_nodes, \
    _iter_sequence_nodes, _iter_pairs_nodes
import contextlib
from ruamel.yaml.constructor import ConstructorError
# TODO: Should this be ordereddict?
from collections import OrderedDict
import re


class OperationsHandler(object):
    def __init__(self, constructor):
        self.constructor = constructor

        self._special_tags = {
            # TODO: Get these their own module.
            # u'!virtualenv': (_venv_context, 'merge'),
            # "!with": (_context, "merge"),
        }

        self._operations = {}

    @contextlib.contextmanager
    def _context(self, node):
        # get sequence of context managers
        context_managers = self.constructor.construct_sequence(node)

        # enter context
        with _with_context(context_managers):
            yield

    @contextlib.contextmanager
    def _no_context(self, node):
        # make sure it is a scalar, but ignore the value
        self.constructor.construct_scalar(node)

        yield

    # _special_tags = {
    #     # TODO: Get these their own module.
    #     # u'!virtualenv': (_venv_context, 'merge'),
    #     # "!with": (_context, "merge"),
    # }

    def _get_node_pair(self, subnode):
        if isinstance(subnode, Node):
            if not isinstance(subnode, MappingNode):
                return None
            if len(subnode.value) != 1:
                return None
            # This allows us to parse "special tags" in a 1-pait mapping node
            # within a !! seq node. This was intended for supporting
            # aggregation operations for arbitrary sequences. However, it
            # could be used to avoid using the !!pair and !!omap types when the
            # sequences items are all just 1pair mapping nodes.
            subnode = subnode.value[0]

        key_node, value_node = subnode
        return key_node, value_node

    def _apply_item(self, loader, dst, node, subnode, **ops):
        # extract key_value nodes
        node_pair = self._get_node_pair(subnode)

        if node_pair is not None:
            key_node, value_node = node_pair

            if key_node.tag in self._special_tags:
                context, op = self._special_tags[key_node.tag]

                operation = ops[op]
                if operation is None:
                    raise ConstructorError(
                        context="while constructing a %s" % node.tag,
                        context_mark=node.start_mark,
                        problem="%s not supported" % key_node.tag,
                        problem_mark=key_node.start_mark,
                    )

                # construct value
                with context(self, key_node):
                    value = loader.construct_object(value_node, deep=True)

                # ignore None values
                if value is not None:
                    operation(self, dst, value)

                return

        # if its a single node, construct the item
        if isinstance(subnode, Node):
            item = loader.construct_object(subnode, deep=True)

        # otherwise, construct a key:value pair
        else:
            key_node, value_node = subnode

            key = loader.construct_object(key_node, deep=True)

            value = loader.construct_object(value_node, deep=True)

            item = key, value

        # add item
        # add_method = ops["add"]
        ops["add"](self, dst, item)

    _operations = {}

    def register_operation(self, op, op_handlers, tag=None, ctx=_no_context):
        self._operations[op] = op_handlers

        if tag:
            self._special_tags[tag] = (ctx, op)

    def _apply_items(
        self,
        loader,
        dst,
        node,
        iter_nodes,
        **ops,
    ):
        for subnode in iter_nodes(node):
            self._apply_item(
                loader,
                dst,
                node,
                subnode,
                **ops,
            )

    def construct_yaml_sequence(self):
        def _construct_yaml_sequence(loader, node):
            # create a list
            data = []
            yield data

            ops = {}
            for op in self._operations:
                if "seq" in self._operations[op]:
                    ops[op] = self._operations[op]["seq"]

            # apply key:value pairs
            self._apply_items(
                loader,
                data,
                node,
                _iter_sequence_nodes,
                **ops,
            )
        return _construct_yaml_sequence

    def construct_yaml_pairs(self):
        def _construct_yaml_pairs(loader, node):
            # create a list
            data = []
            yield data

            ops = {}
            for op in self._operations:
                if "pairs" in self._operations[op]:
                    ops[op] = self._operations[op]["pairs"]

            self._apply_items(
                loader,
                data,
                node,
                _iter_pairs_nodes,
                **ops,
            )
        return _construct_yaml_pairs

    def construct_yaml_set(self):
        def _construct_yaml_set(loader, node):
            # create a set
            data = set()
            yield data

            ops = {}
            for op in self._operations:
                if "set" in self._operations[op]:
                    ops[op] = self._operations[op]["set"]

            # support standard !!merge tag
            if isinstance(node, MappingNode):
                loader.flatten_mapping(node)

            self.apply_items(
                loader,
                data,
                node,
                _iter_mapping_nodes,
                **ops,
            )
        return _construct_yaml_set

    def construct_yaml_omap(self):
        def _construct_yaml_omap(loader, node):
            data = OrderedDict()
            yield data

            ops = {}
            for op in self._operations:
                if "omap" in self._operations[op]:
                    ops[op] = self._operations[op]["omap"]

            self._apply_items(
                loader,
                data,
                node,
                _iter_pairs_nodes,
                **ops,
            )
        return _construct_yaml_omap

    def construct_yaml_map(self):
        def _construct_yaml_map(loader, node):
            data = {}
            yield data

            ops = {}
            for op in self._operations:
                if "map" in self._operations[op]:
                    ops[op] = self._operations[op]["map"]

            if isinstance(node, MappingNode):
                loader.flatten_mapping(node)

            self._apply_items(
                loader,
                data,
                node,
                _iter_mapping_nodes,
                **ops,
            )
        return _construct_yaml_map

    def register_defaults(self, constructor, resolver):
        constructor.add_constructor(
            "tag:yaml.org,2002:map", self.construct_yaml_map()
        )

        constructor.add_constructor(
            "tag:yaml.org,2002:omap", self.construct_yaml_omap()
        )

        constructor.add_constructor(
            "tag:yaml.org,2002:set", self.construct_yaml_set()
        )

        constructor.add_constructor(
            "tag:yaml.org,2002:pairs", self.construct_yaml_pairs()
        )

        constructor.add_constructor(
            "tag:yaml.org,2002:seq", self.construct_yaml_sequence()
        )

        thirdparty.yaml.operation.add.register_operation_add(self)
        thirdparty.yaml.operation.delete.register_operation_delete(self)
        thirdparty.yaml.operation.merge.register_operation_merge(self)
        thirdparty.yaml.operation.merge.register_operation_recursive_merge(
            self)

        resolver.add_implicit_resolver(
            "!merge",
            re.compile("^" + re.escape("<<<<") + "$"),
            ["<"],
        )

        resolver.add_implicit_resolver(
            "!recursive_merge",
            re.compile("^" + re.escape("<<<") + "$"),
            ["<"],
        )
