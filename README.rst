nibble
======

.. image:: https://img.shields.io/pypi/status/nibble.svg
   :target: https://pypi.python.org/pypi/nibble
.. image:: https://img.shields.io/pypi/v/nibble.svg
   :target: https://pypi.python.org/pypi/nibble
.. image:: https://img.shields.io/pypi/pyversions/nibble.svg
   :target: https://pypi.python.org/pypi/nibble
.. image:: https://travis-ci.org/gebn/nibble.svg?branch=master
   :target: https://travis-ci.org/gebn/nibble
.. image:: https://coveralls.io/repos/github/gebn/nibble/badge.svg?branch=master
   :target: https://coveralls.io/github/gebn/nibble?branch=master
.. image:: https://landscape.io/github/gebn/nibble/master/landscape.svg?style=flat
   :target: https://landscape.io/github/gebn/nibble/master

Speed, distance and time calculations around quantities of digital information.

Installation
------------

::

    $ pip install nibble

Demo
----

The following snippet provides an example of Nibble's ability to format and manipulate quantities of information, durations and speeds.
For explanations of what's going on, see each class's section below.

.. code-block:: python

    from nibble import Information, Duration, Speed


    information = Information(123, Information.GIBIBITS)
    print('{0}'.format(information))               # '15.38 GiB'
    print('{0:GB}'.format(information))            # '16.51GB'
    print('{0: GB}'.format(information))           # '16.51 GB'
    print('{0:,.2f| Mb}'.format(information))      # '132,070.24 Mb'

    speed = Speed(Information(20, Information.MEGABITS), Duration.SECOND)
    print('{0}'.format(speed))                     # '2.38 MiB/s'
    print('{0:Mb}'.format(speed))                  # '20Mb/s'
    print('{0: Gb/w}'.format(speed))               # '12,096 Gb/w'
    print(Speed.TEN_GIGABIT / 10
          == Speed.HUNDRED_MEGABIT * 10
          == Speed.GIGABIT)                        # True
    print('{0: dB/y}'.format(Speed.TEN_GIGABIT))   # '39.42 PB/y'
    print('{0:.2f| bB/mo}'.format(Speed.GIGABIT))  # '298.77 TiB/mo'

Information
-----------

Nibble represents all quantities of information in terms of the smallest unit: bits.
The syntax for formatting ``Information`` objects is:

::

   [number format|][ ][unit symbol or category]

- ``[number format|]`` is a valid floating point format specification followed by a pipe symbol so it can be distinguished from the rest of the format string
- ``[ ]`` is an optional blank space separating the number from the unit symbol
- ``[unit symbol or category]`` is either a single unit to represent the information in, e.g. Gb, or a category of units (see below), in which case Nibble will choose the most appropriate one

The default format specification is ``'.2f| bB'``.

Units
~~~~~

At the lower end, Nibble supports bits, nibbles (of course) and bytes.
Larger units fall into one of four categories.
They are either binary or decimal (they can be expressed as 2\ :sup:`n` or 10\ :sup:`n` respectively), or bit or byte based:

+---------+--------+------+----------------+---------------------+
| Base    | Suffix | Unit | Example        | Information         |
+=========+========+======+================+=====================+
| Binary  | Bit    | -ib  | Kibibit (Kib)  | 2\ :sup:`20` bits   |
+---------+--------+------+----------------+---------------------+
| Binary  | Byte   | -iB  | Kibibyte (KiB) | 2\ :sup:`20` bytes  |
+---------+--------+------+----------------+---------------------+
| Decimal | Bit    | -b   | Kilobit (Kb)   | 10\ :sup:`6` bits   |
+---------+--------+------+----------------+---------------------+
| Decimal | Byte   | -B   | Kilobyte (kB)  | 10\ :sup:`6` bytes  |
+---------+--------+------+----------------+---------------------+

It is a `common misconception <https://stackoverflow.com/q/19819763/2765666>`_ that there are 1024 bytes in a kilobyte.
If you'd like to work in multiples of 1024, use the *-ibibyte* units instead.

Nibble supports all of the above units with prefixes from *Ki-* to *Yi-*.
For the full list, consult the ``_SYMBOLS`` dict in the `Information <https://github.com/gebn/nibble/blob/master/nibble/information.py>`_ class.

Categories
~~~~~~~~~~

In addition to representing a quantity of information in a specific unit, nibble can determine the most appropriate one to use from a range.
These ranges are called *categories*, and correspond to rows in the table above.

+----------+---------+--------+---------------+--------------+
| Category | Base    | Suffix | Smallest Unit | Largest Unit |
+==========+=========+========+===============+==============+
| bb       | Binary  | Bit    | Bit           | Yobibit      |
+----------+---------+--------+---------------+--------------+
| bB       | Binary  | Byte   | Byte          | Yobibyte     |
+----------+---------+--------+---------------+--------------+
| db       | Decimal | Bit    | Bit           | Yottabit     |
+----------+---------+--------+---------------+--------------+
| dB       | Decimal | Byte   | Byte          | Yottabyte    |
+----------+---------+--------+---------------+--------------+

The first letter of the category refers to the base, *b* and *d* for binary and decimal respectively.
The second letter refers to the suffix, *b* and *B* for bit and byte respectively.
Therefore, to format an amount of information in the bits, kilobits, megabits, gigabits etc., use ``'{0:db}'.format(...)``.

The only remaining ambiguity is how Nibble determines the best unit to use in each category.
It simply chooses the largest unit where the amount of information to represent is >=1 of that unit, falling back on the smallest unit where that's not possible (e.g. representing less than 1 byte in *bB* or *dB*).
For example, 1 GiB would be shown in GiB. One bit less would be shown in MiB.

Shortcuts
~~~~~~~~~

The following class constants are provided for common quantities of information:

+----------+------------+
| Constant | Equivalent |
+==========+============+
| ``ZERO`` | 0 b        |
+----------+------------+

Duration
--------

This class is Nibble's equivalent of ``datetime.timedelta()``.
Why re-implement?
Because that only goes down to microsecond precision, and lacks months and years.
To make working with this class as easy as possible, a ``from_timedelta()`` method and ``timedelta`` property are provided - however bear in mind these will lose precision by virtue of working at a coarser level of granularity.

The syntax for formatting ``Duration`` objects is:

::

   [number format|][ ][unit symbol]

- ``[number format|]`` is a valid floating point format specification followed by a pipe symbol so it can be distinguished from the rest of the format string
- ``[ ]`` is an optional blank space separating the number from the unit symbol
- ``[unit symbol]`` is a time unit to represent the duration in (see below)

By default, durations will be shown in the largest unit where the time period is greater or equal to 1 of that unit.
For example, 1 minute would be shown as *1 m*. One nanosecond less would be shown as *60.00s*.

Units
~~~~~

+--------+--------------+
| Symbol | Meaning      |
+========+==============+
| ``ns`` | Nanoseconds  |
+--------+--------------+
| ``us`` | Microseconds |
+--------+--------------+
| ``ms`` | Milliseconds |
+--------+--------------+
| ``s``  | Seconds      |
+--------+--------------+
| ``m``  | Minutes      |
+--------+--------------+
| ``h``  | Hours        |
+--------+--------------+
| ``d``  | Days         |
+--------+--------------+
| ``w``  | Weeks        |
+--------+--------------+
| ``mo`` | Months       |
+--------+--------------+
| ``y``  | Years        |
+--------+--------------+

Shortcuts
~~~~~~~~~

The following class constants are provided for common durations:

+------------+------------+
| Constant   | Equivalent |
+============+============+
| ``ZERO``   | 0 ns       |
+------------+------------+
| ``SECOND`` | 1 s        |
+------------+------------+

Speed
-----

Speeds can be created using the standard constructor, or by calling ``.in_duration()` with a ``Duration`` on an ``Information`` object.

The syntax for formatting ``Speed`` objects is:

::

   [number format|][ ][unit symbol or category][/time unit]

- ``[number format|]`` is a valid floating point format specification followed by a pipe symbol so it can be distinguished from the rest of the format string
- ``[ ]`` is an optional blank space separating the number from the unit symbol
- ``[unit symbol or category]`` is either a single unit to represent the information in, e.g. Gb, or a category of units (see above)
- ``[/time unit]`` is the time unit to show the quantity of information over

The default format for speed is ``'.2f| bB/s'``.

Shortcuts
~~~~~~~~~

The following class constants are provided for common speeds:

+---------------------+--------------+
| Constant            | Equivalent   |
+=====================+==============+
| ``ZERO``            | 0 b/s        |
+---------------------+--------------+
| ``TEN_MEGABIT``     | 10 Mb/s      |
+---------------------+--------------+
| ``HUNDRED_MEGABIT`` | 100 Mb/s     |
+---------------------+--------------+
| ``GIGABIT``         | 1 Gb/s       |
+---------------------+--------------+
| ``TEN_GIGABIT``     | 10 Gb/s      |
+---------------------+--------------+
| ``FORTY_GIGABIT``   | 40 Gb/s      |
+---------------------+--------------+
| ``HUNDRED_GIGABIT`` | 100 Gb/s     |
+---------------------+--------------+
| ``E0`` / ``DS0``    | 64 Kb/s      |
+---------------------+--------------+
| ``E1``              | 2.048 Mb/s   |
+---------------------+--------------+
| ``E2``              | 8.448 Mb/s   |
+---------------------+--------------+
| ``E3``              | 34.368 Mb/s  |
+---------------------+--------------+
| ``E4``              | 139.264 Mb/s |
+---------------------+--------------+
| ``E5``              | 565.148 Mb/s |
+---------------------+--------------+
| ``T1`` / ``DS1``    | 1.544 Mb/s   |
+---------------------+--------------+
| ``T1C`` / ``DS1C``  | 3.152 Mb/s   |
+---------------------+--------------+
| ``T2`` / ``DS2``    | 6.312 Mb/s   |
+---------------------+--------------+
| ``T3`` / ``DS3``    | 44.736 Mb/s  |
+---------------------+--------------+
| ``T4`` / ``DS4``    | 274.176 Mb/s |
+---------------------+--------------+
| ``T5`` / ``DS5``    | 400.352 Mb/s |
+---------------------+--------------+

Issues
------

A library like this is useless if not correct, which is why I've invested so much time in test coverage.
If you find an incorrect result, please create a new issue with the input as well as expected and actual output.
