.. Active_Learning_Driver documentation master file, created by
   sphinx-quickstart on Mon May 9 2022.

.. Lines starting with two dots are comments if no special commands are found

############################################
ChIMES Active Learning Driver Documentation
############################################

*Note: This documentation is under still construction.*


.. TO DO:
.. ------

.. * Hierarchical fitting mode overivew
.. * Correction fitting mode overivew
.. * Cluster fitting mode overivew
.. * Committe fitting mode overivew
.. * Sample config files
.. * Complete sample input decks



----------

The Active Learning Driver (ALD) is an extensible multifunction workflow tool for generating ChIMES [1] models. At its simplest, the ALD can be used for model generation via iterative refinement [2], at at its most complex, via active learning [3]. 

Before proceeding, the user is **strongly** encouraged to familiarize themselves with the ChIMES literature (See references below) and ChIMES LSQ user manual. **UPDATE LINK** Note that the ALD itself *only* contains the tools necessary to orchestrate model generation and active learning, and must be used in conjunction with the ChIMES design matrix generator, a supported MD code, and a supported quantum code. Note also that the ALD is *only* intended for use on high performance computing platforms and currently only supports runs via slurm (SBATCH) schedulers. For additional details, see the :ref:`page-quickstart` page.




| [1] `(link) <https://doi.org/10.1021/acs.jctc.7b00867>`_ R.K. Lindsey, L.E. Fried, N. Goldman, *JCTC*, **13**, 6222 (2017)
| [2] `(link) <https://doi.org/10.1063/5.0012840>`_ R.K. Lindsey, N. Goldman, L.E. Fried, S. Bastea, *JCP*, **153** 054103 (2020) 
| [3] `(link) <https://doi.org/10.1063/5.0021965>`_ R.K. Lindsey, L.E. Fried, N. Goldman, S. Bastea, *JCP*, **153** 134117 (2020) 

The ChIMES Calculator is developed at Lawrence Livermore National Laboratory with funding from the US Department of Energy (DOE), and is open source, distributed freely under the terms of the (specify) License.


For additional information, see:

.. toctree::
   :maxdepth: 1
   
   overview
   quickstart
   options
   citing  
   extending
   contact
   legal



.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

---------------

This work was produced under the auspices of the U.S. Department of Energy by
Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

This work was prepared as an account of work sponsored by an agency of the
United States Government. Neither the United States Government nor Lawrence
Livermore National Security, LLC, nor any of their employees makes any warranty,
expressed or implied, or assumes any legal liability or responsibility for the
accuracy, completeness, or usefulness of any information, apparatus, product, or
process disclosed, or represents that its use would not infringe privately owned
rights. Reference herein to any specific commercial product, process, or service
by trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or Lawrence Livermore National Security, LLC. The views and
opinions of authors expressed herein do not necessarily state or reflect those
of the United States Government or Lawrence Livermore National Security, LLC,
and shall not be used for advertising or product endorsement purposes.
