# thirdparty.yaml

YAML Processing Extensions (e.g. Overlays, Recursive Merging, Includes)

## Usage Synopsis

```
from thirdparty.yaml.overlay import YamlOverlay

yaml_overlay = YamlOverlay()
obj = yaml_overlay.load(yaml_string)
print(yaml_overlay.dump(obj))
```

## Overview

`thirdparty.yaml` enables yaml content creators to add include and recursive merge directives within the yaml itself.

Example YAML with recursive_merge and include:

```
---
thing:
  value: 4

<<<:
  thing:
    additional: 6

!recursive_merge :
  thing:
    yet_another_recursive_merge: true

<<<: !include test_simple_mapping.yaml
```

The result of the above is:

```
---
thing:
  value: 4
  additional: 6
  yet_another_recursive_merge: true

otherthings:
  myval: 45
```

## Install

```
python3 -m pip install --upgrade thirdparty-yaml
```

## Contributing

Any contributions and feature requests are welcome! Please submit all contributions for `thirdparty.yaml` as an issue or pull-request (PR) on [thirdparty.yaml's Github Page](https://github.com/third-party-dev/yaml).

## Authors

- Paul Kohout
- Vincent Agriesti

## License

```
MIT License

Copyright (c) 2020 third-party-dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
