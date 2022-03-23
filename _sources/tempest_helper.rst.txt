tempest_helper
==============

Loading data
************

.. currentmodule:: tempest_helper
.. autofunction:: get_trajectories

Saving data
************

.. autofunction:: save_trajectories_netcdf

Plotting data
*************

.. autofunction:: plot_trajectories_cartopy

Analysing data
**************

.. autofunction:: count_hemispheric_trajectories
.. autofunction:: count_trajectories

Utilities
*********

These functions are used by other functions, but have been exposed here in case
they are useful to users.


.. autofunction:: convert_date_to_step
.. autofunction:: fill_trajectory_gaps
.. autofunction:: storms_overlap_in_time
.. autofunction:: storms_overlap_in_space
.. autofunction:: write_track_line
.. autofunction:: rewrite_track_file


Unit tests
**********

.. autoclass:: test_tempest_helper.utils.TempestHelperTestCase
   :members: assertNetcdfEqual, assertTempestDictEqual


