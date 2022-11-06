// ==UserScript==
// @name         freepaste link
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://freepaste.link/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=freepaste.link
// @grant        GM_addStyle

// ==/UserScript==

(function() {
    window.stop();
    const PASSWD = "1020";
    var myHeaders = new Headers();
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        redirect: 'follow'
    };
    let file = window.location.pathname.substring(1);


    fetch(window.location.origin+"/get-paste?slug="+ file +"&password="+ PASSWD, requestOptions)
        .then(response => response.text())
        .then(result => {
        var data = JSON.parse(result)
        if (data.status == "success"){
            document.body.innerHTML = "";
            const mega_re = /Mega.*(https?:\/\/\S+)\nDecry.*{ (.*) }/gm;
            // Sanitizine the incommming data decode to base64, replace + -> %20, UrlDecode
            let raw_content = atob(data.content)
            raw_content = raw_content.replaceAll('+', '%20');
            raw_content = decodeURIComponent(raw_content)

            // chnage Regex links
            let mega_links = raw_content.replace(mega_re,'$1#$2');
            //raw_content = raw_content.concat("\n$$$$$$$$$$$$$$$$\n", mega_links);
            console.log(mega_links);
            var myCodeMirror = CodeMirror();
            myCodeMirror = CodeMirror(document.body, {
                value: mega_links,
                mode:  "txt",
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