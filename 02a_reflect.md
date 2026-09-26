# Notes
- learned about rejection sampling: generate a candidate, test it, keep it only if it passes.
- refreshed my use of while and if loops in Python
- made sure to test at the end of the excercise 

## LinkedIn Post

**02a Rejection Sampling Side Quest**
- In Part 1, I generated 10 random points
- Some of these points did not lie in the Queensland boundaries
- Rejection sampling is a way of only keeping the valid (i.e. inside QLD) points
- I used GeoDataFrame (multi) polygon to check if the points lie inside QLD

Benefits of Claude
- Suggested exploring rejection sampling, so got to learn something new
- Was able to ask questions about how applicable this technique was for larger datasets

Drawbacks of Claude
- I would often skim through explanation rather than absorbing, often wanting to get the code working
- Claude would sass if I asked it to repeat an explanation

**************
Stage 02a: Rejection Sampling Side Quest

In Part 1, I generated 10 random points across a Queensland bounding box but some of them didn't land inside the real QLD boundary.

Rejection sampling fixes this: generate a candidate point, test whether it falls inside QLD, keep it if it does, and repeat until you've got as many valid points as you need. I used a GeoDataFrame (multi)polygon to run the inside/outside check.

Benefits of using Claude as a tutor:
- I got introduced to rejection sampling as a technique, something I hadn't worked with before
- I could ask follow-up questions about when this approach holds up at larger dataset sizes vs when a faster, vectorised method is better

Drawbacks:
- I'd sometimes skim explanations rather than properly absorbing them, more focused on getting the code working
- Worth staying disciplined about actually understanding the why, not just the what
*************

**02a Rejection Sampling Side Quest**

In Part 1, I generated 10 random points across a Queensland bounding box.

🌏 Some points didn't land inside the real QLD boundary, since the state isn't a rectangle
🔁 Rejection sampling fixes this: generate a candidate, test if it falls inside QLD, keep it if it does, repeat until you have enough valid points
🗺️ Used a GeoDataFrame (multi)polygon to run the inside/outside check

Benefits of Claude
🥳 Introduced me to rejection sampling, a technique I hadn't worked with before
🥳 Could ask follow-up questions about when this approach holds up at scale vs a faster, vectorised method

Drawbacks of Claude
🤔 I'd sometimes skim explanations rather than properly absorbing them, more focused on getting the code working

**NEXT** Back to the main pipeline: Stage 2 hazard mapping