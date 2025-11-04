# TODO: Update ADS Display Logic

## Overview
Update the display logic in templates for ADS (ads) to match the requirements:
- For ads labelled "Sell" (ad_type == 'sell'): Display only "Achte" and "Fe piblisite" buttons. Show price for all sell ads. Remove WhatsApp button and special case for 'Siwo Gwosi'.
- For ads labelled "Publish only" (ad_type == 'publish'): Display "WhatsApp" and "Fe piblisite" buttons.

## Steps
1. Update templates/achte.html: Modify the ad-actions logic to remove WhatsApp for sell ads, remove special case for 'Siwo Gwosi', and ensure publish ads show WhatsApp and Fe piblisite.
2. Update templates/batch.html: Apply the same changes as in achte.html for consistency.
3. Test the changes by running the app and verifying the button displays.

## Files to Edit
- templates/achte.html
- templates/batch.html

## Followup
- After editing, run the app to ensure buttons display correctly.
- No DB changes required as this is template logic.

## Progress
- [x] Updated templates/achte.html
- [x] Updated templates/batch.html
- [ ] Test the changes by running the app
