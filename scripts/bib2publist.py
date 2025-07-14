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

    # write header
    lines = []
    lines.extend(
        ["---", "permalink: /publications/", 'title: "List of publications"', "---"]
    )
    lines.append(
        "Titles link to a PDF of that publication (with supplementary information included!). †equal contribution."
    )
    lines.append("")

    # parse entries
    bib_data = pybtex.database.parse_file(path)
    for idx, (cite_key, entry) in enumerate(bib_data.entries.items()):
        if idx > 0:
            lines.append("")
        str_ = "1. "

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
        # str_ += names

        # add title, including link if available
        title_str_ = f"{entry.fields['title'].replace('{', '').replace('}', '')}"
        if (
            "Myurl" in entry.fields
            # and entry.fields["myurl"] != "https://tcmoore3.github.io/pdfs/"
        ):
            title_str_ = "[" + title_str_ + f"]({entry.fields['Myurl']})"
        else:
            # title_str_ = f"<ins>{title_str_}</ins>"
            title_str_ = "[" + title_str_ + "](https://tcmoore3.github.io/pdfs/)"
        title_str_ = "" + title_str_

        publication_info = dict(journal=None, volume=None, year=None)
        for _k in publication_info.keys():
            try:
                _v = entry.fields[_k]
                publication_info[_k] = _v
            except KeyError:
                continue
        printed_publication_info = False
        pub_str_ = ""
        for _k in ["journal", "volume", "year"]:
            if publication_info[_k] is not None:
                printed_publication_info = True
                if _k == "journal":
                    pub_str_ += f" _{publication_info[_k]}_"
                elif _k == "year":
                    pub_str_ += f" ({publication_info[_k]})"
                elif _k == "volume":
                    pub_str_ += f" vol. {publication_info[_k]}"
                else:
                    str_ += f" {publication_info[_k]}"
        if printed_publication_info:
            # str_ += "."
            pass

        doi = entry.fields.get("Doi", None)
        if doi is not None:
            # str_ += f" [doi:{doi}](https://doi.org/{doi})."
            pass

        # combine it all together
        str_ += title_str_

        lines.append(f"{title_str_}. ")
        lines.append(f"{names} ")
        if pub_str_:
            lines.append(f"{pub_str_}. ")
        if doi is not None:
            lines.append(f"[doi:{doi}](https://doi.org/{doi}).")

    lines.append('{: reversed="reversed"}')

    for _line in lines:
        print(_line)
