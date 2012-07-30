var casper = require('casper').create({
  verbose: true,
  logLevel: 'debug'
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
