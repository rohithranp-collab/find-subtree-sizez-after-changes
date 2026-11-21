# find-subtree-sizez-after-changes
# 3331. Find Subtree Sizes After Changes

![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange)
[LeetCode Problem](https://leetcode.com/problems/find-subtree-sizes-after-changes/)

## Problem

You are given a tree rooted at node `0` with `n` nodes numbered `0` to `n - 1`, represented by an array `parent` where `parent[i]` is the parent of node `i` (`parent[0] == -1`). You are also given a string `s` of length `n`, where `s[i]` is the character assigned to node `i`.

Simultaneously for every node `x` from `1` to `n - 1`:

1. Find the closest ancestor `y` of `x` such that `s[x] == s[y]`.
2. If no such `y` exists, do nothing.
3. Otherwise, remove the edge between `x` and its current parent, and make `y` the new parent of `x`.

Return an array `answer` of size `n`, where `answer[i]` is the size of the subtree rooted at node `i` in the final tree.

## Approach

**Key observations**

- All changes happen simultaneously, so "closest ancestor" is always computed on the **original** tree.
- A node's new parent is always one of its original ancestors, so in a post-order traversal of the original tree, every node appears before its new parent.

**Steps**

1. Build the children adjacency list from `parent`.
2. Run a DFS from the root, maintaining `last[26]`, where `last[c]` is the nearest ancestor on the current path with character `c`.
3. When entering node `x`, read `last[s[x]]`. If it exists, that is the new parent; otherwise keep the original parent. Then set `last[s[x]] = x` for the subtree below and restore the old value when leaving (backtracking).
4. Record nodes in post-order. Initialize every `answer[i] = 1`, then walk the post-order list and add `answer[x]` to `answer[newParent[x]]`.

## Complexity

| | Complexity |
|---|---|
| Time | `O(n)` |
| Space | `O(n)` for the adjacency list, recursion stack and post-order list, plus `O(26)` for `last` |

## Solution (C++)

```cpp
class Solution {
public:
    vector<int> findSubtreeSizes(vector<int>& parent, string s) {
        int n = parent.size();
        vector<vector<int>> children(n);
        for (int i = 1; i < n; i++) children[parent[i]].push_back(i);

        vector<int> newPar(parent), order, last(26, -1);
        order.reserve(n);

        function<void(int)> dfs = [&](int u) {
            int c = s[u] - 'a';
            if (u != 0 && last[c] != -1) newPar[u] = last[c];
            int saved = last[c];
            last[c] = u;
            for (int v : children[u]) dfs(v);
            last[c] = saved;
            order.push_back(u);  // post-order
        };
        dfs(0);

        vector<int> ans(n, 1);
        for (int x : order)
            if (x != 0) ans[newPar[x]] += ans[x];
        return ans;
    }
};
```

## Example

```
Input:  parent = [-1,0,0,1,1,1], s = "abaabc"
Output: [6,3,1,1,1,1]
```

## Topics

`Array` · `Hash Table` · `String` · `Tree` · `Depth-First Search`