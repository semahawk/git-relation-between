import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from pygit2 import *
import argparse
import os
import sys

# Check whether you can get to <potential_child> by traversing the
# history starting from <potential_parent>
def is_ancestor(repo, potential_parent, potential_child):
  reachable = False

  for commit in repo.walk(potential_parent.id, GIT_SORT_TOPOLOGICAL):
    if commit.id == potential_child.id:
      reachable = True
      break

  return reachable

# Check whether two commits have a common parent (but are divergent)
def have_common_parent(repo, commit1, commit2):
  merge_base = repo.merge_base(commit1.id, commit2.id)

  return merge_base != None and merge_base != commit1.id and merge_base != commit2.id

def common_parent(repo, commit1, commit2):
  return repo.get(repo.merge_base(commit1.id, commit2.id))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', dest='path', action='store', default=".")
  parser.add_argument('commits', metavar='N', type=str, nargs='+', help='commit hashes')
  args = parser.parse_args()
  graph = nx.DiGraph()

  # path = os.readlink(args.path)
  path = os.path.realpath(args.path)

  try:
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
    commit = repo.revparse_single(commit)
    print("inspecting '%s' (%s)" % (commit.message.rstrip(), commit.id))

    for node in graph.nodes():
      if is_ancestor(repo, node, commit):
        print("-- %s is an ancestor of %s" % (commit.id, node.id))
        graph.add_edge(commit, node)
      elif is_ancestor(repo, commit, node):
        print("-- %s is an ancestor of %s" % (node.id, commit.id))
        graph.add_edge(node, commit)
      elif have_common_parent(repo, commit, node):
        graph.add_edge(common_parent(repo, commit, node), commit)
        graph.add_edge(common_parent(repo, commit, node), node)

    graph.add_node(commit)

  for (f, t) in graph.edges():
    print("edge from %s to %s" % (f.message.rstrip(), t.message.rstrip()))

  for n in graph.nodes():
    print("node %s" % (n.message.rstrip()))

# vi: set ts=2 sw=2 expandtab

