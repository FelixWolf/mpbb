# About
Marketplace Buyer Beware.
A listing for abusive stores in Second Life's market place.

# Setup
For the most part, `setup.py` isn't needed. Just run `start-development` or `start-production`

# Structure
## Static
Anything not dynamically changed(Images, Javascript, etc) goes in static.

## View
All the front end webpages and templates go into View. File format **SHOULD BE** `htm`, not `html`!

## Controllers
Controllers are what handle the requests and display a view.
Generating HTML should be avoided here unless absolutely nessassery. Pass all information to `render_template` from `from .. import render_template` and generate HTML there.

## Models
Models manage data and what not

## Helpers
Helpers are modules/scripts to assist with specific things such as Markdown generation, input sanitization, etc.

# Copyright / License
Copyright (c) 2018 Softhyena.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
