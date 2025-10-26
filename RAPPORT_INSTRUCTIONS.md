# 📋 Rapport de Stage LaTeX - Instructions

## 📄 Fichier Principal
**Fichier**: `RAPPORT_DE_STAGE.tex`

Ce fichier contient un rapport complet de stage en français avec:
- ✅ Page de titre avec Dr. Manel Elleuchi (PDG Wedtect)
- ✅ 8 chapitres complets
- ✅ Métriques réelles du projet
- ✅ Code d'exemple
- ✅ Résultats et performances
- ✅ Web scraping documentation
- ✅ Appendix et références

## 🛠️ Comment Compiler

### Option 1: Utiliser Overleaf (Recommandé - Sans Installation)

1. Allez sur: https://www.overleaf.com
2. Cliquez sur "New Project" → "Upload Project"
3. Sélectionnez `RAPPORT_DE_STAGE.tex`
4. Cliquez sur "Compile"
5. Téléchargez le PDF

### Option 2: Compilation Locale

**Prérequis:**
```bash
# Windows (MiKTeX)
# Télécharger depuis: https://miktex.org/download

# MacOS (MacTeX)
# brew install --cask mactex

# Linux
sudo apt-get install texlive-full
```

**Compilation:**
```bash
# Compiler LaTeX vers PDF
pdflatex RAPPORT_DE_STAGE.tex

# Ou utiliser XeLaTeX pour meilleure police
xelatex RAPPORT_DE_STAGE.tex
```

### Option 3: VS Code avec Extension LaTeX

1. Installer extension "LaTeX Workshop" (James Yu)
2. Ouvrir `RAPPORT_DE_STAGE.tex`
3. Appuyer sur Ctrl+Alt+B pour compiler
4. PDF généré dans le même dossier

## 📑 Contenu du Rapport

### Chapitre 1: Introduction
- Contexte du stage
- Objectifs principaux
- Structure du rapport

### Chapitre 2: Présentation de l'Entreprise
- **Wedtect - La Startup**
  - Dr. Manel Elleuchi (PDG & Fondatrice)
  - Profil de l'entreprise
- **Le Projet**: YOLOv8 OBB pour détection de défauts
- **Dataset**: 1,224 images annotées

### Chapitre 3: Contexte Théorique
- YOLOv8 - Architecture et principes
- OBB (Oriented Bounding Box)
- Architecture du modèle
- Stack technologique complet
- Environnement de développement

### Chapitre 4: Méthodologie
- Processus d'entraînement
- Préparation du dataset
- Hyperparamètres
- Gestion des erreurs

### Chapitre 5: Résultats et Évaluations
- **Métriques finales:**
  - Précision: 83.92%
  - Rappel: 86.06%
  - mAP@50: 87.22%
- Convergence du modèle
- Tests d'inférence
- Distribution des classes

### Chapitre 6: Web Scraping
- Motivation et objectifs
- Trois méthodes de scraping
- Code implémentation
- **Résultats**: 340 images téléchargées
  - Crack: 82 images
  - Dent: 75 images
  - Hole: 97 images
  - Leak: 86 images
- Workflow d'annotation Roboflow
- Améliorations attendues

### Chapitre 7: Déploiement
- Déploiement GitHub
- Documentation produite
- Utilisation du modèle
- Performances en production

### Chapitre 8: Conclusion
- Réalisations du stage
- Apprentissages techniques
- Améliorations futures (court/moyen/long terme)
- Remerciements

### Appendix
- Configuration système complète
- Commandes utiles
- Installation et compilation

## 🎨 Personnalisation

Pour adapter le rapport:

### Modifier informations personnelles
```latex
% Ligne 97-101
{\Large Réalisé par : [Ton Nom]}
{\Large Encadré par : Dr. Manel Elleuchi}
{\Large Université / Entreprise : Wedtect}
```

### Ajouter logo Wedtect
```latex
% Ligne 85
\includegraphics[width=0.8\textwidth]{wedtect_logo.png}
```

Placer l'image `wedtect_logo.png` dans le même dossier que le `.tex`

### Modifier dates
```latex
% Ligne 101
{\Large Date : Septembre - Octobre 2025}
```

### Ajouter images de résultats
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{RESULTS/graphs/training_metrics_detailed.png}
    \caption{Graphique d'entraînement}
\end{figure}
```

## 📊 Sections Importantes

### Résultats du Projet
- Voir **Chapitre 5** (pages ~60-70)
- Tableaux avec précision, rappel, mAP@50
- Résultats de test avec 20 images
- Distribution des classes

### Web Scraping
- Voir **Chapitre 6** (pages ~70-80)
- Trois méthodes de scraping
- Code Python avec GoogleImageCrawler
- 340 images téléchargées
- Workflow complet d'annotation

### GitHub
- Voir **Chapitre 7** (pages ~80-90)
- Structure du repository
- Instructions d'utilisation
- Performances en production

## 🔗 Générer PDF

### Commande rapide (Windows PowerShell)
```powershell
cd "C:\Users\ahmed\OneDrive\Desktop\Everything\Stage Wedtect"
pdflatex RAPPORT_DE_STAGE.tex
pdflatex RAPPORT_DE_STAGE.tex  # Compiler 2x pour TOC
```

### Résultat
Le fichier `RAPPORT_DE_STAGE.pdf` sera généré dans le même dossier.

## ✅ Checklist de Compilation

- [ ] LaTeX installé (MiKTeX/MacTeX/TeX Live)
- [ ] Fichier `RAPPORT_DE_STAGE.tex` dans le dossier du projet
- [ ] Exécuter: `pdflatex RAPPORT_DE_STAGE.tex`
- [ ] Compiler 2 fois pour générer la table des matières
- [ ] Vérifier que `RAPPORT_DE_STAGE.pdf` est créé

## 📧 Support

Si vous avez des problèmes:

1. **Erreurs de compilation**: Vérifier LaTeX installation
2. **Police introuvable**: Utiliser `xelatex` au lieu de `pdflatex`
3. **Images manquantes**: S'assurer que les images sont dans le bon chemin

## 🎓 Détails du Stage

**Informations du rapport:**
- 👤 Superviseur: Dr. Manel Elleuchi
- 🏢 Entreprise: Wedtect
- 📅 Période: Septembre - Octobre 2025
- 🎯 Programme: WE-SPICE (Women & Civil Society - Powering Socio-Economic Change)
- 🏫 Université: Université de Sfax, Tunisie
- 🌍 Partenaires: DAAD, MST, Université Strasbourg

## 📦 Fichiers Associés

- `RAPPORT_DE_STAGE.tex` - Rapport LaTeX complet
- `WORKFLOW_COMPLETE.md` - Workflow complet du projet
- `SCRAPING_GUIDE.md` - Guide du web scraping
- `README.md` - Documentation GitHub principale
- `train_gpu.py` - Script d'entraînement
- `scrape_google_images.py` - Web scraper
- `DEPLOYMENT/model/best.pt` - Modèle entraîné

---

**Status**: ✅ Rapport complet prêt à compiler et présenter
**Format**: LaTeX (PDF)
**Pages**: ~100+ (selon options personnalisation)
**Langue**: Français 🇫🇷
