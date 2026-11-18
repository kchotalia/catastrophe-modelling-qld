# Notes
- Learned about random seeds so point generated are the same every time

# LinkedIn Post
**Stage 2 Catastrophe Modelling: Geospatial Basics and Coastal Exposure Data**

My first synthetic portfolio was scattered across a rectangle but only 7 of 10 properties landed inside the Queensland state boundary. For a cyclone model, exposure near the coast matters most, so I rebuilt the dataset to sit in a 50km coastal zone.

What I learned
🌏 How to turn latitude and longitude into geometry with GeoDataFrames and checking locations against a real boundary with .within()
📏 How to change coordinate systems to create the coastal zone in metres (EPSG:3577), not degrees
🌊 How to build the coastal zone from the whole-Australia shape, so state land borders aren't mistaken for coastline
🎲 Making sure to check random sampling: the hit rate (0.057) matched the exact area ratio (0.0603)
🗺️ Built an interactive map with folium to see the result

Benefits of Claude
🥳 After a break, could go back to previous summaries to remind myself of past tasks, difficulties and ideas
🥳 Could keep asking why until the underlying idea made sense

Drawbacks of Claude
🤔 Some early troubleshooting advice (a map not rendering in VS Code) pointed at the wrong cause until I  ended up back at trusty stack exchange
🤔 Unless prompted, it will decide which way forward is best. Don't stop questioning!

**NEXT:** Joining the properties to a hazard layer (AS/NZS 1170.2 wind regions)

Check out the progress so far at https://github.com/kchotalia/catastrophe-modelling-qld

#catastrophemodelling #claudeai #ailearning #insurance #risk #riskmodelling #python #vscode #git