var casper = require('casper').create({
  logLevel: 'debug',
  verbose: true
});

var x = require('casper').selectXPath;
var to_look = '';

function generatePossibleHref() {
  var r = [],
    x = 1;

  for (x; x <= 90; x = x + 3) {
    r.push(x);
  }

  return r;
}

function clickOrNot(strength) {
  var r = Math.floor(Math.random() * strength) + 1;

  if ((r === 1) || (r === 3)) {
    return true;
  }

  return false;
}

casper.start('http://news.ycombinator.com/', function () {
  if (this.cli.has("title")) {
    to_look = this.cli.get("title");
  } else {
    this.log("No text specified!")
  }

  this.click(x('/html/body/center/table/tbody/tr[1]/td/table/tbody/tr/td[3]/span[@class=\'pagetop\']/a'));
});

casper.then(function () {
  this.debugPage();

  this.fill('form', {
    'u': this.cli.get('username'),
    'p': this.cli.get('password')
  }, true);
});

casper.then(function () {
  var possibleNums = generatePossibleHref(),
    idx = 2,
    match = false;

  this.each(possibleNums, function (self, num) {
    var text = self.fetchText(x("/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[" + num + "]/td[@class='title'][2]/a")),
      link = x("/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[" + num + "]/td[@class='title'][2]/a");

    if (text === to_look) {
      match = true;
    }

    if (clickOrNot(idx) || match) {
      self.log("Clicking on link: " + text);
      self.click(link);
      self.back();
    }

    if (match) {
      self.debugPage();
      self.log("MATCH FOUND WE ARE GO");
      self.click(x("/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[" + num + "]/td[2]/center/a"));
      self.debugPage();
      match = false;
    }

    idx = idx + 1;
  });
});

casper.run(function () {
  this.exit();
});
