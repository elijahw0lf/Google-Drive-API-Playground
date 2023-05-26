## Description
A small app to print files from a Google Drive using Google API. This is meant to give the framework (and to play around) for you to improve the app and have it do something with the information it retrieves!

<br>

## Authentication
There are two types of authentication inside the script: oAuth and Service Account. You can call one or the other to load either type of credentials and authenticate. You need to set these up before the script will run. For more info, have a look at the quick start guide in the resources section below.

<br>

## Language
The app was made using Python v3.11.3 and adopts Google's Python libraries. So these are listed as dependencies below, but are also stored in requirements.txt

<br>

## Resources
Below are some resources that you might find handy as you modify/expand this app:
- [Google Drive API Python Quickstart]
- [Google Drive API Reference]
- [Python Drive API documentation]
- [Python .list() function docs]

<br>

## Dependencies

- cachetools==5.3.0
- certifi==2023.5.7
- charset-normalizer==3.1.0
- google-api-core==2.11.0
- google-api-python-client==2.87.0
- google-auth==2.19.0
- google-auth-httplib2==0.1.0     
- google-auth-oauthlib==1.0.0     
- googleapis-common-protos==1.59.0
- httplib2==0.22.0
- idna==3.4
- oauthlib==3.2.2
- protobuf==4.23.1
- pyasn1==0.5.0
- pyasn1-modules==0.3.0
- pyparsing==3.0.9
- requests==2.31.0
- requests-oauthlib==1.3.1
- rsa==4.9
- six==1.16.0
- uritemplate==4.1.1
- urllib3==1.26.16


[Google Drive API Python Quickstart]: https://developers.google.com/drive/api/quickstart/python
[Google Drive API Reference]: https://developers.google.com/drive/api/reference/rest/v3
[Python Drive API documentation]: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
[Python .list() function docs]: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html#list
