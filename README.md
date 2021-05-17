# chess-openings

## Requirements

- Python3
- Flask

## Usage

Clone repository to local machine:

```
$ git clone git@github.com:BradHersh/chess-openings.git
```

Create virtual environment: 
```
$ python -m venv venv
```


Install requirements: 
```
$ pip install -r requirements.txt
```

Go into the project directory on command line and run the command:

```
$ source venv/bin/activate (for Mac)
```
```
$ venv/Scripts/activate (for Windows)
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
2. Developing many user stories that describe the features of the application. These stories are then broken down into tasks for each sprint filtered by perceived user value. We aimed to complete high value tasks first, followed by lower value tasks. Please see "User Stories Chess.xlsx" for more details..
3. Estimating time and resources required for each story. Allocating team members to different features for each sprint.
4. Consolidating user stories and refactoring code.
5. Designing and executing unit tests at the end of each sprint.

We broke the projec into three major sprints. You can see the designated user stories for each sprint in "User Stories Chess.xlsx". However, we will discuss our overarching philosophy for each sprint below. 

### Sprint 1:
In sprint 1 we primarily focussed on two main areas. Firstly, we fully familarised ourselves with the Flask web application framework and used this to begin building the structure for our application. Secondly, we began completing the most basic high value functionality required in an educational website - practicing content and testing. 

### Sprint 2:
In sprint 2 we were fully educated and capable of building our application, and our application contained essential functionality. In this sprint we began designing the stlying for our website, developing the additional essential functionality and connecting a back end to make our website fully dynamic. 

### Sprint 3:
In sprint 3, we had completely the most important, high value functionality required for our application. Sprint 3 was primarily concerned with including functionality which went above and beyond those required in the project brief. For example, included making the website entirely dynamic using DOM to generate web pages for when openings are added or removed. Furthermore, we worked on improving the aesthetics and styling of our website. 




## Architecture 

The web app was built using a flask web application framework, as well as utilising Python, Javascript, HTML, CSS, Jquery and AJAX. Please see the diagram below for the architecture of the web application. 

![](/app/static/img/Chess%20Architecture.PNG)

## Unit Tests

Unit tests were designed to test all our defined user stories. Frontend tests were created with selenium, while backend tests were created by sending a new user directly to the database. For example, if doing a test, the test will use selenium to: 
1. Open the website
2. Login to a user account
3. Navigate to the testing page
4. Select an opening
5. Complete the test and submit the result

To run these tests, make sure you have run the application using 
```
$ flask run
```

After that IN A NEW TERMINAL run 

```
$ python -m tests.systemtests
```
If all tests run succesfully, your terminal should ouput "Ran 11 tests in 74.166s"
```
$ python -m tests.unittestDB
```

Tests include:
- The ability to register
- The ability to log in
- The ability for an admin to create/delete an opening
- The ability to learn an opening
- The ability to test an opening
- The ability to check progress
- The ability to check results
- The ability to check feedback
- Check if the correct inputs are sent to the databbase


## Commit Logs

See log.txt

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
