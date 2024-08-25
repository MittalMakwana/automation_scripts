// ==UserScript==
// @name         freepaste link
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  try to take over the world!
// @author       You
// @match        https://freepaste.link/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=freepaste.link
// @grant        GM_addStyle
// @updateURL    file:///Users/mittalmak/dev/gm_script/freepaste.js
// @downloadURL  file:///Users/mittalmak/dev/gm_script/freepaste.js
// ==/UserScript==

(function() {
    window.stop();
    var myHeaders = new Headers();
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        redirect: 'follow'
    };
    let file = window.location.pathname.substring(1);

    // Configuration
    const redirect = true; // Set this to false to disable redirection
    const openInNewWindow = false; // Set this to false to open in the same window
    const urlPatterns = [
        /link-target\.net/,
        /link-center\.net/,
        /direct-link\.net/,
        /link-hub\.net/,
        /mega\.nz/,
    ];

    fetch(window.location.origin + "/get-paste?slug=" + file + "&password=1020", requestOptions)
        .then(response => response.text())
        .then(result => {
            var data = JSON.parse(result);
            if (data.status == "success") {
                document.body.innerHTML = "";
                const mega_re = /Mega.*(https?:\/\/\S+)\nDecry.*{ (.*) }/gm;
                // Sanitizing the incoming data decode to base64, replace + -> %20, UrlDecode
                let raw_content = atob(data.content);
                raw_content = raw_content.replaceAll('+', '%20');
                raw_content = decodeURIComponent(raw_content);

                // change Regex links
                let mega_links = raw_content.replace(mega_re, '$1#$2');
                console.log(mega_links);

                // Extract and log all URLs
                const url_re = /(https?:\/\/[^\s]+)/g;
                let urls = raw_content.match(url_re);
                if (urls) {
                    urls.forEach(url => {
                        console.log(url);
                        if (redirect && urlPatterns.some(pattern => pattern.test(url))) {
                            console.log('Redirecting to:', url);
                            if (openInNewWindow) {
                                window.open(url); // Open URL in a new window
                            } else {
                                window.location.href = url; // Open URL in the same window
                            }
                        }
                    });
                }

                var myCodeMirror = CodeMirror(document.body, {
                    value: mega_links,
                    mode: "txt",
                    theme: "3024-day",
                    lineWrapping: true,
                    matchBrackets: true,
                    styleActiveLine: true,
                    readOnly: true,
                });
                hyperlinkOverlay(myCodeMirror);
            }
        })
        .catch(error => console.log('error', error));
})();