var casper = require('casper').create({
  verbose: true,
  logLevel: 'debug',
  pageSettings: {
    javascriptEnabled: true,
    loadImages: true,
    loadPlugins: true,
    userAgent: 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
  }
});

var x = require('casper').selectXPath;

function generateName() {
  if (casper.cli.has('username')) {
    return casper.cli.get('username');
  }

  else {
    casper.echo("Need to specify a username buddy")
    casper.exit(1)
  }
}

casper.start('http://news.ycombinator.com/submit', function () {
  this.fill(x('/html/body/form[2]'), {
    'u': generateName(),
    'p': 'password'
  }, true);
});

casper.then(function () {
  this.debugPage();
});

casper.run(function () {
  this.exit();
});
