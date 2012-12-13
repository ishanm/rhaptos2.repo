# # SpecRunner
# This file waits until jQuery is ready and then runs all
# the jasmine tests listed in `specs`
define ['jquery', 'jasmine-html'], (jQuery, jasmine) ->

  # List all the spec files here
  # They will be loaded via requirejs and then run
  specs = [
    'spec/MetadataSpec'
  ]

  # Set up the jasmine environment for HTML tests
  jasmineEnv = jasmine.getEnv()
  jasmineEnv.updateInterval = 1000
  htmlReporter = new jasmine.HtmlReporter()
  jasmineEnv.addReporter htmlReporter
  jasmineEnv.specFilter = (spec) ->
    htmlReporter.specFilter spec

  # When jQuery is finished loading:
  # * load up each spec using `requirejs`
  # * run them all
  jQuery ->
    require specs, ->
      jasmineEnv.execute()
