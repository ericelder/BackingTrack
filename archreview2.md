SoloBuddy Architectural Review 2

Background and Context:

Seeing as we did not present during the first architectural review, we will be providing slightly more background/context than we otherwise might.
We will provide the audience with an overview of what our project seeks to do, as well as a visual representation of what the final product might
look like. We will explain that our project, SoloBuddy, serves as a learning tool to budding improvizationalsits. It will accept a chord
progression from the user and play a corresponding backing track, while suggesting notes to accent in the user’s solo. Then we will show
our mock-up of the potential display for feedback.

Key Questions:

We are trying to answer four key questions during this architectural review: two technical and two design. The first technical question is whether
or not the way we are treating chords is effective. Currently, we have them stored as a tuple containing the root note and the tonality. To play
the chord, we find the middle C chord that matches the tonality, and modulate it based on the difference between middle C and the root note. This
system works, but it might not be efficient to have to keep accessing the files, and there might be a clean way to package the chord as a single
object instead of two values. We are also wondering about acquiring and storing all the middle C chords. It is possible to record them individually
in SonicPi, but this is time consuming and makes for a lot of inconsistencies between the chords. There might be a more streamlined option.

We also have two design questions that we would like to discuss. First, how could our interface be improved? What does it lack, does it have anything
it shouldn’t, and what are some good ways to handle the display? Second, we have a few ideas for what simple interactions might be good, but what
else should we add? Essentially, we have a skeleton of our project built, and we need to add on things to make it more fun.

Agenda:

4-5 minutes for general explanation of the project: what it is, how it will look
For each of our four key questions:
1-2 minutes of explaining the issue, and our question
2-3 minutes of feedback
