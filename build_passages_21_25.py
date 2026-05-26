# -*- coding: utf-8 -*-
"""
Builder: 3 passages per list for lists 21-25, with harder GRE-style questions
(no answers that can be found by string-matching a phrase from the passage).
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "passages.json"

NEW = {}

# ---------------------------------------------------------------------------
# LIST 21
# ---------------------------------------------------------------------------
NEW["21"] = [
    {
        "title": "Industrious to a Fault",
        "targets": [
            "industrious","modish","ennui","tedious","abstemious","eclectic","prolix",
            "incessant","disquisition","insulate","reluctant","outstrip","revision",
            "deplorable","fragmentary","mandate","grandstand","derivative","negligible",
            "skittish","disintegrate","sift","commence","apparel","numinous"
        ],
        "text": (
            "Reza was the most industrious junior associate the firm had hired in a decade, and the firm "
            "did not, at first, know quite what to do with him. The other juniors were modish in their "
            "habits — dinners, conference circuits, the cultivation of an eclectic professional voice that "
            "would, in time, outstrip the firm itself. Reza was abstemious about all of it. He stayed in "
            "his office, sifted his way through drafts no one had asked him to revise, and produced "
            "reliably prolix memoranda whose recommendations the partners found, after the third or fourth "
            "reading, persuasive.\n\n"
            "The trouble was that Reza's industry insulated him from the firm's other registers. The "
            "partners liked him; the partners' clients, who had to sit across from him at dinner, found "
            "his disquisitions tedious. He could not, or would not, grandstand. A negligible courtesy that "
            "would have cost him nothing — a remark about a client's children, a comment on the apparel of "
            "a visiting consultant — seemed to him a kind of derivative performance, and he could no more "
            "produce it than he could speak a foreign language at will. His ennui at such moments was "
            "palpable; his colleagues, who had once been amused, became skittish about putting him in the "
            "room.\n\n"
            "The mandate his supervising partner finally gave him was deceptively kind. Reza was to "
            "commence a six-month rotation in a satellite office whose deplorable client relations had, "
            "the partner said, become a fragmentary embarrassment. He would have time to think. He would "
            "be left, in the rotation's quieter weeks, to read. The unspoken second clause was that the "
            "firm, in the meantime, would learn whether it could continue without him in its central "
            "rooms.\n\n"
            "Reza accepted the rotation without protest. What none of the partners had quite predicted was "
            "that the satellite office, freed from the central office's incessant revisions, became the "
            "firm's most productive in the year that followed. Whether Reza's industriousness had carried "
            "the office or had merely failed to disintegrate it — whether his removal from the center had "
            "been a numinous correction or a costly exile — remained a question on which the senior "
            "partners, two years later, were privately divided and publicly silent."
        ),
        "questions": [
            {
                "q": "The passage's structure invites the reader to weigh which of the following competing accounts of Reza's removal to the satellite office?",
                "opts": [
                    "Whether the rotation was a constructive use of his talents or a tactful expulsion.",
                    "Whether his prolix memoranda were genuinely useful or only flattered the partners' patience.",
                    "Whether the satellite office's troubles arose from staffing or from external market conditions.",
                    "Whether his colleagues' skittishness toward him was warranted or unjust."
                ],
                "ans": 0,
                "why": "The closing paragraph explicitly leaves open whether the move was 'a numinous correction or a costly exile' and frames the partners' continued silence on the question as evidence the ambiguity is real — the reader is being asked to weigh exactly the constructive/expulsive ambiguity."
            },
            {
                "q": "The passage most strongly implies that Reza's failure with clients stems from",
                "opts": [
                    "an unwillingness to perform social registers he experiences as inauthentic, rather than from inattention or disdain.",
                    "a deficit of relevant expertise that he conceals behind lengthy memoranda.",
                    "a deliberate strategy to avoid being assigned to client-facing work.",
                    "a private contempt for clients that he intermittently fails to suppress."
                ],
                "ans": 0,
                "why": "The passage names the courtesy as 'a kind of derivative performance' he 'could no more produce... than he could speak a foreign language' — the obstacle is constitutional inability to execute a social register, not contempt, expertise gaps, or strategy."
            },
            {
                "q": "If a partner who had supported Reza's rotation were later told that the satellite office's productivity reflected the absence of central-office interference rather than Reza's contribution, that partner would most likely respond that",
                "opts": [
                    "the satellite office had always been competent and the rotation merely revealed it.",
                    "the two explanations are difficult to disentangle, since Reza's presence and the loosened oversight occurred together.",
                    "Reza's prolix style necessarily produced the productivity gains by tightening the office's drafts.",
                    "the rotation should be regarded as a failure on those grounds."
                ],
                "ans": 1,
                "why": "The passage itself frames the question as undecidable — was it correction or exile, his industry or only its failure to disintegrate the office — and the partners are 'divided and silent.' A supporter would echo precisely this confounding rather than concede or insist."
            }
        ]
    },
    {
        "title": "The Capitulation",
        "targets": [
            "capitulate","deplorable","ingratiate","dovish","tyrant","usurp","obsolete",
            "annihilate","rejuvenate","bombard","ennui","showcase","conceal","exacerbate",
            "freewheeling","forerunner","self-defeating","disintegrate","convulsion",
            "revisionary","airtight","apparel","skittish","disparage","incessant"
        ],
        "text": (
            "When the negotiating delegation finally capitulated, the published account was airtight — too "
            "airtight, said the few junior staffers who had been in the room. The delegation, the "
            "statement explained, had reached a difficult but principled accommodation with a counterpart "
            "whose dovish overtures had, at last, prevailed over its more hawkish faction. The "
            "counterpart, in this telling, was rejuvenated; the delegation was reasonable; the "
            "freewheeling decade of friction was now a thing decisively obsolete.\n\n"
            "What the airtight statement could not quite conceal — and what its careful apparel of phrasing "
            "had, in fact, drawn attention to — was the absence of any clear explanation for the speed of "
            "the concessions. The delegation had spent eighteen months bombarding the counterpart with "
            "demands; the entire structure had been overturned in four days. Veterans of comparable "
            "negotiations found the timing deplorable; ingratiating, even. To the freewheeling press of "
            "the smaller cities the agreement was a usurp-ation of a position the country had spent a "
            "generation showcasing.\n\n"
            "The lead negotiator, in a closed briefing reported only in fragmentary form, offered an "
            "explanation that the official statement had no way to incorporate. The counterpart, he said, "
            "had not in fact softened. The forerunner of the new agreement was not a dovish faction across "
            "the table but a quiet realization, on his side, that to continue bombarding the counterpart "
            "would exacerbate a domestic political convulsion his own ministry was no longer in any "
            "position to absorb. The capitulation, in other words, had been self-defeating from one angle "
            "and self-preserving from another, and the official statement had been written to make the "
            "two angles indistinguishable.\n\n"
            "Senior commentators were skittish about adopting either reading in full. To accept the lead "
            "negotiator's account was to disparage a delegation whose careers had been built on the very "
            "narrative they were now defending; to accept the official statement was to credit a tyrant's "
            "supposed conversion that none of the underlying signals supported. The ennui that settled "
            "over the press corps in the months that followed was, one columnist suggested, the most "
            "honest reaction available: a recognition that the actual story had already disintegrated "
            "into the only two accounts the public was permitted to hear."
        ),
        "questions": [
            {
                "q": "The passage's central argument is best summarized as the claim that",
                "opts": [
                    "the delegation's concessions reflected a genuine softening on the counterpart's side that observers had failed to recognize.",
                    "the official statement's tight construction itself made the absence of a credible explanation more conspicuous, leaving the public with two accounts neither of which was fully defensible.",
                    "the lead negotiator's private account exposes the delegation's leadership as motivated by personal political survival.",
                    "the press corps's eventual silence amounted to tacit endorsement of the agreement."
                ],
                "ans": 1,
                "why": "The narrator argues that the very airtightness of the public statement 'drew attention to' the missing explanation, and the final paragraph names the result as a public choice between two inadequate accounts. The claim is about the discursive structure produced by the statement, not about any one account being true."
            },
            {
                "q": "The lead negotiator's account in the third paragraph is offered chiefly to",
                "opts": [
                    "vindicate the delegation against its critics in the smaller-city press.",
                    "displace the official narrative's explanation of motive while leaving its public defense intact.",
                    "argue that the counterpart's hawkish faction had been overestimated by foreign observers.",
                    "explain why future agreements with the counterpart will be difficult to negotiate."
                ],
                "ans": 1,
                "why": "His account contradicts the official explanation of motive (dovish counterpart) but is delivered only in a closed briefing and 'fragmentary' form — i.e. it displaces the motive privately while leaving the public defense uncontradicted, which is exactly the dual-track structure the passage diagnoses."
            },
            {
                "q": "A reader who concluded from the passage that the official statement was straightforwardly false would have",
                "opts": [
                    "drawn the inference the passage's evidence most directly supports.",
                    "extracted only one of the two accounts the passage refuses to choose between.",
                    "accurately reconstructed the lead negotiator's confidential briefing.",
                    "correctly identified the position of the smaller-city press."
                ],
                "ans": 1,
                "why": "The closing paragraph explicitly notes that the actual story had disintegrated into 'the only two accounts the public was permitted to hear' — neither of which the passage endorses. A confident verdict on the official statement collapses the very ambiguity the passage is built to preserve."
            }
        ]
    },
    {
        "title": "The Numinous Stones",
        "targets": [
            "numinous","disquisition","verisimilitude","philosophy","acerbic","ennui",
            "abstain","modish","superstition","eclectic","prolix","fragmentary","conceal",
            "revisionary","derivative","apparel","skittish","incessant","tedious",
            "disparage","forerunner","negligible","unwarranted","reluctant","mandate"
        ],
        "text": (
            "The standing stones at Carn Esk were not, in the strictest sense, scientifically interesting. "
            "Their date was uncontroversial; their builders were anonymous in the ordinary way that the "
            "builders of such monuments are; their alignment with the solstices was real but unremarkable. "
            "Yet they had drawn, over a decade, an eclectic and incessant traffic of weekend visitors who "
            "described their experience of the site in language whose verisimilitude the local archaeologist, "
            "Dr. Lacey, regarded with growing ennui.\n\n"
            "Lacey's first published response was an acerbic disquisition — prolix, almost programmatic — "
            "in which he disparaged the visitors' reports as a kind of modish superstition derivative of "
            "the wellness industry. He proposed, in passing, that the local council mandate signage to "
            "correct the most egregious misapprehensions. The piece was widely circulated and produced, "
            "predictably, the opposite of its intended effect; visitor traffic increased, and Lacey's "
            "name, attached to the stones, became part of the appeal.\n\n"
            "His second piece, three years later, was revisionary in a way the first had given no warning "
            "of. It opened with a fragmentary apology — not for the substance of his earlier argument, "
            "which he still defended, but for its apparel. He had been, he wrote, skittish about the "
            "particular word 'numinous'; he had abstained from it in the first piece because he disliked "
            "the philosophy with which it had become entangled. But the word, properly understood, named "
            "something real about how human beings respond to certain configurations of stone, sky, and "
            "silence. To deny the experience because the wellness industry had appropriated the vocabulary "
            "was to concede to that industry a victory it had not, in fact, earned.\n\n"
            "Lacey's colleagues received the second piece with a mixture of respect and irritation. Those "
            "who had quoted the first piece in their own work felt the revision was unwarranted and a "
            "forerunner of softer pieces to come; those who had always found his acerbic tone tedious "
            "treated the revision as a negligible adjustment that left the underlying disparagement of "
            "visitors intact. Lacey, who had not solicited either response, declined to write a third "
            "piece. The stones, he had begun to think, deserved a quieter custodian than he had been; "
            "what they did not deserve was to be conceded, by his own irritability, to the people he had "
            "spent ten years insisting they did not belong to."
        ),
        "questions": [
            {
                "q": "The revision Lacey performs in his second piece is best characterized as",
                "opts": [
                    "a partial retraction in which he concedes that his earlier substantive claims were mistaken.",
                    "a refinement of vocabulary that preserves his earlier substantive claims while changing the rhetorical posture toward a contested word.",
                    "a public realignment with the wellness industry he had previously criticized.",
                    "a strategic concession designed to recover scholarly allies alienated by his first piece."
                ],
                "ans": 1,
                "why": "The third paragraph specifies that he 'still defended' the substance and apologized only for 'its apparel' — and the body of the revision concerns the word 'numinous' itself, not the underlying argument. The change is rhetorical-lexical, not substantive."
            },
            {
                "q": "Which of the following best describes the function of the second paragraph?",
                "opts": [
                    "It establishes the historical pattern of weekend visitation that the rest of the passage explains.",
                    "It illustrates a recurring dynamic in which polemical correction publicizes the very phenomenon it intends to suppress.",
                    "It introduces the local council whose policies the rest of the passage criticizes.",
                    "It demonstrates that Lacey's scholarly credentials are inadequate to the topic."
                ],
                "ans": 1,
                "why": "The paragraph's load-bearing observation is that the disquisition 'produced... the opposite of its intended effect' and that Lacey's own name became part of the site's appeal — i.e. a small case study of how polemic publicizes its target."
            },
            {
                "q": "Lacey's reasoning in his decision not to write a third piece most strongly relies on the principle that",
                "opts": [
                    "scholars should withdraw from public disputes once they have made their substantive arguments.",
                    "continuing to engage adversaries on their preferred terms can itself surrender ground that engagement was meant to defend.",
                    "the original audience for the stones — local visitors — should determine the terms of public discussion.",
                    "vocabulary contests are intrinsically less important than methodological ones."
                ],
                "ans": 1,
                "why": "Lacey's stated reason is that the stones should not be 'conceded, by his own irritability, to the people he had spent ten years insisting they did not belong to' — i.e. further engagement, even hostile, would itself cede the very ground he had fought for. The principle is about the strategic cost of continued polemic, not about general withdrawal or audience authority."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 22
# ---------------------------------------------------------------------------
NEW["22"] = [
    {
        "title": "The Voracious Sophist",
        "targets": [
            "voracious","sophist","posit","facile","refute","corroborate","clairvoyant",
            "obfuscate","adduce","plethora","unequivocal","preeminent","pithy","disavow",
            "anatomize","beguile","augur","figurative","magisterial","compulsory",
            "incommensurable","misconception","unseemly","compatible","tactful"
        ],
        "text": (
            "Whatever else one thought of Aurelio Castets, one had to admit he was voracious. He had read, "
            "if his admirers were to be believed, more philosophy than any of his contemporaries; he had "
            "adduced, in his most magisterial book, a plethora of sources that drew gasps from his "
            "reviewers and groans from anyone who had to track them down. His enemies called him a "
            "sophist. His defenders, in print, called him preeminent; in private, several of them used the "
            "word 'beguiling.'\n\n"
            "Castets's signature move was a kind of facile generosity. He would posit, in his opening "
            "chapter, that two famously incommensurable schools of thought were not in fact opposed at all "
            "but were, properly anatomized, compatible partners in a single deeper inquiry. The "
            "demonstration that followed was pithy, occasionally clairvoyant, and almost always "
            "underpowered relative to the claim. To refute it on its own terms was, his critics noted, "
            "compulsory work for any serious reader; to corroborate it required a generosity few "
            "specialists could muster.\n\n"
            "What troubled his more tactful interlocutors was not the ambition but the unequivocal "
            "register in which it was conducted. Castets did not present his syntheses as conjectural; he "
            "augured them as discoveries. Where a more careful writer would have disavowed the strongest "
            "form of his claim in a footnote, Castets compounded it in the next chapter. The misconception "
            "his readers acquired — that the disputes he treated had been settled by his treatment — was, "
            "his critics argued, not an unseemly accident but a function of the book's deliberate "
            "rhetorical design.\n\n"
            "Castets, who lived long enough to see his magisterial book outgrown by the field it had "
            "briefly captured, was figurative about the reception in his last interview. The book, he "
            "said, had been a fast door through which a generation of students had passed without paying "
            "the slower tolls the schools it treated would have charged. Whether they would, in time, go "
            "back and pay the tolls — or whether the door had simply admitted them to a country that did "
            "not, in fact, exist — was a question on which he claimed not to have an unequivocal view, "
            "and to which the most plausible answers were neither voracious nor pithy but unmistakably "
            "his own to bear."
        ),
        "questions": [
            {
                "q": "The passage's critics charge that Castets's books mislead readers in which of the following ways?",
                "opts": [
                    "By understating the empirical evidence required to support his syntheses.",
                    "By presenting conjectural reconciliations in a tone whose certainty exceeds what the demonstrations support.",
                    "By concealing his disagreements with his sources behind a pithy prose style.",
                    "By relying on a plethora of citations whose accuracy cannot be independently verified."
                ],
                "ans": 1,
                "why": "The third paragraph names the failure as Castets 'augur[ing] them as discoveries' and refusing to soften the strongest form — the gap is between the assertive register and what the underpowered demonstrations can sustain."
            },
            {
                "q": "Castets's own retrospective description of his book (\"a fast door...\") functions in the passage to",
                "opts": [
                    "endorse the critics' diagnosis while reframing its consequences as a calculated rhetorical choice.",
                    "refute the critics' diagnosis by appealing to the long-run pedagogical value of his synthesis.",
                    "concede that the demonstrations in his book were technically flawed.",
                    "predict that subsequent generations of students will return to his syntheses for guidance."
                ],
                "ans": 0,
                "why": "He does not deny that readers may have been admitted to 'a country that did not... exist' — i.e. he concedes the critics' essential charge — but reframes it as a chosen trade (a fast door, slower tolls deferred), accepting both possibilities as live."
            },
            {
                "q": "Which of the following, if true, would most weaken the critics' central objection to Castets as developed in the passage?",
                "opts": [
                    "Subsequent specialists, having read Castets in graduate school, frequently returned to the original schools and produced corrective scholarship of unusual rigor.",
                    "Castets had read more deeply in both schools than any contemporary critic.",
                    "Castets's book sold more copies than any competing synthesis of its decade.",
                    "Several of Castets's most outspoken critics had personal grievances against him."
                ],
                "ans": 0,
                "why": "The objection is that readers acquire a misconception that the disputes are settled. If readers in fact return to the originals and produce corrective scholarship, the alleged mis-impression is self-correcting and the rhetorical design (Castets's 'fast door' image) is vindicated. The other options either don't address the misconception (sales, depth of reading) or attack the critics' motives rather than their argument."
            }
        ]
    },
    {
        "title": "The Crestfallen Director",
        "targets": [
            "crestfallen","languid","profound","magisterial","exuberant","jovial","feeble",
            "vindicate","propitious","sinister","invasive","bourgeois","insolent","precarious",
            "weather","considerable","beguile","fortify","fathom","mutable","posture",
            "agitate","compassionate","corroborate","skim"
        ],
        "text": (
            "The director's curtain call on opening night was crestfallen in a way the audience could not "
            "fathom. The reviews would not arrive until morning; the cast had performed, by every visible "
            "indication, beyond his hopes; the producers, jovial in their box, had been exuberant enough "
            "during the second act to be heard by the ushers. And yet he came forward at the end of the "
            "applause with the languid bearing of a man who has, in his own count, weathered a small "
            "private failure.\n\n"
            "What had happened, those near him learned later, was a single moment in the third scene — a "
            "moment most viewers had not even registered — in which an actor had skimmed a line whose "
            "weight the director regarded as profound to the play's design. The actor's choice was not "
            "feeble. It was confident; it was, in its own register, a magisterial small interpretation. "
            "And it was, from the director's vantage, sinister to the architecture he had spent fourteen "
            "months building.\n\n"
            "His producers, when he confided the complaint, were compassionate but unimpressed. The play "
            "had landed; the audience was beguiled; the precarious commercial calculation that had "
            "fortified the production from the start had, in a single propitious evening, been vindicated. "
            "What was he agitating about? Nothing the bourgeois ticket-buyer would have noticed had been "
            "lost. The director, who had not, in his own view, posed a bourgeois question, found himself "
            "unable to corroborate his concern to people whose vocabulary did not contain the kind of "
            "weight he meant.\n\n"
            "He directed three more productions in the years that followed, all of them successful in "
            "exactly the way the producers preferred, and in none of them did he ever again entrust the "
            "load-bearing line of a scene to an actor whose interpretation had not, in advance, been "
            "negotiated to the punctuation. His company called the practice invasive. His critics called "
            "it controlling. The director himself, who had become — somewhere in those years — a quieter "
            "and less mutable colleague than he had been, never bothered to explain the practice in print. "
            "It was simply, he sometimes said, what one did after a single opening night had taught one "
            "what an audience could not, on its own, be expected to defend."
        ),
        "questions": [
            {
                "q": "The director's reaction at the curtain call is best understood as a response to",
                "opts": [
                    "a discrepancy between the audience's reception and his own assessment of the production's structural integrity.",
                    "a fear that the morning's reviews would be unfavorable.",
                    "a sudden recognition that the actor in question would resist further direction.",
                    "a private commercial conflict with the producers over future productions."
                ],
                "ans": 0,
                "why": "The opening paragraph notes the contrast between visible success and his bearing, and the second paragraph isolates the cause as a single moment 'most viewers had not even registered' but central to the play's design — i.e. the gap between reception and his own structural assessment."
            },
            {
                "q": "Which of the following best captures the producers' implicit assumption in their response to the director?",
                "opts": [
                    "That an artistic loss undetectable by the ticket-buying audience cannot be a loss the producers need to credit.",
                    "That the director's complaint about the actor was motivated by personal animus.",
                    "That the play's commercial success would protect the cast from future criticism.",
                    "That the director's standards reflected an outdated theatrical training."
                ],
                "ans": 0,
                "why": "The producers' question 'What was he agitating about? Nothing the bourgeois ticket-buyer would have noticed' equates the relevant audience with what the producers credit — making detectability by the audience the implicit criterion for what counts as a loss."
            },
            {
                "q": "The director's later practice of pre-negotiating load-bearing lines is presented in the passage as",
                "opts": [
                    "a vindication of the producers' commercial criteria in artistic form.",
                    "a private adaptation whose terms the director declined to translate into public argument, even as it shaped his subsequent work.",
                    "a punishment of the actor whose interpretation had unsettled him.",
                    "a concession to critics who had described his earlier methods as too permissive."
                ],
                "ans": 1,
                "why": "The closing paragraph emphasizes that he 'never bothered to explain the practice in print' and offered, when pressed, only an oblique remark about what an audience cannot defend on its own. The practice is presented as a private rule that organizes his work without ever being publicly justified."
            }
        ]
    },
    {
        "title": "After the Vaccine Hoax",
        "targets": [
            "clairvoyant","unequivocal","obfuscate","vaccinate","propaganda","plethora",
            "preeminent","disavow","refute","corroborate","facile","misconception",
            "compulsory","beguile","sophist","posit","resign","trigger","weather",
            "ministration","compassionate","dilute","tactful","testimony","ostensibly"[:-1] if False else "primitive"
        ],
        "text": (
            "The hoax had not been clairvoyant in any meaningful sense; it had merely been, like most "
            "successful propaganda, well-timed. A fabricated paper, dressed in the apparel of peer review, "
            "had circulated for eleven weeks before the journal could refute it, and by the time the "
            "preeminent voices in the field had disavowed its claims, the paper had been quoted in two "
            "national broadcasts and forwarded by a plethora of well-meaning friends. The vaccine "
            "campaign, ostensibly on track, had begun to falter in three regions where the testimony of "
            "private corroboration outweighed the unequivocal correction the ministry tried to issue.\n\n"
            "Dr. Tessa Park, who had spent the previous decade trying to vaccinate exactly these "
            "communities, was less surprised than her colleagues. She had argued, in conferences whose "
            "tactful protocols had often diluted her case, that the ministry's response model was a facile "
            "one: it posited a public that, once shown the unequivocal evidence, would necessarily resign "
            "its misconception. The model had been beguiling on paper. In practice, it produced a kind of "
            "sophist's bargain — the louder the official refutation, the more the misconception's holders "
            "treated it as obfuscation by an interested party.\n\n"
            "Park's own approach was compassionate but unromantic. She did not, in the affected districts, "
            "attempt to refute the hoax at all. She trained local nurses to deliver, in compulsory home "
            "visits, the ministration the campaign had been designed around — answer the question the "
            "patient actually had, not the one the ministry wished they had asked. The misconceptions, in "
            "her experience, did not weather such visits well; they required, like most propaganda, a "
            "distance the visits closed.\n\n"
            "The trouble with her approach, as several columnists noted, was that it did not scale. To "
            "make it the centerpiece of the next campaign would trigger a logistical strain the ministry "
            "could not absorb in the months available. Park, who had heard this objection often enough to "
            "predict its phrasing, replied — in print, with a directness her colleagues found bracing — "
            "that the question was not whether her method scaled but whether the existing model worked. If "
            "the existing model was producing the very outcomes it had been designed to prevent, the "
            "logistical convenience of continuing it could not, by itself, be a primitive form of "
            "argument."
        ),
        "questions": [
            {
                "q": "Park's critique of the ministry's model, as developed in the second paragraph, depends most centrally on the claim that",
                "opts": [
                    "the ministry's evidence is technically insufficient to refute the hoax.",
                    "loud official refutation can itself increase the apparent credibility of the very claim it refutes.",
                    "the affected districts are unusually resistant to medical interventions of any kind.",
                    "the ministry's communications staff is institutionally biased against community-level work."
                ],
                "ans": 1,
                "why": "Park's diagnosis is that 'the louder the official refutation, the more the misconception's holders treated it as obfuscation by an interested party' — the mechanism is that the form of correction itself signals self-interest and thereby strengthens the misconception."
            },
            {
                "q": "Park's reply to her columnist critics in the final paragraph turns most heavily on which of the following implicit principles?",
                "opts": [
                    "An intervention's scalability is morally secondary to its accuracy in any individual case.",
                    "An intervention that fails to produce its intended outcome cannot be defended primarily by appeal to its operational convenience.",
                    "Ministries should always prefer ambitious approaches over incremental ones, regardless of capacity.",
                    "Logistical objections to public-health proposals are typically motivated by political rather than technical considerations."
                ],
                "ans": 1,
                "why": "Her reply explicitly reframes the question as 'whether the existing model worked' and asserts that if it produces the outcomes it was designed to prevent, then 'logistical convenience... could not, by itself, be a primitive form of argument' — the principle is that operational ease cannot rescue a method that is failing on its own terms."
            },
            {
                "q": "Which of the following pairs of phenomena best parallels the structural relationship Park describes between official refutation and public misconception?",
                "opts": [
                    "A teacher correcting a student's error and the student adopting the corrected answer.",
                    "A government denial of a rumor giving the rumor's adherents new evidence of the very cover-up they suspect.",
                    "A scientist publishing a peer-reviewed paper that subsequent studies confirm.",
                    "A nurse explaining a medical procedure to a patient who then consents to it."
                ],
                "ans": 1,
                "why": "Park's mechanism is that the act of correction is itself absorbed as evidence for the position being corrected. The denial-as-confirmation pattern (option B) is the only structural analogue; the others depict ordinary information transfer without that feedback loop."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 23
# ---------------------------------------------------------------------------
NEW["23"] = [
    {
        "title": "The Staid Auctioneer",
        "targets": [
            "staid","melodramatic","modicum","fleeting","cosmopolitan","preliminary",
            "consternation","unflagging","fidelity","substantiate","precipitate","second",
            "telltale","occlude","grand","insufficient","platitudinous","despair","retreat",
            "convoluted","extraneous","reverse","stem","analogous","sound"
        ],
        "text": (
            "The auctioneer at Devereux's was famously staid. Where her cosmopolitan rivals across town "
            "favored a melodramatic style — the dramatic pause, the second cough that signaled the room's "
            "appetite had peaked — she conducted her sales with a fidelity to the preliminary catalogue "
            "that struck newcomers as a modicum of theater and connoisseurs as the only kind of fidelity "
            "that mattered. Her bidders, by reputation, did not panic. Her hammer prices, by record, were "
            "no lower than her rivals' over the long run.\n\n"
            "Her detractors in the trade press tried, fleetingly, to substantiate a different story. They "
            "argued that her staid manner occluded a precipitate willingness to second a known buyer's "
            "telltale tick of the catalogue and to retreat from competing bids that came from less "
            "established hands. The accusation was platitudinous in form and convoluted in evidence, and "
            "Devereux's responded only with the grand consternation appropriate to insufficient charges. "
            "The trade press, sensing no fresh material, moved on.\n\n"
            "Among her own staff, however, a quieter critique persisted. The youngest of her cataloguers, "
            "whom she had trained personally, observed that the auctioneer's unflagging composure had a "
            "stemming effect on the room. Bidders who would have, with a louder auctioneer, allowed their "
            "competition to escalate into the extraneous territory where the house earned its highest "
            "commissions, instead settled, in her room, just above the catalogue's reserve. To call this "
            "stemming a fault, the cataloguer admitted, was a reverse of the usual complaint about "
            "auctioneers; but it was, in its analogous way, equally a deviation from the soundest "
            "commercial conduct of a sale.\n\n"
            "The auctioneer, when the cataloguer brought the observation to her over coffee, did not "
            "despair. She agreed, with the modicum of warmth she granted to good arguments she did not "
            "intend to act on, that the room could probably be pushed harder. She had not chosen her "
            "style, she said, in order to maximize the house's commission; she had chosen it in order to "
            "make the catalogue mean something. The two aims were not always identical, and on the rare "
            "occasions when she had to choose between them, the catalogue won."
        ),
        "questions": [
            {
                "q": "The youngest cataloguer's observation is best characterized as a complaint that the auctioneer's manner",
                "opts": [
                    "deceives bidders into believing the catalogue's reserve prices are higher than they are.",
                    "discourages the competitive escalation from which the house derives its largest commissions.",
                    "favors established bidders over newcomers in a way the trade press has misdescribed.",
                    "obscures the true commercial value of items by adhering too literally to the catalogue."
                ],
                "ans": 1,
                "why": "The third paragraph names the effect as 'stemming' bidders who would otherwise allow competition to 'escalate into the extraneous territory where the house earned its highest commissions' — the complaint is precisely about lost upside from cooled competition."
            },
            {
                "q": "The passage's juxtaposition of the trade-press accusation and the cataloguer's observation is most likely designed to",
                "opts": [
                    "show that the auctioneer's reputation is unjust and the cataloguer's critique vindicates her.",
                    "distinguish a refutable charge of malpractice from a more interesting, internally-grounded observation about the cost of her style.",
                    "argue that all internal critiques of auctioneers tend to converge on the same commercial concerns.",
                    "suggest that the cataloguer was recruited by the trade press to develop a more credible attack."
                ],
                "ans": 1,
                "why": "The press attack is dismissed as platitudinous and unsubstantiated; the cataloguer's observation accepts the auctioneer's integrity and identifies a different kind of cost. The juxtaposition separates a discreditable accusation from a serious internal observation."
            },
            {
                "q": "The auctioneer's reply to the cataloguer in the final paragraph most strongly implies that she regards her staid style as",
                "opts": [
                    "an unintended consequence of a temperament she has not chosen.",
                    "a deliberate trade in which a measurable commercial loss is exchanged for an institutional aim she values more.",
                    "a strategy whose commercial benefits are systematically underestimated by her competitors.",
                    "a position she would reconsider if presented with better evidence."
                ],
                "ans": 1,
                "why": "She accepts that the room could 'probably be pushed harder,' explains she chose the style to 'make the catalogue mean something,' and notes that when the two aims conflict the catalogue wins — i.e. she concedes the cost and characterizes it as an accepted trade for a valued aim."
            }
        ]
    },
    {
        "title": "Untrammeled Ambition",
        "targets": [
            "untrammeled","overreach","sycophantic","venerate","salutary","fealty","preliminary",
            "humble","retreat","interdisciplinary","pioneering","obtuse","unflagging","stump",
            "labyrinthine","insidious","convoluted","despair","ostensible","brash","stir",
            "modicum","virtue","retract","like-minded"
        ],
        "text": (
            "The institute's founder had, in his retirement essays, described his career as an exercise in "
            "untrammeled curiosity. The phrase, taken up by his sycophantic biographers, became a kind of "
            "founding scripture. New hires were instructed to venerate it; the preliminary remarks at the "
            "annual lecture rarely failed to recite it; visiting fellows received, with their badges, a "
            "small printed card that summarized the institute's ostensible commitment to pioneering, "
            "interdisciplinary work, unconstrained by the labyrinthine professional norms it had been "
            "founded to escape.\n\n"
            "What the founder's own papers showed, when his successor finally read them carefully, was a "
            "more humble and more salutary record. The founder had, throughout his most pioneering "
            "decade, retreated repeatedly from his own brashest claims when colleagues he respected stumped "
            "him in seminar. He had retracted a small but consequential paper in his fifth year on the "
            "ground that a like-minded but more careful collaborator had identified an obtuse error he "
            "could not, on review, refute. Untrammeled the founder had been about the topics he chose to "
            "investigate; he had not been remotely untrammeled about the standards by which the "
            "investigations were judged.\n\n"
            "The successor's discovery did not, predictably, alter the founding scripture. The institute's "
            "sycophantic core treated the founder's retreats and retractions as private exercises of "
            "virtue that did not bear on the public doctrine. Visiting fellows continued to be told that "
            "the institute existed to defend untrammeled inquiry from the insidious constraints of "
            "ordinary scholarship. The convoluted result was that an institution founded by a "
            "self-correcting scientist had become, in its public life, a venue for the overreach he had "
            "himself spent thirty years declining to perform.\n\n"
            "The successor, who did not despair about institutions but did not entirely trust them either, "
            "made a small administrative change. The card given to new fellows was rewritten to include, "
            "alongside the founder's most stirring phrase, a single sentence summarizing the founder's "
            "retraction. The change produced, in the institute's first year under the new card, a modicum "
            "of confused complaint and, in its second year, no comment at all. Whether the silence "
            "indicated absorption of the lesson or its quiet repudiation was a question the successor "
            "preferred to leave, for the moment, open."
        ),
        "questions": [
            {
                "q": "The central tension the passage develops is between",
                "opts": [
                    "the founder's actual scholarly practice and the doctrine the institute built around a single phrase from his retirement essays.",
                    "the founder's early work and his later, more cautious publications.",
                    "the institute's interdisciplinary aims and the disciplinary expectations of its visiting fellows.",
                    "the successor's reformist instincts and the trustees' commercial concerns."
                ],
                "ans": 0,
                "why": "Paragraphs two and three contrast the actual record — humble retreats, a retraction, deference to like-minded colleagues — with the publicly venerated 'untrammeled inquiry' doctrine derived from a single phrase. That gap is the passage's central tension."
            },
            {
                "q": "The institute's sycophantic core, as described in the third paragraph, can be reconstructed as holding which of the following positions?",
                "opts": [
                    "That the founder's retractions were performed under coercion and should be discounted.",
                    "That private intellectual virtues a founder happens to exhibit need not constrain the public doctrine an institute extracts from his work.",
                    "That the founder's papers had been misinterpreted by his successor.",
                    "That interdisciplinary work necessarily depends on suspending ordinary scholarly correction."
                ],
                "ans": 1,
                "why": "The sycophantic core treats 'the founder's retreats and retractions as private exercises of virtue that did not bear on the public doctrine' — i.e. a clean separation of personal practice from extracted institutional creed."
            },
            {
                "q": "The successor's small administrative change is best understood as an attempt to",
                "opts": [
                    "force a confrontation with the sycophantic core through a publicly disruptive act.",
                    "introduce, at a low-cost institutional point, evidence that complicates the doctrine the institute teaches.",
                    "rewrite the founder's biography in a form more flattering to the successor's own views.",
                    "demonstrate that the institute's public doctrine had no foundation in the founder's papers."
                ],
                "ans": 1,
                "why": "The change is small, administrative (the welcome card), and adds the retraction alongside — not in place of — the famous phrase. The successor's design is to insert a complicating fact at a low-friction point, not to confront, to rewrite, or to refute the entire doctrine."
            }
        ]
    },
    {
        "title": "The Insidious Decay",
        "targets": [
            "corrode","decay","insidious","elucidate","episodic","convoluted","platitudinous",
            "invalidate","rudimentary","exactitude","retract","substantiate","occlude",
            "salutary","stump","analogous","fragile","reverse","preliminary","lurch",
            "imperceptible","despair","stir","extraneous","sound"
        ],
        "text": (
            "The structural engineer's report did not, in its preliminary form, look alarming. The bridge, "
            "Adekunle Lawal wrote, was suffering from a kind of insidious decay — corrosion at the joints "
            "where two previous repairs had left a fragile interface — and would, on the present "
            "trajectory, require either a full reverse-engineering of the 1972 modifications or a "
            "schedule of episodic interventions over the next twenty years. The rudimentary cost figures "
            "were, by Lawal's own admission, preliminary and approximate; the report's substantive case "
            "for elucidating the joint structure before any further repair, however, was sound.\n\n"
            "What complicated the report's reception was not its content but the political weather into "
            "which it lurched. The bridge had become, over the previous year, the rhetorical centerpiece "
            "of a convoluted municipal dispute about infrastructure priorities. To substantiate Lawal's "
            "preferred remedy — full re-engineering — would invalidate, by implication, the platitudinous "
            "claim a council faction had spent two years making, namely that the bridge was a triumph of "
            "the 1972 modifications and required only routine attention. Lawal's report, in other words, "
            "stumped a position the council had not yet retracted.\n\n"
            "The council's response was to treat the report as a fragile document whose extraneous "
            "elements — the cost estimates, the schedule — could be picked apart in committee until the "
            "load-bearing structural finding had been occluded by a thicket of subsidiary disputes. Lawal, "
            "who had seen the maneuver performed on previous reports, did not despair. He requested, in a "
            "calmly worded letter, that the structural finding be considered in isolation and that the "
            "cost estimates be set aside for a second, independent review. The request, salutary in form, "
            "was procedurally difficult to refuse.\n\n"
            "What followed was an exactitude that surprised even Lawal. The independent review confirmed "
            "the structural finding and produced, on the cost side, figures within ten percent of his own. "
            "The council, having committed in writing to the procedural sequence, found the substantive "
            "argument analogous to a wall it had built around itself. The platitudinous claim about the "
            "1972 modifications was, in the next meeting, quietly retracted — not by the faction that had "
            "made it, but by a different councillor whose neutral phrasing left no obvious victor. Lawal, "
            "asked later whether he had stirred this outcome deliberately, declined to answer. The bridge, "
            "he said, had been the only thing he had wanted to stir."
        ),
        "questions": [
            {
                "q": "Lawal's procedural request in the third paragraph is best understood as an attempt to",
                "opts": [
                    "prevent the council from accessing the detailed cost figures in his report.",
                    "isolate the technical finding from subsidiary disputes that the council was using to dilute it.",
                    "build a coalition with councillors who shared his structural assessment.",
                    "trigger a public hearing on the bridge's safety."
                ],
                "ans": 1,
                "why": "The third paragraph describes the council's strategy of occluding the structural finding 'by a thicket of subsidiary disputes,' and Lawal's request specifically separates the structural finding from the cost estimates — i.e. it neutralizes the dilution strategy."
            },
            {
                "q": "The passage suggests that the council's eventual retraction of the platitudinous claim was made possible primarily by",
                "opts": [
                    "a change in the political composition of the faction that had originally made the claim.",
                    "a procedural commitment the council had already made that left it no clean way to resist the substantive finding.",
                    "public pressure from independent engineers who supported Lawal.",
                    "Lawal's willingness to compromise on the structural finding."
                ],
                "ans": 1,
                "why": "The closing paragraph turns on the council 'having committed in writing to the procedural sequence' — that prior commitment is what made the substantive argument 'analogous to a wall it had built around itself,' enabling the retraction."
            },
            {
                "q": "The closing exchange (\"The bridge... had been the only thing he had wanted to stir\") is most naturally read as",
                "opts": [
                    "a denial that Lawal anticipated the political consequences of his procedural request.",
                    "a refusal to claim political credit while leaving open whether such credit might be due.",
                    "an admission that Lawal had been working with the councillor who issued the retraction.",
                    "a complaint that the technical finding had been subordinated to political theater."
                ],
                "ans": 1,
                "why": "The phrasing 'declined to answer' followed by 'the bridge... had been the only thing he had wanted to stir' redirects the question without denying or affirming the political design — a posture of deflection that leaves the political reading available without endorsing it."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 24
# ---------------------------------------------------------------------------
NEW["24"] = [
    {
        "title": "The Vituperative Memo",
        "targets": [
            "vituperate","malicious","treacherous","parochial","falsify","extrapolate",
            "preponderant","hostile","sequester","unyielding","pejorative","construe",
            "stubborn","abridge","misfeasance","mendacity","manipulate","procure",
            "consolidate","circumvent","welter","alleviate","blithe","brink","conducive"
        ],
        "text": (
            "The internal memo, when it leaked, vituperated its targets in language no senior manager had "
            "expected to see attached to a corporate signature. It accused a parochial coalition of "
            "midlevel officers of malicious mendacity in the procurement of two contracts and extrapolated, "
            "from a thin set of emails, a treacherous pattern that — if real — would constitute a "
            "preponderant case of misfeasance against the very managers who had countersigned the memo's "
            "release.\n\n"
            "What was missing from the memo, in the view of the firm's general counsel, was the "
            "elementary discipline that would have alleviated its more obvious vulnerabilities. The "
            "accusations had not been sequestered from the rhetorical frame in which they were delivered; "
            "they were welded to it. To construe the memo's claims charitably required setting aside its "
            "pejorative tone, and the firm's external readers were unlikely to perform that operation in "
            "the firm's favor. The memo, as a procedural matter, had abridged its own credibility.\n\n"
            "The author of the memo, an unyielding senior auditor named Maren Holt, defended it without "
            "apology. The procedural objection, she argued, was a way of manipulating the firm's attention "
            "away from the substantive findings; to circumvent the rhetoric, as the counsel proposed, was "
            "to circumvent the only thing that had finally forced the matter into a room where it could be "
            "addressed. She was not, she said, blithe about the document's vulnerabilities. She had simply "
            "made a calculation: a memo that consolidated the findings and falsified none of them, "
            "delivered in the only register that would not be filed away, was conducive to the outcome "
            "the firm needed even at the cost of being conducive to her own dismissal.\n\n"
            "The findings, after a stubborn three-month review, were largely substantiated. Two contracts "
            "were renegotiated; one midlevel officer resigned. Holt, who had been on the brink of "
            "termination through most of the review, was not in the end terminated but was, in the firm's "
            "preferred euphemism, 'reassigned' to a role from which her vituperative register would "
            "produce no comparable effect. Whether the firm had vindicated her or merely contained her was "
            "a question her supporters and her detractors continued to answer differently for years, "
            "without either side, so far as anyone could tell, having ever convinced the other."
        ),
        "questions": [
            {
                "q": "The general counsel's central objection to the memo is best summarized as",
                "opts": [
                    "the accusations it contained were factually wrong.",
                    "its rhetorical form was so welded to its substantive findings that the findings could not be evaluated independently of the tone.",
                    "the auditor lacked the authority to release such a document without senior approval.",
                    "the document violated procedural confidentiality rules in a way that exposed the firm to litigation."
                ],
                "ans": 1,
                "why": "The second paragraph identifies the failure as the accusations not being 'sequestered from the rhetorical frame' but 'welded to it,' so that charitable reading required setting aside the tone — a procedural-rhetorical critique, not a factual or jurisdictional one."
            },
            {
                "q": "Holt's defense, as developed in the third paragraph, depends on which of the following claims about her audience?",
                "opts": [
                    "That the firm's external readers could be expected to overlook the memo's tone.",
                    "That a more measured memo, however accurate, would have been filed away without producing the outcome the firm required.",
                    "That the firm's leadership shared her assessment of the targeted officers.",
                    "That her own dismissal was unlikely regardless of the memo's reception."
                ],
                "ans": 1,
                "why": "Holt's reasoning is explicit: the only register that would not be 'filed away' was the vituperative one, and she accepted the cost — including her own potential dismissal — for the sake of the substantive outcome. Her claim is about the firm's actual responsiveness to documents of different registers."
            },
            {
                "q": "The closing paragraph's account of Holt's 'reassignment' most strongly supports which of the following inferences about the firm's response?",
                "opts": [
                    "The firm publicly endorsed Holt's methods.",
                    "The firm absorbed Holt's substantive findings while neutralizing the institutional position from which similar memos could be written.",
                    "The firm intended the reassignment as a temporary measure pending a final decision on her status.",
                    "The firm regarded the vituperative tone as the chief reason for the contracts' renegotiation."
                ],
                "ans": 1,
                "why": "Two contracts were renegotiated and an officer resigned (findings absorbed); Holt was retained but moved to a role where her register 'would produce no comparable effect' (position neutralized). The combination is the structural meaning the passage marks: substantive uptake plus institutional containment."
            }
        ]
    },
    {
        "title": "The Gossamer Truce",
        "targets": [
            "gossamer","conciliatory","pellucid","equitable","alleviate","placate","accelerate",
            "deft","conducive","preliminary","construct","abridge","consolidate","provisional",
            "circumvent","disregard","stubborn","brisk","prompt","procure","welter","alleviate",
            "manipulate","unencumbered","accessible"
        ],
        "text": (
            "The truce between the two warehouse unions was gossamer in the sense that everyone who had "
            "negotiated it understood it would not hold. Its language was deliberately pellucid; its "
            "concessions, by design, were equitable enough to placate the rank and file of both sides "
            "without committing either leadership to a course that would alleviate the underlying dispute. "
            "The mediator who drafted the document, Sevda Kaya, called it provisional from the first "
            "preliminary meeting; her job, she told the parties, was not to consolidate a peace but to "
            "accelerate the moment at which the parties would discover what they actually disagreed "
            "about.\n\n"
            "Kaya was deft at this kind of work. She had, over a decade, constructed a quiet practice of "
            "what she called the unencumbered intermediate agreement — a document conducive to a brief "
            "calm during which the parties' real differences could surface in a less explosive form. To "
            "her critics in the field, the practice manipulated the parties into prompt agreements they "
            "would later be unable to circumvent; to her defenders, including most of the parties she had "
            "served, the practice abridged a welter of public conflict into a manageable private one.\n\n"
            "What the gossamer truce produced, in this case, surprised both her critics and her defenders. "
            "The brisk re-emergence of the underlying dispute, on a slightly accelerated timeline, was "
            "expected; what was not expected was the form it took. The two leaderships, having now "
            "experienced each other under the truce's mild constraints, were more disregarding of their "
            "own rank-and-file expectations than they had been before. They had each procured, in the "
            "truce, an accessible picture of what an equitable accommodation would look like, and neither "
            "had the appetite to manipulate the second negotiation back into the conciliatory register the "
            "first had occupied.\n\n"
            "Kaya, when the second round failed and the warehouse went briefly to strike, did not regard "
            "the failure as a defeat for her method. The strike was, by the standards of comparable "
            "industries, conducted with a stubborn restraint that surprised observers. Her gossamer truce "
            "had not held; it had not been meant to. It had alleviated the most acute risks of the first "
            "encounter and had given the parties' eventual confrontation a shape neither side, on its own, "
            "would have constructed. Whether that counted as success was, she said in a later interview, "
            "the kind of question only the parties themselves could answer — and only after enough years "
            "had passed for them to have forgotten how much worse the alternative had been."
        ),
        "questions": [
            {
                "q": "The passage's account of Kaya's method most strongly suggests that the gossamer truce was designed to",
                "opts": [
                    "convert a public conflict into a private resolution that neither party would later contest.",
                    "produce a calm interval during which the parties could discover and reframe the actual structure of their disagreement.",
                    "force one of the two leaderships to abandon its rank-and-file's demands.",
                    "demonstrate the limits of mediated negotiation in cases of entrenched institutional conflict."
                ],
                "ans": 1,
                "why": "Kaya describes her job as accelerating 'the moment at which the parties would discover what they actually disagreed about,' and the truce is provisional by design. The aim is diagnostic reframing through a calm interval, not resolution or coercion."
            },
            {
                "q": "The unexpected outcome described in the third paragraph is best summarized as",
                "opts": [
                    "the two leaderships becoming less responsive to their own rank-and-file's prior expectations as a result of the truce.",
                    "the strike being averted by an accelerated renegotiation.",
                    "the two leaderships forming a private coalition against Kaya.",
                    "the rank and file refusing to accept the second negotiation's outcomes."
                ],
                "ans": 0,
                "why": "The third paragraph specifies that the leaderships were 'more disregarding of their own rank-and-file expectations than they had been before' because the truce had given each an 'accessible picture' of an equitable accommodation. The unexpected element is precisely this loosening of internal constraints."
            },
            {
                "q": "Kaya's evaluation of her own method in the final paragraph relies most heavily on which of the following implicit standards?",
                "opts": [
                    "Whether the parties ultimately reached the agreement Kaya privately preferred.",
                    "Whether the structure of the eventual confrontation was better than the structure either party would have produced unaided, judged over a long enough horizon.",
                    "Whether the strike could have been entirely avoided through a more aggressive intermediate agreement.",
                    "Whether the mediator's reputation in the field improved as a result of the case."
                ],
                "ans": 1,
                "why": "Kaya defends the failed truce on the ground that the eventual confrontation took 'a shape neither side, on its own, would have constructed' and was less acute than the alternative — a counterfactual, long-horizon standard, not one tied to her preferences, total avoidance, or her reputation."
            }
        ]
    },
    {
        "title": "The Refractory Mayor",
        "targets": [
            "refractory","blithe","fanciful","mortify","mendacity","baleful","stoic",
            "punctilious","conciliatory","preponderant","provisional","prevalent","procure",
            "construe","construct","downright","threshold","pellucid","stalemate","enviable",
            "surmise","convoluted","disregard","preliminary","precede"
        ],
        "text": (
            "Mayor Eilis Brennan's reputation for being refractory was, in her first two terms, an "
            "enviable asset. She had built a coalition by being blithe about ordinances she found "
            "fanciful and downright punctilious about the few she found necessary. Her supporters "
            "construed the inconsistency as principle; her critics, more accurately, surmised that it "
            "reflected an idiosyncratic threshold for what counted as worth her time.\n\n"
            "In her third term the same temperament began to mortify the coalition that had built her. "
            "The preponderant question of the term — a long-running budgetary stalemate with the county — "
            "required a kind of patient, conciliatory negotiation for which her refractory habits were "
            "ill-suited. She could not bring herself to attend the preliminary meetings; she construed "
            "the county's procedural requests as a kind of provisional mendacity that preceded the larger "
            "bad-faith request she expected. The county officials, for their part, were not engaged in "
            "any such layered design. They were, prevalent in their own departmental difficulties, simply "
            "trying to procure a clean agreement before the fiscal year closed.\n\n"
            "When the stalemate finally broke, it broke against Brennan. A pellucid memo from the county's "
            "negotiator — leaked through routine channels rather than baleful ones — laid out, in "
            "punctilious detail, the three meetings Brennan had skipped, the four counter-proposals she "
            "had not answered, and the single occasion on which she had construed a routine procedural "
            "letter as 'downright mendacity.' The convoluted defense her staff attempted only consolidated "
            "the impression of a mayor whose refractory style had hardened into something less "
            "enviable.\n\n"
            "Brennan herself was stoic in public. Privately, with the small circle she trusted, she "
            "conceded that the temperament she had relied on for ten years had, in this case, disregarded "
            "the only kind of opposition that did not, in fact, deserve refractory treatment. The county, "
            "she said, had been telling the truth; her instinct had been calibrated for negotiating "
            "partners who lied, and could not, in this case, distinguish honest tedium from strategic "
            "evasion. The lesson was simple. What she did not know, and what the lesson did not tell her, "
            "was whether a temperament that had hardened over twenty years was, at this point in her "
            "career, available for revision."
        ),
        "questions": [
            {
                "q": "The passage suggests that Brennan's refractory temperament was effective in her earlier terms primarily because",
                "opts": [
                    "the issues she faced were less consequential than those of her third term.",
                    "the situations she navigated typically involved opposition whose bad faith her instincts were calibrated to detect.",
                    "her staff was more competent in the early terms than it later became.",
                    "the county was politically aligned with her coalition in the earlier terms."
                ],
                "ans": 1,
                "why": "The closing paragraph specifies that her 'instinct had been calibrated for negotiating partners who lied' — i.e. the temperament's earlier success rested on a fit between her detection instinct and the bad faith she usually faced, a fit that the county's good faith broke."
            },
            {
                "q": "The leaked memo from the county's negotiator damaged Brennan chiefly because it",
                "opts": [
                    "revealed previously unknown personal conflicts between Brennan and county officials.",
                    "documented, in a register her staff could not credibly recast, behavior consistent with the unflattering reading of her temperament.",
                    "introduced new substantive arguments against the city's negotiating position.",
                    "demonstrated that the county had been operating in bad faith throughout the negotiation."
                ],
                "ans": 1,
                "why": "The memo was 'pellucid' and 'punctilious in detail,' listing missed meetings, ignored counter-proposals, and a misconstrued letter — concrete acts that confirmed the unflattering reading, against which her staff's convoluted defense only consolidated the impression."
            },
            {
                "q": "The final paragraph's closing question — whether her temperament is available for revision — most directly conveys",
                "opts": [
                    "an optimistic suggestion that she has begun to change.",
                    "a recognition that diagnosis of the failure does not, by itself, indicate that the underlying disposition can be altered at this stage.",
                    "a determination to resign rather than attempt change.",
                    "a warning to her staff that further failures will not be tolerated."
                ],
                "ans": 1,
                "why": "The paragraph distinguishes the lesson (clearly understood) from the question of whether a 'temperament that had hardened over twenty years' could be revised — i.e. analytical understanding is not the same as the practical capacity to change, which the question deliberately leaves open."
            }
        ]
    },
]

# ---------------------------------------------------------------------------
# LIST 25
# ---------------------------------------------------------------------------
NEW["25"] = [
    {
        "title": "Beleaguered",
        "targets": [
            "beleaguer","ardent","mercurial","perpetuate","demolish","fanatic","luminary",
            "dismantle","economy","reciprocate","obliterate","spurn","flagrant","succumb",
            "pertinent","duplicate","slew","conspicuous","makeshift","equable","liken",
            "tenuous","scrupulous","ethereal","abhor"
        ],
        "text": (
            "Bashar Najem had been beleaguered for nearly a year. The biology institute he had founded "
            "with three colleagues had succumbed, over the previous summer, to the kind of mercurial "
            "trustee dispute that even ardent supporters had warned him about from the institute's "
            "founding. The original luminary patron was now openly hostile; a slew of smaller donors had "
            "spurned the next round of fundraising; the makeshift governance structure they had used in "
            "the first three years was being dismantled, faster than Najem could replace it, by trustees "
            "who likened the original arrangement to a fanatic's economy of scale.\n\n"
            "What Najem found most demoralizing was not the prospect that the institute might be "
            "obliterated — he had reckoned with that possibility from the start — but the flagrant "
            "willingness of trustees who had previously been scrupulous to perpetuate, in their public "
            "statements, a tenuous account of the institute's history that pertained to the present "
            "dispute only as cover. The trustees had, in private, been equable enough about the messy "
            "compromises that had made the institute possible; in public they now spoke as if those "
            "compromises had been ethereal lapses one of their number had heroically resisted.\n\n"
            "Najem chose not to reciprocate in kind. He authorized, against his lawyer's advice, the "
            "release of a brief duplicate of the original founding minutes — minutes whose conspicuous "
            "absence from the trustees' public chronology was, in his view, the document that mattered. "
            "He did not annotate the minutes. He did not, in any accompanying remarks, attempt to "
            "dismantle the trustees' newer narrative. He simply made the original record available and "
            "let the discrepancy do its own work.\n\n"
            "The response was less than he had hoped and more than his lawyer had feared. The original "
            "luminary patron, who had not seen the minutes in years, abhorred the public reopening of "
            "questions he had thought safely closed; two of the more equable trustees, however, took the "
            "minutes as a quiet permission to revise their own positions. The institute was not saved. "
            "What was saved was the harder, longer thing: a record against which any future account of "
            "the institute's founding would now have to argue rather than simply pretend. Najem, who had "
            "stopped sleeping well, treated this outcome as the most his year of being beleaguered was "
            "likely to yield."
        ),
        "questions": [
            {
                "q": "Najem's decision to release the original founding minutes rests most directly on the judgment that",
                "opts": [
                    "annotated commentary would lend the trustees' narrative more credibility than silence.",
                    "an unannotated documentary record, by making the trustees' selective public chronology visible by contrast, would discipline future accounts of the institute more effectively than argument.",
                    "the original luminary patron would, on seeing the minutes again, change his position.",
                    "the lawyers' procedural objections to release were legally unfounded."
                ],
                "ans": 1,
                "why": "Najem releases the minutes without annotation or accompanying argument and 'let[s] the discrepancy do its own work.' His judgment is that the documentary contrast itself disciplines future narratives more effectively than he could by argument — a structural rather than persuasive bet."
            },
            {
                "q": "Najem's distinction between the trustees' private candor and their public statements is offered chiefly to",
                "opts": [
                    "demonstrate that the trustees' positions were inconsistent in ways the founding compromises themselves had been.",
                    "establish that the public account misrepresents history the trustees themselves had previously acknowledged, so that the flagrant element is the disavowal rather than the original compromises.",
                    "suggest that the trustees were privately willing to settle the dispute on terms favorable to Najem.",
                    "argue that the founding compromises should never have been undertaken."
                ],
                "ans": 1,
                "why": "The second paragraph notes that trustees who 'had previously been scrupulous' were now perpetuating a 'tenuous account' that they had been 'equable enough about' in private. The point is the disavowal, not the original compromises — the flagrant element is the public revisionism, which the private record contradicts."
            },
            {
                "q": "The final paragraph's claim about what was \"saved\" most strongly supports which of the following readings of the institute's outcome?",
                "opts": [
                    "The institute survived in altered form thanks to Najem's intervention.",
                    "The institute did not survive, but the documentary basis for any future account of its founding was preserved against revisionism.",
                    "The institute's collapse was a delayed effect of the original founding compromises rather than of the trustee dispute.",
                    "The institute's collapse vindicated the luminary patron's original objections."
                ],
                "ans": 1,
                "why": "The paragraph explicitly states 'The institute was not saved' and identifies what was saved as 'a record against which any future account... would now have to argue rather than simply pretend' — survival of the record, not the institute."
            }
        ]
    },
    {
        "title": "The Brittle Compromise",
        "targets": [
            "brittle","repudiate","succumb","embargo","compromise","makeshift","tenuous",
            "compromise","duplicate","slew","conspicuous","tenuous","emulate","extirpate",
            "garner","interlope","ostentatious","facilitate","liken","involuntary","despot",
            "obedience","mercurial","constitute","economy"
        ],
        "text": (
            "The deal that ended the trade dispute was brittle from the day it was announced. The two "
            "sides had repudiated, in the negotiating room, exactly the positions they would have to "
            "succumb to in public; the embargo provisions were a makeshift compromise neither delegation "
            "could explain to its own base; and the press release, conspicuous in its decorative "
            "language, had been written by a junior staffer who had been involved in none of the "
            "substantive talks. The tenuous nature of the agreement was visible to any reader willing to "
            "compare its public claims to the slew of unanswered questions it left in its annexes.\n\n"
            "The senior negotiator on the larger side, when asked privately why the delegation had "
            "garnered nothing more durable, was unsentimental. The deal, he said, was not designed to be "
            "durable; it was designed to facilitate a six-month interval during which the smaller side's "
            "leadership could be replaced through ordinary political processes that the deal would not "
            "interlope upon. To repudiate the deal openly would have constituted, by the smaller "
            "leadership, a kind of involuntary obedience to its own most despotic faction — exactly the "
            "outcome the negotiation had been intended to extirpate. The mercurial duplicate the deal "
            "left on the smaller side's desk was, in his account, the price of buying the leadership "
            "enough internal time to do what it could not do under the embargo's open pressure.\n\n"
            "He did not pretend the strategy was admirable. It was, he said, a kind of ostentatious "
            "modesty: a public document whose decorative incompleteness emulated a real settlement "
            "without committing either side to the substantive terms a real settlement would have "
            "required. He liked the deal less than his counterparts on the smaller side liked it, which "
            "was perhaps why neither delegation had asked him to defend it in public.\n\n"
            "Whether the strategy worked depended, almost entirely, on what happened in the smaller "
            "side's internal politics in the months that followed. The leadership did, in the end, "
            "consolidate; the despotic faction did not capture the executive; the brittle compromise was "
            "quietly superseded by a more durable agreement nine months later that resembled, in its "
            "substance, what neither delegation had been able to negotiate the first time. The brittle "
            "deal, by then, had been almost entirely forgotten — a fact the senior negotiator counted, "
            "in private, as its primary measure of success."
        ),
        "questions": [
            {
                "q": "The senior negotiator's defense of the brittle deal rests most centrally on the claim that",
                "opts": [
                    "the deal's incompleteness was a deliberate concession to the larger side's domestic constituencies.",
                    "the deal's primary purpose was to create political space within which the smaller side's leadership could survive its internal opposition.",
                    "the deal's substantive terms reflected the best achievable settlement at the time.",
                    "the deal would necessarily have collapsed if the smaller side's leadership had been more decisive."
                ],
                "ans": 1,
                "why": "The negotiator describes the deal as designed to 'facilitate a six-month interval' for ordinary political processes that would extirpate the despotic faction — i.e. its purpose is to protect a window for the smaller side's internal politics, not to settle substance."
            },
            {
                "q": "The phrase \"ostentatious modesty\" in the third paragraph names a strategy whose central feature is",
                "opts": [
                    "a public display of restraint that conceals a privately maximalist position.",
                    "a public document whose conspicuous incompleteness simulates a settlement while binding neither side to substantive terms.",
                    "a deliberate choice to credit junior staff for senior achievements.",
                    "a refusal to take public credit for an agreement one privately authored."
                ],
                "ans": 1,
                "why": "The passage glosses 'ostentatious modesty' as 'a public document whose decorative incompleteness emulated a real settlement without committing either side to the substantive terms a real settlement would have required' — the structure is decorative simulation without binding substance."
            },
            {
                "q": "The negotiator's view that the deal's eventual obscurity was its 'primary measure of success' is most consistent with which of the following implicit principles?",
                "opts": [
                    "Agreements should be designed for their stated public function rather than for any unstated political effect.",
                    "An intermediate instrument whose role is to enable a later, more substantive agreement is best evaluated by what the later agreement makes possible, not by the intermediate instrument's own durability.",
                    "Negotiators should accept public criticism of their methods so long as the substantive outcome is favorable.",
                    "Brittle compromises are typically the most resilient form of international agreement."
                ],
                "ans": 1,
                "why": "The negotiator counts the deal a success because it was 'almost entirely forgotten' after the durable agreement nine months later — i.e. its job was to enable the later substantive deal, and being supplanted is what success looks like for an enabling instrument."
            }
        ]
    },
    {
        "title": "Sluggish Habits",
        "targets": [
            "sluggish","enervate","tenuous","scrupulous","garner","constitute","obedience",
            "perpetuate","liken","makeshift","reckon","ardent","aberration","brittle",
            "extirpate","luminary","reciprocate","embargo","fanatic","constitute","emulate",
            "involuntary","economy","spurn","duplicate"
        ],
        "text": (
            "The training program had been designed to extirpate, over a single residency year, the "
            "sluggish habits that the chief had likened — at the previous year's retreat — to a kind of "
            "involuntary professional erosion. The residents were ardent at the start and scrupulous "
            "almost to the point of fanaticism in the first months. By the residency's midpoint they had "
            "garnered the chief's careful praise. By its endpoint a small but conspicuous slew of them "
            "had reverted, in tenuous but recognizable ways, to the very habits the program had been "
            "constituted to dismantle.\n\n"
            "What the chief had not adequately reckoned with was that the program's most rigorous "
            "elements relied on a brittle external scaffolding — formal weekly reviews, makeshift "
            "duplicate documentation, a luminary visiting faculty whose obedience to the protocol the "
            "residents had emulated almost involuntarily. When the scaffolding was withdrawn at the end "
            "of the year, as the program's design required, the residents were not, in fact, ready to "
            "perpetuate the practices on their own economy. They had performed the protocols under the "
            "embargo of the visiting faculty's attention; they had not, in any deep sense, internalized "
            "them.\n\n"
            "The chief's reaction to the residency's mixed evaluation was, by the standards of senior "
            "physicians, unusually candid. The program, she wrote in a memo distributed to the next "
            "year's cohort, had failed to distinguish between obedience to a protocol under visible "
            "review and the genuine reciprocation of its underlying values. To spurn the easy reading — "
            "that some residents had simply regressed — she would, in the coming year, dismantle the most "
            "ostentatious of the program's enforcement structures, even at the cost of a less impressive "
            "midyear evaluation. The aberration she wanted to extirpate, she said, was not the residents' "
            "regression but the program's own design, which had reliably produced the appearance of the "
            "habit without the habit itself.\n\n"
            "Her own senior faculty were skittish about the change. To liken their previous year's work "
            "to an enervating exercise in surveillance was, several of them suggested, a brittle reading "
            "of evidence that could equally support a more conservative interpretation. The chief did not "
            "argue with them in print. She did, however, file the original program's evaluation forms in "
            "a place she could find them, on the working assumption that her own change would itself need "
            "to be evaluated against a record neither she nor her detractors would, in two years' time, "
            "be able to manipulate after the fact."
        ),
        "questions": [
            {
                "q": "The chief's diagnosis in the third paragraph turns on which of the following distinctions?",
                "opts": [
                    "Between residents who are technically skilled and those who are not.",
                    "Between behavior produced by visible enforcement and behavior that survives the withdrawal of enforcement.",
                    "Between protocols that are well-designed and those that are not.",
                    "Between residents who are ardent at the start of training and those who are not."
                ],
                "ans": 1,
                "why": "The chief's memo distinguishes 'obedience to a protocol under visible review' from 'the genuine reciprocation of its underlying values,' and the second paragraph attributes the failure to performance under the embargo of the visiting faculty's attention rather than internalization."
            },
            {
                "q": "The chief's planned reform — dismantling the most ostentatious enforcement structures — is best understood as a wager that",
                "opts": [
                    "weaker enforcement will produce, in the short term, more impressive residency evaluations.",
                    "the genuine internalization of the underlying habits can be tested only by removing the scaffolding that has been substituting for it.",
                    "residents will perform better under a less rigorous program because they are less stressed.",
                    "senior faculty will resist the reform and thereby validate its premises."
                ],
                "ans": 1,
                "why": "The chief accepts 'a less impressive midyear evaluation' explicitly as the cost of the reform; the reform's logic is that the appearance of the habit (produced by enforcement) needs to be distinguished from the habit itself (which only the absence of enforcement can test)."
            },
            {
                "q": "The chief's quiet decision to preserve the original evaluation forms most strongly suggests that she",
                "opts": [
                    "anticipates being asked to resign and wants the documentation available for an appeal.",
                    "expects her reform's evaluation to be contested and wants a record her opponents cannot retroactively reshape.",
                    "has lost confidence in her own diagnosis and is preparing to retract it.",
                    "intends to publish a comparative study of the two cohorts."
                ],
                "ans": 1,
                "why": "She files the forms 'on the working assumption that her own change would itself need to be evaluated against a record neither she nor her detractors would, in two years' time, be able to manipulate after the fact' — i.e. she anticipates contested evaluation and is locking in evidence."
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
