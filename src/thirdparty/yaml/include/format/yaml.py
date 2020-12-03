import ruamel.yaml


def _load_yaml(self, f):
    return ruamel.yaml.YAML().load(f)
