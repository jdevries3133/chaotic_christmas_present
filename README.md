# Christmas 2020

## See It Live

This project is running live at [thomasdevri.es.](https://thomasdevri.es)

Have fun trying to hack it! It should be easier than it was for my brother
with the source code at your disposal :)

## Running the Project

The project includes the Django web application and the swarm of TCP servers
for the TCP puzzles. Be forewarned that because the TCP servers were
implemented with python subprocesses, they will consume ~2gb of RAM.
I have since learned that I could have built a better implementation
with the [select module,](https://docs.python.org/3/library/select.html)
and maybe I will revisit this and update it some day.

Nonetheless, the project can be installed by enabling the two systemd
services at `custom_protocol_server/puzzle.service` and
`thomasdevri_es/gunicorn/gunicorn.service` (adjusting file paths
within appropriately), or by simply running these two commands from the
project root:

```bash
# no requirements.txt; built-in modules only
python3 -m custom_protocol_server/multiportserver

# in a separate terminal window
pip install -r thomasdevri_es/requirements.txt
python3 thomasdevri_es/manage.py migrate
python3 thomasdevri_es/manage.py runserver
```

## Flow

### Breadcrumbs

## 1. The Card

> Some people don't have the best family relationships, but I've got to say,
> I really `dig thomasdevri.es`! I didn't `curl` any ribbons for you this year
> `thomasdevri.es`, but I think you're going to `SQ`uea`L`ing in excitement
> for your present this year nonetheless.

## 2. `https://thomasdevri.es/`

- At the root url:
  - Have a detailed page
  - Allow a SQL injection attack through a form to expose the next clue.

## 3. SQL Injection

The "message" field of the contact form is vulnerable to SQL injection,
and will spew the results of a valid query back at the user. Thomas can
use this to find the `staff_site_passwords` table, containing plain
text passwords to several inactive users, but one active user: `thomasdev`,
with the password `i_am_an_insecure_chungus`.

## 4. `/staff` route

- Have a page where the user must login
- List it in the `sitemap.xml` and `robots.txt`, so that he can concievably
  find it before he can access it.
- He will have to get the password through SQL injection attack in step 3.

### Staff Login

A plain login page that Thomas can use to get to the dashboard with the
credentials gained through SQL injection

### Staff Dashboard

A mock company dashboard with "top secret data." In part, it will detail the
company's experimental TCP protocols, and give Thomas the ports to look for
(or maybe port ranges to make him sniff it out).

## Custom TCP Protocols

> Implement custom TCP protocols, each of which will be puzzles with clues
> towards the next step.

Implementation is in `custom_protocol_server`. Swarms of simple TCP servers
on many ports can be run together. The `SubprocessServerManager` class only
needs to be provided a schema, a dictionary like the one below, and it
can spin up and supervise many TCP servers with subprocesses.

```python
schema = {
    'unique_server_identifier': {
        'host': '127.0.0.1',
        'port': 6001,
        'message': 'test server 1 message'
    }
}
```

For the puzzle, I used this system to expose several puzzles as linked
lists across many TCP ports. That is achieved by the hard coded default
configuration found
[here.](https://github.com/jdevries3133/chaotic_christmas_present/blob/main/custom_protocol_server/multiportserver/schema.py)
