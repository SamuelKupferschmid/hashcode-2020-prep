## Findings
- Finding optimal solution in this case is easy. (Runtime < 10 sec)
- If problem grows we can no longer rely on Stack (recursion will lead to StackOverflow)
- Define where we will implement checks for Basecases (at beginning of recursive call or just before)
- Validate outputs to save time
- In this case multi threading would be easy as branches don't rely on each other
- Incremental save of the result will preserve us from having no score in the end.