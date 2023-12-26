# 78
zoning_districts = ['BR-MU', 'C-2', 'C-3-G', 'C-3-O', 'C-3-O(SD)', 'C-3-R', 'C-3-S', 'CCB', 'CMUO', 'CRNC', 'CVR',
                    'HP-RA', 'M-1', 'M-2', 'MB-O', 'MB-OS', 'MB-RA', 'MR-MU', 'MUG', 'MUO', 'MUR', 'NC-1', 'NC-2',
                    'NC-3', 'NC-S', 'NCD', 'NCT', 'NCT-1', 'NCT-2', 'NCT-3', 'P', 'P70-MU', 'PDR-1-B', 'PDR-1-D',
                    'PDR-1-G', 'PDR-2', 'PM-CF', 'PM-MU1', 'PM-MU2', 'PM-OS', 'PM-R', 'PM-S', 'PPS-MU', 'RC-3', 'RC-4',
                    'RCD', 'RED', 'RED-MX', 'RH DTR', 'RH-1', 'RH-1(D)', 'RH-1(S)', 'RH-2', 'RH-3', 'RM-1', 'RM-2',
                    'RM-3', 'RM-4', 'RSD', 'RTO', 'RTO-M', 'SALI', 'SB DTR', 'SLI', 'SLR', 'SPD', 'TB DTR', 'TI-MU',
                    'TI-OS', 'TI-PCI', 'TI-R', 'UMU', 'WMUG', 'WMUO', 'YBI-MU', 'YBI-OS', 'YBI-PCI', 'YBI-R']

# 45
neighborhood_commercial_districts = ['Upper Fillmore Street NCD', 'Castro Street NCD', 'Pacific Avenue NCD',
                                     'Valencia Street NCT', 'Excelsior Outer Mission NCD', 'Taraval Street NCD',
                                     'Inner Clement Street NCD', 'Union Street NCD', 'Outer Clement Street NCD',
                                     'Broadway NCD', 'Cortland Avenue NCD', 'Hayes NCT', 'Outer Balboa Street NCD',
                                     'SoMa NCT', 'Lower Polk Street NCD', 'Ocean Avenue NCT', 'West Portal Avenue NCD',
                                     'Irving Street NCD', '24th Street-NoeValley NCD', 'Divisadero Street NCT',
                                     'Mission Street NCT', 'Judah Street NCD', 'Sacramento Street NCD',
                                     'Inner Taraval Street NCD', 'Japantown NCD', 'Mission Bernal NCD',
                                     'North Beach NCD', 'Lower Haight Street NCD', 'Excelsior Outer Mission Street NCD',
                                     'Folsom Street NCT', 'Noriega Street NCD', 'Glen Park NCD', 'Inner Sunset NCD',
                                     'Upper Market NCT', 'Cole Valley NCD', 'San Bruno Avenue NCD',
                                     'Geary Boulevard NCD', 'Fillmore Street NCT', '24th-Mission NCT',
                                     'Haight Street NCD', 'Polk Street NCD', 'Lakeside Village NCD',
                                     'Inner Balboa Street NCD', '24th Street-Mission Street NCD', 'Bayview NCD']

preservation_districts = [
    "Dogpatch Historic District",
    "Buena Vista North Historic District (Proposed)",
    "Duboce Park Landmark District",
    "Liberty-Hill Landmark District",
    "Market Street Masonry Landmark District",
    "South of Market Extended Preservation District",
    "Alamo Square Historic District",
    "Blackstone Court Historic District",
    "Bush Street-Cottage Row Historic District",
    "Civic Center Historic District",
    "Webster Street Historic District",
    "Civic Center Historic District",
    "Commercial-Leidesdorff Conservation District",
    "Front-California Conservation District",
    "Jackson Square Historic District",
    "Kearny-Belden Conservation District",
    "Kearny-Market-Mason-Sutter Conservation District",
    "New Montgomery-Second Street Conservation District",
    "Northeast Waterfront Historic District",
    "Pine-Sansome Conservation District",
    "South End Historic District",
    "South of Market Extended Preservation District",
    "Telegraph Hill Historic District"
]

benchmark = {
    # Recreate the Chris Elmendorf tweet https://x.com/CSElmendorf/status/1726405905112310268?s=20
    "Can you list examples in the planning code where what I'm allowed to build depends on what my neighbors have already built?":
        "SF allows encroachment on rear-yard open space to average depth of neighboring buildings on either side",

    # Can we read non-tidy tables
    "How dense can I build on block 12 in mission bay?":
        'You can build 419 units according to table 920',

    # Can we read tables with merged cells
    "Can I build off-street parking in mission bay's OFFICE, COMMERCIAL-INDUSTRIAL AND HOTEL district?":
    'It is required in the COMMERCIAL-INDUSTRIAL AND HOTEL districts, and for the office district, the rule is'
    'described as follows: 1 space/1,000 s.f. or 2.5 spaces/1,000 s.f. on property zoned MB-CI east of Owens St.',
            

    # Actual mistake from the past.
    # PlanningGPT cites heights from South Beach Downtown Residential Mixed Use District
    # when asked about Transbay Downtown Residential Mixed Use District
    'How tall can you build in the Transbay Downtown Residential Mixed Use District?':
    'This information is contained in Transbay Redevelopment Project Area, not in the SF Planning Code',

    # Interpretation
    "Is supportive housing for the homeless technically a dwelling unit?":
        'it depends on what the Zoning Administrator says',

    # Testing recall
    "Can you list all of the zoning districts in San Francisco?":
        "They are " + ' '.join(zoning_districts),

    # Testing recall 2
   "Can you list all of the neighborhood commercial districts in San Francisco?":
       "They are " + ' '.join(neighborhood_commercial_districts),

    # Testing recall 3
    "Can you list all of the preservation districts in San Francisco?":
        "They are " + ' '.join(preservation_districts),

    # This test picks out whether we can read from a table. Also whether we understand that C in the table refers to conditional uses
    "In NC-1, can I keep my yoga studio open until 11:45 pm?":
        "Store hours that extend between 11 pm and 2 am are only conditionally permitted in NC-1.",

    # Cross-textual references (goal of this test is to see if we can realize one section of code is trumped by another
    #"What temporary uses are permitted in the Mission Bay Use District?",
    #        ""
    
    # This test evaluates whether we can pick up on cross-textual references that, frankly, don't make sense
    "Tell me about the interpretitive ambiguities in uses permitted in the Mission Bay Use District, "
    "with respect to enclosure of permitted uses. Comment only on the interpretative ambiguity that is noted in the code.":
        "The interpretations section of the planning code for the Mission Bay Use District says:"
        "See 'Printing, where allowed, plus: for training purposes 3/97' in the Interpretations - Alphabetical"
        "Code Section: 903(a)(6). According to 'Subject: Printing, where allowed, plus: for training purposes' "
        "Retail printers (those that deal directly with the consumer or ultimate customer on the same premises)"
        " are allowed pursuant to Section 222(h), 790.124 or 890.124. Normally, a nonretail printer would be allowed "
        "only in those districts which allow the uses described in Section 226(a), (b) and (d) and is not allowed in"
        " the Neighborhood Commercial or Mixed Use Districts.   In one case, a retail printer refers a portion of "
        "its work to a nonprofit agency which operates a training facility for printing. The agency produces"
        " the final product in the course of its instruction. There is no customer contact at the site of the"
        " training facility and so it is not a retail printer. The agency is funded through a number of public"
        " and private funding sources to provide housing, counseling and training to the disadvantaged. Since "
        "the agency is a bona fide nonprofit, social service agency providing counseling as well as training on "
        "site, this use would be considered either a personal service [per Section 218, 790.116 or 890.116] or "
        "an institutional use [per Section 209.3, 218, 790.50(a) or (c) or 890.50(f)]."
}

# gpt4 generated
# the following are question answer pairs provided by gpt4 when the context window includes SEC. 250 through SEC. 263.13.

gpt4_pairs = {
    'Q: Under Section 250(e), how does the provision of Article 2.5 apply '
    'to properties and developments in San Francisco?':
        'A: The provision of Article 2.5 applies to all properties and developments,'
        ' both public and private, in San Francisco, including those owned by the City and County of San Francisco.',

    'Q: In the context of Section 251, what specific urban design goal does the establishment of '
    'height and bulk districts serve related to the character of existing development?':
        'A: The establishment of height and bulk districts aims to relate the height of new buildings '
        'to the height and character of existing development, ensuring new constructions harmonize with '
        'the existing cityscape.',

    'Q: According to Section 252, how are the classes of height and bulk districts determined and indicated?':
        'A: The classes of height and bulk districts are determined and indicated on the Zoning Map, '
        'with height limits specified numerically in feet and bulk limits designated by letter symbols '
        'referring to limitations on the plan dimensions of buildings.',

    'Q: Section 253 outlines specific review processes for buildings exceeding certain heights in various '
    'districts. Can you identify a unique condition that triggers a different review process in this section?':
        'A: A unique condition triggering a different review process is in RM or RC Districts with more '
        'than 50 feet of street frontage on the front façade, subjecting buildings over 40 feet in height '
        'to the conditional use requirement.',

    'Q: Analyze Section 260 and explain the method of height measurement for lots that slope upward from '
    'a street. How does this differ from measurement on level lots?':
        'A: For upward sloping lots, the measurement point is taken at curb level for the closest part '
        'of the building within 10 feet of the street property line, with additional points taken as the '
        'average ground elevations at building cross-sections. This contrasts with level lots, where the '
        'point is taken at curb level on the street at the building centerline.',

    'Q: In Section 261, what additional height limits are applied to RH-1(D), RH-1, and RH-1(S) Districts, '
    'and how are they determined?':
        'A: In RH-1(D), RH-1, and RH-1(S) Districts, additional height limits are applied based on the average '
        'ground elevation difference between the front and rear lot lines. For example, the permitted height '
        'increases to 40 feet if the rear lot elevation is 20 or more feet higher than the front.',

    'Q: Describe the purpose of the additional height limits for Narrow Streets and Alleys in Section 261.1 '
    'and how they contribute to the character of these areas.':
        'A: The purpose is to preserve the intimate character of Narrow Streets and Alleys by limiting building '
        'heights to ensure they are not overshadowed or overcrowded, thus maintaining ample sunlight and air, '
        'contributing to the unique character of these areas.',

    'Q: Section 263 provides for special exceptions to height limits. Can you elaborate on a scenario where '
    'these exceptions might be applied and the conditions that must be met?':
        'A: Special exceptions to height limits might be applied in designated height and bulk districts where '
        'buildings exceeding prescribed limits can enhance urban design or serve public interest. Conditions '
        'include Planning Commission approval and adherence to conditional use procedures in Section 303.',

    'Q: Under Section 260(b), what are the criteria for exempting certain building features from height limits, '
    'and how is the total permissible exemption area calculated?':
        'A: Certain building features like mechanical equipment and elevator penthouses are exempt from height '
        'limits, subject to limitations like maximum heights and footprint. The total permissible exemption '
        'area is calculated as a percentage of the roof area, with variations depending on the district and '
        'specific building characteristics.',

    'Q: Explain how Section 261.2 addresses the balance between development heights and the pedestrian '
    'environment along Folsom Street in the Folsom Street NCT District.':
        'A: Section 261.2 focuses on balancing appropriate development heights with maximizing light and '
        'air to sidewalks, parks, and frontages along Folsom Street. It mandates a 15-foot setback for '
        'building portions above 55 feet from property lines fronting Folsom Street, ensuring a high-quality '
        'pedestrian environment while allowing for development.'
}


print(len(gpt4_pairs) + len(benchmark))