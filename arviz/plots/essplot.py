"""Plot quantile or local effective sample sizes."""

import numpy as np 
import xarray as xr

from ..data import convert_to_dataset
from ..labels import BaseLabeller
from ..rcparams import rcParams
from ..sel_utils import xarray_var_iter
from ..stats import ess
from ..utils import _var_names, get_coords
from .plot_utils import default_grid, filter_plotters_list, get_plotting_function
#9 Stmts


def plot_ess(
    idata,
    var_names=None,
    filter_vars=None,
    kind="local",
    relative=False,
    coords=None,
    figsize=None,
    grid=None,
    textsize=None,
    rug=False,
    rug_kind="diverging",
    n_points=20,
    extra_methods=False,
    min_ess=400,
    labeller=None,
    ax=None,
    extra_kwargs=None,
    text_kwargs=None,
    hline_kwargs=None,
    rug_kwargs=None,
    backend=None,
    backend_kwargs=None,
    show=None,
    **kwargs,
): #10 Stmts
    r"""Generate quantile, local, or evolution ESS plots.

    The local and the quantile ESS plots are recommended for checking
    that there are enough samples for all the explored regions of the
    parameter space. Checking local and quantile ESS is particularly
    relevant when working with HDI intervals as opposed to ESS bulk,
    which is suitable for point estimates.

    Parameters
    ----------
    idata : InferenceData
        Any object that can be converted to an :class:`arviz.InferenceData` object
        Refer to documentation of :func:`arviz.convert_to_dataset` for details.
    var_names : list of str, optional
        Variables to be plotted. Prefix the variables by ``~`` when you want to exclude
        them from the plot. See :ref:`this section <common_var_names>` for usage examples.
    filter_vars : {None, "like", "regex"}, default None
        If `None` (default), interpret `var_names` as the real variables names. If "like",
        interpret `var_names` as substrings of the real variables names. If "regex",
        interpret `var_names` as regular expressions on the real variables names. See
        :ref:`this section <common_filter_vars>` for usage examples.
    kind : {"local", "quantile", "evolution"}, default "local"
        Specify the kind of plot:

        * The ``kind="local"`` argument generates the ESS' local efficiency for
          estimating quantiles of a desired posterior.
        * The ``kind="quantile"`` argument generates the ESS' local efficiency
          for estimating small-interval probability of a desired posterior.
        * The ``kind="evolution"`` argument generates the estimated ESS'
          with incrised number of iterations of a desired posterior.

    relative : bool, default False
        Show relative ess in plot ``ress = ess / N``.
    coords : dict, optional
        Coordinates of `var_names` to be plotted. Passed to :meth:`xarray.Dataset.sel`.
        See :ref:`this section <common_coords>` for usage examples.
    grid : tuple, optional
        Number of rows and columns. By default, the rows and columns are
        automatically inferred. See :ref:`this section <common_grid>` for usage examples.
    figsize : (float, float), optional
        Figure size. If ``None`` it will be defined automatically.
    textsize : float, optional
        Text size scaling factor for labels, titles and lines. If ``None`` it will be autoscaled
        based on `figsize`.
    rug : bool, default False
        Add a `rug plot <https://en.wikipedia.org/wiki/Rug_plot>`_ for a specific subset of values.
    rug_kind : str, default "diverging"
        Variable in sample stats to use as rug mask. Must be a boolean variable.
    n_points : int, default 20
        Number of points for which to plot their quantile/local ess or number of subsets
        in the evolution plot.
    extra_methods : bool, default False
        Plot mean and sd ESS as horizontal lines. Not taken into account if ``kind = 'evolution'``.
    min_ess : int, default 400
        Minimum number of ESS desired. If ``relative=True`` the line is plotted at
        ``min_ess / n_samples`` for local and quantile kinds and as a curve following
        the ``min_ess / n`` dependency in evolution kind.
    labeller : Labeller, optional
        Class providing the method ``make_label_vert`` to generate the labels in the plot titles.
        Read the :ref:`label_guide` for more details and usage examples.
    ax : 2D array-like of matplotlib_axes or bokeh_figure, optional
        A 2D array of locations into which to plot the densities. If not supplied, ArviZ will create
        its own array of plot areas (and return it).
    extra_kwargs : dict, optional
        If evolution plot, `extra_kwargs` is used to plot ess tail and differentiate it
        from ess bulk. Otherwise, passed to extra methods lines.
    text_kwargs : dict, optional
        Only taken into account when ``extra_methods=True``. kwargs passed to ax.annotate
        for extra methods lines labels. It accepts the additional
        key ``x`` to set ``xy=(text_kwargs["x"], mcse)``
    hline_kwargs : dict, optional
        kwargs passed to :func:`~matplotlib.axes.Axes.axhline` or to :class:`~bokeh.models.Span`
        depending on the backend for the horizontal minimum ESS line.
        For relative ess evolution plots the kwargs are passed to
        :func:`~matplotlib.axes.Axes.plot` or to :class:`~bokeh.plotting.figure.line`
    rug_kwargs : dict
        kwargs passed to rug plot.
    backend : {"matplotlib", "bokeh"}, default "matplotlib"
        Select plotting backend.
    backend_kwargs : dict, optional
        These are kwargs specific to the backend being used, passed to
        :func:`matplotlib.pyplot.subplots` or :class:`bokeh.plotting.figure`.
        For additional documentation check the plotting method of the backend.
    show : bool, optional
        Call backend show function.
    **kwargs
        Passed as-is to :meth:`mpl:matplotlib.axes.Axes.hist` or
        :meth:`mpl:matplotlib.axes.Axes.plot` function depending on the
        value of `kind`.

    Returns
    -------
    axes : matplotlib_axes or bokeh_figure

    See Also
    --------
    ess : Calculate estimate of the effective sample size.

    References
    ----------
    .. [1] Vehtari et al. (2021). Rank-normalization, folding, and
        localization: An improved Rhat for assessing convergence of
        MCMC. Bayesian analysis, 16(2):667-718.

    Examples
    --------
    Plot local ESS.

    .. plot::
        :context: close-figs

        >>> import arviz as az
        >>> idata = az.load_arviz_data("centered_eight")
        >>> coords = {"school": ["Choate", "Lawrenceville"]}
        >>> az.plot_ess(
        ...     idata, kind="local", var_names=["mu", "theta"], coords=coords
        ... )

    Plot ESS evolution as the number of samples increase. When the model is converging properly,
    both lines in this plot should be roughly linear.

    .. plot::
        :context: close-figs

        >>> az.plot_ess(
        ...     idata, kind="evolution", var_names=["mu", "theta"], coords=coords
        ... )

    Customize local ESS plot to look like reference paper.

    .. plot::
        :context: close-figs

        >>> az.plot_ess(
        ...     idata, kind="local", var_names=["mu"], drawstyle="steps-mid", color="k",
        ...     linestyle="-", marker=None, rug=True, rug_kwargs={"color": "r"}
        ... )

    Customize ESS evolution plot to look like reference paper.

    .. plot::
        :context: close-figs

        >>> extra_kwargs = {"color": "lightsteelblue"}
        >>> az.plot_ess(
        ...     idata, kind="evolution", var_names=["mu"],
        ...     color="royalblue", extra_kwargs=extra_kwargs
        ... )

    """
    coverage_array = []
    #11 Stmts

    valid_kinds = ("local", "quantile", "evolution")
    kind = kind.lower()
    if kind not in valid_kinds:
        coverage_array.append("1")
        raise ValueError(f"Invalid kind, kind must be one of {valid_kinds} not {kind}")
    #16 Stmts

    if coords is None:
        coords = {}
        coverage_array.append("2")
    #19 Stmts

    if "chain" in coords:
        coverage_array.append("3")
        raise ValueError("chain and draw are invalid coordinates for this kind of plot")
    #22 Stmts
    
    if "draw" in coords:
        coverage_array.append("4")
        raise ValueError("chain and draw are invalid coordinates for this kind of plot")
    #25 Stmts

    if labeller is None:
        coverage_array.append("5")
        labeller = BaseLabeller()
    #28 Stmts

    if kind == "evolution":
        coverage_array.append("6")
        extra_methods = False
    else: extra_methods
    #32 Stmts

    data = get_coords(convert_to_dataset(idata, group="posterior"), coords)
    var_names = _var_names(var_names, data, filter_vars)
    n_draws = data.sizes["draw"]
    n_samples = n_draws * data.sizes["chain"]
    #36 Stmts

    ess_tail_dataset = None
    mean_ess = None
    sd_ess = None
    #39 Stmts

    if kind == "quantile":
        coverage_array.append("7")
        probs = np.linspace(1 / n_points, 1 - 1 / n_points, n_points)
        xdata = probs
        ylabel = "{} for quantiles"
        ess_dataset = xr.concat(
            [
                ess(data, var_names=var_names, relative=relative, method="quantile", prob=p)
                for p in probs
            ],
            dim="ess_dim",
        )
        #45 Stmts
    elif kind == "local":
        coverage_array.append("8")
        probs = np.linspace(0, 1, n_points, endpoint=False)
        xdata = probs
        ylabel = "{} for small intervals"
        ess_dataset = xr.concat(
            [
                ess(
                    data,
                    var_names=var_names,
                    relative=relative,
                    method="local",
                    prob=[p, p + 1 / n_points],
                )
                for p in probs
            ],
            dim="ess_dim",
        )
        #51 Stmts
    else:
        coverage_array.append("9")
        first_draw = data.draw.values[0]
        ylabel = "{}"
        xdata = np.linspace(n_samples / n_points, n_samples, n_points)
        draw_divisions = np.linspace(n_draws // n_points, n_draws, n_points, dtype=int)
        ess_dataset = xr.concat(
            [
                ess(
                    data.sel(draw=slice(first_draw + draw_div)),
                    var_names=var_names,
                    relative=relative,
                    method="bulk",
                )
                for draw_div in draw_divisions
            ],
            dim="ess_dim",
        )
        #58 Stmts
        ess_tail_dataset = xr.concat(
            [
                ess(
                    data.sel(draw=slice(first_draw + draw_div)),
                    var_names=var_names,
                    relative=relative,
                    method="tail",
                )
                for draw_div in draw_divisions
            ],
            dim="ess_dim",
        )
        #59 Stmts

    plotters = filter_plotters_list(
        list(xarray_var_iter(ess_dataset, var_names=var_names, skip_dims={"ess_dim"})), "plot_ess"
    )
    length_plotters = len(plotters)
    rows, cols = default_grid(length_plotters, grid=grid)
    #62 Stmts

    if extra_methods:
        coverage_array.append("10")
        mean_ess = ess(data, var_names=var_names, method="mean", relative=relative)
        sd_ess = ess(data, var_names=var_names, method="sd", relative=relative)
    #65 Stmts

    essplot_kwargs = dict(
        ax=ax,
        plotters=plotters,
        xdata=xdata,
        ess_tail_dataset=ess_tail_dataset,
        mean_ess=mean_ess,
        sd_ess=sd_ess,
        idata=idata,
        data=data,
        kind=kind,
        extra_methods=extra_methods,
        textsize=textsize,
        rows=rows,
        cols=cols,
        figsize=figsize,
        kwargs=kwargs,
        extra_kwargs=extra_kwargs,
        text_kwargs=text_kwargs,
        n_samples=n_samples,
        relative=relative,
        min_ess=min_ess,
        labeller=labeller,
        ylabel=ylabel,
        rug=rug,
        rug_kind=rug_kind,
        rug_kwargs=rug_kwargs,
        hline_kwargs=hline_kwargs,
        backend_kwargs=backend_kwargs,
        show=show,
    )
    #66 Stmts

    if backend is None:
        coverage_array.append("11")
        backend = rcParams["plot.backend"]
    backend = backend.lower()
    #70 Stmts

    #true_CV = sum(coverage_array)
    #length_CV= len(coverage_array)
    #tot_CV = (true_CV/length_CV)*100
    with open("essplot_coverage.txt", "a") as output:
        output.write(f"{coverage_array}\n")
    #72 Stmts

    # TODO: Add backend kwargs
    plot = get_plotting_function("plot_ess", "essplot", backend)
    ax = plot(**essplot_kwargs)
    return ax
    #75 Stmts
