This solution is not correct on hackerrank. After viewing discussions
and then the editoriral, it's clear that the solution derived is less
accurate than the one given.

The editorial uses a different approach from me which is fine. However,
the issue that I dislike comes from this line

for(int i = 2; i < n; i++)
    d[i] = (1LL * (k - 2) * d[i - 1] + 1LL * (k - 1) * d[i - 2]) % mod;

Modulo on every single iteration. This is a poor solution in my opinion
because the answer is not accurate. My answer is perfectly accurate
up until the return line. 

My answer is not as space effecient. For the given parameters, it
uses approximately 10x as much memory (although this could be cut
to 5x by removing the "prev..." vars and calculating numXs first).