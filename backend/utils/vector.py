def to_vector_string(vec):
    if not vec:
        return None
    return "[" + ",".join(map(str, vec)) + "]"
