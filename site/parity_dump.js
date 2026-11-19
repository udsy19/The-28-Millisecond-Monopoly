// Parity helper for tests/test_parity.py (not loaded by the page).
// Reads [[fnName, [args...]], ...] as JSON on stdin; prints the results as JSON.
// Null args are passed as undefined so the JS defaults apply, like omitted Python kwargs.
var CHSH = require("./model.js");
var input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", function (c) { input += c; });
process.stdin.on("end", function () {
  var calls = JSON.parse(input);
  var out = calls.map(function (call) {
    var args = call[1].map(function (a) { return a === null ? undefined : a; });
    return CHSH[call[0]].apply(null, args);
  });
  process.stdout.write(JSON.stringify(out));
});
