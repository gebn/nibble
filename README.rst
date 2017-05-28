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

Speed, distance and time calculations around quantities of digital information. Coming soon.

Installation
------------

::

    $ pip install nibble

Demo
----

.. code-block:: python

    from nibble.information import Information
    from nibble.duration import Duration
    from nibble.speed import Speed


    information = Information(1, Information.GIBIBYTES)
    print('{0}'.format(information))               # '1 GiB'
    print('{0:GB}'.format(information))            # '1.07GB'
    print('{0: GB}'.format(information))           # '1.07 GB'
    print('{0:,.2f| Mb}'.format(information))      # '8,589.93 Mb'

    speed = Speed(Information(20, Information.MEGABITS), Duration.SECOND)
    print('{0}'.format(speed))                     # '2.38 MiB/s'
    print('{0:Mb}'.format(speed))                  # '20Mb/s'
    print('{0: Gb/w}'.format(speed))               # '12,096 Gb/w'
    print(Speed.TEN_GIGABIT / 10
          == Speed.HUNDRED_MEGABIT * 10
          == Speed.GIGABIT)                        # True
    print('{0: dB/y}'.format(Speed.TEN_GIGABIT))   # '39.42 PB/y'
    print('{0:.2f| bB/mo}'.format(Speed.GIGABIT))  # 298.77 TiB/mo
