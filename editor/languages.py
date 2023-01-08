class Language:
    top_panel_texts: tuple[str, str] = ("File", "Edit")
    top_panel_file_texts: tuple[str, str, str] = ("New Project...", "New...", "Settings")


languages: dict[(str, Language), ...] = {
    "en": Language()
}