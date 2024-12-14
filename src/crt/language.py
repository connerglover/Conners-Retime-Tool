class Language:
    def __init__(self, language: str = "en"):
        self.language = language
        
        match language:
            case "English":
                self.content = {
                    "Framerate": "Framerate (FPS)",
                    "Start Frame": "Start Frame",
                    "End Frame": "End Frame",
                    "Start Frame (Loads)": "Start Frame (Loads)",
                    "End Frame (Loads)": "End Frame (Loads)",
                    "Paste": "Paste",
                    "Copy Mod Note": "Copy Mod Note",
                    "Add Loads": "Add Loads",
                    "Edit Loads": "Edit Loads",
                    "Without Loads": "Without Loads",
                    "With Loads": "With Loads",
                    "Click to Copy Time": "Click to Copy Time",
                    "File": "File",
                    "New Time": "New Time",
                    "Open Time": "Open Time",
                    "Save": "Save",
                    "Save As": "Save As",
                    "Settings": "Settings",
                    "Exit": "Exit",
                    "Edit (Menu Bar)": "Edit",
                    "Clear Loads": "Clear Loads",
                    "Help": "Help",
                    "Check for Updates": "Check for Updates",
                    "Report Issue": "Report Issue",
                    "Suggest Feature": "Suggest Feature",
                    "About": "About",
                    "Edit Load": "Edit Load",
                    "Save Edits": "Save Edits",
                    "Discard Changes": "Discard Changes",
                    "Edit": "Edit",
                    "Delete": "Delete",
                    "Loads": "Loads",
                    "File Name": "File Name",
                    "Cancel": "Cancel",
                    "CRT Settings": "CRT Settings",
                    "Automatically Check for Updates": "Automatically Check for Updates",
                    "Theme": "Theme",
                    "Automatic": "Automatic",
                    "Dark": "Dark",
                    "Light": "Light",
                    "Language" : "Language",
                    "Restore Defaults": "Restore Defaults",
                    "Apply": "Apply",
                }
            case "Français":
                self.content = {
                    "Framerate": "Taux de refraichissement",
                    "Start Frame": "Première image",
                    "End Frame": "Dernière image",
                    "Start Frame (Loads)": "Première image (chargement)",
                    "End Frame (Loads)": "Dernière image (chargement)",
                    "Paste": "Coller",
                    "Copy Mod Note": "Copier la note de modérateur",
                    "Add Loads": "Ajouter un chargement",
                    "Edit Loads": "Modifier les chargements",
                    "Without Loads": "Sans chargements",
                    "With Loads": "Avec chargements",
                    "Click to Copy Time": "Cliquer pour copier le temps",
                    "File": "Fichier",
                    "New Time": "Nouveau temps",
                    "Open Time": "Ouvrir un temps",
                    "Save": "Enregister",
                    "Save As": "Enregister sous",
                    "Settings": "Paramètres",
                    "Exit": "Quitter",
                    "Edit (Menu Bar)": "Modifier",
                    "Clear Loads": "Effacer les chargements",
                    "Help": "Aide",
                    "Check for Updates": "Vérifier les mises à jours",
                    "Report Issue": "Signaler un problème",
                    "Suggest Feature": "Suggérer une fonctionnalité",
                    "About": "À propos",
                    "Edit Load": "Modifier les chargement",
                    "Save Edits": "Enregistrer les modifications",
                    "Discard Changes": "Annuler les modifications",
                    "Edit": "Modifier",
                    "Delete": "Supprimer",
                    "Loads": "Chargements",
                    "File Name": "Nom du fichier",
                    "Cancel": "Annuler",
                    "CRT Settings": "Paramètres du CRT",
                    "Automatically Check for Updates": "Vérifier automatiquement les mises à jours",
                    "Theme": "Thème",
                    "Automatic": "Automatique",
                    "Dark": "Sombre",
                    "Light": "Clair",
                    "Language" : "Langue",
                    "Restore Defaults": "Restaurer les paramètres par défaut",
                    "Apply": "Appliquer",
                }
            case "Polski":
                self.content = {
                    "Framerate": "Liczba klatek na sekundę",
                    "Start Frame": "Pierwsza klatka",
                    "End Frame": "Ostatnia klatka",
                    "Start Frame (Loads)": "Pierwsza klatka ładowania",
                    "End Frame (Loads)": "Ostatnia klatka ładowania",
                    "Paste": "Wklej",
                    "Copy Mod Note": "Skopiuj notatkę moderatora",
                    "Add Loads": "Dodaj ładowanie",
                    "Edit Loads": "Edytuj ładowania",
                    "Without Loads": "Bez ładowań",
                    "With Loads": "Z ładowaniami",
                    "Click to Copy Time": "Kliknij, aby skopiować czas",
                    "File": "Plik",
                    "New Time": "Nowy czas",
                    "Open Time": "Otwórz czas",
                    "Save": "Zapisz",
                    "Save As": "Zapisz jako",
                    "Settings": "Ustawienia",
                    "Exit": "Quitter",
                    "Edit (Menu Bar)": "Wyjście",
                    "Clear Loads": "Wyczyść ładowania",
                    "Help": "Pomoc",
                    "Check for Updates": "Sprawdź aktualizacje",
                    "Report Issue": "Zgłoś problem",
                    "Suggest Feature": "Zaproponuj funkcję",
                    "About": "O programie",
                    "Edit Load": "Edytuj ładowanie",
                    "Save Edits": "Zapisz zmiany",
                    "Discard Changes": "Odrzuć zmiany",
                    "Edit": "Edytuj",
                    "Delete": "Usuń",
                    "Loads": "Ładowania",
                    "File Name": "Nazwa pliku",
                    "Cancel": "Anuluj",
                    "CRT Settings": "Ustawienia CRT",
                    "Automatically Check for Updates": "Automatycznie sprawdzaj aktualizacje",
                    "Theme": "Motyw",
                    "Automatic": "Automatyczny",
                    "Dark": "Ciemny",
                    "Light": "Jasny",
                    "Language" : "Język",
                    "Restore Defaults": "Przywróć domyślne",
                    "Apply": "Zastosuj",
                }
            case _:
                self.content = {
                    "Framerate": "Framerate (FPS)",
                    "Start Frame": "Start Frame",
                    "End Frame": "End Frame",
                    "Start Frame (Loads)": "Start Frame (Loads)",
                    "End Frame (Loads)": "End Frame (Loads)",
                    "Paste": "Paste",
                    "Copy Mod Note": "Copy Mod Note",
                    "Add Loads": "Add Loads",
                    "Edit Loads": "Edit Loads",
                    "Without Loads": "Without Loads",
                    "With Loads": "With Loads",
                    "Click to Copy Time": "Click to Copy Time",
                    "File": "File",
                    "New Time": "New Time",
                    "Open Time": "Open Time",
                    "Save": "Save",
                    "Save As": "Save As",
                    "Settings": "Settings",
                    "Exit": "Exit",
                    "Edit (Menu Bar)": "Edit",
                    "Clear Loads": "Clear Loads",
                    "Help": "Help",
                    "Check for Updates": "Check for Updates",
                    "Report Issue": "Report Issue",
                    "Suggest Feature": "Suggest Feature",
                    "About": "About",
                    "Edit Load": "Edit Load",
                    "Save Edits": "Save Edits",
                    "Discard Changes": "Discard Changes",
                    "Edit": "Edit",
                    "Delete": "Delete",
                    "Loads": "Loads",
                    "File Name": "File Name",
                    "Cancel": "Cancel",
                    "CRT Settings": "CRT Settings",
                    "Automatically Check for Updates": "Automatically Check for Updates",
                    "Theme": "Theme",
                    "Automatic": "Automatic",
                    "Dark": "Dark",
                    "Light": "Light",
                    "Language" : "Language",
                    "Restore Defaults": "Restore Defaults",
                    "Apply": "Apply",
                }
    
    def translate(self, from_lang: str, to_lang: str, text: str) -> str:
        """
        Translates text from one language to another using language content dictionaries.
        
        Args:
            from_lang (str): The language to translate from.
            to_lang (str): The language to translate to.
            text (str): The text to translate.
        
        Returns:
            str: The translated text.
            
        Raises:
            ValueError: If language is not supported or text not found.
        """
        # Create language instances
        source_lang = Language(from_lang)
        target_lang = Language(to_lang)
        
        # Find key by value in source language
        try:
            key = next(k for k, v in source_lang.content.items() if v == text)
            # Get translation from target language
            return target_lang.content[key]
        except (StopIteration, KeyError):
            return text  # Return original text if translation not found