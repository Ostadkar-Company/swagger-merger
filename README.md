# SWAGGER MERGER

* ### Merge multiple swagger files with single level ref tag ($ref) into one swagger file
* ### We will support multiple level ref tag soon!.
#### $ref
> Includes a _single-level_ of swagger file.



For example:
```yaml
$ref: "./order.yaml"
```

#### You can merge swagger files with command below: (There are some test files in examples directory)

```
merger -f index.yml
```
(index.yml is just a file name in example)

#### You can optionally specify an output filename with the -o argument, the default is swagger.yml

```
merger -f index.yml -o output.yml
```