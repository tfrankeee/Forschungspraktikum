// src/helpers/TestService.js
export class TestService {
  constructor() {
    /** 
     * Hier speichern wir nach dem Parsen alle Tests.
     * Jeder Eintrag hat die Struktur:
     * {
     *   id:    String,           // aus <assessmentTest identifier="…">
     *   title: String,           // aus <assessmentTest title="…">
     *   items: [                 // Array von assessmentItemRef-Infos
     *     { identifier: "…", href: "…" },
     *     …
     *   ]
     * }
     */
    this.tests = [];
    this.isLoaded = false;
  }

  /**
   * Lädt alle XMLs asynchron, parsed sie und füllt this.tests.
   * filenames: Array von Dateinamen, die im public/qti/ liegen.
   */
  async loadAllTests(filenames) {
    if (this.isLoaded) return;      // verhindern, dass zweimal geladen wird
    this.isLoaded = true;

    // Basis-Pfad zu den XMLs (relativ zum public-Verzeichnis)
    const basePath = '/qti/tests/';

    // Hilfsfunktion: Ein einzelnes XML parsen
    const parseOne = async (fileName) => {
      const url = basePath + fileName;
      try {
        const resp = await fetch(url);
        if (!resp.ok) {
          console.warn(`TestService: Konnte ${url} nicht laden (Status ${resp.status})`);
          return null;
        }
        const xmlText = await resp.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlText, 'application/xml');

        // 1) <assessmentTest>
        const testElem = xmlDoc.querySelector('qti-assessment-test');
        if (!testElem) {
          console.warn(`TestService: Kein <qti-assessment-test> in ${fileName} gefunden.`);
          return null;
        }
        const testId = testElem.getAttribute('identifier') || '';
        const testTitle = testElem.getAttribute('title') || '';

        // 2) Alle <assessmentItemRef>-Einträge sammeln
        const itemRefs = Array.from(
          xmlDoc.querySelectorAll('qti-assessment-item-ref')
        ).map(el => ({
          identifier: el.getAttribute('identifier') || '',
          href: el.getAttribute('href') || ''
        }));

        return {
          id: testId,
          title: testTitle,
          items: itemRefs
        };
      } catch (err) {
        console.error(`TestService: Fehler beim Parsen von ${fileName}:`, err);
        return null;
      }
    };

    // 3) Schleife über alle Dateinamen
    const parsedList = [];
    for (const fname of filenames) {
      const parsed = await parseOne(fname);
      if (parsed) {
        parsedList.push(parsed);
      }
    }

    // 4) In den State übernehmen
    this.tests = parsedList;
  }

  /**
   * Gibt das komplette Array aller Tests zurück
   */
  getTests() {
    return this.tests;
  }

  /**
   * Liefert ein einzelnes Test-Objekt nach ID
   */
  getTestById(id) {
    return this.tests.find(t => t.id === id) || null;
  }

  /**
   *
   * - Argument: itemsArray = [ { identifier: "...", href: "..." }, … ]
   *   (das sind genau die assessmentItemRef-Objekte aus test.items)
   * - Für jedes Item: fetch des XMLs, DOMParser, root-Element <qti-assessment-item> auslesen
   * - Gibt zurück: Array von Objekten
   *     {
   *       identifier: <identifier-Attribut des <qti-assessment-item>…>,
   *       guid:       <dito identifier des <qti-assessment-item>>,
   *       xml:        <der vollständige XML-String dieser Frage>
   *     }
   */
  async loadQuestionItems(itemsArray) {
    const basePath = '/qti/tests/';

    const result = [];

    for (const item of itemsArray) {
      // item.href ist z. B. "frage123.xml"
      const url = basePath + item.href;
      try {
        const resp = await fetch(url);
        if (!resp.ok) {
          console.warn(`TestService: Konnte Frage-XML ${url} nicht laden (Status ${resp.status})`);
          continue;
        }
        const xmlText = await resp.text();

        // 1) Vollständiges XML in den Frage-Objekt-Key „xml“ packen
        // 2) DOMParser, um das root-Element <qti-assessment-item> zu finden
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
        const root  = xmlDoc.querySelector('qti-assessment-item');

        if (!root) {
          console.warn(`TestService: Kein <qti-assessment-item> in ${item.href} gefunden.`);
          continue;
        }

        // identifier-Attribut des <qti-assessment-item>
        const ident = root.getAttribute('identifier') || '';

        // Wir setzen identifier und guid jeweils auf dasselbe, 
        // wie vom Root-Element vorgegeben.
        result.push({
          identifier: ident,
          guid:       ident,
          xml:        xmlText
        });
      } catch (e) {
        console.error(`TestService: Fehler beim Laden/Parsen der Frage ${item.href}:`, e);
        continue;
      }
    }

    return result;
  }


}
