import pytest

from ..plots.ecdfplot import plot_ecdf

import pytest
from arviz.plots.ecdfplot import plot_ecdf

def test_confidence_bands_and_pointwise_conflict():
    # Test case where both `confidence_bands` and `pointwise=True` are passed
    with pytest.raises(ValueError, match="Cannot specify both `confidence_bands='auto'` and `pointwise=True`"):
        plot_ecdf(
            values=[1, 2, 3, 4, 5],
            confidence_bands="auto",  # setting confidence_bands to "auto"
            pointwise=True  # setting pointwise=True, which should raise an error
        )

def test_fpr_and_ci_prob_conflict():
    # Test case where both `fpr` and `ci_prob` are passed
    with pytest.raises(ValueError, match="Cannot specify both `fpr` and `ci_prob`"):
        plot_ecdf(
            values=[1, 2, 3, 4, 5],
            fpr=0.05,  # setting fpr
            ci_prob=0.94  # setting ci_prob, which should raise an error
        )

def test_values2_and_cdf_conflict():
    # Test case where both `values2` and `cdf` are passed
    with pytest.raises(ValueError, match="You cannot specify both `values2` and `cdf`"):
        plot_ecdf(
            values=[1, 2, 3, 4, 5],
            values2=[1, 2, 3],  # setting values2
            cdf=lambda x: x  # setting cdf, which should raise an error
        )