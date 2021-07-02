# HiperLine

[![Build](https://github.com/samueljoaquim/hiperline/actions/workflows/build.yml/badge.svg)](https://github.com//samueljoaquim/hiperline/actions/workflows/build.yml)

## About
**HiperLine** is a framework that allows you to build a timeline table of items
(person born, constructions made, places discovered etc.) and compare their ages
with milestones (e.g., an historical event that happened). You can make any
kind of relation, no matter how distant in time items and milestones are.

## Usage example
Supose you want to make a timeline of milestones that happened in a decade, say
the 30s. You can add people (Winston Churchill, Barack Obama, Gandhi and Woody
Allen), historical events (Bastille Day, beggining of Medieval Age) and whatever
you'd like to compare. Then, add milestones of the 30s (Construction of the Empire
State Building, the Hindenburg explosion and outbreak of WW II). Your code should
look like this:

```py
from datetime import datetime
from hiperline.model import Item, Person, Scenario

date_format = "%Y-%m-%d"

items = {
    Person(name="Winston Churchill",start=datetime(1874,11,30), end=datetime(1965,1,24)),
    Person(name="Barack Obama",start=datetime(1961,8,4)),
    Person(name="Mahatma Gandhi",start=datetime(1869,10,2), end=datetime(1984,1,30)),
    Person(name="Woody Allen",start=datetime(1935,12,1)),
    Item(name="Bastille Day",start=datetime(1789,7,14)),
    Item(name="Beggining of Medieval Age",start=datetime(476,1,1))
}

milestones = {
    Item(name="Empire State Building", start=datetime(1931,4,11)),
    Item(name="Hindenburg Explosion", start=datetime(1937,5,6)),
    Item(name="World War II", start=datetime(1939,9,1))
}

scenario = Scenario(
    name="The 30s",
    items=items,
    milestones=milestones,
    start=datetime(1930,1,1),
    end=datetime(1939,12,31)
)

```

Now, if you run ```scenario.generate()```, you will get a Python table that represents
the timeline. You can also use ```print(scenario.pretty())```, which will generate a table
that looks like that:

<table>
    <thead>
        <tr>
            <th></th>
            <th>Empire State Building (11/04/1931)</th>
            <th>Hindenburg Explosion (06/05/1937)</th>
            <th>World War II (01/09/1939)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Beggining of Medieval Age</td>
            <td>Beggining of Medieval Age had happened 1456 year(s) prior</td>
            <td>Beggining of Medieval Age had happened 1462 year(s) prior</td>
            <td>Beggining of Medieval Age had happened 1464 year(s) prior</td>
        </tr>
        <tr>
            <td>Bastille Day</td>
            <td>Bastille Day had happened 141 year(s) prior</td>
            <td>Bastille Day had happened 147 year(s) prior</td>
            <td>Bastille Day had happened 150 year(s) prior</td>
        </tr>
        <tr>
            <td>Mahatma Gandhi</td>
            <td>Mahatma Gandhi had 61 year(s) old</td>
            <td>Mahatma Gandhi had 67 year(s) old</td>
            <td>Mahatma Gandhi had 69 year(s) old</td>
        </tr>
        <tr>
            <td>Winston Churchill</td>
            <td>Winston Churchill had 56 year(s) old</td>
            <td>Winston Churchill had 62 year(s) old</td>
            <td>Winston Churchill had 64 year(s) old</td>
        </tr>
        <tr>
            <td>Woody Allen</td>
            <td>Woody Allen was 4 year(s) short to be born</td>
            <td>Woody Allen had 1 year(s) old</td>
            <td>Woody Allen had 3 year(s) old</td>
        </tr>
        <tr>
            <td>Barack Obama</td>
            <td>Barack Obama was 30 year(s) short to be born</td>
            <td>Barack Obama was 24 year(s) short to be born</td>
            <td>Barack Obama was 21 year(s) short to be born</td>
        </tr>
    </tbody>
</table>

Try it!!
