// ==UserScript==
// @name         clicknupload bypasser
// @downloadURL  https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/clicknupload_bypasser.js
// @updateURL    https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/clicknupload_bypasser.js
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  clicknupload by passer
// @author       orangesoda
// @match        https://clicknupload.to/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=clicknupload.to
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let method_free = document.getElementById("method_free")
    if (method_free.value == "Slow Download"){
     method_free.click();
    }
    let dlBtn = document.querySelector("button")
    dlBtn.disable = false
    let input_captch = document.getElementsByName('code')
    //to do implement a captcha solver
    

})();