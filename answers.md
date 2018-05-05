# Prerequisites
I had initially planned on using a nice Docker/Vagrant setup, but as I progressed, I found that the documentation for using the Datadog agent in Mac OS was a bit clearer. For instance, the Docker documentation is vague on the location of the agent config file. After running into this, comparing the Docker documentation with the Mac OS documentation, I decided to go ahead with a direct installation of the Datadog agent on my Mac OS system. The following answers reflect this environment.

# Collecting Metrics
## Adding tags
In `/opt/datadog-agent/etc`, I configured the file `datadog.yaml` to include the following snippet:

![tags in config]
(https://github.com/cswatt/hiring-engineers/raw/tech-writer/img/01-tags_conf.png)

These uncreatively named tags can then be seen on the Host Map page.

![tags in ui]
(https://github.com/cswatt/hiring-engineers/raw/tech-writer/img/02-tags_ui.png)

## Installing a database integration
Since PostgreSQL was already installed on my machine, I chose to install the PostgreSQL integration. When trying to verify permissions, I encountered the following error in the documentation:

```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

The correct version should be:
```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);" \
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

I have included my postgres config file, [`conf.yaml`](code_samples/conf.yaml).

## Creating a custom agent check and setting collection interval

I added `my_metric.py` and `my_metric.yaml` to the `/opt/datadog-agent/etc/checks.d` and `/opt/datadog-agent/etc/conf.d` folders, respectively. For greater configurability, instead of hardcoding the range [0, 1000] into the check, the instance has configurable variables `floor` and `ceiling`. I then set `min_collection_interval` to 45.


```
instances:
  - floor: 0
    ceiling: 1000
    min_collection_interval: 45
```

### Bonus Question: Collection Intervals
While you could set the collection interval within the Python check file (with the default collection interval being 15s, you could increment a counter with each `check()` call and only call `self.gauge` every 3rd time) but it just seems like a weird approach when the YAML config file is right there. It seems to me that the most obvious way to set the collection interval is within the YAML config file. 

I’m going to assume that the “Python check file” mentioned in the Bonus Question is actually referring to the YAML config file, because otherwise, this question doesn’t seem bonus enough. 

Using Agent 5, it appears you can set `check_freq` in the agent config file. This however is deprecated in Agent 6.

# Visualizing Data
## Creating a Timeboard via API
`create_timeboard.py` uses the Datadog API to create a timeboard called My Fun Timeboard, because I give things terrible names.

I opted to use the `postgresql.rows_fetched` metric (with the anomaly function applied), scoped over all the databases I’ve got on my machine from various past projects.

## Using the Dashboard UI
Here’s what the timeboard looks like by default.

Here’s the timeboard after the timeframe is set to the past 5 minutes.

Here’s a cool email I received!

### Bonus Question: Anomaly Graph
The anomaly graph is the anomaly function applied to `postgresql.rows_fetched{*}`, which is the number of rows fetched across all postgres databases — plus an expected range for how this metric should behave. I used the basic anomaly detection algorithm with `bounds = 2`. The line displays in red when it falls outside the “normal” range expected by the algorithm.
