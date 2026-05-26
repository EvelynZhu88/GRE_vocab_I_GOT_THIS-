# -*- coding: utf-8 -*-
"""
Builder: write 3 GRE-hard reading passages for each of lists 16-30
and merge them into passages.json (preserving lists 1-15).

Run:  python build_passages_16_30.py
"""
import json, sys, io, pathlib

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "passages.json"

NEW = {}

# ---------------------------------------------------------------------------
# LIST 16
# ---------------------------------------------------------------------------
NEW["16"] = [
    {
        "title": "The Restorer's Folly",
        "targets": [
            "dilapidate","opulent","residual","languish","halcyon","antebellum",
            "awash","adorn","contemporary","rarefied","sentimental","providential",
            "ethos","burgeon","anomaly","subterfuge","culpable","high-minded",
            "ponderous","obsessed","calibrate","temporary","calculated"
        ],
        "text": (
            "When Henrietta Vail bought the dilapidated Beauclair estate she described the purchase, "
            "to anyone who would listen, as providential. The house had languished, vacant, for the better "
            "part of a decade — its opulent ballroom awash in pigeon droppings, its antebellum portico "
            "sagging — and the few residual furnishings had been picked over by thieves who, she liked to "
            "say, had at least left her the floor plans. Her stated ethos was preservation: she would restore "
            "Beauclair to its halcyon condition and adorn it, room by room, with the only kind of objects "
            "she trusted, which were those a contemporary collector could no longer afford.\n\n"
            "The trouble with Henrietta's project, her foreman observed, was that she had never calibrated "
            "her ambitions to her budget. She was obsessed with a rarefied notion of authenticity that "
            "treated every modern accommodation — wiring, plumbing, the temporary scaffolding required to "
            "save the roof — as a kind of moral failure. When his crew suggested a hidden steel beam to keep "
            "the second floor from collapse, she received the proposal as if it were an act of subterfuge. "
            "A beam, she said, would make the restoration a fiction; she would rather see the ceiling fall.\n\n"
            "Her critics in the local preservation society, who had once been her allies, came to regard "
            "her project as a sentimental anomaly. They had thought her merely ponderous in her tastes; "
            "now they suspected something less innocent. A house was not a reliquary, one of them wrote in "
            "a high-minded letter to the regional paper; to insist that every nail be antebellum was not "
            "preservation but vanity dressed in the costume of scholarship.\n\n"
            "Henrietta read the letter twice and filed it. She knew the charge was, in some narrow sense, "
            "fair — she was vain about Beauclair, and she did want the credit her vanity required. But she "
            "also believed, with a calculated patience her critics never granted her, that the burgeoning "
            "interest the restoration had drawn would in time outlive her preferences. A century from now, "
            "she told her foreman, no one would remember whose ceiling had cracked under whose budget. They "
            "would only see the house. If she was culpable of any folly, it was the folly of believing that "
            "buildings, unlike the people who fought over them, could be made to keep their promises."
        ),
        "questions": [
            {
                "q": "The author's portrayal of Henrietta is best characterized as",
                "opts": [
                    "wholly sympathetic, presenting her as a misunderstood guardian of heritage.",
                    "ambivalent, granting her motives a certain coherence while exposing their excess.",
                    "satirical, mocking her pretensions through her foreman's commentary.",
                    "censorious, treating her project as a cautionary example of private wealth."
                ],
                "ans": 1,
                "why": "The closing paragraph concedes the charge of vanity is 'in some narrow sense, fair' yet credits her with a 'calculated patience' her critics deny her — a balanced rather than wholly sympathetic or condemnatory portrait."
            },
            {
                "q": "Which of the following, if true, would most undermine the preservation society's objection to Henrietta as quoted in the third paragraph?",
                "opts": [
                    "Comparable estates restored with modern reinforcement have, within a generation, required complete demolition because hidden steel altered the load distribution of original masonry.",
                    "Most visitors to historic houses cannot distinguish original materials from skillful contemporary replicas.",
                    "Henrietta has, in private correspondence, expressed regret about the cost of the restoration.",
                    "The local preservation society has itself accepted donations from collectors with rarefied tastes."
                ],
                "ans": 0,
                "why": "The society's objection rests on the claim that insisting on period-authentic materials is 'vanity dressed as scholarship.' Evidence that compromise restorations actively destroy the very buildings they try to save would turn Henrietta's stubbornness into a defensible technical judgment."
            },
            {
                "q": "In the final paragraph, the phrase \"calculated patience\" most nearly conveys",
                "opts": [
                    "a coldly strategic indifference to present opinion.",
                    "a long-term equanimity arrived at through deliberate, not instinctive, reasoning.",
                    "a willingness to manipulate the timing of public statements for advantage.",
                    "an aloof refusal to engage with critics on any terms."
                ],
                "ans": 1,
                "why": "The phrase contrasts with the critics' picture of vanity by suggesting Henrietta has reasoned her way to her composure rather than felt it; she is patient by design, not by temperament."
            }
        ]
    },
    {
        "title": "The Panegyric Refused",
        "targets": [
            "sententious","exultant","panegyric","condescending","glib","vainglorious",
            "lackluster","mirth","insult","complimentary","disdain","trenchant",
            "scintillating","gaffe","forthright","blameless","fetter","mighty",
            "endorse","cynical","emphatic","strain","predispose"
        ],
        "text": (
            "When the academy announced that its annual panegyric would be delivered in honor of Professor "
            "Halloran, those who knew the man were predisposed to expect a small disaster. Halloran disdained "
            "the genre. He had, on three prior occasions, refused similar tributes from other institutions, "
            "calling them, in one famously trenchant interview, \"the only ceremony at which a scholar is "
            "expected to be both the corpse and the chief mourner.\" That the academy had pressed on anyway "
            "struck many as either brave or vainglorious; few thought it would prove blameless.\n\n"
            "The chosen orator, a younger colleague named Pell, was glib in the way ambitious juniors often "
            "are — fluent, scintillating in short bursts, and prone to confuse sententious phrasing with "
            "depth of thought. His draft, circulated in advance, opened with an exultant comparison of "
            "Halloran to a half-dozen mighty intellectual ancestors, none of whom Halloran had ever "
            "publicly endorsed. The middle pages strained for warmth and produced only a kind of "
            "condescending fondness. By the closing paragraph the tone had become outright complimentary "
            "in the lackluster manner of an awards-show introduction.\n\n"
            "Halloran read the draft on the train and arrived at the ceremony with an emphatic intention: "
            "to neither interrupt nor pretend. When Pell took the lectern he listened, hands folded, with the "
            "patience of a man enduring weather. The audience, alert to the awkwardness, mistook his "
            "stillness for mirth at first; then, as the orator's metaphors grew more strained, for a kind of "
            "icy disdain. Only those nearest the stage could see that his expression was, if anything, sad.\n\n"
            "When the time came for his reply, Halloran did not, as his enemies hoped, deliver an insult. "
            "He thanked Pell with a forthright brevity that surprised the room. Then he said, in a voice "
            "free of any ironic fetter, that the gaffe of such ceremonies was not the speaker's but the "
            "institution's: the academy had chosen to honor what was easiest to praise rather than what was "
            "hardest to understand. He was not, he said, a corpse yet, and he intended to spend whatever "
            "remained of his career making a less convenient subject of himself. The applause was uncertain, "
            "as it always is when an audience suspects that the cynical reading of the evening — that the "
            "honoree has insulted his hosts — may also be the most generous."
        ),
        "questions": [
            {
                "q": "The passage suggests that Halloran's central objection to ceremonial tributes is that they",
                "opts": [
                    "reward seniority rather than current achievement.",
                    "substitute a fixed, flattering image of a scholar for the difficulty of his actual work.",
                    "place too heavy a burden of public performance on the honoree.",
                    "are written by speakers too junior to assess their subjects."
                ],
                "ans": 1,
                "why": "Halloran's reply names the institution's choice to \"honor what was easiest to praise rather than what was hardest to understand\" — i.e. tributes flatten a scholar's work into a manageable image, which is the substantive objection."
            },
            {
                "q": "The author's treatment of Pell is most accurately described as",
                "opts": [
                    "openly contemptuous, attributing his failure to bad faith.",
                    "diagnostic without being cruel, locating his fluency in a recognizable type.",
                    "sympathetic, suggesting he was set up by the academy to fail.",
                    "neutral, withholding judgment on the quality of his speech."
                ],
                "ans": 1,
                "why": "The narrator names Pell as \"glib in the way ambitious juniors often are\" — a type-level diagnosis rather than personal malice, and not openly contemptuous, sympathetic, or neutral."
            },
            {
                "q": "The final sentence implies that the audience's uncertain applause arose because",
                "opts": [
                    "they could not hear Halloran's closing remarks clearly.",
                    "the cynical interpretation of the evening was simultaneously the most flattering one to Halloran.",
                    "they were divided between supporters and detractors of the academy.",
                    "they doubted that Halloran's career still warranted a tribute."
                ],
                "ans": 1,
                "why": "The sentence turns on the paradox that the most cynical reading — Halloran has insulted his hosts — is also the most generous to him, since it credits him with the integrity the speech lacked; that paradox is what makes the applause uncertain."
            }
        ]
    },
    {
        "title": "The Curator's Foray",
        "targets": [
            "curator","divination","espouse","anomaly","peregrinate","burgeon","ethos",
            "camouflage","flamboyant","exceptional","foray","fetishize","obnoxious",
            "discretion","alternative","avant-garde","plagiarize","sympathetic",
            "imbibe","airborne","compartmentalize","providential","sartorial","enjoin"
        ],
        "text": (
            "Lina Park, the new curator at the Walden, had been hired to conduct a foray into the museum's "
            "long-neglected modernist holdings. Her predecessor, a flamboyant collector who had peregrinated "
            "between Berlin and Buenos Aires for twenty years, had left behind a basement awash with works "
            "no one had cataloged. He had espoused, in print and at dinner, an ethos of acquisition that "
            "treated every object as exceptional and every provenance as discretion's burden. The result was "
            "a holding both burgeoning and incoherent — an anomaly even by the standards of midcentury "
            "private-collector museums.\n\n"
            "Park's first decision was sartorial in spirit if not in fact: she would camouflage her foray, "
            "presenting it not as a forensic exercise but as a public exhibition. The alternative, she "
            "explained to her director, was to let the basement go on quietly fetishizing itself — its "
            "obscurity giving it a kind of avant-garde aura the works themselves rarely earned. A show would "
            "force every object into the same airborne light, where its merits could be weighed.\n\n"
            "Her staff found the strategy obnoxious at first. To compartmentalize the collection into "
            "exhibitable categories, they argued, was to plagiarize the very methods of the predecessor she "
            "claimed to be correcting. He, too, had imposed schemes; he, too, had used the camouflage of "
            "thematic display to obscure what he did not understand. Park heard them out. She was sympathetic "
            "to the suspicion — she had imbibed enough institutional history to know that curators tend to "
            "repeat their teachers — but she enjoined them to consider the difference between a scheme "
            "imposed to elevate doubtful objects and one imposed to test them.\n\n"
            "The exhibition, when it opened, was greeted with what the trade papers called a providential "
            "modesty. There were no major rediscoveries; there were, more usefully, several quiet "
            "demotions. A canvas long attributed to a minor surrealist was shown to be the work of his "
            "studio assistant; a sculpture revered as exceptional was revealed, by a wall label written in "
            "Park's own dry hand, as a competent variant of a more famous piece. Critics who had expected "
            "divination — a curator pulling treasures from a dark room — were instead given accounting. "
            "Park, to her staff's surprise, treated the lack of fireworks as a vindication. The museum, she "
            "said, did not need another flamboyant gesture; it needed to know what it owned."
        ),
        "questions": [
            {
                "q": "The passage suggests that Park's chief disagreement with her predecessor's approach concerns",
                "opts": [
                    "his preference for European over American modernists.",
                    "his willingness to acquire works without verifying their attribution.",
                    "his treatment of obscurity as a substitute for evaluation.",
                    "his refusal to display works he had personally collected."
                ],
                "ans": 2,
                "why": "Park's argument for the exhibition is that the basement was 'fetishizing itself' — its obscurity giving works an unearned aura — and that a show would force them into the light where merit could be weighed."
            },
            {
                "q": "The staff's initial objection to Park's plan rests on which of the following assumptions?",
                "opts": [
                    "That any thematic display necessarily distorts the works it organizes.",
                    "That curators who impose interpretive schemes repeat the errors of those they replace.",
                    "That the basement collection contains too few works to justify a public exhibition.",
                    "That Park lacks the scholarly credentials of her predecessor."
                ],
                "ans": 1,
                "why": "The staff argue that to compartmentalize the collection is to 'plagiarize the very methods of the predecessor' — i.e. that imposing a scheme repeats his error, an objection that depends on equating any such scheme with his."
            },
            {
                "q": "The phrase \"providential modesty\" in the final paragraph operates ironically because",
                "opts": [
                    "the exhibition was, in fact, lavish rather than modest.",
                    "the outcomes critics expected to celebrate as fortunate — major rediscoveries — were precisely what the exhibition refused to deliver.",
                    "the press coverage proved to be hostile despite the modest claims of the catalog.",
                    "Park privately considered the exhibition a failure."
                ],
                "ans": 1,
                "why": "Critics expected 'divination' — the providential surfacing of treasures — and instead received reductions of attribution. The phrase reframes what would normally be a disappointment as the actual good fortune the museum needed."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 17
# ---------------------------------------------------------------------------
NEW["17"] = [
    {
        "title": "The Provenance Dispute",
        "targets": [
            "laudatory","controversial","provenance","counterfeit","prescient","apocryphal",
            "delve","conjure","amenable","heinous","forthcoming","constrain","unalloyed",
            "downplay","invidious","misnomer","cunning","prejudice","contaminate","extensive",
            "uncharted","virtuosity","stemma","stereotype","quash","backhanded"
        ],
        "text": (
            "The little panel — eleven inches by eight, oil on a poplar board — had arrived at the institute "
            "with a provenance that was, in the kindest reading, apocryphal. Its owner, a retired importer, "
            "produced two laudatory certificates from dealers long dead and a letter that, on close reading, "
            "delved into the painting's lineage without ever naming the painter. The institute's director, "
            "Marisol Vance, was amenable to investigation but constrained by funds. She authorized an "
            "extensive but quiet examination: no press, no preliminary statements, and — until something was "
            "forthcoming from the lab — no attribution either way.\n\n"
            "The conservator, Idris Owusu, was prescient enough to begin with the wood. A poplar panel of "
            "the alleged period would carry a particular pattern of growth rings; this one did not. The "
            "tree, he told Vance, had been felled at least sixty years too late. The pigment analysis, when "
            "it came, only deepened the suspicion: a synthetic ultramarine that no fifteenth-century "
            "workshop could have conjured. To call the panel a counterfeit, however, struck Owusu as a "
            "misnomer; it was, more precisely, a cunning pastiche, made by someone who had clearly studied "
            "the master's virtuosity and reproduced his stereotype of brushwork without his stemma of "
            "thought.\n\n"
            "The owner, when informed, did not behave as Vance expected. He did not protest, but neither was "
            "he forthcoming. He suggested, with a backhanded smile, that the institute had a prejudice "
            "against unattributed works and that its conclusions would, in time, contaminate his ability to "
            "sell elsewhere. Vance, who had heard versions of this complaint before, replied that the "
            "institute's only invidious habit was to publish what it found.\n\n"
            "The case was, technically, uncontroversial — the science was clean — but the institute's "
            "decision to release a full report rather than quash the matter privately drew unexpected "
            "criticism. Some peers thought the panel's quality was such that a more diplomatic silence "
            "would have served scholarship better; the panel, after all, was a heinous fake only if one "
            "insisted on the original attribution, and a remarkable piece of homage if one did not. Vance "
            "found this reasoning a charted territory she had no wish to revisit. The institute, she wrote "
            "in a short editorial, was not in the business of charting uncharted attributions; it was in "
            "the business of refusing to launder bad ones, however laudatory the original certificates "
            "happened to be."
        ),
        "questions": [
            {
                "q": "Owusu's distinction between a \"counterfeit\" and a \"cunning pastiche\" is most significant because it",
                "opts": [
                    "exonerates the panel's owner of any intent to deceive.",
                    "implies that the panel was produced as an exercise in homage rather than as a fraud, even if it was later sold as one.",
                    "establishes that the panel cannot be legally classified as forged.",
                    "demonstrates that the panel exceeds the master's own work in technical skill."
                ],
                "ans": 1,
                "why": "Owusu locates the deception in the sale, not the making: the maker copied the master's surface but not his thought, suggesting the object began as competent imitation and was only later passed off, which is the distinction the passage trades on."
            },
            {
                "q": "Which of the following best captures the basis on which some of Vance's peers criticized the institute's report?",
                "opts": [
                    "They believed the scientific evidence was insufficient to overturn an existing attribution.",
                    "They held that the panel's aesthetic merit should have inhibited a public correction.",
                    "They suspected that Vance's prior dealings with the owner had prejudiced her judgment.",
                    "They argued that publishing the report exceeded the institute's legal authority."
                ],
                "ans": 1,
                "why": "The criticism is that 'a more diplomatic silence would have served scholarship better' because the panel was a fake only if one insisted on the original attribution; the objection is aesthetic, not evidentiary."
            },
            {
                "q": "Vance's closing position in her editorial most strongly implies that she regards her institute's primary obligation as",
                "opts": [
                    "advancing the most generous possible interpretation of every disputed object.",
                    "refusing to lend credibility to attributions it cannot defend, regardless of an object's quality.",
                    "settling disputes between owners and dealers before they reach the public.",
                    "expanding the historical record by accepting plausible but uncertain attributions."
                ],
                "ans": 1,
                "why": "She frames the institute's job as 'not in the business of laundering bad attributions' — its duty is custodial of credibility, not of objects."
            }
        ]
    },
    {
        "title": "The Recalcitrant Acolyte",
        "targets": [
            "taciturn","ambivalence","recalcitrant","contrite","condone","insipid","abnegation",
            "harsh","apathy","quirky","abominate","earnest","levity","incumbent","oust",
            "apocryphal","spiteful","vacant","missionary","instrumental","handicap","wither",
            "decadent","stereotype","abominate","stereotype"
        ],
        "text": (
            "Of the four students Father Brenner had taken on that year, Jonas was the only one who proved "
            "recalcitrant. The others were earnest, even insipid in their earnestness; they treated their "
            "apprenticeship to the chapel's small library as an exercise in dutiful abnegation and rarely "
            "asked why. Jonas asked nothing else. His questions were never disrespectful, but they were "
            "delivered in a taciturn, slightly quirky manner that some of the older brothers found "
            "harsh.\n\n"
            "Brenner himself felt only ambivalence about the boy. He could not condone the open friction "
            "Jonas occasionally provoked at meals — a single dry remark could leave the refectory in a "
            "vacant, embarrassed quiet — but neither could he treat the boy with the apathy his peers "
            "recommended. Jonas's intelligence was real, if unevenly cultivated; on a good morning he could "
            "explicate a difficult chapter with a missionary's clarity, and on a bad one he could reduce "
            "the same chapter to an apocryphal joke. Levity in the library was incumbent upon no one and "
            "tolerated in only a few; Jonas tested both rules.\n\n"
            "When the request to oust him came formally, from a senior brother whose patience had withered, "
            "Brenner did not act at once. He summoned Jonas, expecting a contrite performance and prepared "
            "to receive one with reservation. Instead Jonas said, plainly, that he had been spiteful in two "
            "particular instances and was sorry; in the others he had only said what he meant. Was Father "
            "Brenner asking him to learn to mean less? The question was not a stereotype of adolescent "
            "defiance; it was, Brenner realized, instrumental in a way the senior brother would never "
            "credit. Jonas was asking, in his sideways manner, what kind of obedience the chapel actually "
            "demanded.\n\n"
            "Brenner kept him. The decision cost him a measure of authority among his peers — some said, "
            "not quite to his face, that he was too decadent in his judgments to lead novices — and he was "
            "not certain, even months later, that he had decided rightly. But he was certain that what he "
            "would have abominated, more than any future scandal Jonas might cause, was the kind of vacant "
            "house the library would have become if every difficult question had been quietly handicapped "
            "out of it."
        ),
        "questions": [
            {
                "q": "The narrator's account of Jonas's apology is structured chiefly to",
                "opts": [
                    "demonstrate that Jonas's contrition is sincere on every point of complaint.",
                    "distinguish a partial moral admission from an unconditional submission to authority.",
                    "show that Jonas has rehearsed an effective defense of his behavior.",
                    "imply that Brenner has underestimated Jonas's diplomatic skill."
                ],
                "ans": 1,
                "why": "Jonas admits only the two cases where he was spiteful and otherwise refuses to retract — the structure of the apology marks a precise distinction between a moral admission and total obedience, which is what then prompts Brenner's deeper question about what obedience requires."
            },
            {
                "q": "Brenner's decision to keep Jonas is best understood as a choice to",
                "opts": [
                    "favor an individual student over the institutional comfort of the chapel.",
                    "test whether his own authority is sufficient to discipline a difficult novice.",
                    "preserve, at some cost to his standing, the chapel's tolerance for unsettling questions.",
                    "rebuke the senior brother who had requested Jonas's removal."
                ],
                "ans": 2,
                "why": "Brenner accepts the loss of authority because what he would have abominated more is a chapel from which difficult questions had been 'quietly handicapped' — i.e. the choice protects an institutional capacity, not just a student."
            },
            {
                "q": "It can be inferred that the senior brother who urged Jonas's removal would most likely characterize Brenner's reasoning as",
                "opts": [
                    "thoughtful but excessively patient with a single student.",
                    "self-indulgent permissiveness disguised as principle.",
                    "an unconscious imitation of the chapel's most demanding teachers.",
                    "a strategic gesture intended to consolidate Brenner's own position."
                ],
                "ans": 1,
                "why": "The senior brother's view is reflected in the line that Brenner was 'too decadent in his judgments to lead novices' — i.e. he would see Brenner's tolerance as self-indulgent permissiveness, not principled defense."
            }
        ]
    },
    {
        "title": "After the Charisma Faded",
        "targets": [
            "charisma","glib","decadent","backhanded","oust","levity","expedite","apathy",
            "downplay","unalloyed","forthcoming","prescient","spiteful","heinous","quash",
            "constrain","prerogative","incumbent","pensive","controversial","extensive",
            "exasperation","cunning","contrite","ignorance"
        ],
        "text": (
            "When the city's most charismatic mayor was finally ousted, the post-mortems were unanimous in "
            "what they identified as his fatal asset. His charisma, the columnists wrote, had not been a "
            "neutral instrument; it had operated as a kind of decadent currency, allowing him to expedite "
            "decisions that, in a less captivating administration, would have provoked extensive debate. "
            "Voters had granted him a long prerogative on the assumption that his glib confidence rested on "
            "private competence. When that competence proved scarce, the same charisma curdled into the "
            "thing they had once forgiven.\n\n"
            "The campaign that finally unseated him was, by any measure, controversial. Its central charge — "
            "that the mayor had quashed an internal report on a heinous procurement scandal — was supported "
            "by two anonymous sources and one document of disputed origin. His allies treated the document "
            "as a forgery, his enemies as prescient evidence; the truth, as is often the case, lay in a "
            "patch of ground neither side wished to occupy. The mayor himself was not forthcoming. He met "
            "the early questions with a backhanded levity that even sympathetic reporters found wearing, "
            "and he met the later, sharper ones with a constrained silence his lawyers had clearly "
            "negotiated.\n\n"
            "What undid him, in the end, was not the document but the apathy of his own base. The voters "
            "who had once defended him with unalloyed loyalty became pensive; their exasperation at being "
            "asked, yet again, to downplay an unflattering story curdled into a quiet refusal. They were "
            "not contrite — most of them, when polled, denied having been wrong to elect him — but they "
            "were no longer willing to expend the social capital that defending him required. A cunning "
            "campaign, his rivals' organizer later said, could not have manufactured such an outcome; she "
            "had merely declined to interrupt it.\n\n"
            "In office, the new mayor was incumbent upon a quieter promise: to be less interesting. She had "
            "campaigned on the apparent paradox that the city was tired enough to find dullness a virtue. "
            "Her first hundred days were criticized by some for their absence of vision and praised by "
            "others for the same reason. Whether her studied colorlessness would, in time, harden into its "
            "own spiteful liability — whether the city's appetite for charisma was only resting — was the "
            "open question, and one her staff was disciplined enough never to discuss in public."
        ),
        "questions": [
            {
                "q": "The passage's central claim about the former mayor's charisma is that it",
                "opts": [
                    "concealed an actual incompetence that voters discovered only late.",
                    "functioned as political credit voters extended in exchange for assumed competence, and collapsed when that assumption did.",
                    "made him unusually vulnerable to opposition campaigning.",
                    "was misread by the press as a substitute for substantive policy."
                ],
                "ans": 1,
                "why": "The opening paragraph frames charisma as 'decadent currency' that voters granted on the assumption of private competence; when competence proved scarce, the same charisma 'curdled' — the claim is about extended credit, not concealment per se."
            },
            {
                "q": "The rival organizer's remark in the third paragraph (\"a cunning campaign... could not have manufactured such an outcome\") most strongly implies that",
                "opts": [
                    "her campaign was, in fact, more cunning than she publicly admitted.",
                    "the mayor's defeat owed more to his base's exhaustion than to any opposition strategy.",
                    "the document of disputed origin was the decisive factor in the election.",
                    "voters were ultimately persuaded by the new mayor's policy proposals."
                ],
                "ans": 1,
                "why": "She credits her side only with 'declining to interrupt' the base's exhaustion — i.e. the outcome was endogenous to the mayor's coalition, not engineered by the rival."
            },
            {
                "q": "The author's tone in the final paragraph, regarding the new mayor's 'studied colorlessness,' is best described as",
                "opts": [
                    "approving, suggesting that her caution is the correct corrective to her predecessor's flaws.",
                    "skeptical, treating her dullness as a strategy whose durability is genuinely uncertain.",
                    "dismissive, implying that her early performance is too thin to merit serious discussion.",
                    "alarmed, predicting that her quiet style will permit hidden abuses."
                ],
                "ans": 1,
                "why": "The author calls her colorlessness 'studied' (deliberate, not principled), notes the mixed early reviews, and explicitly leaves open whether the city's appetite for charisma is only 'resting' — skepticism without commitment."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 18
# ---------------------------------------------------------------------------
NEW["18"] = [
    {
        "title": "The Lucid Surgeon",
        "targets": [
            "assiduous","lucid","unflappable","vertiginous","magnanimous","recondite","peruse",
            "engrossing","artful","limpid","ductile","cryptic","elude","enlighten","mar",
            "scathing","sweeping","sectarian","analytical","futile","prying","contemptuous",
            "vulnerable","absurd","minute"
        ],
        "text": (
            "Dr. Akemi Saito was famously assiduous about her notes. She perused every operative report — "
            "her own, her colleagues', the apocryphal old logs the chief still kept under his desk — with "
            "the patience of a textual scholar and the temperament of an unflappable air-traffic "
            "controller. To her residents she was lucid almost to a fault. A vertiginous case she had "
            "described to me once — an artery torn in a place the standard atlas did not name — she walked "
            "through afterward in such limpid sequence that the recondite anatomy seemed, briefly, ductile "
            "in her hands.\n\n"
            "What made her instruction engrossing was not her command of the cryptic — most senior surgeons "
            "had that — but her refusal to mar a lesson by pretending difficulty had eluded her on the "
            "table. She would tell her residents, plainly, the exact second at which she had been afraid. "
            "She enlightened them, in other words, by being precise about her own vulnerability. It struck "
            "me as an artful pedagogy: an analytical surgeon could afford, perhaps, the magnanimous "
            "admission, because the underlying technique was secure.\n\n"
            "Her one quarrel with the department was a sweeping one. She thought the morbidity conferences "
            "had drifted from analysis into a kind of sectarian theater. The room was eager to issue "
            "scathing assessments of decisions made in seconds, contemptuous of the prying retrospective "
            "questions a calmer review would have spared. To rebuild the conferences, she argued, would "
            "not be futile; it would only require that the senior surgeons agree, in advance, to discuss "
            "the most minute branching points of their reasoning rather than the absurd general lessons "
            "the room preferred.\n\n"
            "The reform she proposed was modest and, predictably, not adopted. What was adopted — quietly, "
            "by her own residents — was the practice itself. Within two years a recognizable cohort had "
            "spread to other hospitals, all of them, when pressed, admitting fear in the operating room "
            "with a precision that bewildered their elders. The chief told her this once, half-jokingly, "
            "as a complaint. She received the joke as she received praise: with the unflappable courtesy "
            "of someone who had already considered the case from several angles and was not, at the "
            "moment, particularly interested in any of them."
        ),
        "questions": [
            {
                "q": "Saito's pedagogy, as the passage describes it, depends most directly on which of the following commitments?",
                "opts": [
                    "A belief that surgical technique is best learned by close imitation of senior practitioners.",
                    "A willingness to identify, in retrospect, the precise moments at which her own judgment was uncertain.",
                    "An insistence that residents memorize a sweeping body of recondite anatomical detail.",
                    "A conviction that morbidity conferences must reach consensus before a case is closed."
                ],
                "ans": 1,
                "why": "The passage locates her distinctive method in her telling residents 'the exact second at which she had been afraid' — pedagogical leverage from precise self-disclosure, not imitation, memorization, or consensus."
            },
            {
                "q": "The passage suggests that Saito's objection to the morbidity conferences rests on the view that the conferences",
                "opts": [
                    "fail to hold senior surgeons accountable for their errors.",
                    "substitute a kind of group performance for fine-grained analysis of the reasoning behind decisions.",
                    "rely too heavily on retrospective documentation rather than firsthand observation.",
                    "favor experienced surgeons at the expense of residents."
                ],
                "ans": 1,
                "why": "She calls the conferences 'sectarian theater' — scathing, contemptuous, drifting from analysis — and proposes returning them to discussion of 'the most minute branching points of reasoning,' opposing performance to fine-grained analysis."
            },
            {
                "q": "The final paragraph's closing description of Saito's reaction to the chief is most plausibly intended to convey her",
                "opts": [
                    "indifference to whether her reforms have institutional standing.",
                    "irritation at being teased about a serious professional dispute.",
                    "modest hope that the chief will yet reverse his earlier decision.",
                    "satisfaction at having outmaneuvered the senior surgeons politically."
                ],
                "ans": 0,
                "why": "She receives the joke with the same composure as praise, having 'already considered the case from several angles and was not, at the moment, particularly interested in any of them' — i.e. she has detached from the institutional question, having already won the practical one."
            }
        ]
    },
    {
        "title": "The Effusive Critic",
        "targets": [
            "effusive","scathing","formulaic","caricature","opinionated","melodious","florid",
            "magnanimous","abrogate","pendulum","nullify","tantalize","tawdry","zealot",
            "albeit","persist","slumberous","absurd","engrossing","prestige","futile",
            "petty","detritus","contemptuous","vibrant"
        ],
        "text": (
            "The theater critic Donal Briggs had, in his middle years, developed a public reputation for "
            "effusive enthusiasm. The pendulum of his career, his enemies liked to say, had swung so far "
            "from his early scathing reviews that the two periods could not have been written by the same "
            "man. The truth was less melodious. Briggs's praise, when it came, was as opinionated as his "
            "censure had been; he had merely refined it into a more florid instrument.\n\n"
            "What he refused to do, persistently, was the formulaic notice. He would not summarize a plot, "
            "rank a season's productions, or commit the petty caricature of a performance for the sake of "
            "a quotable line. A review in his hand was an essay, sometimes engrossing, sometimes — by his "
            "own admission — absurd in its proportions: three hundred words on a single piece of staging, "
            "and a single sentence on the lead actor's performance, when the lead had not interested him. "
            "Editors who tried to abrogate this practice found the result, in his draft, magnanimous "
            "compliance up to the last comma and then a fresh, slumberous evasion of the very edit they "
            "had requested.\n\n"
            "The prestige of his column did not nullify the complaints. A theater whose new production he "
            "had ignored could feel the silence as a tawdry kind of judgment; a young actor on whom he "
            "spent two unflattering paragraphs might find his career briefly tantalized by an offer or two "
            "and then, just as briefly, abandoned. Briggs was unmoved. He treated the consequences of his "
            "writing as a kind of detritus that other people were welcome to pick over.\n\n"
            "He was not, however, a zealot. Late in his career he wrote a vibrant, almost contrite essay "
            "about a production he had savaged twenty years earlier and now believed he had misread. The "
            "essay was not, in the end, futile. It did not undo the original review, but it offered "
            "younger critics a model — albeit a contemptuous one toward the conventions of the form — of "
            "how a critic might revise himself in public. A review of a play is finished, Briggs wrote, "
            "when the play closes; a critic is finished only when he refuses, for the last time, to look "
            "again."
        ),
        "questions": [
            {
                "q": "The passage characterizes Briggs's later, effusive period as",
                "opts": [
                    "a reversal of the convictions that informed his earlier scathing reviews.",
                    "an extension of his earlier severity by other rhetorical means.",
                    "a concession to the editorial pressures of his middle career.",
                    "a sentimental softening that he later came to regret."
                ],
                "ans": 1,
                "why": "The passage explicitly denies the reversal reading ('the truth was less melodious') and says his praise was 'as opinionated as his censure had been' — i.e. continuity, refined into a different instrument."
            },
            {
                "q": "The third paragraph's description of Briggs's treatment of his reviews' consequences (\"a kind of detritus that other people were welcome to pick over\") most strongly suggests that he",
                "opts": [
                    "regretted his earlier reviews but was unwilling to publish corrections.",
                    "regarded the downstream careers of his subjects as outside his proper responsibility.",
                    "was secretly pleased by the harm his unflattering reviews could cause.",
                    "considered his column too marginal to influence professional outcomes."
                ],
                "ans": 1,
                "why": "The metaphor of detritus separates what he produces from what others make of it — a deliberate refusal of responsibility for downstream effects, not regret, malice, or modesty."
            },
            {
                "q": "Which of the following is most consistent with the principle Briggs offers in the passage's closing sentence?",
                "opts": [
                    "A critic should withhold judgment until a production has closed.",
                    "A critic should publish revised judgments of past work whenever new evidence emerges.",
                    "A critic should treat any of his own past judgments as eligible for revision so long as he is still working.",
                    "A critic should retire when he can no longer write with conviction."
                ],
                "ans": 2,
                "why": "Briggs's distinction is between the finished play (closed when it closes) and the finished critic (closed only when he refuses to revise) — i.e. the live duty is permanent eligibility to re-read his own past work, not a duty to publish revisions in any particular case."
            }
        ]
    },
    {
        "title": "Vertigo at the Confluence",
        "targets": [
            "engrossing","confluence","anthropogenic","detritus","cryptic","vertiginous",
            "veer","unearth","mar","scathing","sweeping","futile","persist","analytical",
            "expel","pessimistic","reparation","molder","peer","incursion","entreat",
            "concede","caricature","sever","clamorous"
        ],
        "text": (
            "From the bluff above the confluence the river looked, as my guide Wren described it, "
            "engrossing in the way an old wound is engrossing: it would not let you stop looking. The "
            "anthropogenic detritus — bottles, plastic netting, the cryptic husks of upstream packaging — "
            "had collected in a slow eddy where the two currents met. It veered when the wind veered, and "
            "from a hundred meters up it gave the unsettling impression that the water itself was "
            "rearranging the trash into legible shapes.\n\n"
            "Wren was a research ecologist and an analytical one; he disliked the vertiginous metaphors "
            "his discipline had begun to attract. The river, he said, was not a wound and it was not a "
            "patient. To unearth a useful account of what had happened to it required peering at boring "
            "things — sediment cores, twenty years of mediocre monitoring data, the unloved minutes of a "
            "regional water board. He had written a scathing review of a recent book that, in his view, "
            "had marred a serious case for reparation with sweeping rhetoric the actual evidence did not "
            "support.\n\n"
            "He was not, however, a pessimist. The river was no longer the unbroken bowl of clamorous "
            "industrial discharge it had been in his father's photographs; an incursion of stricter "
            "regulation in the late nineties had expelled the worst offenders, and the most cryptic "
            "molders of the old sediment had, in the absence of new input, slowly begun to break down. To "
            "concede that some kinds of restoration were genuinely working, Wren said, was not to "
            "caricature the remaining damage as solved.\n\n"
            "I asked him whether it was futile to entreat the public to care about a recovery whose "
            "evidence was so dispersed. He thought about this a long time. The mistake, he said finally, "
            "was to imagine that severing the public's attention from the river — letting the trade press "
            "and the regulators carry on alone — would persist as a tenable strategy. The river had once "
            "been a public possession in a clamorous and ugly way, and would need to be one again, in some "
            "quieter and more analytical way, if the slow good work the last two decades had begun was not "
            "to molder for lack of witnesses."
        ),
        "questions": [
            {
                "q": "Wren's objection to the recent book he reviewed is most precisely that the book",
                "opts": [
                    "advocated for restoration policies that the evidence does not support.",
                    "diluted a defensible argument by relying on rhetoric the underlying evidence could not bear.",
                    "ignored the contribution of regulation to the river's partial recovery.",
                    "treated the river as a symbol rather than as an ecosystem."
                ],
                "ans": 1,
                "why": "Wren says the book 'marred a serious case for reparation with sweeping rhetoric the actual evidence did not support' — the case itself is sound; the failure is rhetorical overreach that endangers it."
            },
            {
                "q": "Wren's reasoning in the passage relies on which of the following distinctions?",
                "opts": [
                    "Between scientific evidence and public opinion.",
                    "Between conceding partial success and minimizing remaining damage.",
                    "Between the river's ecological state and its symbolic value.",
                    "Between local restoration efforts and federal regulatory policy."
                ],
                "ans": 1,
                "why": "He insists that admitting that some restoration is working 'was not to caricature the remaining damage as solved' — the load-bearing distinction is between honest concession and dismissive minimization."
            },
            {
                "q": "It can be inferred from Wren's final remarks that he regards continued public attention to the river as",
                "opts": [
                    "a sentimental indulgence the discipline should learn to do without.",
                    "a practical condition for sustaining the unglamorous, slow work of recovery.",
                    "a regulatory matter properly handled by the water board.",
                    "a duty owed to the river itself, independent of any practical effect."
                ],
                "ans": 1,
                "why": "He warns that severing public attention is not 'a tenable strategy' and that the slow good work would 'molder for lack of witnesses' — public attention is treated instrumentally, as the condition for sustaining the work."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 19
# ---------------------------------------------------------------------------
NEW["19"] = [
    {
        "title": "The Itinerant Bishop",
        "targets": [
            "bishop","baroque","multitudinous","evangelist","motley","splendor","seclusion",
            "stilted","sermon","disseminate","sacrifice","prophetic","canonical","castigate",
            "ascetic","compunction","propitious","derelict","betray","leak","bemoan",
            "innocuous","duplicity","modulate"
        ],
        "text": (
            "Bishop Aldis had, in his youth, been an evangelist of an unfashionable kind. He had peregrinated "
            "from one provincial diocese to another, preaching in barns and market squares to congregations "
            "so motley that no two services were alike. The baroque splendor of the cathedral towns made him, "
            "in those years, slightly impatient; he distrusted the multitudinous embellishments by which the "
            "established church seemed to him to disseminate not so much its message as its self-regard. He "
            "called himself, then, an ascetic, and the church called him, when it called him anything, "
            "derelict in his duties.\n\n"
            "His elevation to a bishopric had not, his old friends complained, been propitious for those "
            "convictions. The man who had once castigated cathedral choirs for their stilted Latin now "
            "presided over them; the man who had bemoaned the duplicity of canonical commentary now "
            "produced his own canonical edition of a minor church father. The sermons he preached in his "
            "new robes were innocuous compared to what he had once thundered in barns. To his enemies the "
            "modulation of his style was a kind of leak — convictions slowly draining from a vessel that no "
            "longer needed them — and even his closest friends struggled to defend it as a sacrifice "
            "rather than a betrayal.\n\n"
            "Aldis himself did not pretend, in private, that the change had been costless. He kept, in a "
            "battered notebook, a list of the convictions he had set aside, with the year and the "
            "circumstance of each. The list was not, he said, an act of seclusion or self-castigation; it "
            "was simply the bookkeeping any honest officeholder would do, were he willing.\n\n"
            "Whether he had become prophetic in his new office or merely useful was a question that "
            "outlived him. The official church remembered him as an able administrator who had stabilized "
            "the cathedral's finances and disseminated, in his own modulated way, the gentler doctrines "
            "for which the postwar years were hungry. The barns remembered, where they remembered him at "
            "all, a different man: a younger preacher whose voice had carried across a damp field and "
            "whose later compunction about that voice the barns could not quite forgive."
        ),
        "questions": [
            {
                "q": "The passage's portrait of Aldis is best described as",
                "opts": [
                    "an affirmation that institutional advancement requires the abandonment of principle.",
                    "a presentation of a single life as differently legible from two incompatible vantage points.",
                    "a defense of the established church against the criticisms of its evangelical wing.",
                    "a lament for the disappearance of the barn-preaching tradition."
                ],
                "ans": 1,
                "why": "The closing paragraph explicitly leaves the question of whether Aldis became 'prophetic' or 'merely useful' to two different communities — the official church and the barns — each of which sees him truly but partially; the structure is dual perspective, not univocal verdict."
            },
            {
                "q": "Aldis's notebook of set-aside convictions functions in the passage chiefly to",
                "opts": [
                    "prove that his transformation was insincere.",
                    "qualify the charge of betrayal by showing that he tracked, rather than denied, what he had given up.",
                    "demonstrate that his early convictions had been arbitrary.",
                    "suggest that he intended to return to his early views in retirement."
                ],
                "ans": 1,
                "why": "Aldis frames the notebook as 'bookkeeping' — neither penance nor display, but honest tracking — which complicates the friends' simpler charge of betrayal by inserting a layer of acknowledged cost."
            },
            {
                "q": "The phrase \"a leak — convictions slowly draining from a vessel that no longer needed them\" most precisely conveys his enemies' view that",
                "opts": [
                    "his early convictions had been forcibly suppressed by the institutional church.",
                    "his change of style reflects a gradual loss of beliefs whose disappearance institutional office made painless.",
                    "his later sermons concealed convictions he privately still held.",
                    "his finances rather than his beliefs had driven his elevation."
                ],
                "ans": 1,
                "why": "The image is of slow, passive loss — not suppression, concealment, or financial motive — combined with the cynical suggestion that institutional comfort made the loss easy."
            }
        ]
    },
    {
        "title": "The Pamphleteer's Castigation",
        "targets": [
            "rapacious","opprobrium","castigate","polemic","disseminate","disconcert","grotesque",
            "audacious","ethical","comply","abstruse","reiterate","obligatory","outright",
            "qualify","disavow","attenuate","exculpate","cronyism","duplicity","slipshod",
            "incompatible","exponent","propitious"
        ],
        "text": (
            "Ines Vallejos's pamphlets were rapacious in their appetite for opprobrium. To read one was to "
            "find oneself, within three paragraphs, ushered into a courtroom whose verdict had already been "
            "drafted. She castigated her targets with such confident polemic that her early admirers liked "
            "to call her audacious; her later critics, with equal accuracy, called her obligatory.\n\n"
            "She was, in fairness, not slipshod. The pamphlets disseminated a great deal of accurate detail "
            "about cronyism in the municipal contracting office, and the duplicity she exposed was real. "
            "What disconcerted her sympathetic readers — including, eventually, her own publisher — was "
            "the grotesque uniformity of her tone. Every official was rapacious; every contract was "
            "outright fraud; every defense was complied with the most abstruse self-interest. There was no "
            "case, in the entire run of pamphlets, in which she had reiterated a charge with any "
            "qualification, or attenuated a conclusion even slightly when the evidence demanded it.\n\n"
            "When her publisher finally asked her to disavow a particular accusation that had not held up "
            "under closer examination, Vallejos refused. To qualify the charge, she argued, would be to "
            "exculpate not only that individual but the broader system she had been documenting; the "
            "ethical demand of her project was incompatible with the ordinary scruples of correction. Her "
            "publisher, who had been an exponent of her work for nearly a decade, replied that the demand "
            "was not ethical but rhetorical: she had built a polemic that could not absorb a retraction "
            "without losing the propitious force on which her other claims depended.\n\n"
            "The disagreement broke their partnership. Vallejos took her pamphlets to a smaller press and "
            "continued to publish; her audience, narrower now, was also more credulous. Her former "
            "publisher, in a careful interview some years later, said that he had learned from the episode "
            "the difficult truth that a polemicist's most rapacious enemy is not the rapacious official "
            "she opposes but the structure of her own argument, which after a certain point begins to "
            "require, for its own survival, exactly the kind of moral simplicity that ought to disqualify "
            "it from serious work."
        ),
        "questions": [
            {
                "q": "The publisher's response to Vallejos in the third paragraph turns on which of the following distinctions?",
                "opts": [
                    "Between accurate reporting and effective polemic.",
                    "Between an ethical refusal to retract and a rhetorical inability to retract without structural cost.",
                    "Between a public correction and a private one.",
                    "Between Vallejos's personal convictions and her commercial interests."
                ],
                "ans": 1,
                "why": "He reframes her 'ethical' refusal as a rhetorical necessity: her polemic 'could not absorb a retraction' without losing its force — i.e. the refusal is structurally forced, not principled."
            },
            {
                "q": "The passage's overall judgment of Vallejos's project is best described as",
                "opts": [
                    "an endorsement of her exposures, with regret about the tone that made them possible.",
                    "a dismissal of her work as factually unreliable.",
                    "a defense of polemical writing against the timidity of mainstream publishers.",
                    "an indictment of municipal cronyism that uses Vallejos as a sympathetic example."
                ],
                "ans": 0,
                "why": "The narrator concedes that the cronyism and duplicity she exposed were real and that she was not slipshod, while diagnosing the rhetorical structure that made her unable to retract — endorsement of substance, regret about form."
            },
            {
                "q": "The final paragraph's claim about \"the polemicist's most rapacious enemy\" is best paraphrased as",
                "opts": [
                    "Polemicists ultimately undermine themselves through compromise with their targets.",
                    "Polemicists become hostage to a stylistic and argumentative structure that requires moral oversimplification to survive.",
                    "Polemicists eventually attract the hostility of those they once allied with.",
                    "Polemicists overestimate the corruption of the institutions they attack."
                ],
                "ans": 1,
                "why": "The line names the enemy as the 'structure of her own argument,' which after a point requires the 'moral simplicity that ought to disqualify it from serious work' — i.e. the threat is internal and structural, not external."
            }
        ]
    },
    {
        "title": "The Quizzical Naturalist",
        "targets": [
            "quizzical","juxtapose","ossify","propitious","abstruse","inscrutable","intangible",
            "modulate","prophetic","disseminate","shrewd","meander","presuppose","intriguing",
            "demur","castigate","enigmatic","comply","reiterate","ascetic","abstruse",
            "amorphous","attenuate","derelict"
        ],
        "text": (
            "Dr. Phelan was a naturalist of the quizzical school. He juxtaposed, in his small museum, "
            "specimens of an obvious kinship beside others whose relation was inscrutable, and invited his "
            "visitors to puzzle out what, if anything, connected them. The arrangement struck some as "
            "intriguing and others as derelict; a particularly shrewd local critic, having meandered through "
            "the rooms one Sunday, called the museum an essay disguised as a collection.\n\n"
            "Phelan accepted the description. He had no wish, he said, for his classification to ossify "
            "into the propitious chart that visiting schoolchildren could memorize and forget. The intangible "
            "thing he wanted to disseminate was not a set of facts but a habit — the habit of asking what "
            "an animal's resemblance to another animal could and could not be taken to prove.\n\n"
            "His critics, more orthodox in their methods, were less amorphous in their objections. The "
            "museum, they complained, presupposed visitors already capable of the analysis it sought to "
            "induce. It made an abstruse demand of the unprepared. One reviewer castigated Phelan for "
            "modulating his labels into outright riddles; another, more sympathetic, demurred only on the "
            "ground that some visitors would attenuate the puzzle by simply guessing, and that the "
            "guesses, repeated, would in time ossify into a folklore the museum had unintentionally "
            "produced.\n\n"
            "Phelan reiterated, in a long and almost prophetic essay, his case for the design. The museums "
            "his critics preferred — the ones with confident dioramas and inscrutable interior politics — "
            "were producing, he argued, a generation of visitors who mistook the absence of doubt for the "
            "presence of knowledge. To comply with that taste would be to disseminate the very habit he "
            "had built his small institution to attenuate. The essay was admired, predictably, by people "
            "who already agreed with him, and ignored by those who did not. He took both responses, with "
            "the equanimity of an ascetic, as further evidence that his enigmatic museum was doing exactly "
            "the work it was meant to do."
        ),
        "questions": [
            {
                "q": "Phelan's stated aim in arranging his museum is best described as",
                "opts": [
                    "to demonstrate the limits of contemporary taxonomic methods.",
                    "to cultivate in visitors a disposition to weigh the evidentiary force of resemblance.",
                    "to entertain visitors with puzzles whose solutions he privately knows.",
                    "to attract the patronage of more orthodox natural-history institutions."
                ],
                "ans": 1,
                "why": "Phelan describes the 'intangible thing' he wants to disseminate as a habit — 'the habit of asking what an animal's resemblance to another animal could and could not be taken to prove' — i.e. a disposition about evidence, not a taxonomic critique."
            },
            {
                "q": "The more sympathetic critic's objection (\"some visitors would attenuate the puzzle by simply guessing...\") rests on the worry that",
                "opts": [
                    "Phelan's labels are factually inaccurate.",
                    "the museum's open-ended design risks generating a stable folk knowledge that Phelan never intended.",
                    "visitors will damage specimens while trying to examine them more closely.",
                    "Phelan's essay will be misread by his orthodox colleagues."
                ],
                "ans": 1,
                "why": "The critic's concern is that repeated guesses 'would in time ossify into a folklore the museum had unintentionally produced' — the design's openness has an unintended downstream effect."
            },
            {
                "q": "Phelan's response to the public reaction to his essay (\"admired... by people who already agreed with him, and ignored by those who did not\") most directly implies that he",
                "opts": [
                    "considers the public debate over his museum to be settled in his favor.",
                    "interprets the polarized reception as evidence that the institution is performing its intended function.",
                    "is disappointed that his orthodox critics did not engage with his arguments.",
                    "regards his essay as a final statement and intends to retire."
                ],
                "ans": 1,
                "why": "He treats both responses 'as further evidence that his enigmatic museum was doing exactly the work it was meant to do' — i.e. the polarization is itself diagnostic, not a defeat or vindication in the usual sense."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 20
# ---------------------------------------------------------------------------
NEW["20"] = [
    {
        "title": "The Voluble Lecturer",
        "targets": [
            "voluble","succinct","comprehensive","polymath","prolix","diverting","tentative",
            "obtrusive","draconian","empirical","ephemeral","unrelenting","extraordinary",
            "rhetorical","palpable","banter","comical","echo","persevere","poise",
            "sanction","unfounded","level-headed","trivial","tedious"
        ],
        "text": (
            "Professor Halpern was famously voluble. A polymath by training and a prolix one by habit, he "
            "could spend a full ninety minutes on a single tentative remark a student had made at the "
            "previous week's seminar — quoting it, paraphrasing it, banter-ing with its imagined "
            "implications, and finally subjecting it to a comprehensive critique no one in the room could "
            "have predicted. The lectures were exhausting and diverting in roughly equal proportion. "
            "Students kept attending for the comical certainty that one of them, at some unguarded "
            "moment, would supply the next week's text.\n\n"
            "His critics in the department thought the method ephemeral and obtrusive. It produced, they "
            "said, no comprehensive body of doctrine students could carry away; it asked them to "
            "persevere through nine weeks of unrelenting digression for the sake of a few extraordinary "
            "afternoons. Halpern's reply, when he bothered to give one, was that the most palpable thing "
            "he had to teach was not a syllabus but a way of being level-headed in the face of one's own "
            "half-formed thoughts.\n\n"
            "The chair's draconian solution, in his second term as chair, was to sanction Halpern's "
            "courses with a new requirement that every seminar produce a succinct, written summary at the "
            "end of each term. Halpern complied — he was not, on procedural matters, unfounded in his "
            "respect for the chair — and the summaries became, predictably, a small genre of their own. "
            "Each was a parody of the form, technically succinct and rhetorically subversive, echoing the "
            "term's actual content the way a polite letter echoes an argument it is trying to avoid.\n\n"
            "What no one in the department had quite anticipated was that the summaries became the only "
            "documents of Halpern's teaching to outlast him. After his retirement, the seminars echoed in "
            "memory and on the corridors; on paper, only the trivial little summaries survived. Visiting "
            "scholars who had never sat in the room mistook them, reasonably, for evidence of a tedious "
            "and over-structured course. His former students found this funny, in a way they did not "
            "always succeed in explaining. The empirical record, one of them told me, had been written by "
            "the very procedure the lectures had spent ten years training her not to trust."
        ),
        "questions": [
            {
                "q": "The passage's central irony, developed in its final paragraph, is that",
                "opts": [
                    "Halpern's retirement coincided with the decline of his preferred teaching method.",
                    "the documents that survived Halpern misrepresent the teaching they were imposed to discipline.",
                    "Halpern's students remained loyal to him despite the chair's interventions.",
                    "the chair's procedural reforms unexpectedly enhanced Halpern's reputation."
                ],
                "ans": 1,
                "why": "The closing observation is that the surviving 'empirical record' was produced by 'the very procedure the lectures had spent ten years training her not to trust' — the surviving documents systematically misrepresent the teaching they were meant to constrain."
            },
            {
                "q": "Halpern's compliance with the chair's requirement is best characterized as",
                "opts": [
                    "outright defiance dressed in procedural form.",
                    "genuine acceptance of the legitimacy of the chair's authority.",
                    "literal compliance whose execution undermined the requirement's intent.",
                    "reluctant cooperation that produced documents he privately disowned."
                ],
                "ans": 2,
                "why": "The summaries are 'technically succinct and rhetorically subversive' — Halpern executes the letter of the requirement in a way that defeats its purpose, which is neither outright defiance nor genuine acceptance."
            },
            {
                "q": "Halpern's reply to his critics (\"the most palpable thing he had to teach...\") most precisely defends his method on the ground that",
                "opts": [
                    "comprehensive doctrine cannot be conveyed within the constraints of a single term.",
                    "the proper goal of teaching is a disposition toward one's own thought, not a transferable body of knowledge.",
                    "students learn most effectively when their own remarks become the seminar's text.",
                    "the discipline's existing curricula are too rigid to produce competent scholars."
                ],
                "ans": 1,
                "why": "He claims his real subject is 'a way of being level-headed in the face of one's own half-formed thoughts' — a stance toward one's own thinking, not curricular content or pedagogical technique per se."
            }
        ]
    },
    {
        "title": "The Penitent Editor",
        "targets": [
            "penitent","ephemeral","dissipate","lethargic","prevaricate","emendation","apology",
            "bequeath","grant","soothe","plague","meretricious","absolute","befuddle","delude",
            "tentative","heartrending","comprehensive","grave","stomach","unfounded","sanction",
            "trivial","unrelenting","obtrusive"
        ],
        "text": (
            "The editor's apology, when it finally came, was penitent in tone and ephemeral in its actual "
            "admissions. He regretted, he wrote, the lethargic editorial process that had allowed the "
            "essay to appear with several emendations he had failed to verify; he regretted also that the "
            "magazine had prevaricated, in earlier responses, about whether the original draft had been "
            "altered without the writer's knowledge. He did not, however, grant the more grave charge — "
            "that the alterations had not been clerical mistakes at all but soothing edits designed to "
            "spare a powerful subject the unrelenting force of the writer's actual conclusion.\n\n"
            "The writer, when shown the apology in advance, found it heartrending in a way she had not "
            "expected. It was easier, somehow, to stomach an outright denial than this comprehensive "
            "expression of regret that befuddled the actual question. The apology did not delude her, but "
            "she suspected it would delude others; the lethargic public memory of such episodes was its "
            "own kind of meretricious gift, the absolute fairness of a press conference dissipated within "
            "a week into a vague impression that everyone involved had behaved roughly as well as could be "
            "expected.\n\n"
            "She declined to sign the joint statement the editor proposed. To do so, she wrote in a reply "
            "she did not send for two days, would be to bequeath to future readers a sanctioned version of "
            "events that suppressed the only emendation that mattered. Her actual reply, when she sent "
            "it, was three sentences long and contained no rhetoric at all. She listed the precise lines "
            "that had been changed and the names of the people who had requested the changes, and noted, "
            "tentatively, that the magazine was welcome to print her letter alongside any apology it "
            "chose.\n\n"
            "The magazine did not print the letter. The episode plagued the editor for some years and then "
            "dissipated, as such episodes do, into the journalism schools' case files. The writer found "
            "her own assessment confirmed in the trivial obtrusive way that such things are usually "
            "confirmed: by the unfounded grateful remarks of strangers at parties who told her, almost "
            "without exception, how impressed they had been by the magazine's grave and complete handling "
            "of an unfortunate mistake."
        ),
        "questions": [
            {
                "q": "The writer's central objection to the editor's apology is that it",
                "opts": [
                    "is too brief to address the seriousness of the alterations.",
                    "concedes peripheral procedural failings in order to evade the central substantive charge.",
                    "names individuals who had requested the changes without their consent.",
                    "exposes confidential editorial deliberations to public view."
                ],
                "ans": 1,
                "why": "The apology regrets process and earlier prevarication but withholds the 'more grave charge' — that the edits were substantive and protective, not clerical. The objection is precisely this displacement from substance to procedure."
            },
            {
                "q": "The writer's decision to send a three-sentence reply rather than a longer rebuttal is best understood as a judgment that",
                "opts": [
                    "rhetorical argument would be ineffective against a determined magazine.",
                    "an unornamented record of facts was less easily absorbed into the magazine's preferred narrative.",
                    "she lacked the standing to challenge a senior editor directly.",
                    "she wished to preserve the possibility of further work with the magazine."
                ],
                "ans": 1,
                "why": "She fears that signing a joint statement would 'bequeath... a sanctioned version of events'; her chosen reply is unrhetorical and itemized, designed to resist absorption rather than to win an argument."
            },
            {
                "q": "The closing paragraph's account of \"the unfounded grateful remarks of strangers at parties\" functions chiefly to",
                "opts": [
                    "contrast the writer's bitterness with the public's reasonable equanimity.",
                    "illustrate the very meretricious public memory the writer had earlier predicted.",
                    "suggest that the writer's reading of the apology was, in retrospect, mistaken.",
                    "introduce a new and unrelated set of acquaintances into the writer's life."
                ],
                "ans": 1,
                "why": "The strangers' praise of the magazine's 'grave and complete handling' confirms the writer's earlier prediction that the public memory would dissipate into a flattering vague impression — i.e. it instantiates the meretricious mechanism she had named."
            }
        ]
    },
    {
        "title": "The Draconian Reform",
        "targets": [
            "draconian","doctrinaire","complacent","sanction","palpable","unfounded","apocalypse",
            "bedrock","prevaricate","unrelenting","comprehensive","tentative","timely","empirical",
            "infuriate","self-righteous","insular","minimize","paucity","exotic","detect",
            "imminent","dire","discretionary","grant"
        ],
        "text": (
            "The reform package the new commissioner introduced was, by any reasonable measure, draconian. "
            "It eliminated nine discretionary categories of overtime, imposed comprehensive monitoring on "
            "two field offices that had operated with palpable autonomy for thirty years, and reduced the "
            "paucity of inspections to which the department's smaller subsidiaries had grown complacent. "
            "It was, depending on whom one asked, either a timely correction to an insular culture or a "
            "doctrinaire imposition that minimized the empirical complexity of the work.\n\n"
            "The case for the reform rested on a single, well-documented finding: the rate of "
            "uninvestigated complaints had grown, over a decade, to a level the commissioner described as "
            "an imminent and exotic disaster — not yet a public apocalypse, but the kind of bedrock "
            "structural weakness that, in comparable agencies, had preceded one. Her critics did not deny "
            "the finding. They argued, rather, that the reforms her staff had drafted in response were "
            "unfounded in any operational understanding of the work that produced the backlog. To "
            "sanction the field offices, they said, was to prevaricate about the actual cause, which lay "
            "in budgetary cuts the commissioner herself could not undo.\n\n"
            "What infuriated the commissioner about this objection was less its substance than its "
            "self-righteous form. The same critics had been silent during the decade of paucity her "
            "reforms now addressed; their unrelenting concern for the dignity of the field offices had "
            "developed, with suspicious timing, only after she had detected a dire pattern in the numbers. "
            "She granted, in private, that the reforms were imperfect — that some of the more tentative "
            "monitoring provisions might in time prove counterproductive — but she refused, in public, to "
            "minimize the underlying finding for the sake of a more comfortable rollout.\n\n"
            "A year after the reforms took effect, the backlog had measurably dropped. The two field "
            "offices, predictably, hated the new oversight; some of their staff resigned, and a small "
            "number of complaints that the older system would have buried now reached the press in raw "
            "and embarrassing form. Whether the reforms had been doctrinaire or comprehensive depended, "
            "the commissioner remarked in an interview, on which of the two stories about her tenure one "
            "had already decided to believe."
        ),
        "questions": [
            {
                "q": "Which of the following best describes the structure of the commissioner's critics' position as presented in the passage?",
                "opts": [
                    "They reject both the commissioner's diagnosis and her proposed reforms.",
                    "They accept the diagnosis but contend that the reforms misidentify the operational cause of the problem.",
                    "They argue that the reforms exceed the commissioner's statutory authority.",
                    "They insist that the diagnosis itself was manufactured to justify a preexisting agenda."
                ],
                "ans": 1,
                "why": "The second paragraph explicitly says the critics 'did not deny the finding' and instead claim the reforms are 'unfounded in any operational understanding' — i.e. shared diagnosis, dispute about the remedy."
            },
            {
                "q": "The commissioner's reasoning about her critics relies most heavily on which of the following inferences?",
                "opts": [
                    "That silence during a problem's incubation undermines the credibility of objections raised only after a corrective intervention.",
                    "That her critics had been influenced by donors to the field offices.",
                    "That operational expertise should not constrain executive judgment about institutional priorities.",
                    "That budget cuts cannot have caused the backlog because the cuts predated the backlog."
                ],
                "ans": 0,
                "why": "Her objection to the critics is about timing: they were silent during the decade of paucity and developed concern only once she acted — the inference being that the timing discredits their stated motive."
            },
            {
                "q": "The commissioner's closing remark (\"depended... on which of the two stories about her tenure one had already decided to believe\") is best read as",
                "opts": [
                    "a candid acknowledgment that the empirical record cannot adjudicate the dispute.",
                    "a tactical refusal to take responsibility for the resignations her reforms had caused.",
                    "a rhetorical concession designed to flatter both sides of the debate.",
                    "an admission that the underlying diagnosis was less certain than she had earlier suggested."
                ],
                "ans": 0,
                "why": "She has just noted both a measured success (the backlog dropped) and a cost (resignations, embarrassing complaints reaching the press); her remark observes that the same record reads differently depending on the prior narrative, an acknowledgment that evidence alone will not settle the assessment."
            }
        ]
    },
]


# ---------------------------------------------------------------------------
# Merge and write
# ---------------------------------------------------------------------------
def main():
    existing = json.loads(SRC.read_text(encoding="utf-8"))
    for k, v in NEW.items():
        existing[k] = v
    SRC.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    # Validate
    reloaded = json.loads(SRC.read_text(encoding="utf-8"))
    sys.stdout.reconfigure(encoding="utf-8")
    for k in sorted(reloaded.keys(), key=int):
        print(f"list {k}: {len(reloaded[k])} passages")

if __name__ == "__main__":
    main()
