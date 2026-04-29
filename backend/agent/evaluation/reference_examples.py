"""
Calibration reference examples for LLM evaluation prompts.

Each ReferenceExample is a real CELPIP writing sample with a known band score
and per-criterion analysis. REFERENCE_EXAMPLES contains one Level 9 and one
Level 8 sample for each task type (task_1_email, task_2_survey).
"""

from agent.evaluation.models import ReferenceExample

TASK_A_LEVEL_9 = ReferenceExample(
    text=(
        "To whom it may concern,\n\n"
        "My name is Seth and I am writing to you today regarding the opening hours for the library. "
        "I am an English student and my course requires me to read many books throughout the year. "
        "As a result, I visit the library several times a week to rent the required books. "
        "Books can be very expensive, so the library is a great benefit to me as instead of spending "
        "lots of money buying these expensive books I can rent them instead at a much lower cost.\n\n"
        "I have recently started a new part-time job. Now, my only days off are Sundays and Tuesdays. "
        "The library is closed on Sundays which leaves Tuesday evenings after school as the only time "
        "I can visit the library. As the library closes early on Tuesdays, I have to rush down after "
        "school. This is very stressful for me and it would be much easier if the Library was open on "
        "Sundays as then I would have all day to visit.\n\n"
        "I feel that many other people have the same problem and would benefit greatly if the library "
        "was open every day. I hope you will consider this.\n\n"
        "Thanks,\nSeth"
    ),
    band_score=9,
    task_type="task_1_email",
    analysis=(
        "Content/Coherence: Both tasks are complex with consistent development. Ideas are supported "
        "with personal details (school/work schedule) and broader facts.\n"
        "Vocabulary: Word choices provide accurate details; few errors (most notable: 'rent' instead "
        "of 'borrow'). Comparison words used effectively.\n"
        "Readability: Each paragraph has one clear main idea with supporting details. Grammar control "
        "is strong; errors are infrequent. Complex structures include conditionals ('it would be much "
        "easier if') and varied conjunctions ('as a result', 'instead of').\n"
        "Task Fulfilment: Tone is consistently appropriate. Standard formal phrases used "
        "('I am writing to you today regarding'). Intended meaning is conveyed (though third "
        "sub-task is not fully addressed)."
    ),
)

TASK_B_LEVEL_9 = ReferenceExample(
    text=(
        "I would prefer to have my mail delivered to my home twice a week as opposed to me collecting "
        "it myself at the local post office. The reason I would prefer this is because I have a very "
        "busy schedule and having to collect my own mail from the post office would just take up more "
        "of my spare time. Also, the closest post office to my house is a twenty minute walk. I do not "
        "own a car so I would have to walk this distance in order to collect my mail.\n\n"
        "I feel that having my mail delivered to my home twice a week is a more efficient way of "
        "delivering mail to homes as it limits the amounts of trips the post office has to take in "
        "order to deliver mail. This in turn will save money for the government as instead of spending "
        "money on gas and wages for the employees that deliver the mail every day, they will be only "
        "spending this money two days per week.\n\n"
        "These are the reason I would prefer to have my mail sent out to my home twice a week."
    ),
    band_score=9,
    task_type="task_2_survey",
    analysis=(
        "Content/Coherence: Text is complex with consistent development. Ideas are supported with "
        "personal details (schedule, distance to post office) and broader facts (cost savings).\n"
        "Vocabulary: Accurate and varied; comparison words used effectively "
        "('as opposed to', 'more efficient').\n"
        "Readability: Well-organised paragraphs, each with a clear main idea. Strong grammatical "
        "control; complex structures used ('in turn', 'instead of', 'as opposed to').\n"
        "Task Fulfilment: Tone is consistently appropriate for a survey response. Intended meaning "
        "is fully conveyed."
    ),
)

TASK_A_LEVEL_8 = ReferenceExample(
    text=(
        "Dear Chief Librarian,\n\n"
        "I am writing to you with regards to the operating hours of your library. I would appreciate "
        "that the library committee will consider operating on Sundays and Mondays as well.\n\n"
        "I am a regular patron of your library. I need to visit the library for my research and self "
        "study sessions required for my part time MBA course. Occasionally, I would be required to "
        "work late for meetings and overtime, and would not be meet the library operating hours. I "
        "could only use the library on Saturday, which is a day I would need to complete other "
        "household chores.\n\n"
        "By opening your library daily, it can benefit not just me, but the entire community. Most "
        "families will spend their Sundays doing things together. The library can certainly organize "
        "story telling sessions or talks/workshops that are family friendly on Sundays. There are also "
        "many schools surrounding your library. Your library is an excellent place for highschoolers "
        "to hang out after school for self studies or project meetings. Therefore, there is every "
        "reason to open on Mondays too!\n\n"
        "I hope my suggestions can be considered by the committee. I will look forward to your "
        "favourable response soon.\n\n"
        "Regards\n\nWendy"
    ),
    band_score=8,
    task_type="task_1_email",
    analysis=(
        "Content/Coherence: Main idea developed with supporting details; more specific and less "
        "repetitive than Band 7. Includes personal scenario (MBA course, work schedule) and "
        "community-level reasoning (family sessions, high school students).\n"
        "Vocabulary: Common words used appropriately ('work late', 'hang out', 'every reason', "
        "'community'). Context-specific phrases used ('a regular patron', 'family friendly').\n"
        "Readability: Well-organised paragraphs. Quite a few errors ('would not be meet', "
        "'story telling') but they generally don't impede comprehension.\n"
        "Task Fulfilment: Appropriate mix of personal information and wider community scope. "
        "Contextually appropriate formal phrases used ('I am writing to you with regards to', "
        "'I will look forward to your favourable response')."
    ),
)

TASK_B_LEVEL_8 = ReferenceExample(
    text=(
        "My option is to have my mails delivered to my home twice a week. Though it's only twice a "
        "week, but it does not change my daily routine. We do not need to allocate time for post "
        "office pick up. Sometimes, both my husband and myself may be too occupied at work, and may "
        "miss picking up the mails. I sincerely do not want to miss out important mails for that "
        "reason.\n\n"
        "Base on our mailing records, we do not receive mails daily. At least for relevant mails. "
        "We do have junk mails delivered daily, which is not favoured. We had opted for electronic "
        "mails for most of our banking and financial institutions. So we will not be expecting "
        "regular mails from them. Government bodies are also starting to mail electronically, which "
        "is the our preferred mode of correspondence. Twice a week of mail delivery is about right "
        "for our family. In fact, we do not require to clear our mailbox stuffed with junk mails "
        "everyday anymore!"
    ),
    band_score=8,
    task_type="task_2_survey",
    analysis=(
        "Content/Coherence: Main idea developed with supporting details; more specific than Band 7. "
        "Ideas include personal details (routine, husband's schedule) and broader institutional "
        "trends (banks and government shifting to electronic mail).\n"
        "Vocabulary: Common phrases used appropriately ('at work', 'about right', 'miss out'). "
        "Context-specific expressions used ('junk mails', 'preferred mode of correspondence').\n"
        "Readability: Paragraphs are well-organised. Quite a few errors ('Base on', 'the our') "
        "but they generally don't impede comprehension.\n"
        "Task Fulfilment: Appropriate mix of personal information and wider scope. Contextually "
        "appropriate style ('both my husband and myself may be too occupied')."
    ),
)

REFERENCE_EXAMPLES: list[ReferenceExample] = [
    TASK_A_LEVEL_9,
    TASK_B_LEVEL_9,
    TASK_A_LEVEL_8,
    TASK_B_LEVEL_8,
]
