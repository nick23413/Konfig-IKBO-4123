# Задача 1

```
import re

with open("civgraph.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)
    
    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
    
    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

![image](https://github.com/user-attachments/assets/5669d504-ae98-45de-8ac5-b885cb1dc161)


# Задача 2

> Добавляется строка makefile.write(f"\t@touch {target}\n") для создания или обновления целевого файла с временной меткой

```
import re

with open("civgraph.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)

    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
        makefile.write(f"\t@touch {target}\n")

    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

![image](https://github.com/user-attachments/assets/81cbef1f-e7fa-45c0-b297-da9d4ea2ff60)
