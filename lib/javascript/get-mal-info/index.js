#!/usr/bin/env node
const url = require("url");
const malScraper = require("mal-scraper");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const argv = yargs(hideBin(process.argv)).argv;

if (!argv.url) {
  console.error("get-mal-info: ERROR no url.");
  process.exit(1);
}

const validateMALUrl = (s) => {
  try {
    if (!s) {
      return false;
    }
    var parsed_url = url.parse(s, false);
    if (!parsed_url.protocol || !parsed_url.hostname || !parsed_url.path) {
      return false;
    }
    return (
      parsed_url.protocol === "https:" &&
      parsed_url.hostname === "myanimelist.net" &&
      parsed_url.path.includes("/anime/")
    );
  } catch (err) {
    return false;
  }
};

if (!validateMALUrl(argv.url)) {
  console.error("get-mal-info: ERROR invalid URL");
  process.exit(1);
}

// console.log(search.helpers);
malScraper
  .getInfoFromURL(argv.url)
  .then((data) => console.log(data))
  .catch((err) => {
    console.error(err);
  });
