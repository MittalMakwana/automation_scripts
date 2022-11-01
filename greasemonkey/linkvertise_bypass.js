// ==UserScript==
// @name         Linkvert bypass
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Bypass Linkvert by making an api call and then redirecting the website
// @author       orangesoda
// @match        https://linkvertise.com/*
// @match        https://link-center.net/*
// @match        https://direct-link.net/*
// @match        https://link-hub.net/*
// @match        https://file-link.net/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=linkvertise.com
// @grant        none
// @run-at document-start
// ==/UserScript==

(function () {
    "use strict";
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    fetch("https://bypass.pm/bypass2?url="+document.URL, requestOptions)
        .then(response => response.text())
        .then(result => {
        var data = JSON.parse(result)
        if (data.success){
           window.location.href = data.destination;
        }
    })
        .catch(error => console.log('error', error));
    // The below code is a manual way to navigate through the website
    //
    //
    /*var downloadBtn;

    const checkDataLoaded = () => {
        downloadBtn = document.getElementsByClassName("text countdownTodoText")[1];
    };

    let intervalId = setInterval(() => {
        checkDataLoaded();

        if (downloadBtn) {
            insertBtn();
        }
    }, 1000);

    const insertBtn = () => {
        clearInterval(intervalId);
        document.getElementsByClassName("text countdownTodoText")[1].click();

        document.getElementsByClassName("text countdownTodoText")[1].click();
    };
    */
})();