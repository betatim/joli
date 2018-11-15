import argparse

import black

import nbformat


def is_magic(line):
    line = line.strip()
    return line.startswith("!") or line.startswith("%")


def chunks(source):
    """Split source code into chunks

    Each chunk is either a magic or source code chunk
    """
    chunks = []
    accumulator = []
    current_mode = None
    for line in source.split("\n"):
        line_mode = "magic" if is_magic(line) else "source"
        if line_mode != current_mode:
            if accumulator:
                chunks.append((current_mode, "\n".join(accumulator)))
                accumulator = []

            current_mode = line_mode
        accumulator.append(line)

    if accumulator:
        chunks.append((current_mode, "\n".join(accumulator)))
    return chunks


def format_code(source, line_length):
    parts = []
    for kind, src in chunks(source):
        if kind == "code":
            dst = black.format_str(src, line_length=79)

            black.assert_equivalent(src, dst)
            black.assert_stable(src, dst, line_length=line_length)

            parts.append(dst)

        else:
            parts.append(src)

    return "\n".join(parts)


def error(fname, cell, msg):
    print(f"{fname}:{cell}: {msg}")


def build_parser():
    argparser = argparse.ArgumentParser()

    argparser.add_argument("-l", "--line-length", default=79, type=int)
    argparser.add_argument("notebook", help="Notebooks to lint", nargs="+")
    return argparser


def main():
    argparser = build_parser()
    args = argparser.parse_args()
    line_length = args.line_length

    for nb_path in args.notebook:
        nb = nbformat.read(nb_path, as_version=4)
        skipped_code = []
        out_of_order_code = []
        in_order_code = []

        last_execution_count = 0

        for n, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue

            if cell.execution_count is None:
                skipped_code.append(n + 1)

            else:
                if cell.execution_count - 1 != last_execution_count:
                    out_of_order_code.append(n + 1)
                else:
                    in_order_code.append(n + 1)

            last_execution_count = cell.execution_count

            cell.source = format_code(cell.source, line_length=line_length)

        if skipped_code and any((in_order_code, out_of_order_code)):
            error(nb_path, 0, "E100 Mixture of executed and skipped cells")

            for i in skipped_code:
                error(nb_path, i, "E101 Cell execution skipped")

        for i in out_of_order_code:
            error(nb_path, i, "E102 Cell execution out of order")

        nbformat.write(nb, nb_path)
