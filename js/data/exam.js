// Goethe exam preparation content per level.
const EXAM = {
  A1: {
    name: "Goethe-Zertifikat A1: Start Deutsch 1",
    pass: "You pass with 60 out of 100 points. All four modules are taken together.",
    modules: [
      { name: "Lesen", time: "25 min", desc: "3 parts: short texts (emails, notes), ads, and signs/notices. You match information and answer Richtig/Falsch questions." },
      { name: "Hören", time: "20 min", desc: "3 parts: short everyday conversations, announcements (train station, supermarket), and phone messages. Each is played once or twice." },
      { name: "Schreiben", time: "20 min", desc: "2 parts: fill in a simple form (e.g. hotel registration) and write a short message (~30 words) covering 3 given points." },
      { name: "Sprechen", time: "15 min", desc: "3 parts in a group: introduce yourself (name, age, country, languages, job, hobby), ask & answer questions on a topic card, and make requests with picture cards." }
    ],
    reading: {
      title: "Leseverstehen üben: eine E-Mail",
      text: `Liebe Anna,

wie geht es dir? Ich habe eine neue Wohnung in Hamburg! Sie ist klein, aber schön und nicht teuer. Sie hat zwei Zimmer, eine Küche und ein Bad. Der Supermarkt und die U-Bahn sind ganz in der Nähe.

Am Samstag mache ich eine kleine Party. Sie beginnt um 18 Uhr. Kannst du kommen? Bring bitte einen Salat mit!

Viele Grüße
Maria`,
      questions: [
        { q: "Marias Wohnung ist groß und teuer.", opts: ["Richtig", "Falsch"], a: 1, why: "Sie schreibt: „Sie ist klein … und nicht teuer.“" },
        { q: "Die Wohnung hat zwei Zimmer.", opts: ["Richtig", "Falsch"], a: 0, why: "„Sie hat zwei Zimmer, eine Küche und ein Bad.“" },
        { q: "Die Party ist am Sonntag.", opts: ["Richtig", "Falsch"], a: 1, why: "Die Party ist am Samstag um 18 Uhr." },
        { q: "Anna soll einen Salat mitbringen.", opts: ["Richtig", "Falsch"], a: 0, why: "„Bring bitte einen Salat mit!“" }
      ]
    },
    writing: {
      title: "Schreiben üben",
      prompts: [
        {
          task: "Schreiben Sie eine E-Mail an Ihre Freundin Julia (ca. 30 Wörter): 1) Sie machen am Freitag eine Party. 2) Sagen Sie: wann und wo. 3) Fragen Sie: Kann Julia einen Kuchen mitbringen?",
          model: `Liebe Julia,

am Freitag mache ich eine Party. Sie beginnt um 19 Uhr bei mir zu Hause in der Gartenstraße 5. Kannst du bitte einen Kuchen mitbringen?

Viele Grüße
Amal`
        },
        {
          task: "Schreiben Sie an die Sprachschule (ca. 30 Wörter): 1) Sie möchten einen Deutschkurs machen. 2) Fragen Sie nach dem Preis. 3) Fragen Sie: Wann beginnt der Kurs?",
          model: `Sehr geehrte Damen und Herren,

ich möchte gern einen Deutschkurs an Ihrer Schule machen. Was kostet der Kurs? Und wann beginnt er?

Vielen Dank und freundliche Grüße
Amal Ronalda`
        }
      ]
    },
    speaking: [
      "Sich vorstellen: Name, Alter, Land, Wohnort, Sprachen, Beruf, Hobby. Üben Sie diesen Text, bis er automatisch kommt — er kommt garantiert dran!",
      "Üben Sie auch das Buchstabieren Ihres Namens und Ihrer Stadt (das wird oft gefragt!) sowie Ihre Telefonnummer.",
      "Themen für Teil 2: Essen & Trinken, Familie, Einkaufen, Tagesablauf, Wohnen. Üben Sie W-Fragen: „Was isst du zum Frühstück?“",
      "Teil 3 (Bitten): „Gib mir bitte das Buch!“ / „Kannst du bitte das Fenster öffnen?“ — üben Sie Imperativ und können-Fragen."
    ],
    tips: [
      "Learn the numbers 1–100 perfectly — prices, times and phone numbers appear in Hören and Sprechen.",
      "In Schreiben, always cover ALL three points — each one earns points.",
      "Start and end letters correctly: Liebe/Lieber … + Viele Grüße (informal), Sehr geehrte Damen und Herren + Mit freundlichen Grüßen (formal).",
      "In Hören, read the questions BEFORE the audio starts.",
      "Do the free official practice test (Modellsatz) on goethe.de — the real exam has exactly the same format."
    ]
  },

  A2: {
    name: "Goethe-Zertifikat A2",
    pass: "You pass with 60 out of 100 points. Sprechen is taken with a partner.",
    modules: [
      { name: "Lesen", time: "30 min", desc: "4 parts: newspaper articles, emails, ads and notices. Multiple choice and matching tasks." },
      { name: "Hören", time: "30 min", desc: "4 parts: announcements, short interviews, everyday conversations and radio. Multiple choice and matching." },
      { name: "Schreiben", time: "30 min", desc: "2 parts: a short SMS/message (~20-30 words) to a friend and a semi-formal email (~30-40 words), each with 3 points to cover." },
      { name: "Sprechen", time: "15 min", desc: "3 parts with a partner: answer questions about yourself, tell about your life (with prompt cards), and plan something together (e.g. a visit to the cinema)." }
    ],
    reading: {
      title: "Leseverstehen üben: eine Anzeige",
      text: `Nachhilfe gesucht!

Unsere Tochter Lena (12) braucht Hilfe in Mathematik. Wir suchen eine Studentin oder einen Studenten für zweimal pro Woche, am Nachmittag bei uns zu Hause (Stadtmitte). Wir zahlen 15 Euro pro Stunde.

Sie haben Erfahrung und Geduld? Dann rufen Sie uns an: 0171/2345678 (ab 17 Uhr).

Familie Weber`,
      questions: [
        { q: "Lena braucht Hilfe in Deutsch.", opts: ["Richtig", "Falsch"], a: 1, why: "Sie braucht Hilfe in Mathematik." },
        { q: "Die Nachhilfe ist zweimal pro Woche.", opts: ["Richtig", "Falsch"], a: 0, why: "„für zweimal pro Woche, am Nachmittag“." },
        { q: "Die Familie zahlt 50 Euro pro Stunde.", opts: ["Richtig", "Falsch"], a: 1, why: "Sie zahlen 15 Euro pro Stunde." },
        { q: "Man kann am Vormittag anrufen.", opts: ["Richtig", "Falsch"], a: 1, why: "Anrufen ab 17 Uhr — also am Abend." }
      ]
    },
    writing: {
      title: "Schreiben üben",
      prompts: [
        {
          task: "Schreiben Sie Ihrem Freund Tom (ca. 25 Wörter): 1) Sie können am Samstag nicht zum Fußball kommen. 2) Begründen Sie: warum? 3) Schlagen Sie einen neuen Termin vor.",
          model: `Hallo Tom,

leider kann ich am Samstag nicht zum Fußball kommen, weil ich arbeiten muss. Hast du am Sonntagnachmittag Zeit? Dann können wir zusammen spielen.

Bis bald!
Amal`
        },
        {
          task: "Schreiben Sie an Ihre Vermieterin, Frau Schneider (ca. 35 Wörter): 1) Die Heizung in Ihrer Wohnung funktioniert nicht. 2) Seit wann? 3) Bitten Sie um einen Termin mit dem Hausmeister.",
          model: `Sehr geehrte Frau Schneider,

leider funktioniert die Heizung in meiner Wohnung seit drei Tagen nicht. Es ist sehr kalt. Könnten Sie bitte einen Termin mit dem Hausmeister vereinbaren?

Vielen Dank im Voraus.

Mit freundlichen Grüßen
Amal Ronalda`
        }
      ]
    },
    speaking: [
      "Teil 1: Fragen zur Person mit Stichwörtern (Wohnort? Beruf? Hobbys? Familie?). Antworten Sie in ganzen Sätzen, nicht nur mit einem Wort.",
      "Teil 2: Von sich erzählen, z.B. „Mein Tagesablauf“, „Mein letzter Urlaub“. Üben Sie 4–5 Sätze pro Thema, gern mit Perfekt.",
      "Teil 3: Etwas zusammen planen. Lernen Sie Redemittel: „Hast du am … Zeit?“, „Wollen wir …?“, „Das ist eine gute Idee!“, „Das passt mir leider nicht, aber …“",
      "Reagieren Sie auf Ihren Partner! Zustimmen, ablehnen, Alternative vorschlagen — das gibt Punkte."
    ],
    tips: [
      "Master the Perfekt — most speaking and writing tasks ask about past events.",
      "Learn fixed phrases for arranging appointments and making suggestions; they appear in Schreiben AND Sprechen.",
      "For Hören: the speakers often correct themselves („Also nicht um 3, sondern um 4 Uhr“) — the LAST information counts.",
      "Don't leave any answer blank — wrong answers don't subtract points.",
      "Train with the official Modellsatz and Übungssatz from goethe.de under real time conditions."
    ]
  },

  B1: {
    name: "Goethe-Zertifikat B1",
    pass: "Each module is passed separately with 60/100. You can take (and retake) modules individually!",
    modules: [
      { name: "Lesen", time: "65 min", desc: "5 parts: blog/newspaper texts, press reports, ads, opinions and rules/instructions. Richtig/Falsch and multiple choice." },
      { name: "Hören", time: "40 min", desc: "4 parts: announcements, a presentation, a conversation and a radio discussion. Some parts play only ONCE." },
      { name: "Schreiben", time: "60 min", desc: "3 tasks: an informal email (~80 words), a forum post giving your opinion (~80 words), and a semi-formal email e.g. to a teacher (~40 words)." },
      { name: "Sprechen", time: "15 min", desc: "3 parts with a partner: plan something together, give a short presentation (~3 min) on an everyday topic, then answer questions and give feedback on your partner's presentation." }
    ],
    reading: {
      title: "Leseverstehen üben: ein Forumsbeitrag",
      text: `Immer mehr Menschen arbeiten von zu Hause aus. Was früher die Ausnahme war, ist heute für viele normal. Die Vorteile liegen auf der Hand: Man spart den Weg zur Arbeit, kann sich die Zeit flexibler einteilen und ist oft konzentrierter als im lauten Büro.

Doch es gibt auch Nachteile. Vielen Menschen fehlt der Kontakt zu den Kolleginnen und Kollegen. Außerdem fällt es manchen schwer, nach Feierabend wirklich abzuschalten, weil Arbeit und Privatleben am selben Ort stattfinden. Experten empfehlen deshalb feste Arbeitszeiten und einen eigenen Arbeitsplatz in der Wohnung.

Klar ist: Homeoffice wird nicht wieder verschwinden. Viele Firmen bieten heute eine Mischung an — einige Tage im Büro, einige zu Hause. Diese Lösung scheint für die meisten die beste zu sein.`,
      questions: [
        { q: "Homeoffice ist heute eine Ausnahme.", opts: ["Richtig", "Falsch"], a: 1, why: "„Was früher die Ausnahme war, ist heute für viele normal.“" },
        { q: "Ein Vorteil ist, dass man flexibler arbeiten kann.", opts: ["Richtig", "Falsch"], a: 0, why: "„… kann sich die Zeit flexibler einteilen“." },
        { q: "Experten empfehlen, ohne feste Arbeitszeiten zu arbeiten.", opts: ["Richtig", "Falsch"], a: 1, why: "Experten empfehlen FESTE Arbeitszeiten." },
        { q: "Viele Firmen kombinieren heute Büro und Homeoffice.", opts: ["Richtig", "Falsch"], a: 0, why: "„Viele Firmen bieten heute eine Mischung an.“" }
      ]
    },
    reading2: {
      title: "Leseverstehen üben: eine Stellenanzeige (Acushnet GmbH)",
      text: `Stellenanzeige: Buchhalter/-in (Befristeter Vertrag, 18 Monate)
Arbeitgeber: Acushnet GmbH | Standort: Idstein | Gehalt: 45.000–50.000 € brutto p.a.

Titleist und FootJoy – Namen, die jeder Golfspieler kennt. Diese Marken gehören zu Acushnet, dem weltgrößten Hersteller von Golfausrüstung mit Hauptsitz in Fairhaven, USA.

Für unser Büro in Idstein suchen wir für ein Projekt befristet auf 18 Monate eine/-n Buchhalter/-in. In enger Zusammenarbeit mit der Teamleitung Buchhaltung und dem Finanzchef unterstützen Sie das Team.

Ihre Aufgaben:
Kreditoren: Verarbeitung von Eingangsrechnungen externer Lieferanten (Systeme AS/400 und Rillion) sowie interner Rechnungen; Unterstützung bei der Reisekostenabrechnung.
Debitoren: Verbuchung von Kontoauszügen, Verwaltung des Bestellfreigabeprozesses, Erstellung von Lastschriftdateien, Unterstützung beim Forderungsmanagement.

Ihr Profil: Sehr gute Englischkenntnisse in Wort und Schrift, Erfahrung mit AS/400, sichere MS-Office-Kenntnisse (insbesondere Excel), strukturierte und sorgfältige Arbeitsweise.

Wir bieten: Angenehme Arbeitsatmosphäre in einem freundlichen Team, flexible Homeoffice-Möglichkeit, regelmäßige Mitarbeiterevents, Betriebskantine mit subventioniertem Essen.

Bewerbung: Lebenslauf auf Englisch per E-Mail. Der Auswahlprozess findet teilweise auf Deutsch, teilweise auf Englisch statt.`,
      questions: [
        { q: "Acushnet GmbH ist ein Hersteller von Golfausrüstung.", opts: ["Richtig", "Falsch"], a: 0, why: "„Acushnet, dem weltgrößten Hersteller von Golfausrüstung“." },
        { q: "Die Stelle in Idstein ist unbefristet.", opts: ["Richtig", "Falsch"], a: 1, why: "„befristet auf 18 Monate“ — die Stelle ist also befristet, nicht unbefristet." },
        { q: "Für die Stelle sind Excel-Kenntnisse erforderlich.", opts: ["Richtig", "Falsch"], a: 0, why: "„sichere MS-Office-Kenntnisse (insbesondere Excel)“ sind im Profil gefordert." },
        { q: "Der Lebenslauf soll auf Deutsch geschickt werden.", opts: ["Richtig", "Falsch"], a: 1, why: "„Lebenslauf auf Englisch per E-Mail“ — also auf Englisch, nicht auf Deutsch." },
        { q: "Die Stelle bietet auch die Möglichkeit, von zu Hause zu arbeiten.", opts: ["Richtig", "Falsch"], a: 0, why: "„flexible Homeoffice-Möglichkeit“ wird im Angebot erwähnt." }
      ]
    },
    writing: {
      title: "Schreiben üben",
      prompts: [
        {
          task: "Forumsbeitrag (ca. 80 Wörter): „Sollten Kinder ein eigenes Handy haben?“ Äußern Sie Ihre Meinung mit Begründung, nennen Sie Vor- und Nachteile.",
          model: `Meiner Meinung nach kommt es auf das Alter an. Einerseits kann ein Handy sehr praktisch sein: Die Eltern können ihr Kind immer erreichen, und das Kind kann im Notfall anrufen. Andererseits gibt es auch Nachteile. Viele Kinder verbringen zu viel Zeit mit Spielen und sozialen Medien, deshalb haben sie weniger Zeit für Hausaufgaben und Freunde.

Ich finde, dass Kinder ab etwa zehn Jahren ein einfaches Handy haben sollten. Wichtig ist aber, dass die Eltern Regeln vereinbaren, zum Beispiel feste Handyzeiten.`
        },
        {
          task: "Halbformelle E-Mail (ca. 40 Wörter): Sie können am Mittwoch nicht am Deutschkurs teilnehmen. Schreiben Sie an Ihre Lehrerin, Frau Müller: Entschuldigen Sie sich, nennen Sie den Grund und fragen Sie nach den Hausaufgaben.",
          model: `Sehr geehrte Frau Müller,

leider kann ich am Mittwoch nicht am Unterricht teilnehmen, weil ich einen wichtigen Arzttermin habe. Ich bitte um Entschuldigung. Könnten Sie mir bitte mitteilen, welche Hausaufgaben ich machen soll?

Mit freundlichen Grüßen
Amal Ronalda`
        },
        {
          task: "Informelle E-Mail (ca. 80 Wörter): Ihre Freundin Sara hat Sie zu ihrer Hochzeit eingeladen. Bedanken Sie sich, sagen Sie zu, fragen Sie, ob Sie etwas mitbringen können, und bieten Sie Ihre Hilfe bei der Vorbereitung an.",
          model: `Liebe Sara,

vielen Dank für die Einladung zu deiner Hochzeit! Ich habe mich riesig gefreut und komme natürlich sehr gern. Das wird bestimmt ein wunderschöner Tag.

Sag mir bitte, ob ich etwas mitbringen kann — vielleicht einen Kuchen oder etwas zu trinken? Außerdem helfe ich dir gern bei der Vorbereitung. Wenn du möchtest, kann ich am Tag vorher kommen und beim Dekorieren helfen.

Ich freue mich schon riesig auf die Feier!

Liebe Grüße
Amal`
        },
        {
          task: "Halbformelle E-Mail – Bewerbung (ca. 70 Wörter): Sie haben eine Stellenanzeige für eine Buchhalter/-in-Position bei der Acushnet GmbH in Idstein gelesen. Schreiben Sie eine kurze Bewerbungs-E-Mail: 1) Nennen Sie die Stelle, auf die Sie sich bewerben. 2) Beschreiben Sie kurz Ihre relevanten Kenntnisse (z. B. Finanzunterlagen, Excel, 1C, Englisch). 3) Sagen Sie, dass Sie Ihren Lebenslauf anhängen.",
          model: `Sehr geehrte Frau Focken,

mit großem Interesse habe ich Ihre Stellenanzeige für die Position als Buchhalter/-in gelesen. In meiner Tätigkeit als Hostel-Administrator habe ich Finanzunterlagen verwaltet, und als Call-Center-Mitarbeiter bei Beeline habe ich abrechnungsbezogene Vorgänge und Zahlungsabwicklungen bearbeitet. Darüber hinaus habe ich Buchhaltungsaufgaben teilweise in 1C und Excel ausgeführt und verfüge über sehr gute Englischkenntnisse (C1).

Meinen Lebenslauf auf Englisch habe ich dieser E-Mail beigefügt.

Mit freundlichen Grüßen
Amal Ronalda`
        }
      ]
    },
    speaking: [
      "Teil 1 (Gemeinsam planen): z.B. einen Ausflug, eine Party für den Kurs. Redemittel: „Ich schlage vor, dass …“, „Wie wäre es, wenn …?“, „Da bin ich anderer Meinung, denn …“, „Einverstanden!“",
      "Teil 2 (Präsentation): 5 Folien-Struktur lernen: 1. Thema vorstellen, 2. persönliche Erfahrungen, 3. Situation im Heimatland, 4. Vor- und Nachteile + Meinung, 5. Abschluss & Dank. Üben Sie 2–3 Themen komplett (z.B. „Fast Food“, „Online einkaufen“, „Soziale Netzwerke“).",
      "Teil 3 (Feedback & Fragen): Nach der Präsentation des Partners: „Vielen Dank für deine Präsentation. Sie hat mir gut gefallen, besonders …“ + EINE Frage stellen.",
      "Sprechen Sie laut zu Hause und nehmen Sie sich mit dem Handy auf — so hören Sie Ihre Fehler selbst."
    ],
    tips: [
      "B1 is modular: if one module goes badly, you only retake that module — reduce the pressure!",
      "In Schreiben, ALWAYS use connectors (weil, deshalb, trotzdem, außerdem, einerseits/andererseits) — they are explicitly rewarded.",
      "Watch the clock in Lesen: max. 12-13 minutes per part. If stuck, guess and move on.",
      "For the Präsentation, memorise your structure phrases — they work for ANY topic.",
      "Write the opinion essay (Aufgabe 2) regularly: opinion → reason → example → conclusion in ~80 words.",
      "Use the official B1 Modellsatz with audio on goethe.de, and simulate the full exam at least twice before the real one."
    ]
  }
};
