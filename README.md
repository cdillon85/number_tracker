**Easy Number Tracker (ENT)**

This is a simple app designed to track the numbers you provide it.

You can run ENT's code locally using the command `python manage.py runserver` or you can download a docker image from `cdillon85/numbertracker` and run it via a docker container with the following command `docker run -p <desired port>:8000 cdillon85/numbertracker`.

There is a simple UI through which you can interact with ENT, but if you want to play around with its api you can submit the following types of requests:

`GET /tracker/`: returns ENTs main page

`POST /tracker/number/` + request body `{"number": <number to track>}`: tracks the number you provide. Subsequent requests to this endpoint with the same payload will increment the number's count by 1.

`PUT /tracker/number/` + request body `{"number": <number to track>, "increment_value": <value to increment nunber count by>`: allows you to increment a specific number by an amount greater than 1.

`GET /tracker/numbers/`: returns all the numbers you have tracked so far and their counts

`DELETE /tracker/number/<number>`: deletes the number provided and its counts

