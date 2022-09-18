import warnings

warnings.warn(
    'The module rpy2_arrow.pyarrow_rarrow is moved to rpy2_arrow.arrow',
    DeprecationWarning
)
from .arrow import *  # noqa: E402,F401,F403
