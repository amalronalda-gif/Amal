// Listening practice per level.
// Each level: comprehension exercises (text is read aloud via TTS, not shown
// until answered) and dictation sentences.
const LISTENING = {
  A1: {
    exercises: [
      {
        title: "Durchsage am Bahnhof",
        intro: "You will hear a station announcement. Listen, then answer.",
        text: "Achtung an Gleis 7! Der Zug nach München, Abfahrt 14 Uhr 30, hat heute circa 20 Minuten Verspätung. Wir bitten um Entschuldigung.",
        questions: [
          { q: "Wohin fährt der Zug?", opts: ["Nach Berlin", "Nach München", "Nach Hamburg"], a: 1, why: "„Der Zug nach München …“" },
          { q: "Wie viel Verspätung hat der Zug?", opts: ["10 Minuten", "20 Minuten", "30 Minuten"], a: 1, why: "„… hat heute circa 20 Minuten Verspätung.“" },
          { q: "Von welchem Gleis fährt der Zug?", opts: ["Gleis 7", "Gleis 17", "Gleis 4"], a: 0, why: "„Achtung an Gleis 7!“" }
        ]
      },
      {
        title: "Im Café",
        intro: "A short conversation in a café.",
        text: "Guten Tag! Was möchten Sie bestellen? — Ich nehme einen Kaffee mit Milch und ein Stück Apfelkuchen, bitte. — Gern. Das macht zusammen sechs Euro fünfzig.",
        questions: [
          { q: "Was bestellt die Kundin?", opts: ["Tee und Schokoladenkuchen", "Kaffee und Apfelkuchen", "Nur einen Kaffee"], a: 1, why: "„Ich nehme einen Kaffee mit Milch und ein Stück Apfelkuchen.“" },
          { q: "Wie viel kostet alles zusammen?", opts: ["6,15 Euro", "6,50 Euro", "5,60 Euro"], a: 1, why: "„Das macht zusammen sechs Euro fünfzig.“" }
        ]
      }
    ],
    dictation: [
      "Ich wohne in Berlin.",
      "Der Zug fährt um neun Uhr ab.",
      "Wir kaufen Brot und Käse.",
      "Mein Bruder ist zwanzig Jahre alt.",
      "Kannst du mir bitte helfen?"
    ]
  },

  A2: {
    exercises: [
      {
        title: "Anruf beim Arzt",
        intro: "A phone call with a doctor's office.",
        text: "Praxis Doktor Schmidt, guten Morgen! — Guten Morgen, mein Name ist Yilmaz. Ich habe seit gestern starke Halsschmerzen und Fieber. Kann ich heute noch einen Termin bekommen? — Moment bitte … Ja, kommen Sie heute Nachmittag um 15 Uhr 45. Und bringen Sie bitte Ihre Versichertenkarte mit.",
        questions: [
          { q: "Was hat Herr Yilmaz?", opts: ["Kopfschmerzen", "Halsschmerzen und Fieber", "Bauchschmerzen"], a: 1, why: "„Ich habe seit gestern starke Halsschmerzen und Fieber.“" },
          { q: "Wann ist der Termin?", opts: ["Um 15:45 Uhr", "Um 14:45 Uhr", "Morgen früh"], a: 0, why: "„… kommen Sie heute Nachmittag um 15 Uhr 45.“" },
          { q: "Was soll er mitbringen?", opts: ["Seinen Pass", "Geld", "Seine Versichertenkarte"], a: 2, why: "„Und bringen Sie bitte Ihre Versichertenkarte mit.“" }
        ]
      },
      {
        title: "Durchsage im Supermarkt",
        intro: "An announcement in a supermarket.",
        text: "Liebe Kundinnen und Kunden! Heute im Angebot: ein Kilo Äpfel für nur einen Euro neunundneunzig. Außerdem bekommen Sie an unserer Käsetheke heute alle Käsesorten zwanzig Prozent günstiger. Unser Markt schließt heute um 20 Uhr. Wir wünschen Ihnen einen schönen Einkauf!",
        questions: [
          { q: "Was kostet ein Kilo Äpfel heute?", opts: ["1,99 Euro", "2,99 Euro", "1,09 Euro"], a: 0, why: "„… für nur einen Euro neunundneunzig.“" },
          { q: "Was ist heute 20 % günstiger?", opts: ["Obst", "Käse", "Brot"], a: 1, why: "„… alle Käsesorten zwanzig Prozent günstiger.“" },
          { q: "Wann schließt der Supermarkt?", opts: ["Um 19 Uhr", "Um 20 Uhr", "Um 22 Uhr"], a: 1, why: "„Unser Markt schließt heute um 20 Uhr.“" }
        ]
      }
    ],
    dictation: [
      "Ich habe gestern meine Oma besucht.",
      "Der Termin wurde auf Montag verschoben.",
      "Wenn das Wetter schön ist, fahren wir an den See.",
      "Sie müssen am Hauptbahnhof umsteigen.",
      "Ich interessiere mich für deutsche Musik."
    ]
  },

  B1: {
    exercises: [
      {
        title: "Radiobeitrag: Fahrrad in der Stadt",
        intro: "A short radio report — typical for Goethe B1 Hören.",
        text: "Immer mehr Menschen in deutschen Großstädten fahren mit dem Fahrrad zur Arbeit. Das ist nicht nur gut für die Umwelt, sondern auch für die Gesundheit. Viele Städte bauen deshalb neue Radwege. Kritiker sagen jedoch, dass die Radwege oft zu schmal und gefährlich sind. Die Stadt Hamburg will in den nächsten fünf Jahren über hundert Millionen Euro in den Radverkehr investieren.",
        questions: [
          { q: "Warum fahren mehr Menschen Fahrrad?", opts: ["Es ist billiger als das Auto", "Es ist gut für Umwelt und Gesundheit", "Die Busse sind zu voll"], a: 1, why: "„… nicht nur gut für die Umwelt, sondern auch für die Gesundheit.“" },
          { q: "Was kritisieren manche Leute?", opts: ["Die Radwege sind zu schmal und gefährlich", "Fahrräder sind zu teuer", "Es gibt zu viele Radfahrer"], a: 0, why: "„… dass die Radwege oft zu schmal und gefährlich sind.“" },
          { q: "Was plant Hamburg?", opts: ["Weniger Autos in der Stadt", "Über 100 Millionen Euro für den Radverkehr", "Kostenlose Fahrräder für alle"], a: 1, why: "„… über hundert Millionen Euro in den Radverkehr investieren.“" }
        ]
      },
      {
        title: "Gespräch: Umzug nach Köln",
        intro: "A conversation between two colleagues.",
        text: "Du, Markus, ich habe eine Neuigkeit: Ich ziehe nächsten Monat nach Köln um! — Wirklich? Warum denn das? — Ich habe dort eine neue Stelle als Krankenpflegerin gefunden. Das Gehalt ist besser, und meine Schwester wohnt auch in Köln. — Und deine Wohnung hier? — Die habe ich schon gekündigt. Eine neue Wohnung habe ich aber noch nicht gefunden. Zuerst wohne ich bei meiner Schwester.",
        questions: [
          { q: "Warum zieht die Frau nach Köln?", opts: ["Sie hat dort eine neue Stelle gefunden", "Sie heiratet dort", "Sie beginnt ein Studium"], a: 0, why: "„Ich habe dort eine neue Stelle als Krankenpflegerin gefunden.“" },
          { q: "Wo wohnt sie zuerst?", opts: ["In einem Hotel", "Bei ihrer Schwester", "In ihrer neuen Wohnung"], a: 1, why: "„Zuerst wohne ich bei meiner Schwester.“" },
          { q: "Was stimmt über ihre alte Wohnung?", opts: ["Sie hat sie schon gekündigt", "Sie verkauft sie", "Ihre Schwester übernimmt sie"], a: 0, why: "„Die habe ich schon gekündigt.“" }
        ]
      },
      {
        title: "Telefonat: Bewerbung als Buchhalterin",
        intro: "A job seeker calls a company about an accounting position. Listen carefully — formal German, typical for B1 Hören.",
        text: "Guten Morgen, Acushnet GmbH, Frauke Focken. — Guten Morgen, mein Name ist Amal Ronalda. Ich rufe wegen Ihrer Stellenanzeige für die Position als Buchhalterin an. Ich habe mehrere Jahre Erfahrung in der Kreditorenbuchhaltung und sehr gute Kenntnisse in Excel. — Das klingt gut! Schicken Sie uns bitte Ihren Lebenslauf auf Englisch per E-Mail. Der Auswahlprozess findet teilweise auf Deutsch und teilweise auf Englisch statt. — Vielen Dank. Darf ich fragen, bis wann Bewerbungen möglich sind? — Am besten noch in dieser Woche. — Sehr gut, dann schicke ich Ihnen die Unterlagen noch heute. Auf Wiederhören! — Auf Wiederhören!",
        questions: [
          { q: "Warum ruft Frau Ronalda an?", opts: ["Um einen Termin abzusagen", "Wegen einer Stellenanzeige", "Um Informationen über Produkte zu erhalten"], a: 1, why: "\u201eIch rufe wegen Ihrer Stellenanzeige für die Position als Buchhalterin an.\u201c" },
          { q: "In welchem Bereich hat die Bewerberin Erfahrung?", opts: ["Im Marketing", "In der Debitorenbuchhaltung", "In der Kreditorenbuchhaltung"], a: 2, why: "\u201eIch habe mehrere Jahre Erfahrung in der Kreditorenbuchhaltung.\u201c" },
          { q: "In welcher Sprache soll der Lebenslauf sein?", opts: ["Auf Deutsch", "Auf Englisch", "Auf Englisch und Deutsch"], a: 1, why: "\u201eSchicken Sie uns bitte Ihren Lebenslauf auf Englisch per E-Mail.\u201c" },
          { q: "Wann soll die Bewerbung eintreffen?", opts: ["Bis Ende des Monats", "Noch in dieser Woche", "Bis nächsten Montag"], a: 1, why: "\u201eAm besten noch in dieser Woche.\u201c" }
        ]
      }
    ],
    dictation: [
      "Die Anmeldung muss bis Freitag geschickt werden.",
      "Obwohl es geregnet hat, sind wir spazieren gegangen.",
      "Wenn ich mehr Zeit hätte, würde ich öfter Sport machen.",
      "Nachdem ich die Prüfung bestanden hatte, habe ich gefeiert.",
      "Er bewirbt sich um eine Stelle bei einer großen Firma.",
      "Die Rechnungen werden täglich von der Buchhaltung geprüft.",
      "Ich freue mich darüber, mich bei Ihnen bewerben zu können."
    ]
  }
};
