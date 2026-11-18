import json,sys,re
sys.path.insert(0,'src');from novel_fmr import FMR
EN_T="The First Man in Rome (Colleen McCullough, 1990)"
EN_I="""Colleen McCullough's novel is set between 110 and 100 BC. It follows the rise of two men: Gaius Marius, the provincial “new man” who would be consul seven times, and Lucius Cornelius Sulla, the impoverished patrician. In the background are the war against Jugurtha, the Germanic invasions and the fall of the tribune Saturninus. On the novel's first pages Marius is still hopelessly waiting for the consulship; on the last he is the first man in Rome.

This is a literary walk: it follows the plot of the novel, not a historical account. McCullough drew on many sources, but the characters' private lives, much of the dialogue and several minor figures (Lucius Decumius, for example) are the novel's invention. Where an ancient source also records an event, this is noted separately. References give the volume and page of the Hungarian edition (Árkádia, 1991): I. 12 = volume one, page 12."""
S=[
("New Year on the Palatine: the area Flacciana","""The novel opens at a rainy dawn on 1 January 110 BC. The senator Gaius Julius Caesar, grandfather of the later dictator, lives on the Palatine, in a narrow alley that opens onto the Clivus Victoriae (I. 12). His wife Marcia and their two daughters, Julia and Julilla, do not join the procession: they go along the Clivus Victoriae to a grassy, empty plot with a view over the whole Forum and the Capitol. This is the area Flacciana, the site of the demolished house of Flaccus; from here they watch the new consuls' inauguration (I. 12–14, 32).

The house next door belongs to Clitumna, Sulla's stepmother. Sulla, now thirty, was born a patrician but is so poor that he cannot enter the senate; his stepmother and his mistress Nicopolis keep him (I. 28–30). That morning he goes up to the hillside, needles two noble ladies whose lover he has been, and here sees Caesar's younger daughter, Julilla, close up for the first time (I. 32–33). From the hill the marks of the summer fire are still visible: it burned the Viminal and part of the Esquiline (I. 31–32).

Beyond the novel: the house of Marcus Fulvius Flaccus, ally of Gaius Gracchus, was demolished in 121 BC, and the site was afterwards called the area Flacciana (Cicero, De domo sua 102). Its exact location is unknown; the marker stands on the Forum side of the Palatine, on the site of the later Domus Tiberiana, beside which the Clivus Victoriae ran."""),
("The consuls' inauguration on the Capitol","""The processions of the two new consuls, Marcus Minucius Rufus and Spurius Postumius Albinus, merge in the Forum and climb the Clivus Capitolinus with the knights at their head. At the first bend the priests wait with the two white sacrificial bulls; the procession reaches the temple of Jupiter Optimus Maximus (I. 14–15). Gaius Marius stands in the crowd: he was praetor five years ago, has waited three years for the consulship, and feels that because he is not of noble birth he will never get it (I. 15).

Sulla goes down the Stairs of Vesta to the Forum and joins the back of the crowd in front of the temple. The sacrifice goes badly, the bull dies hard, and Sulla looks with foreboding at the mediocre nobles. Then he notices a former praetor with great eyebrows and a scarred face who reminds him of an eagle: Marius (I. 34–35). Meanwhile Jugurtha, king of Numidia, sits in his rented villa on the slope of the Pincian, because as a king he may not cross the city's sacred boundary, the pomerium (I. 35–36)."""),
("The Subura: the crossroads tavern","""Jugurtha wants to have his cousin Massiva, a rival claimant to the Numidian throne, killed in Rome, but the killer must be a Roman. His confidant Bomilcar goes into the Subura in plain clothes: from the Argiletum through the Fauces Suburae to the Subura Maior, and from there onto the Vicus Patricius, which leads towards the Viminal. Where the Subura Minor runs into it, on a triangular open space, he finds a tavern beside the crossroads shrine and fountain (I. 104–105).

It is the tavern of the crossroads college (collegium); its custodian is Lucius Decumius, a scrawny little man who always smells of onions. Bomilcar finds his assassin here: Decumius himself (I. 106–113, 119). Decumius remains an important character to the end of the novel. Aurelia's apartment block will later stand in the same triangle (see stop 7).

The line of the Vicus Patricius survives in today's Via Urbana."""),
("The murder of Massiva before the temple of Castor","""In the second week of January Marcus Livius Drusus celebrates a triumph. Massiva watches it in the Circus Maximus as the guest of the consul Albinus, then hurries ahead with the consular guests up the Stairs of Cacus, over the Palatine and down the Stairs of Vesta to the Forum, to watch the procession enter along the Via Sacra beside the consuls in front of the temple of Castor and Pollux (I. 113). In the crush he falls behind his escort. Decumius stabs him and vanishes into the white-togaed crowd towards the Argiletum (I. 113–114).

Bomilcar is arrested and locked up in the Lautumiae, the prison in the old quarry on the side of the Capitol (I. 118).

Beyond the novel: the murder of Massiva is historical. According to Sallust, Bomilcar hired the assassins; the killer was caught, Bomilcar fled, and it was then that Jugurtha called Rome a city for sale (Jugurthine War 35). The killer's name and the setting on the day of a triumph are the novel's invention."""),
("Marius elected consul (108 BC)","""Marius is fighting in Africa as Metellus's legate and has difficulty getting leave for the consular elections. After a swift crossing he rides into the Forum and, still without the white candidate's toga, registers as a candidate at the table of the consul presiding over the election; the crowd cheers him (I. 276).

The assembly of the centuries meets on the Campus Martius, at the voting ground called the saepta. Lucius Cassius Longinus is elected first consul; for the second place the race between Marius and Quintus Lutatius Catulus Caesar is so close that it is decided only when the third class votes: Marius wins (I. 278). That evening they celebrate at the house of his father-in-law Caesar, where Marius meets the household's other future son-in-law, Sulla (I. 279).

Beyond the novel: Marius won the consulship for the following year in 108 BC (Sallust, Jugurthine War 73). The republican voting ground lay in the same part of the Campus Martius where Caesar and Augustus later built the marble Saepta Iulia; the marker stands on it."""),
("The army of the poor (107 BC)","""As consul, Marius announces in the senate, in the Curia Hostilia, that he will also recruit soldiers from the propertyless citizens (capite censi). The senators shout in outrage (I. 317). Marius walks out with his quaestor Sulla and the tribune Manlius Mancinus, and turns to the people from the speakers' platform of the Comitium, the rostra. He asks for an army equipped, trained and paid by the state; the crowd cheers, and the other nine tribunes dare not veto (I. 318–319). After the law is passed, Scaurus, the leader of the senate, speaks against Marius in the senate (I. 320).

Beyond the novel: according to Sallust, Marius did recruit from the capite censi (Jugurthine War 86). The African command was given to him by the popular assembly on the proposal of the tribune Titus Manlius Mancinus (Jugurthine War 73)."""),
("Aurelia's apartment block in the Subura (105–100 BC)","""Aurelia, niece of Marcus Aurelius Cotta, marries the younger Gaius Julius Caesar. An apartment block (insula) is bought with Aurelia's money; Cotta finds one in the middle of the Subura. It is a well-built nine-storey house with eight shops, and it fills the whole triangle where the Subura Minor runs into the Vicus Patricius. It stands over a main sewer, so it even has a bathroom and a latrine (I. 445–448). They pay ninety-five talents for it; after the April wedding the wedding party walks through the Subura, and the whole neighbourhood cheers the bride (I. 448–450).

Aurelia lives in the ground-floor apartment and manages the building herself. She may not charge rent for the crossroads tavern in the house; its custodian is Lucius Decumius, who adores Aurelia and regularly sends her flowers (II. 273–274). Here, on the 13th of Quinctilis (July) 100 BC, their son is born: Gaius Julius Caesar, the later dictator (II. 287).

Beyond the novel: according to Suetonius, Caesar lived in his youth in a modest house in the Subura (Divus Iulius 46). The apartment block and the tavern are the novel's invention. The sources give Caesar's birthday as 12 or 13 July."""),
("Jugurtha's end in the Tullianum (104 BC)","""On 1 January 104 BC Marius celebrates his triumph and on the same day enters his second consulship. The evening before, Jugurtha was the guest of Metellus Numidicus and dined on snails. At dawn on the Campus Martius, by the Villa Publica, Sulla, who is staging the triumph, tells him that he will not be strangled: he will be thrown alive into the pit of the Tullianum (II. 14–15). The procession passes along the Vicus Tuscus, through the Forum Boarium and the Circus Maximus, behind the Palatine, then over the Velia and down the Via Sacra into the Forum. Jugurtha is disappointed: the buildings are small and old (II. 17–18).

At the lower end of the Forum his walk ends. At the foot of the Capitol, below the Gemonian Stairs, stands the Tullianum, a single small building of great stones. He is stripped and led to the round opening gaping in the floor. Jugurtha does not wait for the ladder: without a sound he steps into the pit himself (II. 19–20).

Marius reaches the temple of Jupiter by noon. Afterwards he is about to go to the senate's inaugural meeting in his triumphal dress, his face still painted, but Sulla stops him and sends him home to change (II. 20–21).

Beyond the novel: according to Plutarch, Jugurtha was thrown into the prison pit after the triumph and died of starvation six days later (Marius 12)."""),
("Caepio's trial in the Comitium (103 BC)","""Quintus Servilius Caepio, who embezzled the gold of Tolosa and through whose fault the Roman army was destroyed at Arausio, is brought before the popular assembly. The tribune Gaius Norbanus prosecutes him. Two tribunes, Titus Didius and Lucius Aurelius Cotta, try to veto, but the crowd drags them off the rostra, stones fly, and one stone hits Scaurus, the leader of the senate (II. 94–95).

One after another the tribes find Caepio guilty and vote a heavy penalty. Caepio is taken to the Lautumiae prison; his supporter Antistius announces that he will get him out, since no one condemned to exile has ever been imprisoned, and Norbanus mockingly lets him go (II. 95–97).

Beyond the novel: Cicero also discusses Norbanus's trial and the violence around it (De oratore 2.197–203)."""),
("The murder of Nonius in the Carinae (101 BC)","""In the tribunician elections Saturninus comes only eleventh, though there are ten places. One of those elected is the rich Picene Quintus Nonius, the elder brother of Sulla's brother-in-law (II. 257). That evening, on his way home, in the first alley of the Carinae, a dozen men with clubs fall on him and kill him together with two friends (II. 258).

Glaucia is presiding over the election. In the empty Forum he announces that Nonius's place goes to the next candidate, Saturninus. Later he tells Saturninus only that if he asks no questions, he will not have to be lied to (II. 258–259).

Beyond the novel: according to Appian, Nonius was killed by the men of Saturninus and Glaucia, and Saturninus was then elected tribune (Civil Wars 1.28)."""),
("The oath: the temple of Semo Sancus on the Quirinal (100 BC)","""Saturninus's second land law requires every senator to swear an oath to it, not in the usual place, the temple of Saturn, but in the open-air shrine of Semo Sancus Dius Fidius on the lower summit of the Quirinal (II. 274). Anyone who refuses is to be banished from Italy, fined twenty talents and deprived of his citizenship (II. 274–275).

In the senate Marius announces that he will be the first to swear. Scaurus then asks for his private opinion; Marius is forced to admit that in his view the law is probably invalid, and so loses Saturninus's trust (II. 280–281). Metellus Numidicus will not swear. He announces that at dawn the next day he will go into exile on Rhodes, and has the fine brought in, forty sacks of money; his stammering son, the treasury quaestor, has to count it aloud (II. 282–283).

Beyond the novel: Metellus Numidicus refused the oath and went into exile (Plutarch, Marius 29; Appian, Civil Wars 1.29–31). The temple of Semo Sancus stood on the Quirinal, near the Porta Sanqualis; its exact location is unknown. The marker is at the neighbouring temple of Salus."""),
("The murder of Memmius on election day (100 BC)","""In late autumn the consular candidates set off for the saepta to present themselves. Gaius Memmius, whom everyone expects to be the next consul, walks from the Palatine with his supporters. Where the road down from the Quirinal meets the Via Lata, he runs into Glaucia, who is wearing the white candidate's toga against Marius's ban. Words lead to blows: Glaucia's men draw clubs, and Glaucia himself beats Memmius to death (II. 324–326).

Saturninus is in the saepta canvassing for his friend's candidacy when he hears the news; among the angry young senators he sees Sulla, and he flees to the Quirinal (II. 326). Marius stands with Sulla beside the body and says that what is natural on the battlefield is horrifying on the Field of Mars, under the walls of the city (II. 332–333).

Beyond the novel: according to Appian, Memmius was clubbed to death at the consular elections by the men of Glaucia and Saturninus (Civil Wars 1.32). The marker is at the saepta; in the novel the murder happens on the way, beside the Via Lata."""),
("The temple of Bellona: the senate's ultimate decree","""Marius summons the senate to the temple of Bellona, outside the pomerium. Meanwhile news arrives that Saturninus and the mob have occupied the Forum. On Scaurus's proposal the senate unanimously passes the ultimate decree (senatus consultum de re publica defendenda), empowering the consul to defend the Republic (II. 333–334).

Marius appoints Sulla his deputy and has the weapons stored in the temple's cellar handed out. About a thousand citizens arm themselves, mostly from the first and second property classes. Marius speaks to them from the temple's platform: there must be no bloodshed, because the life of the poorest Roman is sacred too, and they may take orders only from him or from Sulla (II. 335–337).

Here the novel also mentions the war column in front of the temple, over which the fetial priest threw a spear towards enemy territory when war was declared (II. 336)."""),
("Saturninus on the Capitol","""Marius's small force charges across the Forum in a shield wall and scatters the mob. Saturninus and his companions flee up to the Capitol, to the temple of Jupiter (II. 338–339). From there he shouts down that the temple will be stained with Roman blood. Marius laughs: he will smoke them out without bloodshed. He sends Sulla to the water office to have the Capitol's water supply cut off (II. 339).

The captured rioters are locked in the Lautumiae. The non-Romans are executed at once; the Roman citizens are condemned the next day and thrown from the Tarpeian Rock, while a large crowd watches from the lower Forum (II. 340–341).

Beyond the novel: Appian and Orosius also record that Saturninus's men, who had fled to the Capitol, surrendered because the water was cut off (Civil Wars 1.32; Orosius 5.17)."""),
("Death in the Curia Hostilia","""Saturninus and his companions surrender on 8 December. As there is no secure prison, on Marius's proposal they are locked in the senate house, the Curia Hostilia: it has no windows, and its doors are the strongest in Rome. Scaurus is shocked but agrees. Meanwhile Sulla is seen talking at suspicious length with the younger Caepio and Metellus Piglet (II. 343–344).

At dawn fifty young nobles climb ladders onto the roof of the curia, tear up the tiles and stone the fifteen prisoners to death through the holes (II. 345). Marius and Scaurus go in alone among the bodies. Marius proclaims an amnesty for the young men, and then from the speakers' platform promises the people nineteen days' grain in his own name (II. 346–349).

At the end of the novel Marius tells Sulla that one day he will be the first man in Rome. Asked who will be first until then, he laughs and answers: no one (II. 352).

Beyond the novel: according to Appian, the crowd killed the prisoners with tiles from the roof of the senate house (Civil Wars 1.32). The Curia Hostilia stood on the north side of the Comitium; the marker is on the Curia Julia, built later beside it."""),
]
assert len(S)==len(FMR["s"])
HU={FMR["t"]:EN_T,FMR["intro"]:EN_I}
for (i,h,x),(eh,ex) in zip(FMR["s"],S):
    HU[h]=eh;HU[x]=ex
F=json.load(open('src/fix_v70_applied.json'))
old=[x['e'] for x in F if x['e'].startswith('      <li><b>Walks from novels.</b>')]
if not old:
    sys.path.insert(0,'src');import en_fabiola  # noqa
assert len(old)==1
HU['__html__']=old[0].replace('Lactantius, <i>De mortibus persecutorum</i> 13.</li>','Lactantius, <i>De mortibus persecutorum</i> 13. Colleen McCullough, <i>The First Man in Rome</i> (1990), Hungarian translation <i>Róma első embere</i> by Anna Dániel and others, Árkádia, Budapest 1991, vols. I–II; references give the volume and page of this edition. Notes beyond the novel: Sallust, <i>Jugurthine War</i> 35, 73, 86; Plutarch, <i>Marius</i> 12, 29; Appian, <i>Civil Wars</i> 1.28–32; Orosius 5.17; Cicero, <i>De domo sua</i> 102, <i>De oratore</i> 2.197–203; Suetonius, <i>Divus Iulius</i> 46.</li>')
assert 'McCullough' in HU['__html__']
M=json.load(open('en/missing.json'));out=[]
for u in M:
    e=HU['__html__'] if u["kind"]=="html" else HU[u["t"]]
    out.append({"id":u["id"],"e":e})
json.dump(out,open('en/fix_v75.json','w'),ensure_ascii=False,indent=0);print('ok',len(out))
