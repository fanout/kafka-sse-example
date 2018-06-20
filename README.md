# Kafka SSE Example

This example project reads messages from a Kafka service and exposes the data over a streaming API using Server-Sent Events (SSE) protocol over HTTP. It is written using Python & Django, and relies on Pushpin for managing the streaming connections.

## Setup and use

Setup virtualenv and install dependencies:

```sh
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

Create a suitable `.env` with Kafka and Pushpin settings:

```sh
KAFKA_CONSUMER_CONFIG={"bootstrap.servers":"localhost:9092","group.id":"mygroup"}
GRIP_URL=http://localhost:5561
```

Run the Django server:

```sh
python manage.py runserver
```

Run Pushpin:

```sh
pushpin --route="* localhost:8000"
```

Run the `relay` command:

```sh
python manage.py relay
```

The `relay` command sets up a Kafka consumer according to `KAFKA_CONSUMER_CONFIG`, subscribes to all topics, and re-publishes received messages to Pushpin, wrapped in SSE format.

Clients can listen to events by making a request (through Pushpin) to `/events/{topic}/`:

```sh
curl -i http://localhost:7999/events/test/
```

The output stream might look like this:

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Transfer-Encoding: chunked
Connection: Transfer-Encoding

event: message
data: hello

event: message
data: world
```

## How it works

The code is relatively simple. [views.py](kafka_events/views.py) sets up the SSE endpoint and [relay.py](kafka_events/management/commands/relay.py) does the message I/O.

## Limitations

This is a simple example project. In a real project you'd want to consider:

* Authenticating clients
* Only subscribing to Kafka topics for which there are listening clients
