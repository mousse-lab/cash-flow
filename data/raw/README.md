# Raw data folder

This folder is intended for raw external source files that are not committed to the repository by default.

Examples:

- Swedbank Försäkring annual report PDFs
- Swedish mortality tables from SCB or another public source
- Swedish interest-rate/yield data from Riksbanken

Large PDFs and downloaded source files should normally stay local and be documented in `external_sources.md` instead of being committed directly.

The modelling workflow should use cleaned inputs from `data/processed/`.
