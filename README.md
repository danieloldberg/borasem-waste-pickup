<!-- # ![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=)
# ![Version](https://img.shields.io/github/v/release/Kaptensanders/skolmat-card)
# ![Installs](https://img.shields.io/badge/dynamic/json?label=Installs&logo=home-assistant&query=%24.skolmat.total&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json) -->

# Borås Energi och Miljö waste pickup custom component for Home Assistant
Get the next Borås Energi och Miljö waste collection dates directly in Home Assistant.

## Description
This component only supports households located and served by Borås Energi och Miljö. It collects data from Borås Energi och Miljö API to create sensor entities based on the household address.
Each household waste container sensor will display the date of the upcoming pickup, as well as some metadata as attributes on the entity.

You may use this information to display in a Lovelace dashboard, or in automations.

The integration is configured using the UI and the data is updated every 24 hours.

## Installation
1. Install with HACS
2. Go to Settings -> Devices and Services -> Add integration -> Borås Energi och Miljö Waste Pickup
3. Enter you address (see information below)
4. Done.

## Finding the address
Borås Energi och Miljö API expects the address to be in a certain format, such as "Address Number, District (Some number combination)".
The final format is important and is validated to create the integration, but we do attempt to perform autocompletion to get the last details.
Try the following:
1. Let's say we live on Hittapåvägen 1B in Randomorten. 1B seems to always be separated by a space, i.e. 1 B.
2. In Home Assistant, try to enter "Hittapåvägen 1 B" (without quotes). This seem to work for 99% of my test cases.
3. If the address is unique among the customer base, the integration automatically resolve to for example "Hittapåvägen 1 B, Randomorten (123456)".
4. If you live on an address that is not unique, or it straight up doesn't work, you may need to feed the exact value. This can be done by visiting "Nästa tömningsdag" at Borås Energi och Miljö website. https://www.borasem.se/webb/privat/avfallochatervinning/abonnemangforhushallsavfall/nastatomningsdag.4.5a231a8f188bd840a1327da.html
5. Enter you address and let the dropdown automatically resolve to your address. Copy + paste the entire resolved value into the Home Assistant integration. This should now work.