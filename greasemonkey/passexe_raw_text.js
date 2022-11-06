// ==UserScript==
// @name         Text editor
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Script to just view the text content of the links
// @author       You
// @match        https://pastexe.com/*
// @match        https://justetext.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=pastexe.com
// @grant        none
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


    fetch(window.location.origin+"/get-paste?slug="+ file +"&password=1020", requestOptions)
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
            console.log(mega_links);

            var code = document.createElement('code');
            code.className = 'language-markup';
            code.textContent = mega_links;
            Prism.highlightElement(code);
            document.body.innerHTML = "<pre><br>" + code.outerHTML + '</pre>';

        }
    })
        .catch(error => console.log('error', error));
})();