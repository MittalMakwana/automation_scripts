// ==UserScript==
// @name         ringid.tech bypasser
// @namespace    http://tampermonkey.net/
// @downloadURL  https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/ringid_bypasser.js
// @updateURL    https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/ringid_bypasser.js
// @version      0.1
// @description  quickbypass for the website
// @author       orangesoda
// @match        https://ringid.tech/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=ringid.tech
// @grant        none
// ==/UserScript==

(function() {
    "use strict";
    let landing_page = document.getElementsByTagName('a')[1].innerText
    if (landing_page == "Get Download Links"){
        window.location.href = document.getElementsByTagName('a')[1].href
    }
    if (window.location.pathname == "/continue.php"){
        var urls = document.getElementsByTagName('input');
        for (let url of urls){
            if (url.value.includes("bayfiles")){
                var link = new URL(url.value)
                var api = "https://api.bayfiles.com/v2/file"+link.pathname+"/info"
                console.log(api)
                //To do add a fetch method to get the bayfile api details, current it is blocked and tells use to use mode no-cours but returns empty result

            }
        }
    }
})();