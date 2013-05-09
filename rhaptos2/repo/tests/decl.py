#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###

import copy

"""
THis file suppplies fixed test data for use with finctional testing the
unpub repo.
"""

sect1 = {"id_":  "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",
         "title": "Introduction",
         "body": """<h1>In CONGRESS, July 4, 1776.</h1>
<p>The unanimous Declaration of the thirteen united States of America,</p>

<p>When in the Course of human events, it becomes necessary for one
people to dissolve the political bands which have connected them with
another, and to assume among the powers of the earth, the separate and
equal station to which the Laws of Nature and of Nature's God entitles
them, a decent respect to the opinions of mankind requires that they
should declare the causes which impel them to the separation.</p>
""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }


sect2 = {"id_":  "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b",
         "title": "Preamble",
         "body": """
<p>We hold these truths to be self-evident, that all men are created
equal, that they are endowed by their Creator with certain unalienable
Rights, that among these are Life, Liberty and the pursuit of
Happiness.</p>

<p>That to secure these rights, Governments are instituted among Men,
deriving their just powers from the consent of the governed, That
whenever any Form of Government becomes destructive of these ends, it
is the Right of the People to alter or to abolish it, and to institute
new Government, laying its foundation on such principles and
organizing its powers in such form, as to them shall seem most likely
to effect their Safety and Happiness. Prudence, indeed, will dictate
that Governments long established should not be changed for light and
transient causes; and accordingly all experience hath shewn, that
mankind are more disposed to suffer, while evils are sufferable, than
to right themselves by abolishing the forms to which they are
accustomed. But when a long train of abuses and usurpations, pursuing
invariably the same Object evinces a design to reduce them under
absolute Despotism, it is their right, it is their duty, to throw off
such Government, and to provide new Guards for their future
security.</p>
""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }


sect3 = {"id_":  "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6",
         "title": "Indictment",
         "body": """
<p>Such has been the patient sufferance of these Colonies; and such is
now the necessity which constrains them to alter their former Systems
of Government. The history of the present King of Great Britain is a
history of repeated injuries and usurpations, all having in direct
object the establishment of an absolute Tyranny over these States. To
prove this, let Facts be submitted to a candid world.</p>

He has refused his Assent to Laws, the most wholesome and necessary
for the public good.

He has forbidden his Governors to pass Laws of immediate and pressing
importance, unless suspended in their operation till his Assent should
be obtained; and when so suspended, he has utterly neglected to attend
to them.

He has refused to pass other Laws for the accommodation of large
districts of people, unless those people would relinquish the right of
Representation in the Legislature, a right inestimable to them and
formidable to tyrants only.

He has called together legislative bodies at places unusual,
uncomfortable, and distant from the depository of their Public
Records, for the sole purpose of fatiguing them into compliance with
his measures.

He has dissolved Representative Houses repeatedly, for opposing with
manly firmness of his invasions on the rights of the people.

He has refused for a long time, after such dissolutions, to cause
others to be elected, whereby the Legislative Powers, incapable of
Annihilation, have returned to the People at large for their exercise;
the State remaining in the mean time exposed to all the dangers of
invasion from without, and convulsions within.

He has endeavoured to prevent the population of these States; for that
purpose obstructing the Laws for Naturalization of Foreigners;
refusing to pass others to encourage their migrations hither, and
raising the conditions of new Appropriations of Lands.

He has obstructed the Administration of Justice by refusing his Assent
to Laws for establishing Judiciary Powers.

He has made Judges dependent on his Will alone for the tenure of their
offices, and the amount and payment of their salaries.

He has erected a multitude of New Offices, and sent hither swarms of
Officers to harass our people and eat out their substance.

He has kept among us, in times of peace, Standing Armies without the
Consent of our legislatures.

He has affected to render the Military independent of and superior to
the Civil Power.

He has combined with others to subject us to a jurisdiction foreign to
our constitution, and unacknowledged by our laws; giving his Assent to
their Acts of pretended Legislation:

For quartering large bodies of armed troops among us:

For protecting them, by a mock Trial from punishment for any Murders
which they should commit on the Inhabitants of these States:

For cutting off our Trade with all parts of the world:

For imposing Taxes on us without our Consent:

For depriving us in many cases, of the benefit of Trial by Jury:

For transporting us beyond Seas to be tried for pretended offences:

For abolishing the free System of English Laws in a neighbouring
Province, establishing therein an Arbitrary government, and enlarging
its Boundaries so as to render it at once an example and fit
instrument for introducing the same absolute rule into these Colonies

For taking away our Charters, abolishing our most valuable Laws and
altering fundamentally the Forms of our Governments:

For suspending our own Legislatures, and declaring themselves invested
with power to legislate for us in all cases whatsoever.

He has abdicated Government here, by declaring us out of his
Protection and waging War against us.

He has plundered our seas, ravaged our coasts, burnt our towns, and
destroyed the lives of our people.

He is at this time transporting large Armies of foreign Mercenaries to
compleat the works of death, desolation, and tyranny, already begun
with circumstances of Cruelty & Perfidy scarcely paralleled in the
most barbarous ages, and totally unworthy the Head of a civilized
nation.

He has constrained our fellow Citizens taken Captive on the high Seas
to bear Arms against their Country, to become the executioners of
their friends and Brethren, or to fall themselves by their Hands.

He has excited domestic insurrections amongst us, and has endeavoured
to bring on the inhabitants of our frontiers, the merciless Indian
Savages whose known rule of warfare, is an undistinguished destruction
of all ages, sexes and conditions.

In every stage of these Oppressions We have Petitioned for Redress in
the most humble terms: Our repeated Petitions have been answered only
by repeated injury. A Prince, whose character is thus marked by every
act which may define a Tyrant, is unfit to be the ruler of a free
people.
""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }


sect4 = {"id_":  "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae",
         "title": "Denunciation",
         "body": """
<p>Nor have We been wanting in attentions to our British brethren. We
have warned them from time to time of attempts by their legislature to
extend an unwarrantable jurisdiction over us. We have reminded them of
the circumstances of our emigration and settlement here. We have
appealed to their native justice and magnanimity, and we have conjured
them by the ties of our common kindred to disavow these usurpations,
which, would inevitably interrupt our connections and
correspondence. They too have been deaf to the voice of justice and of
consanguinity. We must, therefore, acquiesce in the necessity, which
denounces our Separation, and hold them, as we hold the rest of
mankind, Enemies in War, in Peace Friends.</p>

""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }


sect5 = {"id_":  "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389",
         "title": "Conclusion",
         "body": """
<p>We, therefore, the Representatives of the united States of America,
in General Congress, Assembled, appealing to the Supreme Judge of the
world for the rectitude of our intentions, do, in the Name, and by
Authority of the good People of these Colonies, solemnly publish and
declare, That these united Colonies are, and of Right ought to be Free
and Independent States; that they are Absolved from all Allegiance to
the British Crown, and that all political connection between them and
the State of Great Britain, is and ought to be totally dissolved; and
that as Free and Independent States, they have full Power to levy War,
conclude Peace, contract Alliances, establish Commerce, and to do all
other Acts and Things which Independent States may of right do. And
for the support of this Declaration, with a firm reliance on the
protection of divine Providence, we mutually pledge to each other our
Lives, our Fortunes and our sacred Honor.</p>

""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }


sect6 = {"id_":  "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8",
         "title": "Signatures",
         "body": """
    New Hampshire: Josiah Bartlett, William Whipple, Matthew Thornton
    Massachusetts: Samuel Adams, John Adams, John Hancock, Robert Treat Paine, Elbridge Gerry
    Rhode Island: Stephen Hopkins, William Ellery
    Connecticut: Roger Sherman, Samuel Huntington, William Williams, Oliver Wolcott
    New York: William Floyd, Philip Livingston, Francis Lewis, Lewis Morris
    New Jersey: Richard Stockton, John Witherspoon, Francis Hopkinson, John Hart, Abraham Clark
    Pennsylvania: Robert Morris, Benjamin Rush, Benjamin Franklin, John Morton, George Clymer, James Smith, George Taylor, James Wilson, George Ross
    Delaware: George Read, Caesar Rodney, Thomas McKean
    Maryland: Samuel Chase, William Paca, Thomas Stone, Charles Carroll of Carrollton
    Virginia: George Wythe, Richard Henry Lee, Thomas Jefferson, Benjamin Harrison, Thomas Nelson, Jr., Francis Lightfoot Lee, Carter Braxton
    North Carolina: William Hooper, Joseph Hewes, John Penn
    South Carolina: Edward Rutledge, Thomas Heyward, Jr., Thomas Lynch, Jr., Arthur Middleton
    Georgia: Button Gwinnett, Lyman Hall, George Walton
""",
         "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         "copyrightHolders":
         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
         }

# folder

fldr = {"id_":      "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707",
        "title":    "Declaration Folder",
        "body": ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",
                    "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b",
                    "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6",
                    "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae",
                    "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389",
                    "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8",
                    ],
        }

collection = {"id_": "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7",
              "title": "United States Declaration Of Independance",
              "language": "en",
              "subType":  "Other Report",
              "subjects": ["Social Sciences", ],
              "keywords": ["Life", "Liberty", "Happiness"],
              "summary": "No.",
              "authors": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
              "maintainers": ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],
              "copyrightHolders":
                         ["cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383", ],

              "body": '''<ul><li><a href="cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126">Introduction</li>
<li><a href="cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b">Preamble</li>
<li><a href="cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6">Indictment</li>
<li><a href="cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae">Denunciation</li>
<li><a href="cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389">Conclusion</li>
<li><a href="cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8">Signatures</li>
</ul>'''
              
              }

collection_small = copy.deepcopy(collection)
collection_small['body'] = '''<ul><li><a href="cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126">Introduction</li>
<li><a href="cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b">Preamble</li>
</ul>'''



declarationdict = {"sect1": sect1, "sect2": sect2,
                   "sect3": sect3, "sect4": sect4,
                   "sect5": sect5, "sect6": sect6,
                   "folder": fldr, "collection": collection,
                   "module": sect1, "collection_small": collection_small}
# for s in l:
#    print json.dumps(s,sort_keys=True, indent=4)


class tempuser(object):
    """We want to match the same details as in the user dbase.
       THis is for testing only - there is no ref int between repo and users
       openid / Name / user_uri
    """
    def __init__(self, openid, name, useruri):
        self.openid = openid
        self.name = name
        self.useruri = useruri

users = {
    'paul': tempuser("https://paulbrian.myopenid.com", "Paul Brian", "cnxuser:75e06194-baee-4395-8e1a-566b656f6920"),
    'ross': tempuser("https://rossreedstrom.myopenid.com", "Ross Reedstrom", "cnxuser:75e06194-baee-4395-8e1a-566b656f6921"),
    'ed': tempuser("https://edwoodward.myopenid.com", "Ed Woodward", "cnxuser:75e06194-baee-4395-8e1a-566b656f6922"),
    'phil': tempuser("https://philschatz.myopenid.com", "Phil Schatz", "cnxuser:75e06194-baee-4395-8e1a-566b656f6923"),
    'michael': tempuser("https://michaelmulich.myopenid.com", "Michael Mulich", "cnxuser:75e06194-baee-4395-8e1a-566b656f6924"),
}

# added as extra people to every module etc.
acllist = [
    {'beginDateUTC': None,
     'endDateUTC': None,
     'user_uri': users['ross'].useruri,
     'role_type': 'aclro'},

    {'beginDateUTC': None,
     'endDateUTC': None,
     'user_uri': users['michael'].useruri,
     'role_type': 'aclro'}
]

