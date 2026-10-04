def normalize_path(path: str) -> str:
    if len(path) > 4096 or "\x00" in path:
        raise ValueError
    absolute = path.startswith("/")
    pieces = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if pieces and pieces[-1] != "..":
                pieces.pop()
            elif not absolute:
                pieces.append("..")
            continue
        pieces.append(part)
    if absolute:
        return "/" + "/".join(pieces) if pieces else "/"
    return "/".join(pieces) if pieces else "."
