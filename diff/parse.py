def demunge(path):
    special = { "a": "\a",
                "b": "\b",
                "t": "\t",
                "n": "\n",
                "v": "\v",
                "f": "\f",
                "r": "\r",
                '"': '"',
                "'": "'",
                "/": "/",
                "\\": "\\" }

    def unescape(match):
        escaped = match.group(1)
        if escaped in special:
            return special[escaped]
        else:
            return chr(int(escaped, 8))

    return re.sub(r"""\\([abtnvfr"'/\\]|[0-9]{3})""", unescape, path)

    re_diff = re.compile("^diff --git ([\"']?)a/(.*)\\1 ([\"']?)b/(.*)\\3$")
    re_old_path = re.compile("--- ([\"']?)a/(.*)\\1\\s*$")
    re_new_path = re.compile("\\+\\+\\+ ([\"']?)b/(.*)\\1\\s*$")
                    old_name = match.group(2)
                    if match.group(1):
                        old_name = demunge(old_name)
                    new_name = match.group(4)
                    if match.group(3):
                        new_name = demunge(new_name)
                    names = (old_name, new_name)
            match = re_old_path.match(line)
            if match:
                old_path = match.group(2)
                if match.group(1):
                    old_path = demunge(old_path)
            else:
                old_path = None
            match = re_new_path.match(line)
            if match:
                new_path = match.group(2)
                if match.group(1):
                    new_path = demunge(new_path)
            else:
                new_path = None
            if old_path:
                path = old_path
            else:
                path = new_path