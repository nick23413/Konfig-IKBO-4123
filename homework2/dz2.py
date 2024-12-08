import os
import subprocess
import xml.etree.ElementTree as ET

def parse_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    
    config = {
        'visualizer_path': root.find('visualizer_path').text,
        'package_name': root.find('package_name').text,
        'output_image_path': root.find('output_image_path').text,
        'max_depth': int(root.find('max_depth').text),
        'repo_url': root.find('repo_url').text
    }
    
    return config

def get_dependencies(package_name, max_depth):
    dependencies = {}
    queue = [(package_name, 0)]
    
    while queue:
        current_package, depth = queue.pop(0)
        if depth > max_depth:
            continue
        
        cmd = f"npm view {current_package} dependencies --json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Ошибка при выборке зависимостей для {current_package}: {result.stderr}")
            continue
        
        try:
            deps = result.stdout
            deps_json = eval(deps)
            dependencies[current_package] = deps_json
            
            for dep in deps_json.keys():
                queue.append((dep, depth + 1))
        except Exception as e:
            print(f"Ошибка при разборе зависимостей для {current_package}: {e}")
    
    return dependencies

def generate_mermaid_graph(dependencies):
    mermaid_graph = "graph TD;\n"
    
    for package, deps in dependencies.items():
        for dep in deps.keys():
            mermaid_graph += f"    {package} --> {dep};\n"
    
    return mermaid_graph

def save_mermaid_to_png(mermaid_code, visualizer_path, output_image_path):
    with open("temp_mermaid.mmd", "w") as f:
        f.write(mermaid_code)
    
    cmd = f"{visualizer_path} -i temp_mermaid.mmd -o {output_image_path}"
    subprocess.run(cmd, shell=True)
    
    os.remove("temp_mermaid.mmd")

def main(config_path):
    config = parse_config(config_path)
    
    dependencies = get_dependencies(config['package_name'], config['max_depth'])
    mermaid_graph = generate_mermaid_graph(dependencies)
    
    save_mermaid_to_png(mermaid_graph, config['visualizer_path'], config['output_image_path'])
    
    print(f"фото сохранено {config['output_image_path']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    
    main(sys.argv[1])
