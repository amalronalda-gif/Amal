// Quizzes per level: { q, opts, a (index of correct), why }
const QUIZZES = {
  A1: [
    { q: "___ Frau kommt aus Spanien.", opts: ["Der", "Die", "Das", "Den"], a: 1, why: "Frau is feminine → die Frau." },
    { q: "Ich ___ in Berlin.", opts: ["wohnt", "wohnst", "wohne", "wohnen"], a: 2, why: "ich → verb ending -e: ich wohne." },
    { q: "___ du Englisch?", opts: ["Sprichst", "Sprecht", "Spreche", "Sprechen"], a: 0, why: "sprechen changes its stem: du sprichst." },
    { q: "Wir haben ___ Hund.", opts: ["ein", "eine", "einen", "einem"], a: 2, why: "Hund is masculine and the direct object → Akkusativ: einen." },
    { q: "___ kommst du? — Aus Marokko.", opts: ["Wo", "Wohin", "Woher", "Wann"], a: 2, why: "Woher = where from. Wo = where (location), wohin = where to." },
    { q: "Er ___ jeden Tag um 7 Uhr auf.", opts: ["steht", "stehe", "stehst", "stehen"], a: 0, why: "aufstehen is separable: Er steht … auf. er → -t." },
    { q: "Ich ___ gestern Pizza gegessen.", opts: ["bin", "habe", "hat", "ist"], a: 1, why: "essen forms the Perfekt with haben: ich habe … gegessen." },
    { q: "Sie ___ nach Hause gegangen.", opts: ["hat", "habt", "ist", "sind"], a: 2, why: "gehen is a verb of movement → Perfekt with sein: sie ist gegangen." },
    { q: "Das ist ___ Schwester.", opts: ["mein", "meine", "meinen", "meiner"], a: 1, why: "Schwester is feminine → meine." },
    { q: "Ich ___ heute nicht kommen.", opts: ["kann", "kannst", "können", "könnt"], a: 0, why: "ich kann — modal verbs have no ending in ich/er/sie." },
    { q: "Morgen ___ ich Deutsch. (correct word order)", opts: ["ich lerne", "lerne", "lernen", "lernst"], a: 1, why: "The verb must be in position 2: Morgen lerne ich Deutsch." },
    { q: "___ Sie bitte das Formular aus!", opts: ["Füllen", "Füllt", "Füll", "Fülle"], a: 0, why: "Formal imperative: Füllen Sie … aus! (ausfüllen is separable)." },
    { q: "Wie viel ___ das? — 3 Euro 50.", opts: ["kostet", "kosten", "kostest", "koste"], a: 0, why: "das (es) → kostet." },
    { q: "Ich trinke Kaffee ___ Milch.", opts: ["ohne", "für", "um", "gegen"], a: 0, why: "ohne = without. All these prepositions take the accusative." },
    { q: "Wir fahren ___ Bus zur Schule.", opts: ["mit dem", "mit den", "mit der", "mit das"], a: 0, why: "mit always takes dative; Bus is masculine → mit dem Bus." }
  ],

  A2: [
    { q: "Ich helfe ___ Mutter in der Küche.", opts: ["meine", "meiner", "meinen", "meinem"], a: 1, why: "helfen takes the dative; Mutter is feminine → meiner Mutter." },
    { q: "Ich lerne Deutsch, weil ich in Deutschland ___ .", opts: ["möchte arbeiten", "arbeiten möchte", "möchte arbeite", "arbeite möchte"], a: 1, why: "After weil the conjugated verb goes to the very end: … arbeiten möchte." },
    { q: "Gestern ___ ich krank und ___ Fieber.", opts: ["war / hatte", "bin / habe", "wäre / hätte", "wurde / hat"], a: 0, why: "sein and haben are used in the Präteritum: war / hatte." },
    { q: "Berlin ist ___ als München.", opts: ["mehr groß", "großer", "größer", "am größten"], a: 2, why: "Comparative of groß = größer (with umlaut) + als." },
    { q: "Ich freue ___ auf das Wochenende.", opts: ["mir", "mich", "sich", "dich"], a: 1, why: "sich freuen is reflexive: ich freue mich." },
    { q: "Er hat seine Oma ___ .", opts: ["gebesucht", "besucht", "besuchen", "gebesuchen"], a: 1, why: "Inseparable verbs (be-, ver-, er-) form Partizip II without ge-: besucht." },
    { q: "Wohin gehst du? — Ich gehe ___ Kino.", opts: ["im", "ins", "in der", "in dem"], a: 1, why: "Movement (Wohin?) → accusative: in das = ins Kino." },
    { q: "Wo ist das Buch? — Es liegt ___ Tisch.", opts: ["auf den", "auf dem", "auf der", "auf das"], a: 1, why: "Location (Wo?) → dative: auf dem Tisch." },
    { q: "Ich glaube, ___ die Prüfung leicht ist.", opts: ["weil", "dass", "denn", "ob"], a: 1, why: "Ich glaube, dass … (that-clause, verb at the end)." },
    { q: "___ das Wetter schön ist, machen wir ein Picknick.", opts: ["Weil", "Dass", "Wenn", "Denn"], a: 2, why: "wenn = if/when for conditions." },
    { q: "Du ___ mehr Obst essen. (advice)", opts: ["solltest", "sollst", "willst", "musst"], a: 0, why: "Advice is given with the Konjunktiv form sollten: du solltest." },
    { q: "Sie hat den Termin ___ . (= cancelled)", opts: ["abgesagt", "angesagt", "ausgesagt", "zugesagt"], a: 0, why: "absagen = to cancel; Partizip: abgesagt." },
    { q: "Der Zug hat 20 Minuten ___ .", opts: ["Vergangenheit", "Verbindung", "Verspätung", "Versicherung"], a: 2, why: "die Verspätung = delay." },
    { q: "Ich trinke ___ Tee ___ Kaffee. (preference)", opts: ["lieber / als", "gern / wie", "mehr / als", "besser / wie"], a: 0, why: "lieber … als = prefer X to Y." },
    { q: "Wir wohnen ___ zwei Jahren in Hamburg.", opts: ["vor", "seit", "ab", "von"], a: 1, why: "seit + dative for a period continuing until now." }
  ],

  B1: [
    { q: "Das Auto ___ gerade ___ . (Passiv Präsens)", opts: ["wird / repariert", "ist / repariert", "hat / repariert", "wird / reparieren"], a: 0, why: "Vorgangspassiv: werden + Partizip II → wird repariert." },
    { q: "Wenn ich mehr Zeit ___, ___ ich jeden Tag Sport machen.", opts: ["habe / werde", "hätte / würde", "hatte / wurde", "habe / würde"], a: 1, why: "Unreal condition → Konjunktiv II: hätte / würde." },
    { q: "Das ist der Film, ___ ich gestern gesehen habe.", opts: ["der", "den", "dem", "das"], a: 1, why: "Film is masculine; in the relative clause it's the object → Akkusativ: den." },
    { q: "Die Frau, ___ ich arbeite, kommt aus Italien.", opts: ["mit der", "mit dem", "mit die", "mit denen"], a: 0, why: "mit + dative; Frau is feminine → mit der." },
    { q: "___ des schlechten Wetters fand das Konzert statt.", opts: ["Wegen", "Trotz", "Während", "Statt"], a: 1, why: "trotz = despite (+ genitive). The concert happened anyway." },
    { q: "Ich habe vergessen, dich ___ .", opts: ["anrufen", "zu anrufen", "anzurufen", "rufen zu an"], a: 2, why: "Infinitive with zu; separable verb → zu goes inside: anzurufen." },
    { q: "Ich lerne Deutsch, ___ in Deutschland zu studieren.", opts: ["damit", "um", "für", "weil"], a: 1, why: "Same subject → um … zu + Infinitiv." },
    { q: "Ich spreche langsam, ___ alle mich verstehen.", opts: ["um", "damit", "dass", "denn"], a: 1, why: "Different subjects (ich / alle) → damit." },
    { q: "Nachdem ich gegessen ___, ging ich ins Bett.", opts: ["habe", "hatte", "war", "bin"], a: 1, why: "nachdem + Plusquamperfekt: gegessen hatte." },
    { q: "Ich suche eine ___ Wohnung mit einem ___ Balkon.", opts: ["kleine / großen", "kleinen / großem", "kleine / große", "kleiner / großer"], a: 0, why: "eine kleine Wohnung (f, Akk) / mit einem großen Balkon (m, Dat → -en)." },
    { q: "Ich war müde, ___ habe ich weitergelernt.", opts: ["obwohl", "trotzdem", "deshalb", "denn"], a: 1, why: "trotzdem = nevertheless; main clause with verb right after." },
    { q: "___ ich ein Kind war, wohnte ich auf dem Land.", opts: ["Wenn", "Als", "Ob", "Während"], a: 1, why: "als for a single period/event in the past." },
    { q: "Die Anmeldung muss bis Freitag ___ . (Passiv mit Modalverb)", opts: ["geschickt werden", "schicken werden", "geschickt worden", "werden geschickt"], a: 0, why: "Modal + Passiv: muss + Partizip II + werden." },
    { q: "Er bewirbt sich ___ eine Stelle bei BMW.", opts: ["für", "um", "auf", "an"], a: 1, why: "sich bewerben um + Akkusativ." },
    { q: "___ ist es teuer, ___ sehr praktisch.", opts: ["Entweder / oder", "Einerseits / andererseits", "Sowohl / als auch", "Weder / noch"], a: 1, why: "einerseits … andererseits = on the one hand … on the other hand." },
    { q: "Das Buch gehört dem Mann, ___ wir geholfen haben.", opts: ["der", "den", "dem", "dessen"], a: 2, why: "helfen takes the dative → relative pronoun dem." }
  ]
};
