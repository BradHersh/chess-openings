# chess-openings

## Requirements

- Python3
- Flask

## Usage

Clone repository to local machine:

```
$ git clone git@github.com:BradHersh/chess-openings.git
```

Go into the project directory on command line and run the command:

```
$ source venv/Scripts/activate
```
Next, run the application using flask on `localhost` using the following command:

```
$ flask run
```
Open `http://127.0.0.1:5000/` and enjoy!

## Purpose and Design

This web application simulates an educational experience for learning high quality chess openings. 
Users accessing the application can register an account with a username and corresponding password before loggin in.

The applcation consists of several portals, namely a:

- Homepage
- Learn Portal
- Test Portal
- Results Portal
- Feedback Portal

A typical user experience involves the following steps:

1. Using the learning tools to become familiar with and master a number of iconic chess openings. The learning experience is unlimited and can be completed as many times as wanted.
2. Completing a formative assessment for each opening whereby users are required to apply their learning in an environment without teaching support.
3. Accessing results to track learning progess. 
4. Accessing feedback to gain meaningful insights into test performance.

A typical admin experience involves:

1. Being able to view all results, users and openings
2. Hold full control over the addition, deletion and modification of all results, openings and users
3. To log in as an admin, please use the following details:
    Username: admin
    Password: 123

## Development

The chess-openings web application was developed according to an *agile* software development framework. 

This involved the following phases which were carried out in a cyclical manner:

1. Brainstorming the high-level view for the application design.
2. Developing many user stories that describe the features of the application. These stories are then broken down into tasks for each sprint.
3. Estimating time and resources required for each story. Allocating team members to different features for each sprint.
4. Consolidating user stories and refactoring code.
5. Designing and executing unit tests at the end of each sprint.

The following user stories were created, and filtered by sprint and perceived user value. We aimed to complete high value tasks first, followed by lower value tasks. Please see "User Stories Chess.xlsx" for more details.

## Architecture 

The web app was built using a flask web application framework, as well as utilising Python, Javascript, HTML, CSS, Jquery and AJAX. Please see the diagram below for the architecture of the web application. 

![](/app/static/img/Chess%20Architecture.PNG)

## Unit Tests

Unit tests were designed to test all our defined user stories. They were created with selenium. 

STEVE GIVE MORE DETAIL

## Commit Logs

TO BE COMPLETED

## Libraries

The following libraries were used:

1. Chessboard.js:
Link: https://chessboardjs.com/index.html
Github: https://github.com/oakmac/chessboardjs/
Author: Chris Oakman

2. Chart.js
Link: https://www.chartjs.org/
Github: https://github.com/chartjs/Chart.js
Major Contributors (Github usernames): etiemberg, kurkle, benmccann, tannerlinsley, simonbrunel

3. Selenium
Link: https://selenium-python.readthedocs.io/
Github: https://github.com/baijum/selenium-python
Author: Baiju Muthukadan

4. Jquery
Link: https://jquery.com/
Github: https://github.com/jquery/jquery
Author: John Resig

4. Boostrap
Link: https://getbootstrap.com/
Github: https://github.com/twbs
Major Contributors (Github usernames): Bardi Harborow, fat, Gael Poupard, GeoSot, Gleb Mazovetskiy, Johann-S, Martijn Cuppens, Mark Otto, Patrick H. Lauke, Thomas McDonald, XhmikosR, Shohei Yoshida

## Contributors

- Jacob Posel, Brad Hershowitz, Steven Kaye, Dean Kezurerer 
