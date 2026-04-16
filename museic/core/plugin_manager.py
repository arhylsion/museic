import os
import sys
import importlib.util
import inspect

def load_plugins(parser, subparsers):
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
    
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
        return []

    registered_plugins = []

    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(plugin_dir, filename)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, 'register_plugin') and hasattr(module, 'execute'):
                    command_name, help_text, args_setup = module.register_plugin()
                    
                    plugin_parser = subparsers.add_parser(command_name, help=f"[PLUGIN] {help_text}")
                    
                    args_setup(plugin_parser)
                    
                    registered_plugins.append({
                        "command": command_name,
                        "execute": module.execute
                    })
                    print(f"[*] Loaded plugin: {command_name}")
            except Exception as e:
                print(f"[!] Failed to load plugin {filename}: {e}")

    return registered_plugins