class Solution(object):
    def findSubtreeSizes(self, parent, s):
        """
        :type parent: List[int]
        :type s: str
        :rtype: List[int]
        """
        n = len(parent)
        adj = [[] for _ in range(n)]
        for i in range(1,n):
            adj[parent[i]].append(i)

        new_parent = parent[:]
        last_seen = {}

        def dfs_reparent(u):
            ch = s[u]
            prev = last_seen.get(ch, -1)
            if u != 0 and prev != -1:
                new_parent[u] = prev

            last_seen[ch] = u
            for v in adj[u]:
                dfs_reparent(v)
            last_seen[ch] = prev

        dfs_reparent(0)
        new_adj = [[] for _ in range(n)]
        for i in range(1, n):
            new_adj[new_parent[i]].append(i)

        ans = [0] * n
        def dfs_size(u):
            size =1
            for v in new_adj[u]:
                size += dfs_size(v)
            ans[u] = size
            return size
        dfs_size(0)
        return ans