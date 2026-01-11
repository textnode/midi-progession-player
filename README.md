# midi-progession-player

Warning - This document is a Work In Progress

All parameters to the script are supplied on the commandline and are mandatory.

Commandline example:

python3 midi-progression-player.py C 3 60 4 0.1 0 bIII 7 vi7 12

Gives you:

Tonic C

Octave 3

BPM 60

Count 4

Pause 0.1 (seconds)

...and will play canned progression 0, followed by flattened third, then canned progression 7, followed by minor sixth seventh, followed by canned progression 12.


Progression Notation:
* e.g. ii&lt;Enter&gt; for the Minor Second
* e.g. II&lt;Enter&gt; for the Major Second
* e.g. bIII&lt;Enter&gt; for the Flattened Major Third
* e.g. VI7&lt;Enter&gt; for the Major Sixth Dominant Seventh
* e.g. VIM7&lt;Enter&gt; for the Major Sixth Seventh
* e.g. vi7&lt;Enter&gt; for the Minor Sixth Seventh

Also: 
* e.g. IIsus2 or iisus2 for sus2 (not major or minor, express either way)
* e.g. IIsus4 or iisus4 for sus4 (not major or minor, express either way)

* e.g. II+ for Second Augmented
* e.g. II+7 for Second Augmented Seventh

* e.g. iio for Second Diminished


This will play canned progression 0, followed by flattened third, then canned progression 7, followed by minor sixth seventh, followed by canned progression 12.
