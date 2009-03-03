#!/bin/bash

cd applet
zip -r ../bloatedclockplasmoid.zip .
cd ..
plasmapkg -t plasmoid -i bloatedclockplasmoid.zip