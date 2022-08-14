# SnorrenTijd
Tijd voor Snorren - Flask webserver for SnorrenTijd

This is a web app where users can upload pictures of themselves, their friends, or anyone for that matter, and can select a moustache from a selection of moustaches to put on all the faces in the picture. 

##How does it work
A docker container serves a flask app containing a facial recognition algorithm that detects all the faces and sends the relative coordinates of the upper lips of every recognised person in the photo.

## Under development
This is an ongoing project. Currently I am setting up the hosting, fixing some front-end bugs, and have the build more stable so it can run continously with minimum computing resources.
