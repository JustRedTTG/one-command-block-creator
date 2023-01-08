class Language:
    top_panel_texts: tuple[str, str] = ("File", "Edit")


languages: dict[(str, Language), ...] = {
    "en": Language()
}