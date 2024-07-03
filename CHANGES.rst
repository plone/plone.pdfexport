Changelog
=========


1.3 (2024-07-03)
----------------

- Add Bnner image field, reander banner in page headers
  [MrTango]


1.2 (2021-10-26)
----------------

- Provide both page mode's (landscape and portrait) with a default setting and switch thru a request mode parameter
  [MrTango]


1.1 (2021-10-08)
----------------

- Improved image handling, now support also original images (without @@images/scales).
  [MrTango]


1.0 (2021-10-06)
----------------

- Improve German translations
  [MrTango]

- Improve error handling and add more tests
  [MrTango]


1.0b1 (2021-07-15)
------------------

- Resolve images internally in a custom WeasyPrint url_fetcher, this removes the need to resolves url's for WeasyPrint, which was problematic with permissions or https cert issues
  [MrTango]


1.0a4 (2021-07-14)
------------------

- Don't use  optimize_images=True in weasyprint for now, it only works in Py3 versions
  [MrTango]

1.0a3 (2021-07-14)
------------------

- Add print_image_scale to control panel and use custom image scale for PDF export
  [MrTango]


1.0a2 (2021-07-14)
------------------

- Fix missing lead image viewlet in PDF export
  [MrTango]

- Merge content css classes with body tag classes instead of overriding them
  [MrTango]


1.0a1 (2021-07-13)
------------------

- Initial release.
  [MrTango]
