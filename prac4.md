# Задача 1

С помощью команд эмулятора git получить следующее состояние проекта. Прислать свою картинку.

```
git commit
git tag in
git branch first
git branch second
git commit
git checkout first
git commit
git checkout second
git commit
git commit
git checkout first
git commit
git checkout master
git commit
git merge first
git checkout second
git rebase master
git checkout master
git merge second
git checkout 0e7469f
```

![image](https://github.com/user-attachments/assets/01c78289-5390-4e65-8a0e-fda7f7b62178)

# Задача 2

```
$ mkdir my_project
$ cd my_project
$ git init
Initialized empty Git repository in /home/student/my_project/.git/
$ git config user.name "coder1"
$ git config user.email "coder1@yandex.ru"
nano prog.py
```
> print("Hellow, world!")
```
$ git status
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    prog.py

nothing added to commit but untracked files present (use "git add" to track)
$ git add prog.py
$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
    new file:   prog.py
$ git commit -m "First program"
[master (root-commit) dea4dd0] First program
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py
```

# Задача 3

```
$ cd ..
$ git init --bare server.git
Initialized empty Git repository in /home/student/server.git/
$ cd my_project
$ git remote add server ../server.git
$ git remote -v
server	../server.git (fetch)
server	../server.git (push)
$ git push server master
Counting objects: 3, done.
Writing objects: 100% (3/3), 229 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
 * [new branch]      master -> master
$ cd ..
$ git clone server.git coder2_project
Cloning into 'coder2_project'...
done.
$ cd coder2_project
$ git config user.name "coder2"
$ git config user.email "coder2@google.com"
$ nano readme.md
```
> Just a new readme.
```
$ git add readme.md
$ git commit -m "Adding readme.md"
[master 3367a5f] Adding readme.md
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md
$ git push origin master
Counting objects: 3, done.
Writing objects: 100% (3/3), 290 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To /home/student/server.git
 dea4dd0..3367a5f     master -> master
$ cd ../my_project
$ git pull server master
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
From ../server.git
 * branch            master     -> FETCH_HEAD
Updating dea4dd0..3367a5f
Fast-forward
 readme.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md
$ nano readme.md
```
> Just a new readme.
> 
> Author: coder1
```
$ git add readme.md
$ git commit -m "Adding new author"
[master e62fe91] Adding new author
 1 file changed, 1 insertion(+)
$ git push server master
Counting objects: 3, done.
Writing objects: 100% (3/3), 303 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
   3367a5f..e62fe91  master -> master
$ cd ../coder2_project
$ git pull origin master
Auto-merging readme.md
CONFLICT (content): Merge conflict in readme.md
Automatic merge failed; fix conflicts and then commit the result.
$ nano readme.md
```
> Just a new readme.
> 
> Author: coder1
> 
> Author: coder2
```
$ git add readme.md
$ git commit -m "Resolve conflict and adding new author"
[master e62fe91] Resolve conflict and adding new author
$ git push origin master
Counting objects: 3, done.
Writing objects: 100% (3/3), 306 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To ../server.git
   e62fe91..a09244c  master -> master
$ git log
```

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 3367a5f  e62fe91
| | Author: Coder 2 <coder2@google.com>
| | Date:   Sun Oct 27 11:27:09 2024 +0300
| | 
| |     Resolve conflict and adding new author
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@example.com>
| | Date:   Sun Oct 27 11:22:52 2024 +0300
| | 
| |     Adding new author
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 27 11:24:00 2024 +0300
|   
|       Adding readme.md
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 1 <coder1@yandex.ru>
| Date:   Sun Oct 27 11:11:46 2024 +0300
| 
|     First program

First program

----------------------------------------
Object ID: 76afbe2870db34c3a6fddcdd3743b8c8a402d34f
Content:
100644 blob f7cf60e14f9a9e9805e0463e7fa33b6c91204c4d	prog.py
100644 blob 0d890f0ac261649a0329efc54788e5380a610f4b	readme.md

----------------------------------------
Object ID: f7cf60e14f9a9e9805e0463e7fa33b6c91204c4d
Content:
print("Hello, world!")

----------------------------------------
Object ID: 0d890f0ac261649a0329efc54788e5380a610f4b
Content:
Just a README file.
Author: Coder 1

----------------------------------------
Object ID: 27ea4b92b6f71ed0e25c36316929c0ee753f1429
Content:
100644 blob f7cf60e14f9a9e9805e0463e7fa33b6c91204c4d	prog.py
100644 blob 5f5fd4c84d1d9ce71e57afcabcf376e6d38ae8f4	readme.md

----------------------------------------
Object ID: 5f5fd4c84d1d9ce71e57afcabcf376e6d38ae8f4
Content:
Just a README file.

----------------------------------------
Object ID: 5114700b1b645fea04e657e23eec4af1171a57a4
Content:
100644 blob f7cf60e14f9a9e9805e0463e7fa33b6c91204c4d	prog.py

----------------------------------------
```
