# Christmas 2020

## Flow

## 1. "I really dig your name"

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

### Ideas for Data to Send

- It turns out, you can put an arbitrary amount of bullshit before or after
  the body of a pdf file, meaning that a pdf document can be obfuscated
  by surrounding it by a huge amount of nonsense.
