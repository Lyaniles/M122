# M122
Dies ist ein Repo für das Modul 122 der TBZ.

---
# Guide um Github Repo mit VS Code zu verbinden.


#  1. Das Remote-Repository verknüpfen

Bevor du Daten übertragen kannst, muss dein lokaler Ordner wissen, wohin die Reise geht. Mit dem Befehl `remote add` stellst du die Verbindung zu deinem GitHub-Repository her. Wir nennen diese Verbindung standardmäßig `origin`

``` Shell
 git remote add origin https://github.com/Lyaniles/M122
```

# 2. Abgleich mit dem Server (Synchronisation)

Um sicherzustellen, dass dein lokaler Stand nicht mit Änderungen auf GitHub kollidiert, führen wir einen `pull` durch. Die Flag `--rebase` sorgt dabei für eine saubere Historie, indem sie deine lokalen Änderungen "oben auf" die neuesten Änderungen vom Server setzt, anstatt einen unübersichtlichen Merge-Commit zu erstellen.

``` Shell
git pull origin main --rebase
```
> **Hinweis:** Falls dein Haupt-Branch auf GitHub anders heißt (z.B. `master`), passe den Namen im Befehl entsprechend an. 

# 3. Die Daten hochladen

Sobald dein lokaler Stand aktuell ist, kannst du deine Arbeit auf GitHub veröffentlichen. Mit der Flag `-u` (kurz für `--set-upstream`) speicherst du die Verbindung für die Zukunft. Das bedeutet, dass du ab jetzt einfach nur noch `git push` eingeben musst, ohne jedes Mal `origin main` zu wiederholen.

``` Shell
git push -u origin main
```

### 1. Änderungen speichern (Der Standard-Zyklus)

Wenn du Dateien bearbeitet hast, musst du diese „stagen“ (vormerken) und dann „committen“ (festschreiben).

- **Status prüfen:** Schau nach, welche Dateien geändert wurden:
    ``` Shell
    git status
    ```
    
- **Dateien hinzufügen:** Alle Änderungen für den nächsten Commit vormerken:
    ```Sh
    git add .
    ```
    
- **Änderungen festschreiben:** Erstelle einen Snapshot deiner Arbeit mit einer kurzen Nachricht:
    ```Sh
    git commit -m "Hier beschreiben, was du gemacht hast"
    ```
    
- **Hochladen:** Deine Commits an GitHub senden:
    ```Sh
    git push
    ```

### 2. Mit Branches arbeiten (Parallel arbeiten)

Falls du ein neues Feature ausprobieren willst, ohne den Hauptcode (`main`) zu gefährden, solltest du einen eigenen Zweig (Branch) verwenden.

- **Neuen Branch erstellen:**
    ```Sh
    git checkout -b mein-neues-feature
    ```
    
- **Zwischen Branches wechseln:**
    ```Sh
    git checkout main
    ```
    
- **Branches zusammenführen (Merge):** Wenn dein Feature fertig ist, wechselst du zurück in den `main` und holst dir die Änderungen:
    ```Sh
    git checkout main
    git merge mein-neues-feature
    ```
    
