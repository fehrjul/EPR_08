# Ökosystem – Der Lauf der Natur 🌿🦁

Dieses Projekt implementiert ein **simulationsbasiertes Ökosystem** mithilfe objektorientierter Programmierung (OOP) in Python. Die Simulation bildet ein dynamisches Habitat ab, in dem Pflanzen und Tiere über diskrete Runden hinweg wachsen, interagieren, sich reproduzieren und sterben.

Das Projekt entstand als Umsetzung der Aufgabenstellung *„Ökosystem – der Lauf der Natur“* im Rahmen des Moduls **Einführung in die Praktische Informatik (EPR)** im Wintersemester 2025/26 (Übungsblatt `UE08`).

---

## 👥 Autoren
* **Projektmitglieder:** 8766674 (Fehr), 7791598 (Schidlauskat)

---

## 🎯 Ziel & Anforderungen

Das primäre Ziel ist die realitätsnahe Modellierung biologischer Wechselwirkungen in einem geschlossenen Raum unter Berücksichtigung von Ressourcenknappheit und Umweltfaktoren.

### Umgesetzte Features:
- [x] **Diskrete Rundensimulation:** Zeitabhängige Steuerung aller Lebenszyklen.
- [x] **Artenvielfalt:** Mindestens 3 Pflanzenarten und 3 Tierarten (Herbivore, Carnivore, Omnivore).
- [x] **Räumliche Begrenzung:** Das Habitat besitzt eine limitierte Kapazität (begrenzter Platz).
- [x] **Biologische Kernprozesse:** Wachstum, Nahrungsaufnahme (Fressen/Jagen), Reproduktion und natürlicher oder unnatürlicher Tod.
- [x] **Stochastische Dynamik:** Zufallsbasierte Ereignisse beeinflussen das Überleben.
- [x] **Interaktives UI:** Konsolenbasierte Benutzeroberfläche zur Steuerung und Überwachung.

---

## 🏗️ Programmstruktur & Klassenhierarchie

Das Projekt setzt konsequent auf Vererbung und Polymorphie. Die Architektur gliedert sich in folgende zentrale Komponenten:

### 📱 Benutzeroberfläche & Orchestrierung
* **`ConsoleUI`**: Steuert die Benutzereingaben, initialisiert die Startkonfiguration und verwaltet den interaktiven Ablauf der Simulation.
* **`Habitat`**: Der zentrale Koordinator des Systems. Verwaltet alle Lebewesen, überwacht den verfügbaren Platz, steuert den Wechsel der Jahreszeiten und triggert den Rundenablauf.

### 🧬 Vererbungshierarchie der Lebewesen

              [ LivingBeing (abstrakt) ]
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
    [ Plant (abstrakt) ]       [ Animal (abstrakt) ]
           │                           │
           ├─► SummerPlant             ├─► Herbivore (Pflanzenfresser)
           ├─► WinterPlant             ├─► Carnivore (Fleischfresser)
           └─► PoisonPlant             └─► Omnivore  (Allesfresser)

- **`LivingBeing`**: Abstrakte Basisklasse für alle Entitäten mit grundlegenden Eigenschaften wie Alter und Lebensstatus.
- **`Plant`**: Abstrahierende Oberklasse für die Flora. Spezialisiert in saisonale Gewächse und toxische Verteidigungspflanzen.
- **`Animal`**: Abstrahierende Oberklasse für die Fauna, aufgeteilt nach Ernährungs- und Jagdtypen.

---

## 📜 Regelwerk des Ökosystems

### Allgemeine Regeln
* **Altern:** Jedes Lebewesen altert pro simulierter Runde um den Wert `1`.
* **Bereinigung:** Am Ende jeder Runde werden verstorbene oder gefressene Entitäten vollständig aus dem Habitat entfernt.

### 🌱 Pflanzen-Mechaniken
* **Größenrestriktion:** Pflanzen besitzen eine minimale und eine maximale Größe.
* **Saisonales Wachstum:** Die Wachstumsrate ist direkt an die Pflanzenart und die aktuelle Jahreszeit gekoppelt.
* **Kritische Untergrenze:** Fällt eine Pflanze durch äußere Einflüsse unter ihre minimale Größe, stirbt sie sofort.
* **Platzmangel:** Pflanzen können **nur wachsen**, wenn im Habitat noch freier Platz vorhanden ist.

### 🐺 Tier-Mechaniken
* **Metabolismus:** Tiere verlieren pro Runde kontinuierlich Energie (Stoffwechsel).
* **Nahrungsaufnahme:** Um zu überleben, müssen Tiere fressen. Fleisch- und Allesfresser können aktiv Jagd auf andere Tiere machen.
* **Fortpflanzung:** Die Reproduktion erfolgt autonom, ist jedoch streng an ein Mindestalter und ein ausreichendes Energieniveau gebunden.
* **Energetischer Tod:** Fällt die Energie eines Tieres auf `≤ 0`, stirbt es unverzüglich.

---

## ⚡ Spezialregeln & Zufallseinflüsse

Um die Simulation dynamisch und unvorhersehbar zu gestalten, wurden folgende Sonderregeln implementiert:

* **Das Giftpflanzen-Risiko (`PoisonPlant`):** Frisst ein Tier eine Giftpflanze, besteht eine **30%-ige Wahrscheinlichkeit**, dass das Tier Energie *verliert* statt gewinnt.
* **Winterschlaf:** Carnivoren halten im Winter Winterschlaf, sofern sie im Herbst genügend Reserven gesammelt haben (Energie `≥ 3`).
* **Saisonale Jagd:** Der Jagderfolg von Fleischfressern ist stark von der aktuellen Jahreszeit abhängig.
* **Stochastische Faktoren:** - Erfolg einer Jagd
  - Intoxikation durch Giftpflanzen
  - Wahrscheinlichkeit der Reproduktion von Flora und Fauna

---

## 💻 Benutzerführung (UI)

Beim Programmstart wird der Nutzer interaktiv durch die Konfiguration geleitet:
1. Definition der **Habitatgröße** (maximaler Platz).
2. Festlegung der **Startanzahl** der jeweiligen Lebewesen.

Nach der Initialisierung wechselt die Anwendung in den Steuerungsmodus. Der Nutzer hat folgende Optionen:
* **`1` Eine einzelne Runde simulieren** – Führt genau einen Zeitschritt aus.
* **`2` Mehrere Runden simulieren** – Lässt das Ökosystem über einen längeren Zeitraum autark laufen.
* **`3` Simulation pausieren** – Hält den Durchlauf an, um den aktuellen Zustand zu analysieren.

**Ausgabe-Dashboard nach jeder Runde:**
Nach jedem Schritt gibt die Konsole einen detaillierten Statusbericht aus:
* Aktuelle Jahreszeit (`season`)
* Anzahl der lebenden Tiere (aufgeschlüsselt)
* Anzahl der vorhandenen Pflanzen
* Log-Protokoll der aufgetretenen Ereignisse (Tode, Geburten, Jagderfolge)

---

## ⚙️ Voraussetzungen & Annahmen

### Technische Voraussetzungen
* **Runtime:** Python 3.10 oder neuer.
* **Abhängigkeiten:** Ausschließlich Python-Standardbibliothek (keine externen Pakete benötigt).

### Modell-Annahmen
* **Lebensdauer:** Ein expliziter Tod durch Altersschwäche existiert nicht; er wird indirekt über den progressiven Energieverlust im Alter simuliert.
* **Jahreszeitenzyklus:** Die Jahreszeiten wechseln zyklisch **alle zwei Runden**. Der Ablauf startet im Frühling:
  `Frühling -> Sommer -> Herbst -> Winter`
