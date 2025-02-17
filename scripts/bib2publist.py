import pathlib

import pybtex.database

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bib_path", help="path to bibtex file, usually ~/jobs/cv/refernces.bib"
    )
    args = parser.parse_args()
    path = pathlib.Path(args.bib_path)
    bib_data = pybtex.database.parse_file(path)
    lines = []
    lines.extend(
        ["---", "permalink: /publications/", 'title: "List of publications"', "---"]
    )
    lines.append(
        "Titles link to a PDF of that publication (with supplementary information included!). †equal contribution."
    )
    lines.append("")
    for idx, (cite_key, entry) in enumerate(bib_data.entries.items()):
        str_ = f"{len(bib_data.entries) - idx}. "

        # add names
        names = ""
        for _person_idx, _person in enumerate(entry.persons["author"]):
            if _person_idx > 0:
                names += " and "
            name = (_person.__str__()).replace(r"\textsuperscript{\textdagger}", "†")
            name = name.replace(r"\bf ", "")
            if name.startswith("{"):
                name = name.replace("{", "").replace("}", "")
            if name.startswith("Moore, T. C."):
                names += "__"
            last_name = name.split(",")[0]
            last_name = last_name.replace("McCabe", "M<sup>c</sup>Cabe").replace(
                r"\textsuperscript{c}", "<sup>c</sup>"
            )
            names += f"{last_name},"
            first_names = name.split(", ")[1].split(" ")
            first_names_str = ""
            for _first_name_idx, _first_name in enumerate(first_names):
                if _first_name_idx >= 0:
                    first_names_str += " "
                first_names_str += f"{_first_name[0]}."
                if _first_name[-1] == "†":
                    first_names_str += _first_name[-1]
            names += first_names_str
            if name.startswith("Moore, T. C."):
                names += "__"
        str_ += names

        # add title with link
        if "Myurl" in entry.fields:
            str_ += f" [{entry.fields['title']}]({entry.fields['Myurl']})."
        else:
            str_ += f" {entry.fields['title']}."
        link = "https://tcmoore3.github.io/pdfs/zhong_et_al-natchemeng-2024.pdf"

        publication_info = dict(journal=None, volume=None, year=None)
        for _k in publication_info.keys():
            try:
                _v = entry.fields[_k]
                publication_info[_k] = _v
            except KeyError:
                continue
        printed_publication_info = False
        for _k in ["journal", "volume", "year"]:
            if publication_info[_k] is not None:
                printed_publication_info = True
                if _k == "journal":
                    str_ += f" _{publication_info[_k]}_"
                elif _k == "year":
                    str_ += f" ({publication_info[_k]})"
                elif _k == "volume":
                    str_ += f" vol. {publication_info[_k]}"
                else:
                    str_ += f" {publication_info[_k]}"
        if printed_publication_info:
            str_ += "."

        doi = entry.fields.get("Doi", None)
        if doi is not None:
            str_ += f" [doi:{doi}](https://doi.org/{doi})."

        lines.append(str_)
    lines.append('{: reversed="reversed"}')

    for _line in lines:
        print(_line)
