UK-Weather-Analyzer
========

> **UK-Weather-Analyzer** is a web visualization website build on Google App Engine using Python, Django, AngularJS, Bootstrap, Chart.js and other technologies.

![UK-Weather-Analyzer](https://raw.githubusercontent.com/yashrajsingh/uk-weather-analyzer/master/uk_weather_analyzer/static/uk_weather_analyzer/images/logo.png)

`NOTE` Scraps data from public sector information licensed under the [Open Government Licence v1.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/) [view data source](http://www.metoffice.gov.uk/climate/uk/datasets/#). 

Available online:
[https://uk-weather-analyzer.appspot.com/](https://uk-weather-analyzer.appspot.com/)

Requirements
------------

  - [Google App Engine SDK for Python][]
  - [pip][], [virtualenv][], [perl][]
  - [OS X][] or [Linux][] or [Windows][]


Initializing
-----------------------------------
To get started:

 - Clone this repo (don't forget to change the origin to your own repo!)
 - Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
 - `python manage.py runserver`


To test it visit `http://localhost:8080/` in your browser.


Running First Time
------------------------------------

To scrap and store live data for the first time, navigate to `http://localhost:8080/update_all/` in your browser.


Deploying on Google App Engine
------------------------------

Create a Google App Engine project. Edit `app.yaml` and change `application: uk-weather-analyzer` to `application: your-app-id`. 
Then, if you're in the `uk-weather-analyzer` directory, run:

    $ appcfg.py update ./

If you have two-factor authentication enabled in your Google account, run:

    $ appcfg.py --oauth2 update ./


Tech Stack & Credits
----------

  - [Google App Engine][], [NDB][]
  - [Django][], [AngularJS][],
  - [Bootstrap][], [jQuery][], 
  - [angular-kudos][], [ngStorage][], 
  - [angular-chart][], [Chart.js][], 
  - [angular-busy][], [angular-animate][], 
  - [social-buttons][], [ui-bootstrap][], 
  - [Python 2.7][], [pip][], [virtualenv][]

Help & Support
----------
  - [Author][]

[bootstrap]: http://getbootstrap.com/
[google app engine sdk for python]: https://developers.google.com/appengine/downloads
[google app engine]: https://developers.google.com/appengine/
[jquery]: https://jquery.com/
[linux]: http://www.ubuntu.com
[ndb]: https://developers.google.com/appengine/docs/python/ndb/
[os x]: http://www.apple.com/osx/
[pip]: http://www.pip-installer.org/
[python 2.7]: https://developers.google.com/appengine/docs/python/python27/using27
[virtualenv]: http://www.virtualenv.org/
[windows]: http://windows.microsoft.com/
[perl]: https://www.perl.org/
[Django]: https://www.djangoproject.com/
[Djangae]: https://github.com/potatolondon/djangae
[AngularJS]: https://angularjs.org/
[angular-kudos]: https://github.com/oojr/inspiration
[ngStorage]: https://github.com/gsklee/ngStorage
[angular-chart]: https://jtblin.github.io/angular-chart.js/
[Chart.js]: https://www.chartjs.org
[angular-busy]: http://cgross.github.io/angular-busy/
[angular-animate]: https://docs.angularjs.org/guide/animations
[social-buttons]: https://github.com/carrot/share-button
[ui-bootstrap]: https://angular-ui.github.io/bootstrap/
[Author]: http://yashrajsingh.net/
