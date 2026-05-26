# -*- coding: utf-8 -*-
"""
Builder: 3 passages per list for lists 26-30 (harder GRE-style questions).
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "passages.json"

NEW = {}

# ---------------------------------------------------------------------------
# LIST 26
# ---------------------------------------------------------------------------
NEW["26"] = [
    {
        "title": "The Intransigent Donor",
        "targets": [
            "intransigent","axiomatic","qualm","candid","unfaltering","precursor","tailor",
            "promulgate","oblivious","heed","unassailable","commensurate","escalate",
            "pristine","contagious","preconception","tangible","favorable","quintessential",
            "outmoded","pervasive","yardstick","peculiar","seminal","inveterate"
        ],
        "text": (
            "When Eleanor Marsh announced her gift, she did so with an unfaltering clarity that struck "
            "the gallery's trustees as a precursor to trouble. Her conditions were not extreme; they were "
            "axiomatic, as if she had drawn them from a yardstick everyone in the room ought already to "
            "have applied. The gift, she said, would be commensurate with the gallery's ambitions only if "
            "the gallery agreed to tailor its acquisitions policy to a set of principles she would "
            "promulgate in a forthcoming pamphlet — principles she had spent her professional life, in a "
            "field unrelated to art, refining for a different industry altogether.\n\n"
            "The trustees, candid in their private deliberations, had qualms. The principles, when the "
            "pamphlet arrived, were not in fact pernicious. Several were even, on a generous reading, "
            "tangible improvements over the gallery's outmoded existing language. What the trustees "
            "objected to was less the content than the structural posture: a donor whose conditions had "
            "to be heeded as if unassailable was a donor whose subsequent gifts could be expected to "
            "escalate the conditions in proportion to her oblivious confidence that the gallery had, in "
            "accepting the first set, signaled their pristine reasonableness.\n\n"
            "The chair of the board, who had negotiated a comparable gift a decade earlier, observed "
            "that Marsh's intransigence was contagious in a peculiar way. The board's own discussion was "
            "drifting, almost without anyone noticing, toward a quintessentially symmetrical "
            "intransigence: to refuse the gift on principle, regardless of the principles' merit, simply "
            "because accepting them on the donor's terms would set a pervasive precedent. The chair had "
            "no preconception about which intransigence was correct. He suspected, however, that either "
            "choice made on those grounds would prove less seminal for the gallery's future than the same "
            "choice made for substantive reasons either way.\n\n"
            "The board, in the end, accepted the gift after a small set of inveterate negotiations that "
            "tailored Marsh's principles to a form the gallery could heed without ceding the structural "
            "concession. Marsh herself, who had expected an unassailable victory, was surprised to find "
            "the result favorable. The chair's quiet condition — that the principles would be reviewed by "
            "the gallery's own advisory committee on a schedule the gallery, not the donor, controlled — "
            "had cost her nothing she could articulate and had, almost imperceptibly, removed the "
            "structural posture the board had spent two months trying to defeat."
        ),
        "questions": [
            {
                "q": "The trustees' qualm with Marsh's gift, as developed in the second paragraph, is best characterized as concern about",
                "opts": [
                    "the substantive content of the principles in her pamphlet.",
                    "the precedent set by accepting any conditions delivered with the structural posture that they cannot be revised.",
                    "the donor's lack of expertise in the gallery's field.",
                    "the gallery's outmoded existing acquisitions policy."
                ],
                "ans": 1,
                "why": "The trustees' objection 'was less the content than the structural posture' — a donor whose conditions had to be 'heeded as if unassailable.' The worry is about the precedent of unrevisable conditions, not the principles themselves."
            },
            {
                "q": "The chair's observation about a \"symmetrical intransigence\" most strongly implies that he regards",
                "opts": [
                    "intransigence as an effective negotiating tactic in donor relations.",
                    "an oppositional refusal made primarily to resist the donor's posture as itself a form of capitulation to that posture's terms of debate.",
                    "the board as having lost the substantive case for the gift's principles.",
                    "Marsh's intransigence as a tactical performance rather than a sincere position."
                ],
                "ans": 1,
                "why": "The chair frames the board's drift toward refusing-on-principle as a 'quintessentially symmetrical intransigence' — i.e. an opposition organized by the donor's posture rather than by substance, which mirrors and thereby concedes the donor's terms."
            },
            {
                "q": "The chair's quiet condition succeeded chiefly because it",
                "opts": [
                    "imposed an obvious cost on the donor that she was willing to pay for the principles' acceptance.",
                    "modified the gift's structural terms in a way that the donor could not, given her own framing of the principles as reasonable, easily resist.",
                    "delayed the gift's acceptance until the donor lost interest in the conditions.",
                    "secured the support of a faction on the board that had previously opposed the gift."
                ],
                "ans": 1,
                "why": "The condition 'cost her nothing she could articulate' and 'almost imperceptibly removed the structural posture the board had spent two months trying to defeat' — its success lay in changing the structure under a procedural label the donor's own framing made hard to refuse."
            }
        ]
    },
    {
        "title": "The Prosaic Visionary",
        "targets": [
            "prosaic","arcane","panorama","seminal","prototype","candid","intransigent",
            "fabricate","escalate","outmoded","peculiar","propitiate","tangible","oblivious",
            "yardstick","ingenious","preconception","goad","pristine","commensurate",
            "pervasive","frantic","unfaltering","heed","precocious"
        ],
        "text": (
            "The trouble with describing Jia Tan as visionary was that her actual contributions were so "
            "prosaic. Her prototypes did not promise a panorama of the future; they did one ingenious "
            "thing each, with a peculiar economy that her precocious students sometimes mistook for "
            "limitation. Visiting venture capitalists, oblivious to the local convention of judging work "
            "by what it had quietly absorbed rather than what it had loudly proposed, regularly told her "
            "to escalate her ambitions. She regularly declined.\n\n"
            "What her admirers, more candid than her promoters, identified as her seminal contribution "
            "was less any single prototype than her habit of refusing to fabricate the connective tissue "
            "between them. She did not, in print or in interviews, propitiate the arcane theoretical "
            "frameworks in which her field expected its leading figures to traffic. She offered no "
            "yardstick by which her body of work could be commensurately summarized. To readers raised on "
            "the pervasive expectation that a senior researcher should produce a unified vision, Tan's "
            "papers read as a series of unrelated practical interventions whose tangible utility never "
            "added up to a doctrine.\n\n"
            "Her own preconception about the field, she told a frantic interviewer late in her career, "
            "was that the outmoded doctrines her contemporaries kept generating were precisely the "
            "fixtures that goaded the next generation into unproductive frantic imitations of the doctrine "
            "rather than productive imitations of the work. She had been, throughout her career, "
            "intransigent on this single point: a researcher's job was not to produce a pristine "
            "framework but to leave behind a workable set of solved problems whose collective shape no "
            "one — including the researcher — needed to articulate.\n\n"
            "Tan's intransigence was not, in the end, costless. Her field's pervasive memory tends to "
            "favor figures whose unfaltering doctrines can be taught in a single seminar; Tan, who had "
            "produced no such doctrine, faded faster from the syllabi than her own students thought "
            "fair. What did not fade was the prototypes themselves, which kept reappearing — sometimes "
            "unattributed — in the load-bearing layers of work her doctrinaire contemporaries' "
            "successors built. Whether her refusal to articulate a vision had cost her commensurately "
            "with what it had preserved, her students continued to argue, in language Tan herself, "
            "characteristically, would have found unhelpful."
        ),
        "questions": [
            {
                "q": "The passage suggests that Tan's contemporaries' insistence on unified doctrines is, in her view, harmful chiefly because such doctrines",
                "opts": [
                    "limit the practical applicability of any single prototype.",
                    "encourage the next generation to imitate the doctrine itself rather than the practical work it claimed to organize.",
                    "are usually theoretically incoherent on close examination.",
                    "displace empirical research with abstract speculation."
                ],
                "ans": 1,
                "why": "Tan's stated objection is that the outmoded doctrines 'goaded the next generation into unproductive frantic imitations of the doctrine rather than productive imitations of the work' — the harm is downstream pedagogical, not technical or methodological."
            },
            {
                "q": "The passage's discussion of Tan's reception in her field implies that the academic memory it describes operates on which of the following implicit criteria?",
                "opts": [
                    "It rewards research whose practical applications can be quantitatively measured.",
                    "It rewards bodies of work whose teachable doctrines can be summarized in a single seminar, independent of whether the underlying work persists in use.",
                    "It rewards researchers whose students achieve independent reputations.",
                    "It rewards researchers who maintain unfaltering positions over a long career."
                ],
                "ans": 1,
                "why": "The closing paragraph states that 'the field's pervasive memory tends to favor figures whose unfaltering doctrines can be taught in a single seminar,' and explicitly contrasts that memory with the persistence of Tan's prototypes in actual use — the implicit criterion is teachability rather than continued utility."
            },
            {
                "q": "The closing description of the students' continued argument — that they argue \"in language Tan herself, characteristically, would have found unhelpful\" — most strongly conveys that",
                "opts": [
                    "Tan's students misunderstood her work and continued to misrepresent it after her career.",
                    "the dispute about whether Tan's refusal was worth its cost is itself being conducted in the kind of evaluative doctrine her work was intended to refuse.",
                    "Tan had explicitly forbidden her students from discussing her career in print.",
                    "the question of Tan's legacy has been answered but the students refuse to accept the answer."
                ],
                "ans": 1,
                "why": "The line is ironic: the students are arguing about whether her refusal-to-articulate-a-vision was worth the cost using precisely the kind of summarizing evaluative language Tan would have rejected — i.e. the form of the debate enacts what her work refused, which is the line's point."
            }
        ]
    },
    {
        "title": "Foment in the Square",
        "targets": [
            "foment","anarchy","totalitarian","transmogrify","escalate","quandary","squelch",
            "tailor","derogate","frantic","preconception","pervasive","panorama","seminal",
            "outmoded","intransigent","propitiate","commensurate","tangible","oblivious",
            "heed","pristine","conundrum","precocious","favorable"
        ],
        "text": (
            "Whether the demonstrations in the central square had been fomented or had merely arisen "
            "became, within two weeks, a question whose answer no honest observer could give. The "
            "official press described an organized network bent on totalitarian replacement of a "
            "legitimate government; the protesters' own publications, when they could be found, derogated "
            "the official account as the kind of preconception authorities reliably promulgate when "
            "confronted with spontaneous discontent. Both accounts contained a measure of the truth. The "
            "deeper conundrum was that neither account could absorb the measure the other contained "
            "without losing the clarity its political moment required.\n\n"
            "Dr. Lin, the sociologist who had been studying the square for three years before the "
            "demonstrations began, was unwilling to tailor her data to either narrative. The pervasive "
            "expectation among visiting journalists was that she would, as an expert, escalate either the "
            "foment account or the spontaneity account into a tangible doctrine she could be quoted "
            "endorsing. Her actual finding was less convenient: the demonstrations had been neither "
            "fomented in any classical sense nor had they arisen with the pristine spontaneity protesters "
            "preferred to claim. They had been catalyzed — a word she chose with care — by a small set "
            "of organizers whose contribution had been to recognize and amplify a discontent the "
            "organizers themselves had not produced.\n\n"
            "Lin's distinction was not, by her own account, seminal. It was descriptive. But it placed "
            "her, almost involuntarily, into a quandary neither the government's nor the protesters' "
            "preferred narrative had room for. The government wished to squelch what it could not, on the "
            "evidence, prove had been organized; the protesters wished to derogate the very existence of "
            "the organizers whose work, in Lin's account, had been crucial to the demonstrations' scale. "
            "Lin's catalysis hypothesis transmogrified, in each side's hands, into a propitiation of the "
            "other side — exactly the rhetorical position she had spent her career refusing to occupy.\n\n"
            "What she did not say in any of her press interviews — but did say, in a long footnote of "
            "her eventual book — was that the public debate's frantic insistence on a single account had "
            "itself transformed the demonstrations. By the third week, the protesters were behaving in "
            "ways the spontaneity account required; by the fourth, the organizers, threatened with the "
            "government's totalitarian response, had begun to act in ways the foment account had "
            "predicted. The two narratives, intransigent in their original incompatibility, had become "
            "commensurate by the simple mechanism of the actors on the ground tailoring their behavior to "
            "fit one or the other. Whether either narrative had ever been adequate to the square's "
            "original condition was, by then, a question oblivious to any tangible answer."
        ),
        "questions": [
            {
                "q": "Lin's distinction between \"foment\" and \"catalysis\" is offered chiefly to",
                "opts": [
                    "demonstrate that the demonstrations were neither organized nor spontaneous in any sense.",
                    "name an intermediate mode in which a small group amplifies but does not produce the discontent it organizes, which neither side's preferred narrative can incorporate without weakening.",
                    "establish that the organizers were more important to the demonstrations than the government had acknowledged.",
                    "argue that the demonstrations would have occurred without the organizers' involvement."
                ],
                "ans": 1,
                "why": "Lin defines catalysis as recognizing and amplifying discontent the organizers 'had not produced,' and the passage shows both sides unable to absorb this intermediate mode without losing their preferred clarity. The point is to name an intermediate that neither narrative can hold."
            },
            {
                "q": "The closing paragraph's account of how the demonstrations changed over their first four weeks most strongly supports which of the following claims?",
                "opts": [
                    "Both the government and the protesters had been correct from the start about the demonstrations' nature.",
                    "The public insistence on a single account was itself a causal force that drove participants to behave in ways consistent with one narrative or the other, retrospectively rendering each narrative more accurate than it had originally been.",
                    "Lin's sociological method was unable to track rapid changes in the demonstrations' character.",
                    "The organizers had planned from the outset to escalate the demonstrations beyond their original scope."
                ],
                "ans": 1,
                "why": "The closing paragraph describes participants 'tailoring their behavior to fit one or the other' under pressure of the public debate — the narratives became commensurate not because they were originally adequate but because the debate caused the actors to make them so. That is the central causal claim."
            },
            {
                "q": "It can be inferred that Lin reserved her observation about the narratives' self-fulfilling effect for a footnote of her book, rather than for her press interviews, because",
                "opts": [
                    "she was uncertain whether the observation could be empirically substantiated.",
                    "the observation, if delivered in the press's frantic register, would itself be absorbed into one of the two narratives she had spent her career refusing to occupy.",
                    "she wished to preserve the observation for academic readers who would find it more interesting.",
                    "she was concerned that the protesters would interpret the observation as an endorsement of the government."
                ],
                "ans": 1,
                "why": "The passage establishes that Lin's catalysis hypothesis was already being transmogrified by each side into propitiation of the other — exactly the position she refused. A self-fulfillment claim delivered through the same press would suffer the same fate, which the footnote venue evades."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 27
# ---------------------------------------------------------------------------
NEW["27"] = [
    {
        "title": "The Cavilling Editor",
        "targets": [
            "cavil","superfluous","quibble","monotonous","bombastic","perspicacious","competent",
            "trifling","proffer","diatribe","artificial","intrepid","reticent","propound",
            "wallow","heartfelt","probity","jumble","unbounded","witless","relegate",
            "transient","glancing","dispute","efficacy"
        ],
        "text": (
            "The senior editor, Halvar Ek, was famously perspicacious about everything except his own "
            "appetite for cavil. To his own writers he was reticent in praise and unbounded in technical "
            "objection; to other editors he proffered, at dinner, the more or less monotonous diatribe "
            "that contemporary nonfiction had relegated structure to a trifling afterthought. His "
            "manuscript notes were a jumble of competent diagnostic remarks and what one of his more "
            "patient writers called artificial quibbles — corrections that, on inspection, addressed a "
            "version of the sentence the writer had not, in fact, written.\n\n"
            "What kept his writers loyal, despite the diatribes, was an underlying probity that the "
            "diatribes themselves could not undermine. Ek did not, even in his most bombastic moods, "
            "demand that a sentence be changed merely because he had failed to read it carefully. When "
            "his attention had been glancing and the writer pointed this out, he proffered a heartfelt "
            "and somewhat embarrassed correction, and the manuscript improved. His writers, having "
            "learned which of his objections deserved to be heeded and which were the superfluous output "
            "of a tired afternoon, found the underlying judgment intrepid in ways that compensated for "
            "the apparatus.\n\n"
            "His difficulty came when he was assigned to edit a writer who declined to make this "
            "distinction. The writer, a younger essayist of genuine talent, treated every objection as "
            "load-bearing and rewrote her paragraphs to accommodate even the most transient of his "
            "marginal complaints. The resulting drafts were technically responsive and progressively "
            "witless; the more she heeded him, the more her sentences came to wallow in the precisely "
            "calibrated phrasings that satisfied his quibbles without serving her own argument. Ek, "
            "perspicacious enough to recognize the pattern, did not at first know how to stop it.\n\n"
            "What he eventually did was, by his own standards, drastic. He sent her back her own original "
            "manuscript with all his marginal notes erased and a single sentence on the cover page: "
            "publish this version, or argue with me about any specific change before you make it. The "
            "essayist disputed the propriety of the gesture in print some years later, in a piece whose "
            "efficacy as a complaint was undercut by her parenthetical admission that the original "
            "version had, in fact, been the better one. The cavil, Ek told a colleague privately at the "
            "time, was a useful tool against careless writing but a corrosive one against careful "
            "writers, and the only way to tell the difference was to watch whether the writer's prose "
            "improved or merely complied."
        ),
        "questions": [
            {
                "q": "The central diagnostic Ek arrives at in the third paragraph turns on which of the following distinctions?",
                "opts": [
                    "Between technical competence and original talent in writers.",
                    "Between writers whose prose improves under editorial pressure and writers whose prose merely complies with it.",
                    "Between editors who deliver criticism harshly and those who deliver it gently.",
                    "Between essays whose arguments are sound and those whose arguments are unsound."
                ],
                "ans": 1,
                "why": "The closing paragraph distills the diagnosis: 'the only way to tell the difference was to watch whether the writer's prose improved or merely complied.' The distinction is between productive and merely compliant response to criticism."
            },
            {
                "q": "Ek's eventual intervention — returning the original manuscript with erased notes — is best understood as an attempt to",
                "opts": [
                    "abandon his editorial responsibilities in protest at the writer's overcompliance.",
                    "force the writer to defend specific changes individually, thereby breaking the deference that had been hollowing out her prose.",
                    "demonstrate to other editors that the writer was incapable of independent judgment.",
                    "punish the writer for declining to make the distinction his other writers made."
                ],
                "ans": 1,
                "why": "The cover-page condition is 'publish this version, or argue with me about any specific change before you make it' — a procedural change that forces the writer to defend each modification individually, dismantling the indiscriminate deference."
            },
            {
                "q": "The essayist's later complaint — that her parenthetical admits the original version was better — is recounted in the passage to",
                "opts": [
                    "vindicate Ek by demonstrating that his judgment was correct after all.",
                    "suggest that the essayist had insufficient self-knowledge to evaluate her own work.",
                    "complicate any simple reading of the encounter by showing the substantive vindication of Ek's gesture coexisting with the essayist's procedural objection to it.",
                    "demonstrate that the essayist had remained loyal to Ek despite their disagreement."
                ],
                "ans": 2,
                "why": "The essayist disputes the propriety of the gesture, but in the same piece concedes the original was better — the passage preserves both elements (procedural objection + substantive concession) rather than resolving them, complicating a unified verdict."
            }
        ]
    },
    {
        "title": "The Quiescent Hour",
        "targets": [
            "quiescent","transient","imperturbable","propitiate","sanctimonious","kindred",
            "humdrum","reassure","heartfelt","secure","reticent","tether","competent",
            "tangible","clearheaded","wont","wallow","relegate","glancing","fluster",
            "intractable","probity","quibble","insufferable","downcast"
        ],
        "text": (
            "The hospice nurse Anastacia Reed had a reputation for being imperturbable. Family members "
            "wont to be flustered in the doorway of the dying steadied themselves when she entered the "
            "room; patients, in the quiescent hour before sleep, found her presence less reassuring than "
            "tethering. She did not, however, regard her composure as a tangible asset. It was, she said "
            "in the only interview she ever gave, a humdrum habit she had developed in her first decade "
            "and could no more turn off than she could turn off the color of her eyes.\n\n"
            "Her colleagues, with whom she was reticent about her practice, were less reticent about her. "
            "Some thought her almost saintly; others, more clearheaded, suspected the imperturbability "
            "was a kind of relegation of her own emotional life that the families benefited from and the "
            "nurse paid for. The kindred competing readings did not, in Reed's view, deserve a great "
            "deal of public debate. She knew which of them was nearer to the truth; she also knew that "
            "the families she served had no use for the truer reading, and that any sanctimonious "
            "discussion of the cost of her composure would propitiate exactly the kind of attention her "
            "work had been designed to make unnecessary.\n\n"
            "What troubled her was not the cost but a transient, glancing worry about her successors. The "
            "younger nurses who had begun to imitate her manner, she suspected, had not built the same "
            "scaffolding underneath. To wallow openly in the difficulty of the work, as some of them did "
            "in supervision, struck her as a more honest stance than the imperturbable surface she had "
            "trained them, by example, to maintain. Her wonted approach, when one of them sought her out, "
            "was to quibble heartfelt-ly with their imitation: she had not, in fact, taught them to be "
            "composed; she had only taught them what composure looked like from the outside.\n\n"
            "Reed retired without writing the practical manual several editors had asked her for. What "
            "she left behind, in the supervision notes her colleagues eventually published, was an "
            "intractable observation: a manner adopted in advance of the underlying experience that "
            "produced it does not, however competent the imitation, secure the same internal goods. To "
            "teach the manner first was to leave the next generation downcast in private and "
            "insufferable in public, and the only useful thing she could think to say to anyone tempted "
            "to imitate her was that she had, by accident, become what she had spent her career trying "
            "not to be confused with."
        ),
        "questions": [
            {
                "q": "Reed's central worry about her successors, as developed in the third paragraph, is that they",
                "opts": [
                    "lack the technical training necessary for hospice work.",
                    "have adopted the external manner of her composure without the underlying experience that originally produced it.",
                    "are inclined to wallow openly in difficulties that competent nurses should suppress.",
                    "imitate the practical procedures of her work too literally."
                ],
                "ans": 1,
                "why": "Reed's worry is that the younger nurses 'had not built the same scaffolding underneath' her manner and that she had taught them not 'to be composed' but only 'what composure looked like from the outside' — i.e. manner without underlying experience."
            },
            {
                "q": "Reed's reasoning in the second paragraph, about not engaging publicly with debates over the cost of her composure, depends most heavily on the judgment that",
                "opts": [
                    "such debates would damage her professional reputation.",
                    "such debates would draw attention of a kind that would undermine the very function her composure was designed to perform.",
                    "her colleagues lacked the standing to assess her practice.",
                    "the more sympathetic reading of her composure was, on the evidence, mistaken."
                ],
                "ans": 1,
                "why": "Reed reasons that 'sanctimonious discussion of the cost of her composure would propitiate exactly the kind of attention her work had been designed to make unnecessary' — i.e. debate would call attention to her interior in a way that defeats the function of her exterior."
            },
            {
                "q": "The passage's closing observation — that she became \"what she had spent her career trying not to be confused with\" — most plausibly refers to her becoming",
                "opts": [
                    "a saintly figure whose composure invites uncritical imitation, when her actual work depended on a private interior the imitation cannot transmit.",
                    "a public expert on hospice practice whose theoretical views her actual practice could not support.",
                    "an administrator distant from the day-to-day work of patient care.",
                    "a critic of the younger nurses' practice without offering them any practical alternative."
                ],
                "ans": 0,
                "why": "The passage builds the irony in the third and fourth paragraphs: Reed's success as a model becomes the very mechanism by which her external manner is reproduced without the interior — i.e. she became the surface-imitable figure her career's actual work resisted being reduced to."
            }
        ]
    },
    {
        "title": "The Intractable Case",
        "targets": [
            "intractable","perspicacious","exigent","paradigm","undeniable","reassure",
            "frown","capture","propound","disguise","disposable","clearheaded","accommodate",
            "vehement","tether","quibble","reticent","scatter","tailor","atypical","fissure",
            "imperil","competent","headlong","intrepid"
        ],
        "text": (
            "The case the office had been calling intractable was, in Inspector Riad Faraj's perspicacious "
            "summary, not intractable at all. It was atypical, exigent, and embarrassing — a "
            "combination, he said, that the office had a paradigm for treating as intractable so that the "
            "embarrassment would not, in the period of investigation, propound itself into a public "
            "fissure the office could not absorb. The case's undeniable difficulty had become a "
            "disposable rhetorical cover for institutional convenience.\n\n"
            "Faraj's reading was vehement in private and reticent in public. He did not, in any official "
            "communication, dispute the office's framing; he simply, on his own initiative, began to "
            "tailor his investigative effort along the lines an honest treatment of the case would have "
            "required. He interviewed witnesses the office had scattered to peripheral assignments; he "
            "frowned at exhibits the office had quietly demoted to its disposable categories; he "
            "captured, in a private log, the discrepancies between the office's official chronology and "
            "the documentary record an intrepid reader of the case file could assemble.\n\n"
            "The office, alert to his work, did not at first interfere. Its preferred maneuver was to "
            "accommodate Faraj's exertions in the file's margins while continuing to call the case "
            "intractable in its public summaries. Faraj had foreseen this. His own purpose was not to "
            "force the office into a public admission — that would have imperiled the case in a more "
            "headlong way than it deserved — but to construct, with a clearheaded patience, the kind of "
            "documentary record that would make any future treatment of the case impossible to disguise "
            "as intractability.\n\n"
            "He never published his log. He did, before his retirement, transfer it to a younger "
            "colleague whose competence he had reassured himself of over three years of glancing tests. "
            "The case did not, in his lifetime, produce the resolution he had worked toward. The younger "
            "colleague, however, was tethered to a record her predecessor's office had never expected "
            "her to inherit, and the office's preferred framing of the case — that it was a regrettable "
            "intractable matter no competent investigator had ever been able to advance — quietly ceased "
            "to be available the moment her first careful memo cited a discrepancy from his log. Whether "
            "the case would ever be resolved was, by then, less interesting than the fact that the "
            "office's framing of it had been."
        ),
        "questions": [
            {
                "q": "Faraj's central claim in the first paragraph is that the office's use of the word \"intractable\" functions chiefly to",
                "opts": [
                    "describe the genuine evidentiary difficulty of the case.",
                    "convert an embarrassing-but-tractable case into a category that protects the office from public scrutiny during the investigation.",
                    "warn investigators away from approaches that have previously failed.",
                    "reassure the public that experienced officers are handling the matter."
                ],
                "ans": 1,
                "why": "Faraj specifies that the office has a 'paradigm for treating' atypical, exigent, embarrassing cases as intractable so the embarrassment 'would not... propound itself into a public fissure.' The word's function is institutional protection during investigation, not description."
            },
            {
                "q": "Faraj's strategy throughout the passage is best characterized as",
                "opts": [
                    "open confrontation with the office's framing of the case.",
                    "private accumulation of a documentary record whose existence would, in the future, constrain the office's continued use of its preferred framing.",
                    "public publication of evidence sufficient to force the office's hand.",
                    "recruitment of allies within the office to overturn its leadership."
                ],
                "ans": 1,
                "why": "Faraj is 'reticent in public,' captures discrepancies 'in a private log,' and aims to make 'any future treatment of the case impossible to disguise as intractability' — a constraint-on-future-framing strategy, not confrontation, publication, or coalition."
            },
            {
                "q": "The passage's final sentence implies that, by the time of the younger colleague's memo, the more interesting question about the case had become",
                "opts": [
                    "whether the original suspects would ever be identified.",
                    "how a prior institutional framing of a case is dismantled, rather than whether the case itself is resolved.",
                    "whether Faraj's log would itself withstand legal scrutiny.",
                    "whether the office's leadership would resign in response to the memo."
                ],
                "ans": 1,
                "why": "The closing sentence subordinates the question of resolution to 'the fact that the office's framing of it had been' [resolved/foreclosed]. The passage's interest has migrated from the case's substantive outcome to the structural dismantling of the framing that had protected the office."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 28
# ---------------------------------------------------------------------------
NEW["28"] = [
    {
        "title": "The Indefatigable Investigator",
        "targets": [
            "indefatigable","surreptitious","abscond","muckrake","incisive","abeyance",
            "plastic","interrelated","striking","cursory","painstaking","besmirch","retiring",
            "negligent","provocative","apostle","outlaw","provision","tactless","banal",
            "obdurate","gut-level","cliquish","disregard","forgo"
        ],
        "text": (
            "The reporter, Yolanda Reyes, had spent eleven years on a single corruption beat. She was, by "
            "the testimony of colleagues who did not always like her, indefatigable — willing to forgo "
            "obvious stories for the painstaking accumulation of small documentary anomalies whose "
            "interrelated significance she could not, at any single moment, prove. Her editors, "
            "cliquish in the manner of small-town newsrooms, treated her as both an asset and an "
            "inconvenience. The asset was the occasional incisive piece her years of work produced; the "
            "inconvenience was the negligent volume of routine coverage she declined to provide in the "
            "intervening months.\n\n"
            "Her central subject, a former county comptroller who had absconded with a striking sum and "
            "then returned to local life under a vaguely retiring posture, had become for her something "
            "more durable than a target. She did not consider what she was doing muckraking; the word, "
            "she said, had become a banal label that obdurate readers attached to any sustained "
            "investigative work they preferred to keep in abeyance. She was attempting, more "
            "modestly, to construct a record that no future apostle of the comptroller's rehabilitation "
            "could disregard.\n\n"
            "Her method was surreptitious in a particular way. She did not interview the comptroller; "
            "she did not solicit on-the-record statements that the comptroller's lawyers would have "
            "treated as provocations. She read, instead, the cursory documents that institutions are "
            "required by provision of law to produce — utility filings, zoning notices, the gut-level "
            "indicators of a person's daily movements that no individual document discloses but a "
            "patient accumulation of them does. To outlaw such reading, in her view, would be to "
            "besmirch a tradition of accountability journalism for which the alternative was the "
            "tactless interview that produced nothing but a denial.\n\n"
            "What she eventually published was not, by the standards of her colleagues, plastic or "
            "striking. It was a long, sober piece in which the comptroller's post-departure life was "
            "documented in such interrelated detail that the gentle reading he had cultivated locally "
            "became, paragraph by paragraph, impossible to sustain. The piece won no prizes. It produced "
            "no resignations. Its longest-running effect, four years later, was that when the comptroller's "
            "associates attempted to install him on a charitable board, the board's own due diligence "
            "officer cited Reyes's piece by name and the appointment quietly went into abeyance. Reyes, "
            "asked at her retirement what she had aimed for in eleven years on the beat, said that this "
            "was approximately it — the kind of outcome a muckraking piece could not have produced, and a "
            "patient piece could only produce by refusing the muckraking register that would have made "
            "it satisfying to write."
        ),
        "questions": [
            {
                "q": "Reyes's reasoning in the second paragraph implies that she rejects the label \"muckraking\" because",
                "opts": [
                    "she objects to the historical associations of the term with sensationalism.",
                    "the label functions, in the hands of obdurate readers, as a way of bracketing the kind of sustained investigative work she does so that it can be set aside without engagement.",
                    "her work does not, in fact, expose any institutional wrongdoing.",
                    "she prefers terms that align her work with adversarial rather than investigative traditions."
                ],
                "ans": 1,
                "why": "Reyes argues the word has 'become a banal label that obdurate readers attached to any sustained investigative work they preferred to keep in abeyance' — i.e. the label's function is dismissive bracketing, not description."
            },
            {
                "q": "The passage suggests that Reyes's preference for documentary research over interviews depends most heavily on which of the following judgments?",
                "opts": [
                    "Interviews are too time-consuming relative to the information they yield.",
                    "Direct interviews would produce predictable denials and would tactlessly trigger legal responses that documentary work avoids.",
                    "Subjects of investigation are entitled to refuse to answer questions.",
                    "Documentary research is more legally defensible in court than interview-based reporting."
                ],
                "ans": 1,
                "why": "The third paragraph specifies that interviews would have been 'tactless' and 'produced nothing but a denial' and that on-the-record statements would have been 'treated as provocations' by the lawyers. The reasoning is about predictable denial plus tactical exposure, not time, ethics, or legal admissibility."
            },
            {
                "q": "Reyes's retirement remark — that the board appointment's quiet collapse was \"approximately\" what she had aimed for — is most consistent with which of the following views of investigative journalism's purpose?",
                "opts": [
                    "Investigative journalism succeeds chiefly when it produces immediate and visible institutional consequences.",
                    "Investigative journalism's most durable function may be to populate the record relied on by other institutional actors, producing effects displaced in both time and forum from the original publication.",
                    "Investigative journalism is only valuable when it wins formal recognition through prizes.",
                    "Investigative journalism should aim to provoke confrontation between its subjects and their critics."
                ],
                "ans": 1,
                "why": "The piece produced no resignations and no prizes but four years later was cited by a due-diligence officer at a different institution — Reyes treats this displaced, downstream institutional effect as 'approximately' her aim, which matches the record-populating view."
            }
        ]
    },
    {
        "title": "The Quixotic Architect",
        "targets": [
            "quixotic","plastic","supple","adroit","riveting","portentous","superficial",
            "extravagant","apostle","banal","didactic","essential","postulate","forgo",
            "imperil","whet","painstaking","cursory","striking","outlaw","gut-level",
            "disposable","tactless","unfeeling","aggrandize"
        ],
        "text": (
            "The architect Solenne Aubert was, depending on the room, called quixotic or didactic. Her "
            "buildings were supple in plan, riveting in their use of light, and — to clients whose taste "
            "she had not yet won over — extravagant in the small expensive choices on which she did not, "
            "as a matter of practice, compromise. She had an adroit way of refusing such compromises "
            "without making the client feel refused. The client, after a meeting with her, often left "
            "with the impression that she had agreed to several points she had, in fact, declined to "
            "concede.\n\n"
            "Her admirers thought her an apostle of an essential principle the discipline had begun to "
            "forgo: that the small expensive choices were not, in any properly architectural sense, "
            "ornamental. They were the building's gut-level commitments to the people who would inhabit "
            "it. To strip them out for cost was not to make the building less extravagant but to make it "
            "superficial in a way the inhabitants would, in time, register without being able to name. "
            "Aubert's most riveting buildings, on her admirers' account, were riveting precisely because "
            "she had not allowed the cursory accountancy of the construction phase to outlaw what the "
            "design phase had identified as essential.\n\n"
            "Her critics, more cluttered in their objections, called the position quixotic and, in some "
            "of its applications, banal. To postulate that every small expensive choice was essential "
            "was, they said, to imperil the discipline's ability to build at all. The actual buildings "
            "Aubert had been hired to design served populations whose needs the extravagant choices, "
            "however gut-level, could not always whet into priority over the painstaking accounting "
            "without which the buildings would not, in many cases, exist. A portentous defense of essential "
            "choices was, in their view, an aggrandizing form of tactless professional self-regard.\n\n"
            "Aubert's reply, when she gave one, was striking in its narrowness. She did not deny that her "
            "principle, applied universally, would imperil the discipline. She denied only that the "
            "principle could be applied universally. The architect's job, in any individual case, was to "
            "decide which of the small expensive choices were essential and which were the disposable "
            "habits of a previously extravagant taste. That decision could not be made by the cursory "
            "criteria the accountants preferred, and it could not be evaded by the portentous criteria "
            "her own admirers occasionally promulgated. The choice was painstaking, case by case, and "
            "the discipline's failure to teach it was, she suspected, the real cause of the buildings "
            "her critics held against her, which had not been designed by anyone with the patience to "
            "make the choice well."
        ),
        "questions": [
            {
                "q": "Aubert's reply to her critics in the final paragraph is best characterized as",
                "opts": [
                    "a denial that her principle has the consequences her critics identify.",
                    "a concession that her principle cannot be applied universally, combined with a relocation of the architect's task to a case-by-case judgment her critics' criteria cannot perform.",
                    "an attack on the painstaking accounting practices her critics defend.",
                    "a withdrawal of her earlier position in light of new information."
                ],
                "ans": 1,
                "why": "Aubert 'did not deny' that her principle, applied universally, would imperil the discipline; she denied only that it could be applied universally and reframed the architect's job as case-by-case judgment about which choices are essential — a precise concession plus relocation."
            },
            {
                "q": "The passage suggests that Aubert's admirers and her critics are most likely to agree on which of the following claims?",
                "opts": [
                    "That Aubert's buildings serve their inhabitants better than her competitors' buildings.",
                    "That the discipline's accountants exercise too much influence over the construction phase.",
                    "That a defense of small expensive choices applied as a blanket principle would have impractical consequences for the discipline.",
                    "That the distinction between essential and disposable choices can be made by general criteria."
                ],
                "ans": 2,
                "why": "Aubert herself, in the fourth paragraph, agrees that the principle 'applied universally' would imperil the discipline — which is exactly the critics' charge against the universal form of her position. Both camps, on the universal version, agree about its consequences; they disagree about whether anyone in fact holds it universally."
            },
            {
                "q": "Aubert's diagnosis of the buildings her critics hold against her implies that those buildings exemplify",
                "opts": [
                    "the dangers of her principle when extended beyond its proper scope.",
                    "a failure to perform the case-by-case judgment her principle properly requires, rather than an excess of her principle.",
                    "an accommodation to accounting pressures that any responsible architect would have made.",
                    "an early phase of her own career whose limitations she has since outgrown."
                ],
                "ans": 1,
                "why": "Aubert attributes those buildings to 'the discipline's failure to teach' the case-by-case choice — i.e. they exhibit the absence of the judgment her principle calls for, not its overapplication or its prudent compromise."
            }
        ]
    },
    {
        "title": "The Iconoclast's Lecture",
        "targets": [
            "iconoclast","didactic","soliloquy","postulate","banal","provocative","apostle",
            "vain","insufferable","aggrandize","incendiary","retiring","unimpeachable","odious",
            "essential","disposable","forgo","cede","subservient","memorandum","superficial",
            "cursory","jarring","striking","plentiful"
        ],
        "text": (
            "The visiting lecture by the iconoclast historian Dr. Voskuyl was, those who attended agreed, "
            "unimpeachable in its scholarship and didactic to the point of insufferable in its delivery. "
            "He postulated, in the opening soliloquy, that the discipline had ceded its most essential "
            "questions to a generation of apostles whose own banal answers had become subservient to the "
            "professional incentives that had produced them. The provocative claim was not new in "
            "Voskuyl's work, but the lecture's striking form — eighty minutes without a question — gave "
            "the audience little room to do anything but absorb it.\n\n"
            "What Voskuyl's allies in the room found odious about the reception was less the critical "
            "response than its retiring form. No senior figure rose, in the question period that finally "
            "began, to engage him on the substantive postulate. The remarks that did follow were "
            "superficial, cursory, polite — the kind of memorandum-quality engagement the room reserved "
            "for visitors whose conclusions it had decided in advance to forget. The discipline, "
            "Voskuyl's allies suspected, had become incapable of the jarring engagement his lecture had "
            "been designed to provoke; it would absorb the provocation in the manner the lecture had "
            "itself diagnosed.\n\n"
            "Voskuyl's own assessment, delivered later to a smaller gathering, was less self-aggrandizing "
            "than his allies expected. The lecture, he said, had been a vain exercise — not because the "
            "diagnosis was wrong, but because the lecture form was incommensurate with the diagnosis. "
            "To deliver an incendiary postulate without inviting interruption was to produce, in the "
            "audience, exactly the disposable polite reception the postulate had been intended to "
            "criticize. He had, in effect, performed the very pathology he had come to name; the only "
            "honest response his audience could have offered, given the form, was the response they had "
            "in fact offered.\n\n"
            "What he proposed to do next, he told the smaller gathering, was to forgo the lecture as a "
            "format for the substantive argument and to publish, instead, a plentiful series of short "
            "essays designed to be interrupted — pieces whose claims could not, by their construction, "
            "be absorbed without the reader's response becoming part of the next piece's premise. The "
            "iconoclast, he said, had a habit of mistaking the format that flattered his self-image for "
            "the format that served his argument; he had, in this case, made exactly that mistake, and "
            "he was prepared to give up the lecture's striking pleasures for a less subservient one."
        ),
        "questions": [
            {
                "q": "Voskuyl's later self-assessment, in the third paragraph, depends most heavily on which of the following claims about the relationship between form and content?",
                "opts": [
                    "Audiences will always misinterpret a substantive argument unless the lecturer simplifies it.",
                    "A diagnosis delivered in a form that prevents engagement produces, in its audience, exactly the inattentive reception the diagnosis criticizes, so the form contradicts the content.",
                    "Iconoclasts should never deliver public lectures because their views are too radical to be absorbed in real time.",
                    "Substantive criticism is always best delivered in writing rather than in person."
                ],
                "ans": 1,
                "why": "Voskuyl's specific diagnosis is that 'to deliver an incendiary postulate without inviting interruption was to produce... exactly the disposable polite reception the postulate had been intended to criticize' — the form's preclusion of engagement enacts the very pathology the content criticizes."
            },
            {
                "q": "Voskuyl's planned next step — short essays \"designed to be interrupted\" — is best understood as an attempt to",
                "opts": [
                    "reach a wider audience than the lecture format permitted.",
                    "structure his argument so that audience engagement becomes a structural precondition of the next installment, rather than an optional sequel to a completed claim.",
                    "avoid the institutional politics of academic lecturing.",
                    "test which of his views are most likely to provoke incendiary response."
                ],
                "ans": 1,
                "why": "The essays are described as pieces whose 'claims could not, by their construction, be absorbed without the reader's response becoming part of the next piece's premise' — i.e. engagement is built into the next installment's logic, not merely solicited."
            },
            {
                "q": "Voskuyl's self-assessment that the iconoclast \"had a habit of mistaking the format that flattered his self-image for the format that served his argument\" most directly applies to which of the following choices Voskuyl made?",
                "opts": [
                    "Choosing to lecture at all rather than to publish in writing.",
                    "Choosing the eighty-minute uninterrupted soliloquy form, whose striking pleasures conflicted with the engagement his diagnosis required.",
                    "Choosing to deliver the substantive postulate to an audience already disposed against it.",
                    "Choosing to deliver his self-assessment to a smaller gathering rather than the full audience."
                ],
                "ans": 1,
                "why": "The passage names the lecture's 'striking form' as an eighty-minute uninterrupted soliloquy and Voskuyl explicitly identifies the lecture's 'striking pleasures' as what he is now prepared to forgo — the specific format choice, not the choice to lecture, is what flattered him while undermining the argument."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 29
# ---------------------------------------------------------------------------
NEW["29"] = [
    {
        "title": "The Fastidious Reviewer",
        "targets": [
            "fastidious","sonorous","verbose","malign","protean","accolade","prodigal",
            "dispassionate","subsequent","ruminate","accent","consequential","facet",
            "ethnic","forbear","civility","proclivity","fastidious","circumlocution","scorn",
            "self-effacing","saturate","static","minuscule","corrosive"
        ],
        "text": (
            "Dr. Quentin Marsh's book reviews were celebrated for their fastidious civility. He did not, "
            "in print, malign the writers he disagreed with; he forbore even the minuscule sonorous "
            "swipe that the genre's conventions permitted. His reviews ruminated, accented their "
            "objections through circumlocution, and produced — over a decade — a small body of "
            "consequential criticism whose protean influence on the field was difficult to map.\n\n"
            "What his admirers, more dispassionate than his colleagues realized, identified as his "
            "central virtue was less the civility than what the civility enabled. By refusing the "
            "corrosive accent that his contemporaries reflexively adopted, Marsh had purchased a kind of "
            "evaluative authority that scorn would have forfeited. Writers whose work he criticized "
            "subsequent-ly cited his reviews approvingly in their own subsequent prefaces — a facet of "
            "his influence no prodigal reviewer of the same period could claim. The accolade most often "
            "given him, that he was the only critic in the field whose objections enriched his targets, "
            "was not, in his admirers' view, an exaggeration.\n\n"
            "His critics were a smaller and more saturated camp. They held that Marsh's self-effacing "
            "civility was a strategic posture whose costs were borne by readers who needed clearer signals "
            "about which books to read. The protean influence his admirers prized was, in this account, "
            "evidence of a reviewer whose refusal to commit to a static evaluation had left his "
            "readership unsure what he actually thought. A reviewer's proclivity to forbear was, his "
            "critics argued, a luxury the field could afford only if the reviewer's circumlocutions "
            "could be reliably decoded — and Marsh's, they said, could not.\n\n"
            "Marsh himself addressed the dispute only once, in a brief note appended to a late "
            "anthology. The note was sonorous in its way and dispassionate in its substance. The critics, "
            "he wrote, had identified a real cost. He had, in fact, often left readers unsure what he "
            "thought; he had, in fact, sometimes preferred the protean influence over the static "
            "evaluation. The trade was deliberate. The kinds of books worth reviewing fastidiously, in "
            "his view, were the kinds whose value would only emerge from the slow accent of subsequent "
            "readers' work, and the reviewer's job was to ruminate honestly enough to leave that "
            "subsequent work room to develop. The static evaluation his critics preferred would have "
            "served the readers who wanted to choose well in the moment; the rumination he had chosen "
            "served the readers who would, in time, choose differently."
        ),
        "questions": [
            {
                "q": "Marsh's admirers, as developed in the second paragraph, locate the central value of his civility in",
                "opts": [
                    "the absence of personal animus in his reviews.",
                    "the evaluative authority his refusal of corrosive register purchased, evidenced by his criticized writers' subsequent approving citation of him.",
                    "the political safety his style afforded him within his field.",
                    "the consistency of his judgments across his career."
                ],
                "ans": 1,
                "why": "The admirers' account specifies that by refusing corrosive accent he had 'purchased a kind of evaluative authority that scorn would have forfeited,' and the evidence offered is criticized writers citing him approvingly — i.e. the value lies in the authority purchased and its observable downstream effect."
            },
            {
                "q": "Marsh's late note implicitly accepts which of the following elements of his critics' position?",
                "opts": [
                    "That his style had concealed his actual judgments from readers.",
                    "That readers seeking to decide what to read in the moment were, in fact, served less well by his style than by the static evaluations his critics preferred.",
                    "That his protean influence was a sign of intellectual incoherence.",
                    "That his civility was a strategic posture rather than a temperamental disposition."
                ],
                "ans": 1,
                "why": "Marsh concedes that 'static evaluation his critics preferred would have served the readers who wanted to choose well in the moment' — he accepts the readers-in-the-moment cost specifically, while defending his choice on a different audience's behalf. He does not accept concealment, incoherence, or insincerity."
            },
            {
                "q": "The structure of Marsh's defense in the final paragraph is best characterized as",
                "opts": [
                    "a denial that his style had any costs.",
                    "a concession of a specific cost paired with the identification of a different beneficiary whose interests the cost was traded to serve.",
                    "a refusal to take the critics' position seriously enough to engage it.",
                    "a withdrawal of the position the critics had attacked."
                ],
                "ans": 1,
                "why": "Marsh concedes that he 'often left readers unsure what he thought' and that he 'sometimes preferred the protean influence over the static evaluation' — naming the cost — and explicitly identifies the trade's beneficiaries as readers who would 'in time, choose differently.' Concession + identified beneficiary is the structure."
            }
        ]
    },
    {
        "title": "Harbinger of Change",
        "targets": [
            "harbinger","emergent","supersede","predate","ruminate","arbitrary","unwitting",
            "proclivity","skew","prodigal","negate","prepossessing","slippery","artless",
            "satiate","fledgling","subvert","static","trepidation","elusive","resilient",
            "wistful","slight","saturate","sophisticated"
        ],
        "text": (
            "The economist Tomasz Vyrwa had spent a decade arguing that a certain narrow technical "
            "indicator was a reliable harbinger of broader emergent shifts in regional employment. The "
            "indicator predated his own work; he had not invented it, only — through a long series of "
            "papers — rescued it from the more arbitrary uses to which it had been put. By the time the "
            "indicator's predictive value had been ratified by a slow ruminating consensus, it was, in "
            "the public mind, his.\n\n"
            "What Vyrwa's most prepossessing critics, more sophisticated than his casual ones, observed "
            "was that the very success of his rescue had begun to subvert the indicator. Policymakers, "
            "unwitting in their proclivity to act on emergent signals their predecessors had ignored, "
            "had begun to skew their own interventions in anticipation of the indicator's predictions, "
            "with the result that the indicator's relationship to the underlying labor market was no "
            "longer the resilient one Vyrwa's papers had documented. His indicator was, in technical "
            "language, becoming endogenous to the very interventions it had originally been used to "
            "predict.\n\n"
            "Vyrwa's response to this critique was, in the field, slightly notorious for its trepidation. "
            "He did not negate the critique. He did not, on the other hand, satiate the critics by "
            "withdrawing the indicator from his subsequent papers. His proclivity, instead, was to "
            "publish a series of artless short notes whose explicit purpose was to track the indicator's "
            "changing relationship to its referents over the period of policy uptake. The notes did not "
            "supersede his original papers; they did not contradict them. They simply added, with a "
            "wistful candor, that an indicator's predictive value was a slippery property whose "
            "saturation by use could turn a fledgling harbinger into a static fixture whose subsequent "
            "predictions deserved less weight than its earlier ones.\n\n"
            "The notes were, on the whole, more influential than Vyrwa's enemies expected and less "
            "satisfying than his admirers had hoped. They preserved, in the field's standard "
            "introductions to the indicator, both the original argument and the subsequent qualification, "
            "in language careful enough that subsequent readers had no excuse for using the indicator "
            "without acknowledging the qualification. Whether the qualification would, in time, be "
            "respected — or whether subsequent generations of policymakers, prodigal as their "
            "predecessors had been, would treat the indicator as a static harbinger long after its "
            "predictive value had become an artifact of its own popularity — was a question on which "
            "Vyrwa, asked at his retirement, declined to be optimistic."
        ),
        "questions": [
            {
                "q": "The critique developed in the second paragraph claims that the indicator's predictive value has weakened because",
                "opts": [
                    "the underlying labor-market data have become less accurate.",
                    "policymakers' anticipatory interventions in response to the indicator have changed the relationship between the indicator and its referent.",
                    "competing indicators have superseded it in the field's attention.",
                    "Vyrwa's original papers contained methodological errors that subsequent work has revealed."
                ],
                "ans": 1,
                "why": "The critique specifies that policymakers 'skew their own interventions in anticipation of the indicator's predictions, with the result that the indicator's relationship to the underlying labor market was no longer the resilient one' — i.e. anticipatory intervention has made the indicator endogenous to its own effects."
            },
            {
                "q": "Vyrwa's response — publishing short notes rather than retracting or defending the original work — is best understood as a choice to",
                "opts": [
                    "concede the critics' objection in full while preserving his own reputation.",
                    "embed the qualification into the same published record as the original argument, so that subsequent users of the indicator cannot legitimately cite the original without the qualification.",
                    "delay engaging with the critique until the field had reached its own consensus.",
                    "establish a separate body of work distinct from his early papers."
                ],
                "ans": 1,
                "why": "The fourth paragraph specifies that the notes were preserved 'in the field's standard introductions to the indicator' alongside the original argument, 'in language careful enough that subsequent readers had no excuse for using the indicator without acknowledging the qualification.' The strategy is co-publication, not concession, delay, or rebranding."
            },
            {
                "q": "Vyrwa's pessimism at his retirement most plausibly reflects his judgment that",
                "opts": [
                    "the qualification will be forgotten when his career ends.",
                    "the structural incentive for policymakers to treat a recognized indicator as still predictive is independent of the documentary record's careful qualification.",
                    "the indicator will be discredited entirely by subsequent research.",
                    "the next generation of policymakers will be less competent than his own contemporaries."
                ],
                "ans": 1,
                "why": "Vyrwa's pessimism concerns whether 'prodigal' policymakers will treat the indicator as static long after its predictive value has become an artifact of its popularity — i.e. the worry is structural (incentive-driven misuse despite the record), not about forgetting, discrediting, or competence."
            }
        ]
    },
    {
        "title": "The Gadfly Senator",
        "targets": [
            "gadfly","dispassionate","rebuke","subvert","animus","thwart","minuscule",
            "scorn","corrosive","trendy","accolade","verbose","fastidious","protean",
            "premonitory","provident","consequential","quell","arbitrary","skew","facet",
            "objectionable","commodious","resourceful","slight"
        ],
        "text": (
            "Senator Aldura's career had been, by her own account, that of a gadfly. She had introduced "
            "few bills of her own; she had, more commodiously, made it her practice to rebuke other "
            "senators' bills in a fastidious dispassionate register that more verbose colleagues found "
            "objectionable. Her interventions were not, in the trendy sense, corrosive. They were "
            "premonitory: she identified, in the language of a proposed bill, the specific clauses whose "
            "downstream effects would skew the bill's stated purpose into a different and often "
            "contradictory one.\n\n"
            "What her enemies misread as animus was, on closer reading, a kind of provident discipline. "
            "Aldura did not scorn her colleagues' purposes; she scorned the slight, almost arbitrary "
            "drafting choices that subverted those purposes without anyone in the room noticing. To "
            "thwart, in committee, a single clause whose effect would have negated the bill's stated "
            "aim was, in her view, an accolade to the bill's stated aim itself. She had, over a decade, "
            "performed this work for bills she would have voted against in their final form, on the "
            "theory that a bill she disagreed with should at least be defeated on its actual merits "
            "rather than allowed to fail through drafting errors no one had bothered to identify.\n\n"
            "Her colleagues' eventual response to her practice was, in its way, premonitory of how "
            "institutions adjust to gadflies they cannot quell. The senate's drafting office began, "
            "without acknowledgment, to circulate proposed bills to Aldura's staff in advance of "
            "introduction. The minuscule corrective effect of these informal circulations had, over "
            "three years, a measurable consequential effect on the quality of bills emerging from the "
            "committee. The senate as a whole became, by the protean facet of its operation she had been "
            "criticizing, slightly more resourceful at its own stated work.\n\n"
            "Aldura herself, when this development was pointed out to her, treated it with the "
            "dispassionate amusement her colleagues had learned to expect. She had not, she said, "
            "intended to reform the senate's drafting practice. She had only intended to be a "
            "consequential nuisance to a specific set of bills. That the senate had quietly absorbed her "
            "nuisance into its workflow was, in her view, a small and slightly objectionable accolade — "
            "small, because it gave her no credit she could claim publicly; objectionable, because the "
            "improved workflow would in time, she suspected, make gadflies like her unnecessary, and "
            "every institution she had ever served had been more interesting when it still needed "
            "them."
        ),
        "questions": [
            {
                "q": "Aldura's reasoning in the second paragraph implies that she regards her interventions on bills she disagreed with as defensible because",
                "opts": [
                    "any improvement to a bill, regardless of one's overall position on it, increases the chance the bill will pass.",
                    "a bill she opposed should be defeated on its actual merits rather than through drafting errors that obscure those merits.",
                    "drafting corrections do not, in any consequential way, change a bill's substantive content.",
                    "her opposition to a bill is provisional and might change once the bill is properly drafted."
                ],
                "ans": 1,
                "why": "Aldura's stated principle is that 'a bill she disagreed with should at least be defeated on its actual merits rather than allowed to fail through drafting errors no one had bothered to identify' — the defense is about the integrity of the basis for defeat, not about increasing passage, neutrality of corrections, or her own provisionality."
            },
            {
                "q": "The senate's quiet practice of circulating bills to Aldura's staff is presented in the passage as",
                "opts": [
                    "a public acknowledgment of Aldura's contribution to the senate's work.",
                    "an institutional adaptation that absorbed her interventions into a routine workflow, producing measurable consequential effects without crediting her.",
                    "an attempt to neutralize her political influence by capturing her staff's loyalty.",
                    "a procedural reform that other senators publicly opposed."
                ],
                "ans": 1,
                "why": "The third paragraph specifies the circulation was 'without acknowledgment' and produced 'a measurable consequential effect on the quality of bills' — an unacknowledged institutional absorption with downstream effect, not public credit, capture, or contested reform."
            },
            {
                "q": "Aldura's final remark — that the absorbed workflow is \"a small and slightly objectionable accolade\" — most precisely conveys her ambivalence about",
                "opts": [
                    "the credit she has been denied for an institutional improvement she did not seek.",
                    "the simultaneous fact that the institution has paid her work the form of recognition that consists in adopting it, and that this adoption will make further gadflies like her unnecessary.",
                    "the senate's reluctance to formally amend its drafting procedures.",
                    "the slow pace at which the institutional improvement has occurred."
                ],
                "ans": 1,
                "why": "Aldura's own gloss specifies both elements: the accolade is small because she can claim no public credit, and objectionable because the improved workflow will 'make gadflies like her unnecessary' — institutional uptake plus the obsolescence of the role it absorbs."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 30
# ---------------------------------------------------------------------------
NEW["30"] = [
    {
        "title": "The Sardonic Doctor",
        "targets": [
            "sardonic","hereditary","prognosis","temperate","diffident","specious","resolve",
            "disprove","short-lived","comport","upheaval","truncate","euphemism","savor",
            "altruistic","pugnacious","unctuous","meager","intervene","remonstrate","deflect",
            "formidable","canny","cathedral","consort"
        ],
        "text": (
            "Dr. Ileana Cassar had a sardonic bedside manner that other physicians in the cathedral "
            "hospital found alternately formidable and unprofessional. She did not, on a patient's first "
            "visit, soften a hereditary prognosis with the unctuous euphemisms her colleagues preferred. "
            "She delivered the prognosis directly, in the temperate register of someone who had "
            "consorted long enough with bad news to have developed a vocabulary that did not, in her "
            "view, deflect from it.\n\n"
            "Her diffident colleague Dr. Mendez had remonstrated with her about this approach for "
            "several years. The specious comfort of euphemism, he argued, was not specious to patients "
            "in their first hour of bad news; the short-lived softening it offered was, however meager, "
            "altruistic in a sense Cassar's directness was not. To savor one's own intellectual honesty "
            "at such a moment was, he suggested, a kind of pugnacious self-regard the patient was in no "
            "position to defend against.\n\n"
            "Cassar's reply to Mendez, recorded in a small note her residents passed around for years, "
            "was canny in its narrowness. She did not disprove his account of the patient's first hour. "
            "She did not even resolve to soften her own approach. She did, however, observe that the "
            "patient's first hour was not the consultation's only consequential interval. Patients to "
            "whom one delivered, in the first hour, the temperate prognosis they would in any case have "
            "to absorb were patients who, in the subsequent weeks, did not have to navigate the upheaval "
            "of discovering that their physician had been quietly truncating the prognosis to spare "
            "them. The euphemism's altruism in the first hour was, in many cases, traded for a sharper "
            "upheaval in the second week — a trade her colleagues' unctuous habits had a proclivity to "
            "ignore.\n\n"
            "Mendez did not, in the end, adopt her approach; Cassar did not adopt his. What they did "
            "develop, over a long correspondence, was a shared diagnosis of the specious comfort their "
            "discipline had institutionalized — a comfort whose costs were borne by patients in a "
            "register their physicians, in their first hour with each new patient, had no canny way of "
            "seeing. Whether the discipline's preference for euphemism reflected the patients' actual "
            "preferences or only the physicians', neither of them was willing to claim to know. They "
            "did, however, agree that the question deserved more formidable attention than the field "
            "had so far given it."
        ),
        "questions": [
            {
                "q": "Cassar's reply to Mendez, as developed in the third paragraph, accepts which element of Mendez's account?",
                "opts": [
                    "That her directness causes lasting psychological harm to patients.",
                    "That euphemism does, in the first hour of bad news, offer patients a meager but real softening.",
                    "That her sardonic manner reflects intellectual self-regard.",
                    "That patients prefer euphemism over direct prognosis when surveyed."
                ],
                "ans": 1,
                "why": "Cassar 'did not disprove his account of the patient's first hour' — she accepts that euphemism offers meaningful softening in that interval. Her response is to expand the time horizon, not to deny the first-hour effect."
            },
            {
                "q": "Cassar's broader argument depends most heavily on which of the following inferences?",
                "opts": [
                    "That patients always discover, in time, that their physicians have softened a prognosis.",
                    "That an intervention's costs and benefits to the patient must be assessed across the full course of the patient's experience, not within the consultation alone.",
                    "That physicians who use euphemism are typically less skilled than those who do not.",
                    "That the discipline's preference for euphemism is driven primarily by physicians' interests."
                ],
                "ans": 1,
                "why": "Cassar's specific move is to identify the 'first hour' as not 'the consultation's only consequential interval' and to identify costs in the 'second week' that the first-hour analysis ignores. Her argument is a time-horizon expansion, not a claim about universal discovery, physician skill, or motive."
            },
            {
                "q": "The closing paragraph's joint conclusion — that the discipline's preference for euphemism may reflect either patients' or physicians' preferences — is offered chiefly to",
                "opts": [
                    "argue that the discipline's current practice is justified by patient demand.",
                    "identify a question that the dispute between Cassar and Mendez has, despite years of correspondence, left structurally unresolved and worth more formal attention.",
                    "demonstrate that Mendez has been persuaded by Cassar's position.",
                    "suggest that the choice between euphemism and directness is ultimately a matter of personal style."
                ],
                "ans": 1,
                "why": "The paragraph specifies that neither was 'willing to claim to know' the answer and that the question 'deserved more formidable attention than the field had so far given it' — i.e. it names an unresolved structural question, not a verdict, persuasion, or stylistic equivalence."
            }
        ]
    },
    {
        "title": "The Pugnacious Wastrel",
        "targets": [
            "pugnacious","wastrel","hidebound","unctuous","errant","totemic","upheaval",
            "lush","savor","truncate","cache","specious","sardonic","short-lived","singular",
            "diffident","epitome","restive","intervene","deflect","altruistic","comport",
            "remonstrate","meager","unqualified"
        ],
        "text": (
            "The family had, for two generations, treated cousin Ferran as a wastrel. The label was "
            "totemic; it was applied without examination at every family gathering, and the cousin "
            "himself, by his thirties, had become so accustomed to its application that he had ceased "
            "to remonstrate with it. He comported himself, at the lush family dinners, with a sardonic "
            "diffidence that the older relatives took as confirmation of the label and the younger "
            "ones, who were more restive about family verdicts in general, suspected of being a quite "
            "different thing.\n\n"
            "What the younger relatives' diffident investigations eventually uncovered was a cache of "
            "letters in the family attic showing that Ferran, in his twenties, had been the singular "
            "supporter of two relatives the family had since canonized as exemplars of self-made "
            "success. He had paid for one cousin's medical training; he had truncated his own "
            "professional ambitions to manage, in an unctuous family arrangement, the affairs of an "
            "aging great-aunt whose meager pension would otherwise have collapsed. The family's totemic "
            "label had been built on a specious foundation: Ferran's apparent idleness had, for fifteen "
            "years, been the altruistic absorption of family responsibilities that no one had thanked "
            "him for and several had implicitly required.\n\n"
            "The upheaval the discovery caused was both short-lived and intervening. The older relatives "
            "did not, on the whole, deflect from the new evidence; they did, however, find it difficult "
            "to revise the totemic label, which had become useful to them as a kind of family epitome "
            "of what self-discipline did not look like. Ferran himself was unqualifiedly uninterested in "
            "the revision. He had, he told the younger cousin who delivered the cache to him, made his "
            "choices in full knowledge of how they would be read; to be revised now would require him to "
            "savor a vindication he had spent thirty years declining to pursue.\n\n"
            "What the younger relatives did, with Ferran's reluctant permission, was to copy the most "
            "consequential letters and place them, without commentary, in the family archive. The "
            "totemic label, by the next year's family dinner, had begun to operate less reliably; the "
            "older relatives still applied it, but had begun, when they did, to glance instinctively at "
            "the archive shelf. Whether the label would, over time, be fully retired was a question the "
            "younger cousin did not particularly care to settle. What had been settled, she felt, was "
            "the harder thing: any future application of the label would have to argue against a record "
            "the family had previously not been required to acknowledge."
        ),
        "questions": [
            {
                "q": "Ferran's reaction to the discovery, as developed in the third paragraph, is best characterized as",
                "opts": [
                    "satisfaction that his sacrifices have finally been recognized.",
                    "indifference to public revision of his reputation, grounded in his having long ago made his choices in full awareness of how they would be read.",
                    "regret at having been misjudged for so long.",
                    "anger at the relatives who had benefited from his support without acknowledging it."
                ],
                "ans": 1,
                "why": "Ferran is 'unqualifiedly uninterested in the revision' and explicitly says he made his choices 'in full knowledge of how they would be read' and that revision now would require him to savor a vindication he had 'spent thirty years declining to pursue.' Conscious indifference to public revision, grounded in prior choice, is the precise stance."
            },
            {
                "q": "The hidebound element of the older relatives' response is best captured by the observation that they",
                "opts": [
                    "denied the authenticity of the letters from the attic cache.",
                    "accepted the new evidence factually but were unable to revise a label that had become useful to them as a family epitome.",
                    "blamed the younger cousins for disturbing a settled family judgment.",
                    "refused to allow the letters to be placed in the family archive."
                ],
                "ans": 1,
                "why": "The third paragraph specifies that the older relatives 'did not... deflect from the new evidence; they did, however, find it difficult to revise the totemic label, which had become useful to them' — factual acceptance combined with institutional reluctance to revise the operative label."
            },
            {
                "q": "The younger cousin's reasoning in the final paragraph parallels which of the following strategies discussed elsewhere in the passages of this list?",
                "opts": [
                    "Replacing one family verdict with another, more flattering verdict.",
                    "Placing an unannotated record in a position where it constrains the future application of a contested label, without seeking to win the contest immediately.",
                    "Withdrawing from a dispute when the original parties cannot agree.",
                    "Documenting harm in order to seek compensation from the responsible parties."
                ],
                "ans": 1,
                "why": "She places the letters in the archive 'without commentary,' does not particularly care whether the label is retired, and identifies the settled outcome as that any future application 'would have to argue against a record the family had previously not been required to acknowledge' — a record-constrains-future-framing strategy, parallel to Najem's and Faraj's elsewhere in the lists."
            }
        ]
    },
    {
        "title": "After the Upheaval",
        "targets": [
            "upheaval","restive","deflect","formidable","canny","remonstrate","truncate",
            "intervene","short-lived","comport","savor","nadir","pillory","temperate",
            "specious","resolve","disprove","prognosis","exterminate","altruistic","unctuous",
            "consort","euphemism","sardonic","singular"
        ],
        "text": (
            "The upheaval that had emptied the cathedral square three years earlier had been, by every "
            "subsequent measure, the city's nadir. The provisional government that had been formed in "
            "the aftermath was restive about its own legitimacy and had, in its first eighteen months, "
            "deflected almost every formidable structural question into the more comfortable territory "
            "of euphemism. Its sardonic critics in the press had, with predictable canniness, pilloried "
            "the government's preference for unctuous reassurance over substantive prognosis.\n\n"
            "Within the government itself, the most influential temperate voice was the deputy "
            "secretary Iulia Petran. She was not, in the manner of the more pugnacious reformers around "
            "her, given to public remonstration. Her interventions, when she made them, were singular "
            "in their narrow construction: she resolved, at meetings, not to disprove the government's "
            "preferred euphemisms but to truncate, with a single carefully chosen substitution, the "
            "specific phrase whose use was about to commit the government to a position it would later "
            "have to deflect from. A short-lived rephrasing introduced at the right meeting, she had "
            "observed, prevented a longer and more formidable rephrasing some months later.\n\n"
            "What her colleagues found difficult to comport themselves toward was not her method but "
            "her refusal to savor its successes. She did not, in any subsequent meeting, claim credit "
            "for the substitution. She did not consort with the press to identify the moments in which "
            "her interventions had spared the government a later embarrassment. Her sardonic critics "
            "within the cabinet treated this refusal as a specious altruism; her admirers, more "
            "carefully, treated it as the canny recognition that an intervention claimed publicly would "
            "be neutralized by exactly the cabinet politics it was designed to circumvent.\n\n"
            "Petran's eventual fall from the cabinet, when it came, was almost incidental — a political "
            "realignment that exterminated her faction without addressing the substantive work that "
            "faction had been doing. The government, freed from her interventions, returned to a "
            "rhetorical register that her short-lived presence had only temporarily disciplined. What "
            "outlived her tenure, however, was a meeting culture among the surviving deputies in which "
            "the substitution of a single phrase at the right moment had become a recognized, if "
            "unattributed, practice. Whether Petran had intended to leave behind this practice — or "
            "whether the practice was, like much of her career, the byproduct of an instinct she had "
            "declined to articulate — was a question the surviving deputies had no canny way to answer, "
            "and which her departure had made permanently impossible to put to her directly."
        ),
        "questions": [
            {
                "q": "Petran's method, as developed in the second paragraph, depends most heavily on which of the following judgments?",
                "opts": [
                    "That the government's substantive positions can be corrected only through public debate.",
                    "That a small, well-placed rephrasing at the meeting where a commitment is forming prevents the larger remedial work that the same commitment, once made, would later require.",
                    "That the government's euphemisms reflect a deeper disagreement that her colleagues are unwilling to acknowledge.",
                    "That her own reformist allies underestimate the difficulty of changing institutional language."
                ],
                "ans": 1,
                "why": "Petran's observation is that 'a short-lived rephrasing introduced at the right meeting... prevented a longer and more formidable rephrasing some months later' — an upstream-intervention judgment about the asymmetric cost of pre-commitment vs. post-commitment correction."
            },
            {
                "q": "Petran's refusal to claim credit for her substitutions is, in her admirers' reading, best explained as",
                "opts": [
                    "personal modesty consistent with her temperate manner.",
                    "the recognition that a publicly claimed intervention would be neutralized by the very cabinet politics the intervention was designed to circumvent.",
                    "a wish to spare the colleagues whose preferred phrases she had been quietly correcting.",
                    "a strategy to preserve plausible deniability in case her substitutions caused political harm."
                ],
                "ans": 1,
                "why": "The third paragraph specifies the admirers' reading: an intervention 'claimed publicly would be neutralized by exactly the cabinet politics it was designed to circumvent' — a structural-political judgment about how public claiming would undo the intervention itself, not modesty, tact, or deniability."
            },
            {
                "q": "The closing observation that the question of Petran's intent \"had been made permanently impossible to put to her directly\" most precisely conveys",
                "opts": [
                    "regret that Petran did not document her career in writing.",
                    "the structural cost, for the surviving deputies, of having lost both the practitioner and the only person who could have articulated the practice's design.",
                    "the impossibility of evaluating any institutional practice in the absence of its originator.",
                    "the cabinet's continued hostility to her faction even after her departure."
                ],
                "ans": 1,
                "why": "The closing turn is specifically about the surviving deputies' inability to learn from Petran whether the practice was intended or instinctive — the loss is dual (practitioner + articulator), not a general claim about institutions or about hostility."
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
    reloaded = json.loads(SRC.read_text(encoding="utf-8"))
    sys.stdout.reconfigure(encoding="utf-8")
    for k in sorted(reloaded.keys(), key=int):
        print(f"list {k}: {len(reloaded[k])} passages")

if __name__ == "__main__":
    main()
