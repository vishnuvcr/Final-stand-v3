# Data-source review

## Primary exchange sources
- NSE derivatives reports: https://www.nseindia.com/all-reports-derivatives
- NSE NIFTY 50 F&O contract page: https://www.nseindia.com/static/products-services/equity-derivatives-nifty50
- NSE contract specifications: https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- NSE expiry-day circular: NSE/FAOP/68747

NSE states that current NIFTY weekly index options expire Tuesday (previous trading day if Tuesday is a holiday). NSE's circular documents the transition from Thursday weekly expiries to Tuesday weekly expiries in 2025.

## Intraday option datasets

### Hugging Face — thetrademarkk/india-index-options-1m
Dataset URL: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- 1-minute OHLCV(+OI) for NIFTY, BANKNIFTY and SENSEX.
- Approximately 2021-2026 coverage.
- NIFTY option files are organized as options/NIFTY/{EXPIRY}.parquet.
- Schema includes timestamp (IST), OHLC, volume, open_interest, trading_day, symbol, strike, option_type and expiry.
- Dataset notes partial coverage of illiquid/far strikes.
- License: CC BY-NC 4.0.
- Raw files will NOT be committed to this public repository. GitHub Actions will download and cache them using HF_TOKEN; provenance and hashes will be retained here.

### GitHub / broker-dependent alternatives
- i9-tradebot/NIFTY_Options_Historical_Data_Collector: 1-minute NIFTY option candles, broker/API dependent.
- JATINDHURVE/Indian-market-data-pipeline: ICICI Breeze based 1-minute NIFTY weekly options.
- mukhilj/breeze_options_pipeline: 1-minute NIFTY options downloader.
- balfundalgo/breeze-data-downloader: ICICI Breeze 1-minute NIFTY/BANKNIFTY historical options.
- SynapticTrading/options_dataprocessing: vendor-derived large NIFTY options dataset, 1-minute, partial 2025 coverage.
- VinayJogani14/Nifty-Options-Backtest: reusable backtest architecture with externally supplied data.
These are useful for methodology and cross-checking, but this project will prefer a source with directly downloadable parquet files and documented provenance.

## Bid/ask limitation
The located public intraday datasets expose OHLCV rather than historical bid/ask for the full chain. The research therefore treats fill/slippage assumptions as a first-class sensitivity rather than pretending OHLC equals executable quotes.

## Broker cost source
Paytm Money's current F&O FAQ states 10 rupees brokerage per unique executed F&O order. A Paytm Money historical pricing notice documents account-vintage-dependent brokerage: 10 rupees for users from before August 2022, 15 rupees for users joining between August 2022 and August 2023, and 20 rupees for new users from 25-Aug-2023. The cost engine therefore supports dated/account-vintage brokerage sensitivity rather than hard-coding one value for all periods.

## Statutory cost source
The Finance Bill 2026 proposes raising STT on option sale premium from 0.10% to 0.15%, effective 1-May-2026. The backtest cost table will therefore be date-dependent.

## Literature and conceptual sources
- Rhoads, The Trading Options material on ratio spreads: ratio spreads use more short than long option contracts and have asymmetric tail risk.
- Carr & Wu (2016), Journal of Financial Economics: volatility risk premia vary over the option surface.
- Hu & Liu (2022), Journal of Financial and Quantitative Analysis: volatility and jump risks and return patterns differ across index option moneyness.
- Padhi & Shaikh (2014), Journal of Banking & Finance: Nifty implied volatility contains information about future realized volatility.
- Shaikh & Padhi: stylized Nifty implied-volatility smile/skew and term-structure behaviour.
These sources motivate regime and volatility segmentation, but they do not validate this particular trading rule.

## Video and educational source inventory
YouTube searches were included in the Phase 1 source inventory. No video was used as quantitative evidence; peer-reviewed and primary exchange sources are preferred for claims used in the backtest.
