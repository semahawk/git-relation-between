import networkx as nx
from pygit2 import *
import argparse
import os
import sys

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', dest='path', action='store', default=".")
  parser.add_argument('commits', metavar='N', type=str, nargs='+', help='commit hashes')
  args = parser.parse_args()
  graph = nx.DiGraph()

  # path = os.readlink(args.path)
  path = os.path.realpath(args.path)

  try:
    print("using repository in %s" % (path))
    repo = Repository(path + "/.git")
  except KeyError:
    print("Couldn't find a git repository in %s" % (path))
    sys.exit(1)

  for commit in args.commits:
    error = False
    try:
      obj = repo.revparse_single(commit)
    except:
      error = True
      sys.exit(1)

  for commit in args.commits:
    graph.add_node(commit)

  print(graph.graph)

# vi: set ts=2 sw=2 expandtab
