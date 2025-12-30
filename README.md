# Mini Projet 3 – P3-C1  
## Silent Execution : Simulation d’un malware éducatif (Sandbox Only)

### Étudiant
- Nom : youssef ben ameur
- Classe : li3 tp4
- Année : 2025 / 2026

---

## 1. Objectif du projet
Ce mini-projet a pour objectif de **simuler le comportement d’un malware moderne** tout en restant dans un **cadre pédagogique et sécurisé**.

L’application développée semble **légitime** (mini calculatrice), mais elle intègre un module caché qui **simule** plusieurs comportements typiques d’un malware :
- persistance,
- duplication,
- reconnaissance des fichiers,
- comportement de type ransomware,
- propagation logique.

⚠️ **Aucune action malveillante réelle n’est effectuée.**

---

## 2. Principe général
Le projet repose sur une **séparation claire** entre :
- **Apparence légitime** : une mini calculatrice fonctionnelle.
- **Comportement caché simulé** : déclenché manuellement via l’interface graphique.

Toutes les opérations sont limitées à un **dossier sandbox** nommé `demo_data`.

---

## 3. Sécurité et cadre pédagogique
- Aucune modification du système Windows.
- Pas de registre, pas de service, pas de réseau.
- Aucun chiffrement réel des fichiers.
- Toutes les actions sont **réversibles**.

Le dossier `demo_data/` sert uniquement de **bac à sable** pour la simulation.

---

## 4. Fonctionnalités simulées

### 🔹 Persistance (simulée)
Création d’un fichier `autostart_entry.txt` dans `demo_data/system_boot` pour représenter une persistance au démarrage.

### 🔹 Duplication (simulée)
Création de copies d’un fichier fictif dans `demo_data/strategic_locations`.

### 🔹 Scan des fichiers
Analyse des fichiers présents dans `demo_data/user_files` et enregistrement des métadonnées.

### 🔹 Ransomware (faux)
- Création d’un fichier `LOCKED.txt`
- Renommage fictif des fichiers en `.locked`
- Aucun chiffrement réel

### 🔹 Undo ransomware
Restauration des fichiers renommés.

### 🔹 Propagation logique
Simulation d’une propagation via une machine d’états :
IDLE → DISCOVERY → STAGING → EXECUTION → CLEANUP

---

## 5. Logs
Toutes les actions sont enregistrées dans :
- `demo_data/logs/sim.log` : log lisible
- `demo_data/logs/sim.jsonl` : log structuré (JSON)

Ces logs permettent une **analyse comportementale complète**.

---

## 6. Lancement du projet

### Lancer l’application graphique
```bash
python app_gui.py
