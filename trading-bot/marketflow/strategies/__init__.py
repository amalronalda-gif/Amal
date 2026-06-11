"""Strategy registry."""

from .base import Context, Signal, Strategy, NEUTRAL
from .liquidity_sweep import LiquiditySweep
from .trend_following import TrendFollowing
from .momentum import Momentum
from .mean_reversion import MeanReversion
from .market_structure import MarketStructure
from .fair_value_gap import FairValueGap
from .breakout import Breakout
from .candlestick import Candlestick
from .volume_flow import VolumeFlow
from .ichimoku_cloud import IchimokuCloud
from .support_resistance import SupportResistance
from .order_block import OrderBlock
from .rsi_divergence import RsiDivergence
from .vwap_flow import VwapFlow
from .trend_pullback import TrendPullback
from .double_top import DoubleTopBottom
from .head_shoulders import HeadShoulders
from .trendline import Trendline
from .rci_reverse import RciReverse
from .session_manipulation import SessionManipulation
from .ict_ote import IctOte

ALL_STRATEGIES: list[type[Strategy]] = [
    LiquiditySweep,
    TrendFollowing,
    Momentum,
    MeanReversion,
    MarketStructure,
    FairValueGap,
    Breakout,
    Candlestick,
    VolumeFlow,
    IchimokuCloud,
    SupportResistance,
    OrderBlock,
    RsiDivergence,
    VwapFlow,
    TrendPullback,
    DoubleTopBottom,
    HeadShoulders,
    Trendline,
    RciReverse,
    SessionManipulation,
    IctOte,
]
