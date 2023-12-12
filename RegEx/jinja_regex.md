
RegEx for matching simple variables in jinja
```reg
\{\{(.*?)\}\}
```


regex for matching the variables in for loops
```reg
\{\%\-?\s*for\s+([\w\.]+)\s+in\s+([\w\.]+)\s*\%\}
```

regex for matching simple if statements

```
\{\%\-?\s*if\s+([\w\.]+)\s*\%\}|\{\%\-?\s*if\s+([\w\.]+)\s*in\s+([\w\.]+)\s*\%\}
```