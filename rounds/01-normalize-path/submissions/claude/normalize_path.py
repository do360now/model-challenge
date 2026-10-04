"""Round 1: lexical path normalization (Claude)."""

MAX_LEN = 4096


def normalize_path(path: str) -> str:
    if len(path) > MAX_LEN or "\x00" in path:
        raise ValueError("path too long or contains NUL")

    absolute = path.startswith("/")
    stack: list[str] = []
    for piece in path.split("/"):
        if piece == "" or piece == ".":
            continue
        if piece == "..":
            if stack and stack[-1] != "..":
                stack.pop()
            elif not absolute:
                stack.append("..")
            # absolute and at root: drop
            continue
        stack.append(piece)

    if absolute:
        return "/" + "/".join(stack)
    return "/".join(stack) or "."
