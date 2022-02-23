def filterfields(schema, dtype):
    if schema['statistics'][dtype] == 0:
        return []
    else:
        return list(filter(lambda x: (x["type"] == dtype) , schema['fields']))