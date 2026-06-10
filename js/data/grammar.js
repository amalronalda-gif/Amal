// Grammar lessons for A1, A2 and B1.
// Each lesson: { id, title, desc, body (HTML) }
const GRAMMAR = {
  A1: [
    {
      id: "a1-articles",
      title: "Artikel & Genus: der, die, das",
      desc: "The three genders and definite/indefinite articles",
      body: `
        <p>Every German noun has a <b>gender</b>: masculine (<b>der</b>), feminine (<b>die</b>) or neuter (<b>das</b>). Always learn a noun together with its article!</p>
        <table class="gram">
          <tr><th></th><th>masculine</th><th>feminine</th><th>neuter</th><th>plural</th></tr>
          <tr><td>definite (the)</td><td>der Mann</td><td>die Frau</td><td>das Kind</td><td>die Kinder</td></tr>
          <tr><td>indefinite (a/an)</td><td>ein Mann</td><td>eine Frau</td><td>ein Kind</td><td>— Kinder</td></tr>
        </table>
        <h3>Useful patterns</h3>
        <p>• Nouns ending in <b>-ung, -heit, -keit, -schaft, -ion</b> → almost always <b>die</b> (die Zeitung, die Freiheit).<br>
        • Nouns ending in <b>-chen, -lein</b> → always <b>das</b> (das Mädchen).<br>
        • Days, months, seasons → <b>der</b> (der Montag, der Sommer).</p>
        <div class="example"><div class="de">Das ist ein Tisch. Der Tisch ist groß.</div><div class="en">That is a table. The table is big.</div></div>
      `
    },
    {
      id: "a1-praesens",
      title: "Präsens: Verb-Konjugation",
      desc: "Regular and important irregular verbs in the present tense",
      body: `
        <p>German verbs change their ending depending on the person. Regular pattern with <b>wohnen</b> (to live):</p>
        <table class="gram">
          <tr><th>Person</th><th>Ending</th><th>wohnen</th><th>sein (to be)</th><th>haben (to have)</th></tr>
          <tr><td>ich</td><td>-e</td><td>wohne</td><td>bin</td><td>habe</td></tr>
          <tr><td>du</td><td>-st</td><td>wohnst</td><td>bist</td><td>hast</td></tr>
          <tr><td>er/sie/es</td><td>-t</td><td>wohnt</td><td>ist</td><td>hat</td></tr>
          <tr><td>wir</td><td>-en</td><td>wohnen</td><td>sind</td><td>haben</td></tr>
          <tr><td>ihr</td><td>-t</td><td>wohnt</td><td>seid</td><td>habt</td></tr>
          <tr><td>sie/Sie</td><td>-en</td><td>wohnen</td><td>sind</td><td>haben</td></tr>
        </table>
        <p>Some verbs change their stem vowel in <b>du</b> and <b>er/sie/es</b>: sprechen → du sprichst, fahren → du fährst, lesen → du liest, essen → du isst.</p>
        <div class="example"><div class="de">Ich wohne in Berlin. Wo wohnst du?</div><div class="en">I live in Berlin. Where do you live?</div></div>
      `
    },
    {
      id: "a1-wordorder",
      title: "Satzbau & Fragen",
      desc: "Word order: the verb in position 2, yes/no and W-questions",
      body: `
        <p>The golden rule: in a German statement, the conjugated verb is always in <b>position 2</b>.</p>
        <div class="example"><div class="de">Ich <b>lerne</b> heute Deutsch. / Heute <b>lerne</b> ich Deutsch.</div><div class="en">I'm learning German today. (Whatever comes first, the verb stays second.)</div></div>
        <h3>W-Fragen (question words)</h3>
        <p><b>Wer</b> (who), <b>Was</b> (what), <b>Wo</b> (where), <b>Woher</b> (where from), <b>Wohin</b> (where to), <b>Wann</b> (when), <b>Wie</b> (how), <b>Warum</b> (why). The verb stays in position 2:</p>
        <div class="example"><div class="de">Woher kommst du? — Ich komme aus Syrien.</div><div class="en">Where do you come from? — I come from Syria.</div></div>
        <h3>Ja/Nein-Fragen</h3>
        <p>For yes/no questions, the verb moves to <b>position 1</b>:</p>
        <div class="example"><div class="de">Sprichst du Englisch? — Ja, ein bisschen.</div><div class="en">Do you speak English? — Yes, a little.</div></div>
      `
    },
    {
      id: "a1-akkusativ",
      title: "Der Akkusativ",
      desc: "Direct objects: den, die, das + einen, eine, ein",
      body: `
        <p>The accusative is the case of the <b>direct object</b> — the thing the action happens to. Only the <b>masculine</b> article changes!</p>
        <table class="gram">
          <tr><th></th><th>masculine</th><th>feminine</th><th>neuter</th><th>plural</th></tr>
          <tr><td>Nominativ</td><td>der / ein</td><td>die / eine</td><td>das / ein</td><td>die</td></tr>
          <tr><td>Akkusativ</td><td><b>den / einen</b></td><td>die / eine</td><td>das / ein</td><td>die</td></tr>
        </table>
        <div class="example"><div class="de">Ich kaufe <b>einen</b> Apfel und <b>eine</b> Banane.</div><div class="en">I'm buying an apple and a banana.</div></div>
        <p>Common verbs that take the accusative: <b>haben, kaufen, essen, trinken, sehen, suchen, brauchen, nehmen, es gibt</b>.</p>
        <p>Prepositions that always take accusative: <b>für, ohne, gegen, um, durch</b> (merk-word: <i>FOGUD</i>).</p>
      `
    },
    {
      id: "a1-possessiv",
      title: "Possessivartikel",
      desc: "mein, dein, sein, ihr … — saying 'my', 'your', 'his', 'her'",
      body: `
        <table class="gram">
          <tr><th>Person</th><th>Possessive</th><th>Example</th></tr>
          <tr><td>ich</td><td>mein</td><td>mein Bruder, meine Schwester</td></tr>
          <tr><td>du</td><td>dein</td><td>dein Buch</td></tr>
          <tr><td>er/es</td><td>sein</td><td>sein Auto</td></tr>
          <tr><td>sie (she)</td><td>ihr</td><td>ihr Mann</td></tr>
          <tr><td>wir</td><td>unser</td><td>unsere Wohnung</td></tr>
          <tr><td>ihr</td><td>euer</td><td>eure Kinder</td></tr>
          <tr><td>sie/Sie</td><td>ihr/Ihr</td><td>Ihre Adresse (formal)</td></tr>
        </table>
        <p>Possessives take the same endings as <b>ein</b>: feminine and plural add <b>-e</b> (meine Mutter), masculine accusative adds <b>-en</b> (Ich sehe meinen Vater).</p>
        <div class="example"><div class="de">Das ist meine Familie: mein Vater, meine Mutter und mein Bruder.</div><div class="en">This is my family: my father, my mother and my brother.</div></div>
      `
    },
    {
      id: "a1-modal",
      title: "Modalverben: können, müssen, wollen, möchten",
      desc: "Modal verbs and the sentence bracket",
      body: `
        <table class="gram">
          <tr><th></th><th>können (can)</th><th>müssen (must)</th><th>wollen (want)</th><th>möchten (would like)</th></tr>
          <tr><td>ich</td><td>kann</td><td>muss</td><td>will</td><td>möchte</td></tr>
          <tr><td>du</td><td>kannst</td><td>musst</td><td>willst</td><td>möchtest</td></tr>
          <tr><td>er/sie/es</td><td>kann</td><td>muss</td><td>will</td><td>möchte</td></tr>
          <tr><td>wir</td><td>können</td><td>müssen</td><td>wollen</td><td>möchten</td></tr>
          <tr><td>ihr</td><td>könnt</td><td>müsst</td><td>wollt</td><td>möchtet</td></tr>
          <tr><td>sie/Sie</td><td>können</td><td>müssen</td><td>wollen</td><td>möchten</td></tr>
        </table>
        <p><b>Satzklammer:</b> the modal verb goes in position 2, the main verb goes to the <b>end</b> as infinitive:</p>
        <div class="example"><div class="de">Ich <b>kann</b> heute nicht <b>kommen</b>. / Wir <b>möchten</b> zwei Kaffee <b>bestellen</b>.</div><div class="en">I can't come today. / We'd like to order two coffees.</div></div>
      `
    },
    {
      id: "a1-perfekt",
      title: "Perfekt (Einführung)",
      desc: "Talking about the past: haben/sein + Partizip II",
      body: `
        <p>In spoken German, the past is usually expressed with the <b>Perfekt</b>: <b>haben/sein</b> (position 2) + <b>Partizip II</b> (end).</p>
        <p>• Regular verbs: <b>ge…t</b> → machen → gemacht, kaufen → gekauft, lernen → gelernt<br>
        • Irregular verbs: <b>ge…en</b> → sehen → gesehen, essen → gegessen, trinken → getrunken<br>
        • Verbs of movement / change use <b>sein</b>: gehen → ist gegangen, fahren → ist gefahren, fliegen → ist geflogen, bleiben → ist geblieben</p>
        <div class="example"><div class="de">Ich <b>habe</b> gestern Pizza <b>gegessen</b>. Dann <b>bin</b> ich nach Hause <b>gegangen</b>.</div><div class="en">I ate pizza yesterday. Then I went home.</div></div>
        <p>Verbs ending in <b>-ieren</b> get no ge-: studieren → studiert, telefonieren → telefoniert.</p>
      `
    },
    {
      id: "a1-imperativ",
      title: "Imperativ & trennbare Verben",
      desc: "Commands and separable verbs (aufstehen, einkaufen …)",
      body: `
        <h3>Imperativ</h3>
        <table class="gram">
          <tr><th>Form</th><th>kommen</th><th>nehmen</th></tr>
          <tr><td>du</td><td>Komm!</td><td>Nimm!</td></tr>
          <tr><td>ihr</td><td>Kommt!</td><td>Nehmt!</td></tr>
          <tr><td>Sie</td><td>Kommen Sie!</td><td>Nehmen Sie!</td></tr>
        </table>
        <div class="example"><div class="de">Öffnen Sie bitte das Fenster! / Mach die Tür zu!</div><div class="en">Please open the window! / Close the door!</div></div>
        <h3>Trennbare Verben</h3>
        <p>With separable verbs the prefix splits off and goes to the <b>end</b>: <b>auf</b>stehen, <b>ein</b>kaufen, <b>an</b>rufen, <b>fern</b>sehen, <b>mit</b>kommen.</p>
        <div class="example"><div class="de">Ich stehe um 7 Uhr <b>auf</b>. Rufst du mich morgen <b>an</b>?</div><div class="en">I get up at 7. Will you call me tomorrow?</div></div>
      `
    }
  ],

  A2: [
    {
      id: "a2-dativ",
      title: "Der Dativ",
      desc: "Indirect objects: dem, der, dem + dative prepositions",
      body: `
        <table class="gram">
          <tr><th></th><th>masculine</th><th>feminine</th><th>neuter</th><th>plural</th></tr>
          <tr><td>Dativ</td><td><b>dem / einem</b></td><td><b>der / einer</b></td><td><b>dem / einem</b></td><td><b>den …n</b></td></tr>
        </table>
        <p>The dative marks the <b>indirect object</b> (to/for whom). In the plural the noun adds <b>-n</b>: mit den Kindern.</p>
        <p>Verbs with dative: <b>helfen, danken, gefallen, gehören, schmecken, antworten</b>.</p>
        <div class="example"><div class="de">Ich helfe <b>meinem</b> Bruder. Das Buch gehört <b>der</b> Lehrerin.</div><div class="en">I help my brother. The book belongs to the teacher.</div></div>
        <p>Prepositions that always take dative: <b>aus, bei, mit, nach, seit, von, zu</b> (sing them to a melody — it works!).</p>
        <div class="example"><div class="de">Ich fahre mit dem Bus zur Arbeit. Nach der Arbeit gehe ich zum Sport.</div><div class="en">I take the bus to work. After work I go to the gym.</div></div>
      `
    },
    {
      id: "a2-perfekt2",
      title: "Perfekt (Vertiefung)",
      desc: "Separable, inseparable and -ieren verbs in the Perfekt",
      body: `
        <table class="gram">
          <tr><th>Type</th><th>Rule</th><th>Example</th></tr>
          <tr><td>regular</td><td>ge…t</td><td>gemacht, gearbeitet</td></tr>
          <tr><td>irregular</td><td>ge…en</td><td>geschrieben, gefunden</td></tr>
          <tr><td>separable</td><td>prefix + ge</td><td>eingekauft, angerufen, ferngesehen</td></tr>
          <tr><td>inseparable (be-, ver-, er-…)</td><td>no ge-</td><td>besucht, verstanden, erzählt</td></tr>
          <tr><td>-ieren</td><td>no ge-</td><td>studiert, passiert, repariert</td></tr>
        </table>
        <div class="example"><div class="de">Ich habe gestern eingekauft, dann habe ich meine Oma besucht.</div><div class="en">Yesterday I went shopping, then I visited my grandma.</div></div>
        <p><b>sein</b> is used with movement (gehen, fahren, kommen, fliegen), change of state (aufstehen, einschlafen) and: bleiben, sein, passieren.</p>
        <div class="example"><div class="de">Was ist passiert? — Ich bin zu spät aufgestanden!</div><div class="en">What happened? — I got up too late!</div></div>
      `
    },
    {
      id: "a2-praeteritum",
      title: "Präteritum: war, hatte & Modalverben",
      desc: "Simple past of sein, haben and the modal verbs",
      body: `
        <p>Even in spoken German, <b>sein</b>, <b>haben</b> and modal verbs are used in the Präteritum instead of the Perfekt.</p>
        <table class="gram">
          <tr><th></th><th>sein</th><th>haben</th><th>können</th><th>müssen</th><th>wollen</th></tr>
          <tr><td>ich/er/sie</td><td>war</td><td>hatte</td><td>konnte</td><td>musste</td><td>wollte</td></tr>
          <tr><td>du</td><td>warst</td><td>hattest</td><td>konntest</td><td>musstest</td><td>wolltest</td></tr>
          <tr><td>wir/sie</td><td>waren</td><td>hatten</td><td>konnten</td><td>mussten</td><td>wollten</td></tr>
          <tr><td>ihr</td><td>wart</td><td>hattet</td><td>konntet</td><td>musstet</td><td>wolltet</td></tr>
        </table>
        <div class="example"><div class="de">Gestern war ich krank. Ich hatte Fieber und konnte nicht arbeiten.</div><div class="en">Yesterday I was sick. I had a fever and couldn't work.</div></div>
      `
    },
    {
      id: "a2-komparativ",
      title: "Komparativ & Superlativ",
      desc: "Comparing things: schöner, am schönsten",
      body: `
        <table class="gram">
          <tr><th>Positiv</th><th>Komparativ</th><th>Superlativ</th></tr>
          <tr><td>klein</td><td>kleiner</td><td>am kleinsten</td></tr>
          <tr><td>alt</td><td>älter</td><td>am ältesten</td></tr>
          <tr><td>groß</td><td>größer</td><td>am größten</td></tr>
          <tr><td>gut</td><td>besser</td><td>am besten</td></tr>
          <tr><td>viel</td><td>mehr</td><td>am meisten</td></tr>
          <tr><td>gern</td><td>lieber</td><td>am liebsten</td></tr>
        </table>
        <p>Short adjectives with a, o, u usually take an umlaut (alt → älter, jung → jünger, groß → größer).</p>
        <p>Comparisons: <b>… als</b> (than) and <b>so … wie</b> (as … as).</p>
        <div class="example"><div class="de">Berlin ist größer als München, aber München ist so teuer wie Hamburg. Am liebsten trinke ich Tee.</div><div class="en">Berlin is bigger than Munich, but Munich is as expensive as Hamburg. I like drinking tea the most.</div></div>
      `
    },
    {
      id: "a2-nebensatz",
      title: "Nebensätze: weil, dass, wenn",
      desc: "Subordinate clauses — the verb goes to the end!",
      body: `
        <p>After <b>weil</b> (because), <b>dass</b> (that), <b>wenn</b> (if/when), <b>obwohl</b> (although), the conjugated verb moves to the <b>end</b> of the clause:</p>
        <div class="example"><div class="de">Ich lerne Deutsch, <b>weil</b> ich in Deutschland arbeiten <b>möchte</b>.</div><div class="en">I'm learning German because I want to work in Germany.</div></div>
        <div class="example"><div class="de">Ich glaube, <b>dass</b> die Prüfung nicht schwer <b>ist</b>.</div><div class="en">I think that the exam is not difficult.</div></div>
        <div class="example"><div class="de"><b>Wenn</b> das Wetter schön <b>ist</b>, machen wir ein Picknick.</div><div class="en">If the weather is nice, we'll have a picnic.</div></div>
        <p>⚠️ Note: when the sentence <i>starts</i> with the subordinate clause, the main clause begins with the verb (verb–verb in the middle: „…ist, machen wir…“).</p>
        <p>Coordinating conjunctions <b>und, aber, oder, denn</b> do NOT change word order.</p>
      `
    },
    {
      id: "a2-reflexiv",
      title: "Reflexive Verben",
      desc: "sich freuen, sich treffen, sich interessieren …",
      body: `
        <p>Many German verbs need a reflexive pronoun: <b>mich, dich, sich, uns, euch, sich</b>.</p>
        <table class="gram">
          <tr><th>Person</th><th>sich freuen (to be happy)</th></tr>
          <tr><td>ich</td><td>freue <b>mich</b></td></tr>
          <tr><td>du</td><td>freust <b>dich</b></td></tr>
          <tr><td>er/sie/es</td><td>freut <b>sich</b></td></tr>
          <tr><td>wir</td><td>freuen <b>uns</b></td></tr>
          <tr><td>ihr</td><td>freut <b>euch</b></td></tr>
          <tr><td>sie/Sie</td><td>freuen <b>sich</b></td></tr>
        </table>
        <p>Common combinations: <b>sich freuen auf</b> (+Akk, look forward to), <b>sich interessieren für</b>, <b>sich treffen mit</b>, <b>sich ärgern über</b>, <b>sich erinnern an</b>.</p>
        <div class="example"><div class="de">Ich freue mich auf das Wochenende. Interessierst du dich für Musik?</div><div class="en">I'm looking forward to the weekend. Are you interested in music?</div></div>
      `
    },
    {
      id: "a2-wechsel",
      title: "Wechselpräpositionen",
      desc: "in, an, auf, über, unter … — Wohin? (Akk) vs. Wo? (Dat)",
      body: `
        <p>Nine prepositions take <b>accusative</b> with movement (Wohin?) and <b>dative</b> with location (Wo?): <b>in, an, auf, über, unter, vor, hinter, neben, zwischen</b>.</p>
        <table class="gram">
          <tr><th>Wohin? → Akkusativ</th><th>Wo? → Dativ</th></tr>
          <tr><td>Ich gehe <b>in die</b> Schule.</td><td>Ich bin <b>in der</b> Schule.</td></tr>
          <tr><td>Ich hänge das Bild <b>an die</b> Wand.</td><td>Das Bild hängt <b>an der</b> Wand.</td></tr>
          <tr><td>Ich lege das Buch <b>auf den</b> Tisch.</td><td>Das Buch liegt <b>auf dem</b> Tisch.</td></tr>
        </table>
        <p>Useful contractions: in + das = <b>ins</b>, in + dem = <b>im</b>, an + das = <b>ans</b>, an + dem = <b>am</b>.</p>
        <div class="example"><div class="de">Am Samstag gehen wir ins Kino. Im Kino ist es dunkel.</div><div class="en">On Saturday we're going to the cinema. It's dark in the cinema.</div></div>
      `
    },
    {
      id: "a2-futur",
      title: "Zukunft & Empfehlungen: werden, sollten",
      desc: "Future with werden and advice with sollten",
      body: `
        <p>The future can be expressed with the present tense + a time word, or with <b>werden + Infinitiv</b>:</p>
        <div class="example"><div class="de">Morgen fahre ich nach Köln. / Ich werde nächstes Jahr die B1-Prüfung machen.</div><div class="en">Tomorrow I'm going to Cologne. / Next year I will take the B1 exam.</div></div>
        <table class="gram">
          <tr><th>Person</th><th>werden</th></tr>
          <tr><td>ich</td><td>werde</td></tr>
          <tr><td>du</td><td>wirst</td></tr>
          <tr><td>er/sie/es</td><td>wird</td></tr>
          <tr><td>wir/sie/Sie</td><td>werden</td></tr>
          <tr><td>ihr</td><td>werdet</td></tr>
        </table>
        <p>For advice use <b>sollten</b>:</p>
        <div class="example"><div class="de">Du solltest mehr Wasser trinken. Sie sollten jeden Tag Vokabeln lernen.</div><div class="en">You should drink more water. You should learn vocabulary every day.</div></div>
      `
    }
  ],

  B1: [
    {
      id: "b1-passiv",
      title: "Das Passiv",
      desc: "werden + Partizip II — when the action matters, not the actor",
      body: `
        <p><b>Vorgangspassiv:</b> werden + Partizip II. The object becomes the subject.</p>
        <div class="example"><div class="de">Aktiv: Der Mechaniker repariert das Auto. → Passiv: Das Auto <b>wird repariert</b>.</div><div class="en">The car is being repaired.</div></div>
        <table class="gram">
          <tr><th>Tense</th><th>Form</th><th>Example</th></tr>
          <tr><td>Präsens</td><td>wird + P II</td><td>Das Haus wird gebaut.</td></tr>
          <tr><td>Präteritum</td><td>wurde + P II</td><td>Das Haus wurde gebaut.</td></tr>
          <tr><td>Perfekt</td><td>ist + P II + worden</td><td>Das Haus ist gebaut worden.</td></tr>
          <tr><td>mit Modalverb</td><td>muss + P II + werden</td><td>Das Haus muss gebaut werden.</td></tr>
        </table>
        <p>The actor can be added with <b>von + Dativ</b>: Der Brief wurde <b>von meiner Chefin</b> geschrieben.</p>
        <p>Very common in the B1 exam in formal texts: „Die Anmeldung <b>wird</b> bis Freitag <b>verlängert</b>.“</p>
      `
    },
    {
      id: "b1-konjunktiv",
      title: "Konjunktiv II",
      desc: "würde, hätte, wäre, könnte — polite requests and unreal wishes",
      body: `
        <table class="gram">
          <tr><th>Verb</th><th>Konjunktiv II</th><th>Use</th></tr>
          <tr><td>werden</td><td>würde + Infinitiv</td><td>most verbs: Ich würde gern reisen.</td></tr>
          <tr><td>haben</td><td>hätte</td><td>Ich hätte gern einen Kaffee.</td></tr>
          <tr><td>sein</td><td>wäre</td><td>Das wäre schön!</td></tr>
          <tr><td>können</td><td>könnte</td><td>Könnten Sie mir helfen?</td></tr>
          <tr><td>sollen</td><td>sollte</td><td>Du solltest früher schlafen gehen.</td></tr>
        </table>
        <h3>Uses</h3>
        <p>1. <b>Polite requests:</b> Könnten Sie das bitte wiederholen? / Wären Sie so nett …?<br>
        2. <b>Wishes:</b> Ich hätte gern mehr Zeit. / Wenn ich reich wäre, …<br>
        3. <b>Unreal conditions:</b></p>
        <div class="example"><div class="de">Wenn ich mehr Zeit <b>hätte</b>, <b>würde</b> ich jeden Tag Deutsch <b>lernen</b>.</div><div class="en">If I had more time, I would study German every day.</div></div>
        <p>4. <b>Advice:</b> An deiner Stelle würde ich den Kurs besuchen.</p>
      `
    },
    {
      id: "b1-relativ",
      title: "Relativsätze",
      desc: "der, die, das as relative pronouns — describing nouns",
      body: `
        <p>Relative clauses describe a noun. The pronoun matches the noun's <b>gender/number</b>, but its <b>case</b> comes from its role in the relative clause. The verb goes to the end.</p>
        <table class="gram">
          <tr><th></th><th>m</th><th>f</th><th>n</th><th>pl</th></tr>
          <tr><td>Nominativ</td><td>der</td><td>die</td><td>das</td><td>die</td></tr>
          <tr><td>Akkusativ</td><td>den</td><td>die</td><td>das</td><td>die</td></tr>
          <tr><td>Dativ</td><td>dem</td><td>der</td><td>dem</td><td>denen</td></tr>
        </table>
        <div class="example"><div class="de">Das ist der Mann, <b>der</b> neben mir wohnt.</div><div class="en">That's the man who lives next to me. (subject → Nominativ)</div></div>
        <div class="example"><div class="de">Das ist der Film, <b>den</b> ich gestern gesehen habe.</div><div class="en">That's the film that I saw yesterday. (object → Akkusativ)</div></div>
        <div class="example"><div class="de">Die Frau, <b>mit der</b> ich arbeite, kommt aus Italien.</div><div class="en">The woman I work with is from Italy. (preposition + case)</div></div>
      `
    },
    {
      id: "b1-genitiv",
      title: "Der Genitiv",
      desc: "des Mannes, der Frau — possession and genitive prepositions",
      body: `
        <table class="gram">
          <tr><th></th><th>m</th><th>f</th><th>n</th><th>pl</th></tr>
          <tr><td>Genitiv</td><td>des Mannes</td><td>der Frau</td><td>des Kindes</td><td>der Kinder</td></tr>
        </table>
        <p>Masculine and neuter nouns add <b>-s/-es</b>. The genitive expresses possession or belonging:</p>
        <div class="example"><div class="de">Das Auto <b>meines Vaters</b> ist alt. Die Farbe <b>der Wand</b> gefällt mir.</div><div class="en">My father's car is old. I like the colour of the wall.</div></div>
        <p>Prepositions with genitive: <b>wegen</b> (because of), <b>trotz</b> (despite), <b>während</b> (during), <b>statt</b> (instead of).</p>
        <div class="example"><div class="de">Wegen des Regens bleiben wir zu Hause. Trotz der Kälte gehen wir spazieren.</div><div class="en">Because of the rain we're staying home. Despite the cold we're going for a walk.</div></div>
        <p>In spoken German, <b>von + Dativ</b> often replaces it: das Auto von meinem Vater.</p>
      `
    },
    {
      id: "b1-infinitiv",
      title: "Infinitiv mit zu & damit/um…zu",
      desc: "Ich habe vergessen, dich anzurufen. Purpose clauses.",
      body: `
        <p>After many verbs and expressions, use <b>zu + Infinitiv</b>: vergessen, versuchen, anfangen, aufhören, vorhaben, Lust haben, Zeit haben, es ist wichtig/schwer …</p>
        <div class="example"><div class="de">Ich habe vergessen, dich <b>anzurufen</b>. Es ist wichtig, jeden Tag <b>zu üben</b>.</div><div class="en">I forgot to call you. It's important to practise every day.</div></div>
        <p>⚠️ With separable verbs, <b>zu</b> goes inside: an<b>zu</b>rufen, ein<b>zu</b>kaufen.</p>
        <h3>Purpose: um … zu vs. damit</h3>
        <p>Same subject → <b>um … zu</b>; different subjects → <b>damit</b>:</p>
        <div class="example"><div class="de">Ich lerne Deutsch, <b>um</b> in Deutschland <b>zu studieren</b>.</div><div class="en">I'm learning German (in order) to study in Germany.</div></div>
        <div class="example"><div class="de">Ich spreche langsam, <b>damit</b> alle mich verstehen.</div><div class="en">I speak slowly so that everyone understands me.</div></div>
      `
    },
    {
      id: "b1-adjektiv",
      title: "Adjektivdeklination",
      desc: "der gute Mann, ein guter Mann — adjective endings",
      body: `
        <p>Adjectives before a noun take endings. Two key patterns:</p>
        <h3>After der/die/das (weak)</h3>
        <table class="gram">
          <tr><th></th><th>m</th><th>f</th><th>n</th><th>pl</th></tr>
          <tr><td>Nom</td><td>der gut<b>e</b></td><td>die gut<b>e</b></td><td>das gut<b>e</b></td><td>die gut<b>en</b></td></tr>
          <tr><td>Akk</td><td>den gut<b>en</b></td><td>die gut<b>e</b></td><td>das gut<b>e</b></td><td>die gut<b>en</b></td></tr>
          <tr><td>Dat</td><td colspan="4">always <b>-en</b></td></tr>
        </table>
        <h3>After ein/kein/mein (mixed)</h3>
        <table class="gram">
          <tr><th></th><th>m</th><th>f</th><th>n</th></tr>
          <tr><td>Nom</td><td>ein gut<b>er</b> Mann</td><td>eine gut<b>e</b> Frau</td><td>ein gut<b>es</b> Kind</td></tr>
          <tr><td>Akk</td><td>einen gut<b>en</b> Mann</td><td>eine gut<b>e</b> Frau</td><td>ein gut<b>es</b> Kind</td></tr>
        </table>
        <p>Memory aid: in the dative (and genitive) it's almost always <b>-en</b>. In the plural after die/keine/meine → <b>-en</b>.</p>
        <div class="example"><div class="de">Ich suche eine kleine Wohnung mit einem großen Balkon.</div><div class="en">I'm looking for a small flat with a big balcony.</div></div>
      `
    },
    {
      id: "b1-plusquam",
      title: "Plusquamperfekt & nachdem",
      desc: "hatte/war + Partizip II — 'past before the past'",
      body: `
        <p>The Plusquamperfekt describes what happened <b>before</b> another past event: <b>hatte/war + Partizip II</b>. It is the typical partner of <b>nachdem</b>:</p>
        <div class="example"><div class="de"><b>Nachdem</b> ich gegessen <b>hatte</b>, ging ich ins Bett.</div><div class="en">After I had eaten, I went to bed.</div></div>
        <div class="example"><div class="de"><b>Nachdem</b> wir angekommen <b>waren</b>, riefen wir unsere Eltern an.</div><div class="en">After we had arrived, we called our parents.</div></div>
        <p>Rule of thumb for nachdem-sentences: <b>Nebensatz = Plusquamperfekt, Hauptsatz = Präteritum/Perfekt</b>.</p>
        <p>Other useful temporal connectors: <b>bevor</b> (before), <b>während</b> (while), <b>seitdem</b> (since), <b>bis</b> (until), <b>als</b> (when – single past event), <b>wenn</b> (when – repeated/present).</p>
        <div class="example"><div class="de"><b>Als</b> ich ein Kind war, wohnte ich auf dem Land.</div><div class="en">When I was a child, I lived in the countryside.</div></div>
      `
    },
    {
      id: "b1-konnektoren",
      title: "Konnektoren: deshalb, trotzdem, obwohl …",
      desc: "Linking ideas like a B1 pro — essential for Schreiben & Sprechen",
      body: `
        <table class="gram">
          <tr><th>Konnektor</th><th>Meaning</th><th>Word order</th></tr>
          <tr><td>deshalb / deswegen / darum</td><td>therefore</td><td>verb directly after (Position 1)</td></tr>
          <tr><td>trotzdem</td><td>nevertheless</td><td>verb directly after</td></tr>
          <tr><td>außerdem</td><td>moreover</td><td>verb directly after</td></tr>
          <tr><td>obwohl</td><td>although</td><td>verb to the end</td></tr>
          <tr><td>denn</td><td>because</td><td>normal word order</td></tr>
          <tr><td>entweder … oder</td><td>either … or</td><td>—</td></tr>
          <tr><td>sowohl … als auch</td><td>both … and</td><td>—</td></tr>
        </table>
        <div class="example"><div class="de">Ich war müde, <b>trotzdem</b> habe ich weitergelernt.</div><div class="en">I was tired; nevertheless I kept studying.</div></div>
        <div class="example"><div class="de"><b>Obwohl</b> Deutsch schwer ist, macht es mir Spaß. <b>Deshalb</b> übe ich jeden Tag.</div><div class="en">Although German is hard, I enjoy it. That's why I practise every day.</div></div>
        <p>💡 Using these connectors correctly is one of the easiest ways to earn points in the Goethe B1 writing and speaking modules!</p>
      `
    }
  ]
};
