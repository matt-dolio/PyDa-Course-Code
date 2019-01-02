# PyDa Revisions

Following the guide, I was able to run into some issues that weren't present in the tutorial and saw to it that I fix these issues and improve some of the code. Some improvements include:
+ Wikipedia fallback no longer potentially snipping user input
+ Wikipedia lists more specific article names in the case of DisambiguationError
+ Added some common language shortcodes for programmers' ease of use
+ Easily modifiable query modifiers for Wikipedia snipping (who is, what is, etc.)
+ Fixed issue with speech recognition only setting the value in the box and not updating the user input value, causing Wikipedia to freak out
