// ==UserScript==
// @name         Bay File API
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Redirect the file to Bay File api for direct download link
// @author       orangesoda
// @match        https://bayfiles.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=bayfiles.com
// @grant        none
// @run-at       document-start
// ==/UserScript==


// api for the website: https://api.bayfiles.com/v2/file/Oet1I1Ffy0/info

(function () {
    "use strict";
    var url = "https://api.bayfiles.com/v2/file"+window.location.pathname+"/info"
    window.location.href = url;
    console.log('here');
    console.log(url);
})();