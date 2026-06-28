// Job posting reading exercises — real German Stellenanzeigen for B1+ reading practice.
const JOBS = [
  {
    id: "notarfachangestellte-credo24",
    level: "B1",
    tag: "Recht & Notariat",
    company: "Credo24 GmbH",
    title: "Notarfachangestellte (m/w/d)",
    location: "Frankfurt am Main",
    type: "Zeitarbeit mit Option auf Übernahme",
    salary: "32,00 – 40,00 €/Std.",
    intro: "Wir suchen für einen renommierten Kunden in Frankfurt am Main eine erfahrene Notarfachangestellte (m/w/d) mit sehr guten Deutsch- und Englischkenntnissen und Teamgeist.",
    text:
`NEUE WEGE! CHANCEN! PERSÖNLICHKEIT!

Seit vielen Jahren arbeiten wir mit renommierten Kanzleien zusammen. Mit uns lernen Sie alle Aspekte des Handels- und Zivilrechts in einem harmonischen Team kennen. Wir bieten umfassende Unterstützung und vielfältige Möglichkeiten zur beruflichen Weiterentwicklung.

Temporäres Personal mit Perspektive auf sofortige Festanstellung.

Ihre Aufgaben:
• Unterstützung unserer neu bestellten Notarin bei der Einrichtung und Organisation einer Notariatskanzlei
• Entwurf, Vorbereitung und Abwicklung von Verträgen, Vereinbarungen und sonstigen Urkunden, insbesondere im Gesellschafts- und Immobilienrecht
• Selbstständige Korrespondenz mit Behörden, Gerichten und Beteiligten
• Erstellung von Kostenabrechnungen
• Führung der notariellen Dokumentation einschließlich des Grundstücksregisters

Anforderungsprofil:
• Ausgebildete Notarfachangestellte bzw. Notariatsfachfrau oder ausgebildete Rechtsanwaltsfachangestellte / Bürokauffrau mit Berufserfahrung in einer Notariatskanzlei
• Mehrjährige Berufserfahrung, idealerweise mit Schwerpunkt Gesellschaftsrecht und Immobilienrecht
• Sicherer Umgang mit MS Office und entsprechender Notariatssoftware
• Freude an der Einrichtung der Räumlichkeiten für die neue Notariatskanzlei und organisatorisches Talent
• Sorgfältige und selbstständige Arbeitsweise
• Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift

Wir bieten:
• Abwechslungsreiche Aufgaben in einem motivierten Team mit attraktiver Vergütung (32 – 40 €/Std.)
• Modernes, zukunftsorientiertes Arbeitsumfeld im Herzen Frankfurts
• Hohe Anforderungen und strukturierte Einarbeitung
• Förderung durch Schulungen, Weiterbildungen und verschiedene Mitarbeiterevents
• Bezuschussung für ein breites Spektrum an Sport- und Wellnessaktivitäten (EGYM)

Bewerbung: creod24gmbh@aol.com
Kontakt: Frau Beate Bernhauser, erreichbar Mo–So 9:00–20:00 Uhr, Tel. 0157-58514743`,
    vocab: [
      { de: "der Notar / die Notarin", en: "notary public", note: "beurkundet Verträge und bestätigt ihre Rechtsgültigkeit" },
      { de: "die Urkunde", en: "legal document / deed", note: "offizielles schriftliches Dokument mit rechtlicher Wirkung" },
      { de: "die Kanzlei", en: "law office / chambers", note: "Büro eines Anwalts oder Notars" },
      { de: "der Vertrag", en: "contract", note: "bindende rechtliche Vereinbarung zwischen Parteien" },
      { de: "das Immobilienrecht", en: "real estate law", note: "Rechtsgebiet rund um Grundstücke und Gebäude" },
      { de: "das Gesellschaftsrecht", en: "corporate law", note: "Rechtsgebiet zu Unternehmen und Gesellschaften (GmbH, AG, …)" },
      { de: "das Gericht", en: "court (of law)", note: "Institution, bei der Rechtsfälle verhandelt werden; auch: Essen/Gericht = dish" },
      { de: "der Entwurf", en: "draft", note: "vorläufige Fassung eines Dokuments oder einer Idee" },
      { de: "die Abwicklung", en: "processing / handling", note: "das Durchführen und Abschließen eines Vorgangs" },
      { de: "das Grundstücksregister", en: "land register", note: "amtliches Verzeichnis aller Grundstücke und Eigentümer" },
      { de: "sorgfältig", en: "careful / thorough", note: "mit großer Aufmerksamkeit und Genauigkeit arbeitend" },
      { de: "selbstständig", en: "independent / autonomous", note: "ohne ständige Anleitung arbeiten können; auch: selbstständig = self-employed" },
      { de: "die Vergütung", en: "remuneration / pay", note: "Entgelt, das für geleistete Arbeit gezahlt wird" },
      { de: "die Einarbeitung", en: "induction / onboarding", note: "strukturierte Einführung in eine neue Stelle" },
      { de: "die Weiterbildung", en: "further training / CPD", note: "zusätzliche Qualifikationen nach der Grundausbildung erwerben" },
      { de: "die Korrespondenz", en: "correspondence", note: "der schriftliche Austausch (Briefe, E-Mails) mit anderen Parteien" }
    ],
    questions: [
      {
        q: "Die Stelle befindet sich in München.",
        a: 1, opts: ["Richtig", "Falsch"],
        why: "Falsch — in der Stellenanzeige steht: „Wir suchen für einen bekannten Kunden in Frankfurt am Main"."
      },
      {
        q: "Die Stelle wird zunächst als Zeitarbeit mit der Möglichkeit auf Übernahme angeboten.",
        a: 0, opts: ["Richtig", "Falsch"],
        why: "Richtig — die Anzeige nennt „Temporäres Personal mit Perspektive auf sofortige Festanstellung"."
      },
      {
        q: "Sehr gute Englischkenntnisse sind ausdrücklich gefordert.",
        a: 0, opts: ["Richtig", "Falsch"],
        why: "Richtig — im Anforderungsprofil steht: „Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift"."
      },
      {
        q: "Nur Bewerber mit nachgewiesener Erfahrung im Gesellschaftsrecht werden akzeptiert.",
        a: 1, opts: ["Richtig", "Falsch"],
        why: "Falsch — die Anzeige sagt „idealerweise mit Schwerpunkt Gesellschaftsrecht", was einen Wunsch, keine zwingende Bedingung darstellt."
      },
      {
        q: "Der Stundenlohn liegt zwischen 32 und 40 Euro.",
        a: 0, opts: ["Richtig", "Falsch"],
        why: "Richtig — unter „Wir bieten" steht die Vergütung von 32 – 40 €/Std."
      },
      {
        q: "Das Unternehmen bietet Zuschüsse für Sport- und Wellnessaktivitäten an.",
        a: 0, opts: ["Richtig", "Falsch"],
        why: "Richtig — „Bezuschussung für ein breites Spektrum an Sport- und Wellnessaktivitäten (EGYM)" ist im Angebot enthalten."
      }
    ]
  }
];
