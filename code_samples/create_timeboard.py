from datadog import initialize, api

options = {
	'api_key': 'c8eebbe62a568f8c2387936ef8793553',
	'app_key': 'aacf9a5ef2fb925a9e51b13ea2be14da9b27d25c'
}

initialize(**options)

title = "My Fun Timeboard"
description = "A pleasant timeboard that contains a custom metrics and \
							other potentially interesting things."
graphs = [{
	"definition":{
		"events": [],
		"requests": [
			{"q": "my_metric{host:if.local}"},
			{"q": "anomalies(avg:postgresql.rows_fetched{*}, 'basic', 2)"}
		],
		"viz": "timeseries"
	},
	"title": "my_metric, Postgres Anomalies"
}]

api.Timeboard.create(title=title,
										 description=description,
										 graphs=graphs,
										 read_only=True)