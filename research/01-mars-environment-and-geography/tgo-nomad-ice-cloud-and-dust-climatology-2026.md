# TGO/NOMAD Ice-Cloud and Dust Climatology Across Four Martian Years

**Evidence label:** Established orbital retrieval and rover cross-comparison; local operational conditions remain uncertain without site- and time-specific data
**Last checked:** 2026-10-16
**Author:** Habitat Sol research scan
**Scope:** What the 2026 TGO/NOMAD-UVIS aerosol climatology establishes about seasonal, spatial and diurnal patterns in Martian water-ice clouds and dust, and how its retrieval limits constrain operational use.

## Short answer

ExoMars Trace Gas Orbiter NOMAD/UVIS nadir observations now provide a consistent retrieval of water-ice-cloud and dust optical depth spanning almost four Martian years, from mid-MY34 to mid-MY38. The record reproduces major seasonal aerosol patterns and agrees qualitatively with rover observations, but orbital and surface optical-depth values are not interchangeable: the orbital retrieval is usually lower than or similar to Mastcam and Mastcam-Z measurements and remains sensitive to assumed particle size, aerosol altitude and scattering properties.

## What we know

- **The retrieval covers almost four Martian years with one instrument and method.**
  - **Evidence:** Willame et al. derived ice-cloud and dust optical depth from dayside nadir measurements by the UVIS channel of NOMAD aboard ESA's ExoMars Trace Gas Orbiter, spanning mid-Mars Year 34 to mid-Mars Year 38. The associated archive dates the observations from 2018-05-01 through 2025-09-16. [1][3]
  - **Conditions / limits:** Optical depth is a column-integrated measure of light extinction. It does not by itself give near-surface particle concentration, wind, deposition rate, visibility at a particular location, or abrasive loading on equipment.

- **The revised dust retrieval explicitly tests multiple effective particle sizes.**
  - **Evidence:** The retrieval uses a nominal effective radius of 1.5 micrometres and additional 2.0 and 2.5 micrometre cases. The authors report that including the larger sizes improves retrieval during high-dust-loading events. [1][2]
  - **Conditions / limits:** These are retrieval assumptions used to represent aerosol optical behaviour, not a claim that every dust event contains only three discrete particle sizes.

- **The record resolves recurring seasonal and geographic aerosol structures.**
  - **Evidence:** The study presents zonal-mean and mapped water-ice-cloud optical depth for the aphelion cloud belt, orographic clouds and polar-cloud edges, along with a diurnal cloud trend during aphelion season and a seasonal zonal distribution of dust optical depth. [1][2]
  - **Conditions / limits:** A multi-year climatology describes recurring distributions and variability; it is not a forecast for a particular sol, settlement site or storm.

- **Orbital and rover aerosol records agree on seasonal behaviour more clearly than on absolute values.**
  - **Evidence:** Comparison with Curiosity Mastcam and Perseverance Mastcam-Z optical-depth records showed good qualitative agreement and usually reproduced seasonal variation. Quantitatively, NOMAD/UVIS values were usually lower than or similar to the rover values. [1][2]
  - **Conditions / limits:** The observing geometries and retrieval methods differ. The authors specifically identify sensitivity to aerosol altitude profile, particle size and scattering properties as possible contributors to the difference.

- **The released data include a documented low-angle caution.**
  - **Evidence:** The Royal Belgian Institute for Space Aeronomy archive publishes the nominal dust-plus-ice and secondary ice-only retrievals as CSV files. It warns that dust optical depth retrieved at low solar-zenith or phase angles can become too low and should be treated cautiously, typically below 35 degrees for either angle. [3]
  - **Conditions / limits:** This is a quality caveat on part of the retrieval, not evidence that actual atmospheric dust decreases under those geometries.

## Constraints and uncertainties

- Nadir ultraviolet retrievals depend on assumptions about surface reflectance, aerosol vertical distribution, particle size and scattering. The paper reports sensitivity analysis rather than eliminating those dependencies.
- Combining measurements into zonal, seasonal or multi-year products can obscure short-lived local events and local-time differences.
- Ice-cloud optical depth and dust optical depth affect illumination and atmospheric heating differently; a combined aerosol opacity should not be treated as a direct dust measurement without checking the product definition.
- Neither column optical depth nor a climatological map directly determines filter loading, seal wear, solar-panel soiling, electrostatic behaviour or human visibility. Those require near-surface measurements and engineering models.
- The comparison establishes broad consistency with two rover records, not universal calibration at all latitudes, elevations, seasons or local times.

## Operational implications

- **Established inference:** Mars environmental planning should preserve separate dust and water-ice-cloud terms and should record the retrieval geometry and assumed particle model behind an optical-depth value.
- **Established inference:** Rover and orbital aerosol products can corroborate seasonal timing while still differing in absolute opacity; mixing them into one threshold without cross-calibration would create false precision.
- **Plausible extrapolation:** Multi-year aerosol climatology can support preliminary seasonal power, visibility and thermal-risk envelopes, but local design margins still need site-specific surface observations or conservative bounding cases.
- **Detail to avoid or qualify:** Do not convert orbital optical depth directly into a filter-replacement interval, surface dust flux, storm wind speed or solar-array loss percentage.

## Research-library boundary

- This note records measured atmospheric evidence and retrieval limitations. It makes no fictional-history or canon decision.
- Applying the climatology to a specific habitat or operational architecture requires a separate, explicit engineering model for location, season, local time, hardware and acceptable risk.

## Sources

1. Willame, Y.; Neary, L.; Daerden, F.; et al., *Ice Cloud and Dust Climatologies Over 4 Martian Years From TGO/NOMAD-UVIS Nadir Retrieval*, Journal of Geophysical Research: Planets 131(6) (published online 2026-06-22). https://doi.org/10.1029/2025JE009633 . Accessed 2026-10-16.
2. NOMAD Science Team, *Publications: Ice Cloud and Dust Climatologies Over 4 Martian Years From TGO/NOMAD-UVIS Nadir Retrieval*, Royal Belgian Institute for Space Aeronomy. https://nomad.aeronomie.be/index.php/publications . Accessed 2026-10-16.
3. Willame, Y., *Ice cloud and dust optical depth columns from nadir retrieval with NOMAD-UVIS/TGO (2025)*, version 1, Royal Belgian Institute for Space Aeronomy data repository. https://doi.org/10.18758/69qazhkk . Accessed 2026-10-16.
