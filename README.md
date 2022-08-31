<p style="text-align:center;">
    <img src="./doc/ChIMES_Github_logo-2.png" alt="" width="250"/>
</p>
<hr>

ChIMES Active Learning Driver Documentation
------------------------------------------------


*Note: This documentation is under still construction.*

The Active Learning Driver is an extensible multifunction workflow tool for generating ChIMES [1] models. At its simplest, the ALD can be used for model generation via iterative refinement [2], at at its most complex, via active learning [3].

Before proceeding, the user is strongly encouraged to familiarize themselves with the ChIMES literature (See references below) and ChIMES LSQ user manual. Note that the ALD itself only contains the tools necessary to orchestrate model generation and active learning, and must be used in conjunction with the ChIMES design matrix generator, a supported MD code, and a supported quantum code. Note also that the ALD is only intended for use on high performance computing platforms and currently only supports runs via Slurm (SBATCH) schedulers. 

* [1] [**link**](https://doi.org/10.1021/acs.jctc.7b00867) R.K. Lindsey, L.E. Fried, N. Goldman, JCTC, 13, 6222 (2017)
* [2] [**link**](https://doi.org/10.1063/5.0012840) R.K. Lindsey, N. Goldman, L.E. Fried, S. Bastea, JCP, 153 054103 (2020)
* [3] [**link**](https://doi.org/10.1063/5.0021965) R.K. Lindsey, L.E. Fried, N. Goldman, S. Bastea, JCP, 153 134117 (2020)

The Active Learning Driver was developed at Lawrence Livermore National Laboratory with funding from the US Department of Energy (DOE), and is open source, distributed freely under the terms of the LGPL v3.0 License.

This work was produced under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.


<hr>

Documentation
----------------

[**Documentation**](https://https://al-driver.readthedocs.io/en/latest/) is available, but under construction.

<hr>

Community
------------------------

Questions, discussion, and contributions (e.g. bug fixes, documentation, and extensions) are welcome. 

Additional Resources: [ChIMES Google group](https://groups.google.com/g/chimes_software).

<hr>

Contributing
------------------------

Contributions to the The ChIMES AL Driver should be made through a pull request, with ``develop`` as the destination branch. A test suite log file should be attached to the PR.  The `develop` branch has the latest contributions. Pull requests should target `develop`, and users who want the latest package versions, features, etc. can use `develop`.

<hr>


Authors
----------------

The The ChIMES AL Driver was developed by Rebecca K. Lindsey.

Contributors can be found [here](https://github.com/rk-lindsey/al_driver/graphs/contributors).

<hr>

<!--- Citing
<!--- ----------------
<!--- 
<!--- See [the documentation](https://chimes-calculator.readthedocs.io/en/latest/citing.html) for guidance on referencing ChIMES and the ChIMES calculator in <> a publication.

<hr>

License
----------------

The ChIMES AL Driver is distributed under terms of [LGPL v3.0 License](https://github.com/rk-lindsey/chimes_calculator/blob/main/LICENSE). This work was produced under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. LLNL-CODE-839335
