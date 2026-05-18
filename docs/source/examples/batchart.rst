batchart.py
===========

Analyse a bat call, consisting of a sequence of pulses, and chart the timing parameters.

.. image:: ../ecology/pulse_width.png
  :width: 600
  :alt: Pulse Width

Pulse width is the duration of each pulse in milliseconds.

.. image:: ../ecology/pulse_pri.png
  :width: 600
  :alt: Pulse Repetition Interval

PRI (Pulse Repetition Interval) is the time between the peak of one pulse and the peak of
the next pulse. It is commonly used to examine echolocation rhythm and attack structure.

.. image:: ../ecology/pulse_ipi.png
  :width: 600
  :alt: Inter-Pulse Interval

IPI (Inter-Pulse Interval) is the silent interval between the end of one pulse and the start
of the next. Unlike PRI, it excludes pulse duration itself.

.. image:: ../ecology/pulse_dpri.png
  :width: 600
  :alt: Change in Pulse Repetition Interval


DPRI (Delta PRI) is the change in PRI between adjacent pulse pairs. Negative DPRI values indicate
shortening PRI values and therefore accelerating pulse rhythm ("speeding up"). Positive DPRI values
indicate increasing PRI values and therefore decelerating pulse rhythm ("slowing down").

.. automodule:: examples.batchart
   :members:
