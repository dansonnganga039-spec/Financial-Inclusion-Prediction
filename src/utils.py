def inclusion_label(value: int) -> str:
    return "Included" if int(value) == 1 else "Excluded"


def county_key(value: object) -> str:
    key = (
        str(value)
        .strip()
        .lower()
        .replace("'", "")
        .replace(".", "")
        .replace(" ", "-")
    )
    return {"nairobi-city": "nairobi"}.get(key, key)
