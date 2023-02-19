Mirror of git repository of docutils
====================================

This is a mirror of the git mirror of docutils. It is used for
developing features needed for our juggling group webpage so it might
not be so useful for the general public but feel free to look around.

navigation directive
--------------------

This creates some navigation elements.

Example
_______

.. code-block:: rest

   .. navigation::
      :class: navigation
      :title: Verein
      :index: 1
      :base: /var/www/jonglaria.org/hidden/src
      :language: de

Options:
________

class
  class if used in html element for css (optional)


title
  Title of page in navigation element


index
  Index used to order navigation elements


base
  Base path of rst file


language
  Language used for this page (optional, defaults to 'de')

form directive
--------------

Example
_______

.. code-block:: rest

   .. form:: regjugglingforfuture
      :method: post
      :phpmode: checkandembedvalue
      :phpvar: $formcontents
      :phpvalidvar: $validinput
      :phpvalidvarstring: $invalidinputstrings
   
      Da wir vereinzelt Probleme mit der Emailzustellung der
      elektronischen Tickets hatten wird ein Accountname und
      ein Passwort benötigt. Dieser kann frei gewählt werden und aus den
      Zeichen a-z, A-Z, 0-9 und _ bestehen.
   
      [  ] accountname "" raccountname Accountname
      [ * ] password "" rpassword Passwort
   
   
      Um gegebenenfalls Leute nochmal wegen verlorener Sachen
      oder anderen Problemen kontaktieren zu können behalten wir uns vor,
      die Daten bis zu einem Monat nach Ende der Convention zu speichern.
   
      Optionale Daten können jederzeit gelöscht werden, alle gespeicherten
      personenbezogenen Daten können außerdem jederzeit heruntergeladen werden.
   
      [ ] confirmdata participantreadandunderstooddataprotectionrules confirmdataid Ich habe die Datenschutzerklärung gelesen, verstanden und stimme ihr zu.
      [ OK ] submitdata "Daten absenden und fortfahren"
      [ X ] resetdata "Daten zurücksetzen"

Example 2
_________

.. code-block:: rest

   .. form:: regcookiecon
      :method: post
      :phpmode: checkandembedvalue
      :phpvar: $formcontents
      :phpvalidvar: $validinput
      :phpvalidvarstring: $invalidinputstrings
   
      Die Emailadresse wird benötigt um den Teilnehmer zu allen Belangen
      der Convention kontaktieren zu können und gegebenenfalls das
      Passwort zurückzusetzen.
   
      [  ] regperson[prename] "" rprename Vorname
      [  ] regperson[surname] "" rsurname Nachname
      [  ] regperson[email] "" remail Email
   
      Das Alter wird zum Feststellen des Conventionbeitrags benötigt, zum
      Anderen müssen für Minderjährige zusätzliche Felder ausgefüllt werden
      damit ein Erziehungsberechtigter / eine vom erziehungsberechtigten
      beauftragte Betreuungsperson dem Organisationsteam bekannt ist.
   
      [ YYYY-MM-DD ] regperson[birthday] "2002-01-01" rbirthday Geburtstag
      
      :raw-html:`<?php print '<input id="rorderhash" name="regperson[orderhash]" type="hidden" value="'.$openorderhash.'" />'; ?>`
   
      [ OK ] submitdata "Person hinzufügen" submitdataid Neu anlegen:
      [ X ] resetdata "Daten zurücksetzen"

Options
_______

class
  class if used in html element for css (optional)

name


action


target


method
  **post** or **get**


accept-charset


enctype


phpmode
  Can be one of

  - **off** No php is inserted in the output (default)
  - **checkandembedvalue** Values received via get/post are tested for existance and put in place else the default value is put in place
  - **embedvalue** Values received via get/post are put in place without testing (This assumes previous check of \$POST_, \$GET_, ... variable and does ignores the default values)


phpvar
  Form contents end up in this variable


phpvalidvar
  Validation result ends up in this variable


phpvalidvarstring
  In case of failed validation error strings end up in this variable


Extensions to block patterns to generate the forms
__________________________________________________

form_checkbox
.............

This is a simple checkbox.

.. code-block:: rest

   [ ] <name> <value>
   [x] <name> <value>
   [X] <name> <value>

   [ ] <name> <value> <formid> <text>
   [x] <name> <value> <formid> <text>
   [X] <name> <value> <formid> <text>

form_radio
..........

Same as checkbox but in radio group.


.. code-block:: rest

   ( ) <name> <value>
   (x) <name> <value>
   (X) <name> <value>

   ( ) <name> <value> <formid> <text>
   (x) <name> <value> <formid> <text>
   (X) <name> <value> <formid> <text>


form_text
.........

This is a textfield.

.. code-block:: rest

   [  ] <name> <value>
   [__] <name> <value>
   [_<number-size>_] <name> <value>

   [  ] <name> <value> <formid> <text>
   [__] <name> <value> <formid> <text>
   [_<number-size>_] <name> <value> <formid> <text>


form_date
.........

This allows entry of a date.

.. code-block:: rest

   [ YYYY-MM-DD ] <name> <value>
   [ YYYY-MM-DD ] <name> <value> <formid> <text>


form_textarea
.............

This allows to have a text area.

.. code-block:: rest

   [_<number-cols>x<number-rows>_] <name> <value>
   [_<number-cols>x<number-rows>_] <name> <value> <formid> <text>


form_password
.............

This gives a text input field suitable for the entry of a password (i.e. chars are not shown)

.. code-block:: rest

   [ * ] <name> <value>
   [ * ] <name> <value> <formid> <text>


form_submitreset
................

This gives buttons to submit a form or to reset it

Submit

.. code-block:: rest

  [ OK ] <name> <value>
  [ Ok ] <name> <value>
  [ ok ] <name> <value>
  [ OK ] <name> <value> <formid> <text>
  [ Ok ] <name> <value> <formid> <text>
  [ ok ] <name> <value> <formid> <text>


Reset

.. code-block:: rest

  [ X ] <name> <value>
  [ x ] <name> <value> <formid> <text>


form_select
...........


.. code-block:: rest

   \/ <text>
   \/ <text> <text> <text>
   \/ "<text>"
   \/ "<text>" "<text>" <text>


Don't remember if this works at all. Seems to be implemented though.

form_datalist
.............

Regex for this seems to be broken.
