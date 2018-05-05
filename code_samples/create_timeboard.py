from datadog import initialize, api

# Redacted for security.
options = {
	'api_key': '',
	'app_key': ''
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