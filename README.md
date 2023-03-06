# Medimagehub
Online platform for sharing and studying medical images (built in Django)

A project in bachelor thesis computer science DTE-2708, 
Online platform for sharing and studying medical images, UiT The Arctic University of Norway.

A system built on Django where you can upload, view and share DICOM files.

For testing settings.py are set up to be used in local computer. Local email SMTP is used.

To use local email just go to terminal and type:

`python -m smtpd -n -c DebuggingServer localhost:1025`

For deployment it uses some environment variables, and needs to work with PostgreSQL database, Redis cache, and email server. To use it you need to go to settings.py and change email, file storage, data base settings on settings.py file.
See comments and commented codes in settings.py

You need to make changes in the Dockerfile too.

The DICOM viewer is built on JavaScript, and is taken from another repository.

To use the application you need to register admin user first on terminal.
