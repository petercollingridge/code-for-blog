var getSillyWord = (function() {
    var prefixes = ["B", "Br", "Dw", "Fl", "Fw", "Thr", "Pr", "Tr", "L", "Y", "Scr", "Sm", "Sp", "Squ", "M", "Wh"];
    var vowels = ["a", "e", "ee", "o", "oo", "i", "u"];
    var shortEndings = ["m", "rp", "rk", "rf", "nk", "mp", "b", "f", "zz", "x", "ng", "d", "p"];
    var longEndings = ["zz", "dd", "rp", "mp", "pp", "ck", "bb", "nk", "rf", "ng"];
    var longEndings2 = ["ok", "le", "le", "le", "et", "et", "aldo"];

    var randFromArray = function(arr) {
        return arr[Math.floor(arr.length * Math.random())];
    };

    var randFromArrayNotX = function(arr, x) {
        var result = x;
        while (result === x) {
            result = randFromArray(arr);
        }
        return result;
    };

    var mickleMackleMoo = function(prefix, vowel, end) {
        var word = "-" + prefix + randFromArrayNotX(vowels, vowel) + end;
        return word + Math.random() < 0.25 ? "-" + prefix + "oo" : "";
    };

    var yungoSpungo = function(prefix, vowel, end) {
        return "-" + randFromArrayNotX(prefixes, prefix) + vowel + end;
    };

    var avoidUglyPatterns = function(start, vowel, end) {
        // Avoid "ror" patterns
        if (start.charAt(start.length - 1) === end.charAt(0)) {
            end = end.substr(1);
        }
        
        // Avoid "Squu"
        if (start.charAt(start.length - 1) === 'u' && vowel === 'u') {
            vowel = randFromArrayNotX(vowels, 'u');
        }
        
        return [start, vowel, end];
    };

    var getLongName = function() {
        var start = randFromArray(prefixes);
        var vowel = randFromArray(vowels);
        var end = randFromArray(longEndings) + randFromArray(longEndings2);
        
        return avoidUglyPatterns(start, vowel, end);
    };

    var getShortName = function() {
        var start = randFromArray(prefixes);
        var vowel = randFromArray(vowels);
        var end = randFromArray(shortEndings);
        
        return avoidUglyPatterns(start, vowel, end);
    };

    return function() {
        var word, r;

        if (Math.random() < 0.5) {
            // Long name
            var parts = getLongName();
            word = parts.join("");
            r = Math.random();

            if (r < 0.2) {
                word += mickleMackleMoo.apply(null, parts);
            } else if (r < 0.4) {
                word += yungoSpungo.apply(null, parts);
            }
        } else {
            // Short name
            var parts = getShortName();
            word = parts.join("");
            r = Math.random();

            if (r < 0.2) {
                word += "-" + getLongName().join("");
            } else if (r < 0.4) {
                word = getLongName().join("") + "-" + word;
            } else if (r < 0.65) {
                word += randFromArray(vowels);
            } else if (r < 0.8) {
                var finalConsonant = parts[2].charAt(word.length - 1);
                var vowel = randFromArrayNotX(vowels, "e");
                word += vowel + finalConsonant + vowel;
            }
        }

        return word;
    };
})();