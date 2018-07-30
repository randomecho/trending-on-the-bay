# Trending on the Bay

Search and decide what products might be worth flipping
on eBay based on current and sold listings.

## Setup

Run the app locally with Docker:

    docker build . -t trending_bay
    docker run -d --name trending_app -p 3516:80 trending_bay

The web app should now be accessible via: http://0.0.0.0:3516/

## License

Released under [BSD 3-Clause](./LICENSE).


### Healthcheck

[![Build Status](https://travis-ci.com/randomecho/trending-on-the-bay.svg?branch=master)](https://travis-ci.com/randomecho/trending-on-the-bay)

[![Maintainability](https://api.codeclimate.com/v1/badges/4981c1bb648ae7f65170/maintainability)](https://codeclimate.com/github/randomecho/trending-on-the-bay/maintainability)
