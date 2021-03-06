# **notes_map**
analyses text file with notes and tags, builds graph of tags and their relations

# Usage:
```
usage: notes_map.py [-h] [--maxtop MAX_TOP_TAGS] [--size PIC_SIZE] [--graph]
                    [--subgraph] [--tags KEY_TAGS] [--routes ROUTES]
                    notes_file

graph analysis of text file with notes and tags

positional arguments:
  notes_file            file with notes

optional arguments:
  -h, --help            show this help message and exit
  --maxtop MAX_TOP_TAGS
                        number of popular tags, default=7
  --size PIC_SIZE       graph size, default=100x80
  --graph
  --subgraph
  --tags KEY_TAGS       list of tags to analyse: tag1,tag2,tag3
  --routes ROUTES       list of tags to build routes from tag1: tag1,tag2,tag3

```
# Sample command and output:
```
payton notes_map.py sample.txt --tags lorem,шрифт,html --maxtop=3  --routes lorem,html
```

```text
5 заметок, 10 тэгов, 8 уникальных тэгов, 3 самых популярных тэгов: lorem:2, качество:2, шрифт:1
граф тэгов имеет 8 вершин и 6 ребер
тэг 'lorem' имеет вес 2 связан с тэгами: шрифт,пример,качество
тэг 'шрифт' имеет вес 1 связан с тэгами: lorem
тэг 'html' имеет вес 1 связан с тэгами: качество
тэг lorem и тэг html имеют ассоциации: качество
```


# Requirements:
Python 3.6, packages: networkx 1.11, matplotlib 2.0.2