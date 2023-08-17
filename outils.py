from pathlib import Path

log = print

def cheminFichier(dossier, nom) -> Path:
    """Retourne le chemin complet pour ce fichier """
    return Path(dossier+nom)

def cheminWebscrap(nom, dossier='/home/claude/zdata/webscraping/') -> Path:
    """ nom de dossier en 'dur' """
    return cheminFichier(dossier=dossier, nom=nom)

