import inspect
import os
import tempfile

import yaml


def get_yaml_config(environment: str) -> str:
    _directory = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))
    _default_yaml_config_path = os.path.join(_directory, "config.yaml")
    _custom_yaml_config_path = os.path.join(_directory, f"config.{environment}.yaml")
    if os.path.exists(_custom_yaml_config_path):
        with open(_default_yaml_config_path, "r") as f:
            default_config = yaml.safe_load(f)

        with open(_custom_yaml_config_path, "r") as f:
            custom_config = yaml.safe_load(f)

        def merge_dicts(default, custom):
            for key, value in custom.items():
                if isinstance(value, dict) and key in default:
                    default[key] = merge_dicts(default[key], value)
                else:
                    default[key] = value
            return default

        _combined_yaml_config_path = tempfile.NamedTemporaryFile().name

        with open(_combined_yaml_config_path, "w") as f:
            yaml.dump(
                merge_dicts(default_config, custom_config), f, default_flow_style=False
            )
        return _combined_yaml_config_path
    else:
        return _default_yaml_config_path
