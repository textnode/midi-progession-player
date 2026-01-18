# midi-progession-player

Warning - This document is a Work In Progress

Commandline structure:

python3 midi-progression-player.py &lt;Tonic&gt; &lt;Octave&gt; &lt;BPM&gt; &lt;Count&gt; &lt;Pause&gt; &lt;OmitTonics&gt; &lt;Progression and/or Canned Progressions...&gt;

Commandline example:

python3 midi-progression-player.py C 3 60 4 50 OT 0 bIII 7 vi7 12

Gives you:

* Tonic C

* Octave 3

* BPM 60

* Count 4 (number of times the chord is played within the beat)

* Pause 50 (percentage of the measure in which chord is being played)

* Omits Tonics

* ...and will play canned progression 0, followed by flattened third, then canned progression 7, followed by minor sixth seventh, followed by canned progression 12.

"OT" (Omit Tonics) is the only optional parameter - include if you want to fill those in using another instrument.



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

* e.g. iiT for where you ONLY want the Tonic played
