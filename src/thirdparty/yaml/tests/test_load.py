# import pytest
from thirdparty.yaml.overlay import YamlOverlay
from pkg_resources import resource_filename
import inspect
from ruamel.yaml.compat import ordereddict

# https://yaml.org/spec/1.2/spec.html

TESTPKG = "thirdparty.yaml.tests"

yaml_overlay = YamlOverlay()


# from io import StringIO
# with StringIO() as string_stream:
#     obj = xyaml.load(source)
#     xyaml.dump(obj, string_stream)

#     pprint(obj)
#     print(string_stream.getvalue())


def test_load_empty():
    obj = yaml_overlay.load("")
    assert obj is None


def test_load_single_scalar():
    o = yaml_overlay.load("1")
    assert o == 1


def test_load_single_key_value():
    o = yaml_overlay.load("scalar: 1")
    assert o == {"scalar": 1}


def test_load_sequence():
    data = "- one: 1\n- two: 2\n- one: 1\n"
    o = yaml_overlay.load(data)
    assert o == [{"one": 1}, {"two": 2}, {"one": 1}]


def test_load_mapping():
    data = "top:\n  attr1: value1\n  attr2:\n    scalar: 1\n"
    expected = {"top": {"attr1": "value1", "attr2": {"scalar": 1}}}
    o = yaml_overlay.load(data)
    assert o == expected


# https://yaml.org/type/pairs.html
def test_load_pairs():
    data = "pair_seq: !!pairs\n- num: 1\n- num: 2\n- other: 3"
    expected = {"pair_seq": [("num", 1), ("num", 2), ("other", 3)]}
    o = yaml_overlay.load(data)
    assert o == expected


# https://yaml.org/type/omap.html
def test_load_ordered_map():
    data = "mymap: !!omap\n- a: 1\n- b: 2\n- c: 3\n- d: 4\n- e: 5\n"
    expected = {
        "mymap": ordereddict(
            [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]
        )
    }
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_ordered_map_with_duplicates():
    data = "mymap: !!omap\n- a: 1\n- a: 2\n- c: 3\n- d: 4\n- e: 5\n"
    expected = {"mymap": ordereddict([("a", 2), ("c", 3), ("d", 4), ("e", 5)])}
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_recursively_merging_sequences():
    data = inspect.cleandoc(
        """
        myseq:
        - v: 1
        - v: 2

        <<<:
          myseq:
          - v: 3
          - v: 4
    """
    )
    expected = {"myseq": [{"v": 1}, {"v": 2}, {"v": 3}, {"v": 4}]}
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_recursively_merging_scalars():
    data = inspect.cleandoc("""
        myscalar: valuehere
        <<<:
          myscalar: valuenothere
    """)
    expected = {"myscalar": "valuenothere"}
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_recursively_merging_maps():
    data = inspect.cleandoc(
        """
        data:
          attr:
            first: value
            second:
              another: thing

        <<<:
          data:
            another_branch:
              with: more
              stuff: 4
            attr:
              second:
                merged_attr: 42
    """
    )
    expected = {
        "data": {
            "attr": {
                "first": "value",
                "second": {"another": "thing", "merged_attr": 42},
            },
            "another_branch": {"with": "more", "stuff": 4},
        }
    }
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_recursively_merging_maps_with_explicit_call():
    data = inspect.cleandoc(
        """
        data:
          attr:
            first: value
            second:
              another: thing

        !recursive_merge :
          data:
            another_branch:
              with: more
              stuff: 4
            attr:
              second:
                merged_attr: 42
    """
    )
    expected = {
        "data": {
            "attr": {
                "first": "value",
                "second": {"another": "thing", "merged_attr": 42},
            },
            "another_branch": {"with": "more", "stuff": 4},
        }
    }
    o = yaml_overlay.load(data)
    assert o == expected


def test_load_fobj_with_include_recursive_merge():
    """
    --- test.yaml ---
        thing:
        value: 4

        <<<:
        thing:
            additional: 6

        !recursive_merge :
        thing:
            yet_another_recursive_merge: true

        <<<: !include test_simple_mapping.yaml

    --- stuff.yaml ---
        otherthings:
          myval: 45
    """
    expected = {
        "thing": {
            "value": 4,
            "additional": 6,
            "yet_another_recursive_merge": True,
        },
        "otherthings": ordereddict([("myval", 45)]),
    }
    fpath = resource_filename(TESTPKG,
                              "data/test_include_recursive_merge.yaml")
    with open(fpath, "r") as fobj:
        o = yaml_overlay.load(fobj)
        assert o == expected


def test_local_include_bin_file():
    # !include:bin <PATH>
    expected = {"value": b"some data to copy verbatim"}
    fpath = resource_filename(TESTPKG, "data/test_include_verbatim.yaml")
    with open(fpath, "r") as fobj:
        o = yaml_overlay.load(fobj)
        assert o == expected


# TODO: Mock urllib up correctly.
# def test_include_bin_via_url():
#     # !include-url:bin <URL>
#     expected = {"value": b"some data to copy verbatim"}
#     with open("test_include_url.yaml", "r") as fobj:
#         o = yaml_overlay.load(fobj)
#         assert o == expected
