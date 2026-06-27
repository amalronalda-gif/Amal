"""Strategy registry.

Ablation-tested (4 markets, ~7 months of data): strategies that consistently
hurt results or never fire are kept on disk but NOT registered:
candlestick (-7.6R), support_resistance (-7.0R), trend_pullback (-4.7R),
ict_ote (-4.1R), session_manipulation (-2.6R), rci (-0.4R, fires 2% of bars),
amd_phase (-7.2R: a fade signal that overlaps liquidity_sweep/order_block
and suppresses borderline trend trades — combined edge dropped +37.7->+30.5R).
Re-add an import + list entry to re-enable one.
"""

from .base import Context, Signal, Strategy, NEUTRAL
from .liquidity_sweep import LiquiditySweep
from .trend_following import TrendFollowing
from .momentum import Momentum
from .mean_reversion import MeanReversion
from .market_structure import MarketStructure
from .fair_value_gap import FairValueGap
from .breakout import Breakout
from .volume_flow import VolumeFlow
from .ichimoku_cloud import IchimokuCloud
from .order_block import OrderBlock
from .rsi_divergence import RsiDivergence
from .vwap_flow import VwapFlow
from .double_top import DoubleTopBottom
from .head_shoulders import HeadShoulders
from .trendline import Trendline

ALL_STRATEGIES: list[type[Strategy]] = [
    LiquiditySweep,
    TrendFollowing,
    Momentum,
    MeanReversion,
    MarketStructure,
    FairValueGap,
    Breakout,
    VolumeFlow,
    IchimokuCloud,
    OrderBlock,
    RsiDivergence,
    VwapFlow,
    DoubleTopBottom,
    HeadShoulders,
    Trendline,
]
