// ==UserScript==
// @name         terabox link
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       Orangesoda
// @match        https://www.1024tera.com/*
// @match        https://terabox.app/*
// @icon         https://s3.teraboxcdn.com/common-static/favicon.ico
// @grant        GM_addStyle
// @updateURL    https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/terabox.js
// @downloadURL  https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/terabox.js
// ==/UserScript==

(function() {
    window.stop();
    var myHeaders = new Headers();

    // Configuration
    const redirect = true; // Set this to false to disable redirection
    const openInNewWindow = false; // Set this to false to open in the same window
    const urlPatterns = [
        /1024tera\.com\/sharing\/link\?surl=/,
        /terabox\.app\/sharing\/link\?surl=/,
        /teraboxlink\.com\/s\//,
        /terafileshare\.com\/s\//,
        /terafox\.app\/sharing\/link\?surl=/
    ];

    const currentUrl = window.location.href;
    const match = urlPatterns.some(pattern => pattern.test(currentUrl));

    if (match && redirect) {
        const urlParams = new URLSearchParams(window.location.search);
        const surl = urlParams.get('surl');
        if (surl) {
            const newUrl = `https://terabox.tech/?url=${surl}`;
            if (openInNewWindow) {
                window.open(newUrl, '_blank');
            } else {
                window.location.href = newUrl;
            }
        }
    }

    fetch(currentUrl)
        .then(response => response.text())
        .then(result => {})
        .catch(error => console.log('error', error));
})();