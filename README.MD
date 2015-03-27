# Test of Chotot.vn

## TODO
	
* Refactor, reduce line of code, optimze processing
* Separate development mode, test mode and production mode for database
* Optimize queries

**Change database connect at *model/base.py*. We should refactor it to config file soon**

Install requirements

	pip install -r requirements.txt

Run tests

	python test.py

Result:

![Previews](http://i.imgur.com/ysMtTa5.png)

List of GETs API:

List of users
	
	GET /api/v1/users

Return from server
	
	{
		"status": "SUCESS",
		"data": [
			{
				"email": "duy.thinht@gmail.com",
				"id": 1
			},
			{
				"email": "duythinht@gmail.com",
				"id": 2
			}
		]
	}


User Detail

	GET /api/v1/users/:id

Return from server

	{
		"data": {
			"email": "duy.thinht@gmail.com",
			"id": 1
		},
		"status": "SUCCESS"
	}


List of projects
	
	GET /api/v1/projects

Return from server
	
	{
		"status": "SUCESS",
		"data": [
			{
				"content": "Just a test for project data", 
				"due_date": "Thu, 12 Mar 2015 12:00:00 GMT", 
				"id": 1, 
				"title": "Test Project"
			},
			{
				"content": "Just a test for project data", 
				"due_date": "Thu, 12 Mar 2015 12:00:00 GMT", 
				"id": 1, 
				"title": "Test Project"
			}
		]
	}


User Detail

	GET /api/v1/projects/:id

Return from server

	{
		"data": {
			"content": "Just a test for project data", 
			"due_date": "Thu, 12 Mar 2015 12:00:00 GMT", 
			"id": 1, 
			"title": "Test Project"
		},
		"status": "SUCCESS"
	}


# Same as other apis:
List of teams
	
	GET /api/v1/teams


Detail of team

	GET /api/v1/teams/:id

List of tasks

	GET /api/v1/tasks

Detail of tasks
	
	GET /api/v1/tasks/:id	
