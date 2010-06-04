FEVERBUDDY
----------
Written to access Hot Items on the Desktop with Geektool or Nerdtool, like the iCalBuddy and TwitterBuddy programs others have written. 

----------

This is for accessing the Fever API (http://www.feedafever.com/api)
Currently it is only useful for retrieving Hot Items

Options:
-s, --server: specify the location of a fever installation  [required] 
-e, --email: specify the email associated with the installation [required]
-p, --password: specify the password [required]
-d, --days: specify days value [required]

Example Usage:
python FeverBuddy.py -s mydomain.com/fever -e me@mydomain.com -p password -d 2 -i